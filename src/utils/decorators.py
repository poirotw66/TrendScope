import time
from src.utils.logging_utils import logger

def retry_on_exception(max_retries=3, wait_seconds=5):
    """Decorator: Automatically retries when an exception occurs."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error: {e}, retrying attempt {attempt}...")
                    if attempt < max_retries:
                        time.sleep(wait_seconds * attempt)
                    else:
                        logger.error("Retry failed, abandoning the task.")
                        return None
        return wrapper
    return decorator