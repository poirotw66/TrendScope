"""
爬蟲主程式
提供命令行介面以運行各種爬蟲
"""
import argparse
import os
from datetime import datetime

# 導入所有爬蟲
from scrapers.parsers.aws_london import AWSLondonScraper
from scrapers.parsers.aicon_infoq import AiconInfoqScraper
from scrapers.parsers.qcon_infoq import QconInfoqScraper

def main():
    """
    主函數，處理命令行參數並運行相應的爬蟲
    """
    parser = argparse.ArgumentParser(description='運行各種爬蟲')
    
    # 添加爬蟲選擇參數
    parser.add_argument('scraper', choices=['aws_london', 'aicon_infoq', 'qcon_infoq'], help='選擇要運行的爬蟲')
    
    # 添加通用參數
    parser.add_argument('--headless', action='store_true', help='是否使用無頭模式（不顯示瀏覽器窗口）')
    parser.add_argument('--wait-time', type=int, default=30, help='等待元素的最大時間（秒）')
    parser.add_argument('--output-dir', type=str, default='data/sheet', help='輸出目錄')
    
    # 添加 BigQuery 相關參數
    parser.add_argument('--use-bigquery', action='store_true', help='是否將數據上傳到 BigQuery')
    parser.add_argument('--bq-credentials', type=str, help='BigQuery 憑證路徑')
    parser.add_argument('--bq-project-id', type=str, help='BigQuery 項目 ID')
    
    args = parser.parse_args()
    
    # 確保輸出目錄存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 根據選擇運行相應的爬蟲
    if args.scraper == 'aws_london':
        scraper = AWSLondonScraper(
            headless=args.headless,
            wait_time=args.wait_time,
            use_bigquery=args.use_bigquery,
            bq_credentials=args.bq_credentials,
            bq_project_id=args.bq_project_id
        )
        scraper.run(output_dir=args.output_dir)
    elif args.scraper == 'aicon_infoq':
        scraper = AiconInfoqScraper(
            headless=args.headless,
            wait_time=args.wait_time,
            use_bigquery=args.use_bigquery,
            bq_credentials=args.bq_credentials,
            bq_project_id=args.bq_project_id
        )
        scraper.run(output_dir=args.output_dir)
    elif args.scraper == 'qcon_infoq':
        scraper = QconInfoqScraper(
            headless=args.headless,
            wait_time=args.wait_time,
            use_bigquery=args.use_bigquery,
            bq_credentials=args.bq_credentials,
            bq_project_id=args.bq_project_id
        )
        scraper.run(output_dir=args.output_dir)
    
if __name__ == '__main__':
    main()
