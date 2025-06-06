#!/usr/bin/env python3
"""
Batch Meeting Transcript Summarization Tool - Processes transcripts in a folder (Multithreaded Version)
"""
import sys
import os
import argparse
import time
from pathlib import Path
import concurrent.futures
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

from config.config import (
    MAX_REQUESTS_PER_MINUTE, DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_FORMAT, DEFAULT_WORKERS, SUPPORTED_FILE_EXTENSIONS,
    REQUEST_INTERVAL, MAX_RETRIES, RETRY_DELAY, PROJECT_ROOT
)
from src.utils.file_utils import FileUtils
from src.utils.logging_utils import logger
from src.api.quota_manager import ApiQuotaManager
from src.utils.decorators import retry_on_exception

class TranscriptProcessor:
    """Processor for transcripts, responsible for summary generation and saving."""
    def __init__(self, output_dir):
        from src.transcript_summarizer import TranscriptSummarizer
        self.summarizer = TranscriptSummarizer()
        self.output_dir = output_dir
        self.api_quota_manager = ApiQuotaManager(MAX_REQUESTS_PER_MINUTE)

    def save_summary(self, summary, output_path, output_format, file_path):
        """Saves the summary to a file in the specified format."""
        try:
            FileUtils.write_file(summary["summary"], output_path)
            self.save_html_summary(summary, file_path)
        except Exception as e:
            logger.error(f"Error saving summary {output_path}: {e}")
            return False
        return True

    def save_html_summary(self, summary, file_path):
        """Saves the summary in HTML format."""
        html_dir = os.path.join(self.output_dir, "session")
        os.makedirs(html_dir, exist_ok=True)
        safe_stem = FileUtils.normalize_filename(file_path.stem)
        html_output_path = os.path.join(html_dir, safe_stem + ".html")
        meeting_title = file_path.stem.replace("_", " ").title()
        self.summarizer.save_summary_html(summary, html_output_path, meeting_title)
        logger.info(f"HTML summary saved to: {html_output_path}")

    @retry_on_exception(max_retries=MAX_RETRIES, wait_seconds=RETRY_DELAY)
    def _call_summarizer_with_retry(self, transcript_text, meeting_title):
        """Calls the summarizer and handles retry logic."""
        return self.summarizer.summarize(transcript_text, meeting_title)

    def process_file(self, file_info):
        """Processes a single transcript file (with API rate limiting and retry for summarization)."""
        file_path, output_format, total_files, file_index = file_info
        logger.info(f"Processing ({file_index + 1}/{total_files}): {file_path.name}")

        transcript_text = FileUtils.read_file(file_path)
        if not transcript_text:
            logger.warning(f"File {file_path.name} is empty or failed to read, skipping.")
            return False

        meeting_title = file_path.stem

        summary = None
        try:
            self.api_quota_manager.wait_for_quota()
            summary = self._call_summarizer_with_retry(transcript_text, meeting_title)

            if not summary or summary.get("status") == "error":
                error_msg = summary.get("error_message", "Unknown error") if summary else "Summary returned None"
                logger.error(f"File {file_path.name} failed to generate summary (after retries): {error_msg}")
                return False

        except Exception as e:
            logger.error(f"Unexpected error during summarization step for file {file_path.name}: {e}", exc_info=True)
            return False
        finally:
            time.sleep(REQUEST_INTERVAL)

        if summary and summary.get("status") == "success":
            safe_stem = FileUtils.normalize_filename(file_path.stem)
            output_filename = safe_stem + f".{output_format}"
            format_dir = os.path.join(self.output_dir, output_format)
            os.makedirs(format_dir, exist_ok=True)
            output_path = os.path.join(format_dir, output_filename)

            try:
                save_successful = self.save_summary(summary, output_path, output_format, file_path)
                if save_successful:
                    logger.info(f"File {file_path.name} processed successfully, summary saved.")
                else:
                    logger.error(f"File {file_path.name} summary saving failed.")
                return save_successful
            except Exception as e:
                logger.error(f"Unexpected error saving file {output_path}: {e}", exc_info=True)
                return False
        else:
            logger.warning(f"File {file_path.name} did not generate a successful summary, skipping save.")
            return False


class BatchProcessor:
    """Batch processor responsible for handling multiple files using multithreading."""
    def __init__(self, input_dir, output_dir, output_format, max_workers):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_format = output_format
        self.max_workers = max_workers
        self.processor = TranscriptProcessor(str(self.output_dir))

    def display_progress(self, completed, failed, total_files, start_time):
        """Displays the processing progress."""
        elapsed = time.time() - start_time
        progress = (completed + failed) / total_files * 100
        logger.info(f"Progress: {progress:.1f}% ({completed + failed}/{total_files}), "
                   f"Completed: {completed}, Failed: {failed}, Elapsed time: {elapsed:.1f}s")
                   
    def process(self):
        """Processes all transcript files in the specified directory using multithreading."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        transcript_files = FileUtils.get_files_by_extensions(str(self.input_dir), SUPPORTED_FILE_EXTENSIONS)

        if not transcript_files:
            logger.warning(f"No supported text files ({SUPPORTED_FILE_EXTENSIONS}) found in {self.input_dir}")
            return

        total_files = len(transcript_files)
        effective_workers = max(1, min(self.max_workers, total_files))
        logger.info(f"Found {total_files} transcript files, processing with up to {effective_workers} threads (API Limit: {MAX_REQUESTS_PER_MINUTE} RPM, Request Interval: {REQUEST_INTERVAL}s)")

        tasks = [(Path(file_path), self.output_format, total_files, i)
                 for i, file_path in enumerate(transcript_files)]

        start_time = time.time()
        completed, failed = 0, 0

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=effective_workers) as executor:
                futures = {executor.submit(self.processor.process_file, task): task[0].name for task in tasks}
                for future in concurrent.futures.as_completed(futures):
                    file_name = futures[future]
                    try:
                        if future.result():
                            completed += 1
                        else:
                            failed += 1
                            logger.warning(f"File {file_name} processing failed.")
                    except Exception as exc:
                        failed += 1
                        logger.error(f"Unexpected error processing file {file_name}: {exc}")
                    self.display_progress(completed, failed, total_files, start_time)
        except KeyboardInterrupt:
            logger.warning("\nProcess interrupted by user. Waiting for current tasks to complete...")
        except Exception as e:
            logger.error(f"A critical error occurred during execution: {e}")

        logger.info(f"Batch processing completed. Success: {completed}, Failed: {failed}")
        logger.info(f"Total time taken: {time.time() - start_time:.2f} seconds")
        logger.info(f"Summary files saved in: {self.output_dir}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Batch process meeting transcripts and generate summaries (Multithreaded Version)")
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT_DIR, help=f"Input directory (Default: {DEFAULT_INPUT_DIR})")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, help=f"Output directory (Default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--format", choices=["json", "txt", "md"], default=DEFAULT_OUTPUT_FORMAT, help=f"Output format (Default: {DEFAULT_OUTPUT_FORMAT})")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"Maximum number of worker threads (Default: {DEFAULT_WORKERS})")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_dir():
        logger.error(f"Error: Input path {args.input} is not a valid directory")
        return 1
    processor = BatchProcessor(args.input, args.output, args.format, args.workers)
    processor.process()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
