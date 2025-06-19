from src.summarize_pdf import summarize_pdf
from src.batch_md_to_html_pdf import batch_md_to_html
import pathlib
import threading
import time

pdf_dir = pathlib.Path("data/202505_aicon_ppt")
csv_path = "data/sheet/20250523_上海_AICon_v1.csv"
output_md_dir = "aicon/md"
output_html_dir = "aicon/topic/session"

MAX_THREADS = 4
REQUEST_INTERVAL = 4
MAX_RETRIES = 3
RETRY_DELAY = 10  # 秒

semaphore = threading.Semaphore(MAX_THREADS)

def worker(pdf_file):
    with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"正在處理: {pdf_file} (嘗試第{attempt}次)")
                summarize_pdf(str(pdf_file), csv_path, output_md_dir)
                break  # 成功則跳出重試迴圈
            except Exception as e:
                print(f"處理 {pdf_file} 發生錯誤: {e}")
                if attempt < MAX_RETRIES:
                    print(f"{RETRY_DELAY}秒後重試...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"{pdf_file} 已達最大重試次數，跳過。")
        time.sleep(REQUEST_INTERVAL)

# threads = []
# for pdf_file in pdf_dir.glob("*.pdf"):
#     t = threading.Thread(target=worker, args=(pdf_file,))
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()

batch_md_to_html(output_md_dir, output_html_dir, 3)