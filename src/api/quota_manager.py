import threading
import time
from datetime import datetime, timedelta
from src.utils.logging_utils import logger

class ApiQuotaManager:
    """API quota manager to ensure API request limits are not exceeded."""
    def __init__(self, max_requests_per_minute):
        if max_requests_per_minute <= 0:
            raise ValueError("max_requests_per_minute must be a positive number")
        self.max_requests_per_minute = max_requests_per_minute
        self.api_requests = []
        self.api_counter_lock = threading.Lock()
        logger.info(f"ApiQuotaManager initialized with limit: {max_requests_per_minute} RPM")

    def wait_for_quota(self):
        """Waits for API quota to become available, ensuring the per-minute limit is not exceeded."""
        current_time = datetime.now()
        with self.api_counter_lock:
            one_minute_ago = current_time - timedelta(minutes=1)
            self.api_requests[:] = [req for req in self.api_requests if req >= one_minute_ago]

            if len(self.api_requests) >= self.max_requests_per_minute:
                wait_time = (self.api_requests[0] + timedelta(minutes=1) - current_time).total_seconds()
                wait_time = max(0, wait_time)
                logger.info(f"API request limit reached ({len(self.api_requests)}/{self.max_requests_per_minute}), waiting for {wait_time + 0.5:.2f} seconds...")
                time.sleep(wait_time + 0.5)
                return self.wait_for_quota()

            self.api_requests.append(current_time)
            return True