import logging
import threading
from datetime import datetime
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent.parent

class ThreadSafeLogger:
    """Thread-safe logging class."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, name="google_next", level=logging.INFO, log_dir=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ThreadSafeLogger, cls).__new__(cls)
                cls._instance.logger = logging.getLogger(name)
                cls._instance.logger.setLevel(level)
                cls._instance.lock = threading.Lock()

                if not cls._instance.logger.handlers:
                    console = logging.StreamHandler()
                    console.setLevel(level)
                    formatter = logging.Formatter(
                        '%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
                    console.setFormatter(formatter)
                    cls._instance.logger.addHandler(console)

                    if log_dir is None:
                        log_dir = PROJECT_ROOT / "logs"
                    else:
                        log_dir = Path(log_dir)

                    log_dir.mkdir(parents=True, exist_ok=True)
                    log_file = log_dir / f"batch_process_{datetime.now().strftime('%Y%m%d')}.log"
                    file_handler = logging.FileHandler(log_file, encoding='utf-8')
                    file_handler.setLevel(level)
                    file_handler.setFormatter(formatter)
                    cls._instance.logger.addHandler(file_handler)
        return cls._instance

    def info(self, message):
        """Logs an info level message."""
        with self._lock:
            self._instance.logger.info(message)

    def error(self, message):
        """Logs an error level message."""
        with self._lock:
            self._instance.logger.error(message)

    def warning(self, message):
        """Logs a warning level message."""
        with self._lock:
            self._instance.logger.warning(message)

    def debug(self, message):
        """Logs a debug level message."""
        with self._lock:
            self._instance.logger.debug(message)

logger = ThreadSafeLogger()