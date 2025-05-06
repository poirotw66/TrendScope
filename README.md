google_next/
├── config/
│   └── config.py           # 集中所有配置參數
├── src/
│   ├── api/
│   │   └── gemini_api.py   # API 請求與配額管理
│   ├── utils/
│   │   ├── file_utils.py   # 檔案讀寫工具
│   │   └── logging_utils.py # 日誌工具
│   ├── models/
│   │   └── summarizer.py   # 摘要引擎
│   └── templates/
│       └── html_template.py # HTML 樣板
├── scripts/
│   ├── batch_summarize.py  # 批量摘要處理
│   ├── generate_home.py    # 生成首頁
│   └── context_diagram.py  # 生成脈絡圖
├── tests/                  # 單元測試
├── output/                 # 輸出目錄
│   ├── summaries/
│   ├── topic/
│   └── diagrams/
└── requirements.txt        # 依賴套件


python 01_batch_summarize_process.py -i 輸入目錄 -o 輸出目錄 --format md --workers 4

python 01_batch_summarize_process.py -i data/test/ -o test/ --format md --workers 4

python 02_generator_topic.py 

python 03_generator_home.py -i data/sheet/GTC25.csv -c gtc
