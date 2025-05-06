import os
import re
from pathlib import Path
from src.utils.logging_utils import logger

class FileUtils:
    """File processing utility class."""

    @staticmethod
    def read_file(file_path, encoding='utf-8'):
        """Safely reads file content."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {Path(file_path).name}: {e}")
            return None

    @staticmethod
    def write_file(content, file_path, encoding='utf-8'):
        """Safely writes content to a file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            logger.info(f"File saved: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            return False

    @staticmethod
    def get_files_by_extensions(directory, extensions):
        """Gets all files in the specified directory matching the extensions."""
        files = []
        directory_path = Path(directory)
        if not directory_path.is_dir():
            logger.error(f"Provided path is not a valid directory: {directory}")
            return files
        for ext in extensions:
            files.extend(directory_path.glob(f'*{ext}'))
        return files

    @staticmethod
    def normalize_filename(title):
        """Normalizes the filename by removing illegal characters."""
        title = re.sub(r'[\\/:*?"<>|]', '', str(title))
        return title.strip()