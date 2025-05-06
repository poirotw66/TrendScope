import pandas as pd
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from config.config import (
    OUTPUT_MD_DIR, OUTPUT_HTML_DIR, SESSION_HTML_DIR,
    INPUT_CSV_PATH, TOP_N_MEETINGS, BATCH_MD_TO_HTML_INDEX
)
from src.utils.logging_utils import logger
from src.utils.file_utils import FileUtils
from src.batch_md_to_html import batch_md_to_html

output_md_dir = Path(OUTPUT_MD_DIR)
output_html_dir = Path(OUTPUT_HTML_DIR)
session_html_dir = Path(SESSION_HTML_DIR)
input_csv_path = Path(INPUT_CSV_PATH)

output_md_dir.mkdir(parents=True, exist_ok=True)
output_html_dir.mkdir(parents=True, exist_ok=True)
session_html_dir.mkdir(parents=True, exist_ok=True)


def find_same_name_html(meeting_title, session_dir: Path, output_html_base_dir: Path):
    """Finds an HTML file in session_dir matching the meeting title."""
    normalized_meeting_title = FileUtils.normalize_filename(meeting_title)
    if not session_dir.is_dir():
        logger.error(f"Session directory not found: {session_dir}")
        return None

    for item in session_dir.iterdir():
        if item.is_file() and item.suffix.lower() == ".html":
            file_stem_normalized = FileUtils.normalize_filename(item.stem)
            print(f"Comparing: '{normalized_meeting_title}' vs '{file_stem_normalized}' (from {item.name})")
            if normalized_meeting_title == file_stem_normalized:
                try:
                    relative_path = item.relative_to(output_html_base_dir)
                    return str(relative_path).replace(os.path.sep, '/')
                except ValueError:
                    logger.error(f"Could not determine relative path for {item} from base {output_html_base_dir}")
                    return None

    logger.warning(f"No matching HTML file found for meeting: {meeting_title} in {session_dir}")
    return None

def export_topic_markdown(df: pd.DataFrame, md_dir: Path, session_dir: Path, output_html_base_dir: Path, top_n: int):
    """Exports meetings grouped by topic into Markdown files."""
    topics = df['Topic'].dropna().unique()
    logger.info(f"Exporting top {top_n} meetings for each topic...")
    for topic in topics:
        topic_df = df[df['Topic'] == topic][['Meeting', 'URL', 'Key']].dropna().head(top_n)
        if topic_df.empty:
            logger.info(f"No meetings found for topic: {topic}")
            continue

        safe_topic_filename = FileUtils.normalize_filename(topic) + ".md"
        md_path = md_dir / safe_topic_filename
        md_content = f"# {topic}\n\n"

        for _, row in topic_df.iterrows():
            meeting = str(row['Meeting'])
            html_path = find_same_name_html(meeting, session_dir, output_html_base_dir)
            url = row['URL']
            keytakeway = row['Key']

            md_content += f"## {meeting}\n"
            if html_path:
                md_content += f"### <a href=\"{html_path}\" style=\"text-decoration: none; color: inherit;\">Detailed Summary Page</a>\n"
            else:
                md_content += f"### Detailed Summary Page (Not Found)\n"
            md_content += f"- Link: [{url}]({url})\n"
            md_content += f"- Summary: {keytakeway}\n\n"

        if FileUtils.write_file(md_content, md_path):
            logger.info(f"Saved Markdown for topic '{topic}': {md_path}")
        else:
            logger.error(f"Failed to save Markdown for topic '{topic}': {md_path}")


def run_category_page_generation():
    """Reads CSV, generates topic Markdown files, and converts them to HTML."""
    try:
        if not input_csv_path.is_file():
            logger.error(f"CSV file not found: {input_csv_path}")
            return

        df = pd.read_csv(input_csv_path)
        export_topic_markdown(df, output_md_dir, session_html_dir, output_html_dir, top_n=TOP_N_MEETINGS)
        batch_md_to_html(str(output_md_dir), str(output_html_dir), BATCH_MD_TO_HTML_INDEX)
        logger.info("Category page generation process completed.")
    except FileNotFoundError:
        logger.error(f"Error: CSV file not found {input_csv_path}")
    except pd.errors.EmptyDataError:
        logger.error(f"Error: CSV file is empty or invalid: {input_csv_path}")
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}", exc_info=True)

if __name__ == "__main__":
    run_category_page_generation()
