# Google Next 2025 報告生成器

這個專案是一個自動化工具，用於處理、摘要並生成關於 Google Next 2025 和 NVIDIA GTC 2025 會議內容的結構化報告。

## 專案說明

此工具能夠從原始會議文字記錄中，利用生成式 AI 進行摘要處理，並組織成結構化的報告頁面，包括：
- 會議內容摘要（按主題分類）
- 各主題頁面生成
- 首頁報告生成
- 上下文關聯圖表生成

## 功能特點

- **批次處理會議文字記錄**：自動處理大量會議記錄文件
- **AI 摘要生成**：利用 Gemini API 自動生成會議內容的結構化摘要
- **分類整理**：按技術主題進行分類整理
- **HTML 報告輸出**：將摘要和分類結果輸出為網頁形式的報告
- **多線程處理**：支援多線程批次處理以提高效率
- **錯誤重試機制**：API 呼叫失敗時自動重試
- **配額管理**：管理 API 呼叫頻率以遵守限制

## 目錄結構

- **config/**: 配置文件
- **data/**: 原始會議文字資料
  - **google_next_txt/**: Google Next 2025 會議文字記錄
  - **GTC_all_transcript/**: NVIDIA GTC 2025 會議文字記錄
  - **sheet/**: 會議表格資料
- **scripts/**: 處理腳本
  - **01_batch_summarize_process.py**: 批次摘要處理
  - **02_category_page.py**: 分類頁面生成
  - **03_generator_home.py**: 首頁生成
  - **04_context_diagram.py**: 上下文圖表生成
- **src/**: 核心源代碼
  - **api/**: API 相關模組
  - **templates/**: HTML 模板
  - **utils/**: 工具類函數
- **summaries/**: 生成的摘要
  - **html/**: HTML 格式摘要
  - **md/**: Markdown 格式摘要
  - **session/**: 會議摘要
- **output/**: 最終輸出報告

## 安裝與設定

### 環境需求
- Python 3.10+
- 按照 requirements.txt 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 環境變數配置
創建 `.env` 文件，包含以下設定：
```
GEMINI_API_KEY=your_api_key
DEFAULT_INPUT_DIR=data/google_next_txt
DEFAULT_OUTPUT_DIR=summaries/md
```

## 使用方法

### 1. 會議文字摘要處理

```bash
python scripts/01_batch_summarize_process.py -i data/google_next_txt -o summaries/md
```

### 2. 生成分類頁面

```bash
python scripts/02_category_page.py
```

### 3. 生成首頁

```bash
python scripts/03_generator_home.py -c google_next -i data/sheet/20250427_Qcon.csv -o output/google_next25_report
```

### 4. 生成上下文圖表

```bash
python scripts/04_context_diagram.py
```

## 輸出結果

處理完成後，您可以在 `output/google_next25_report` 目錄下找到生成的報告網頁，包括：
- 首頁概覽
- 按主題分類的會議摘要
- 各個會議的詳細內容摘要

## 依賴套件

- google-generativeai: Google Gemini API 的 Python 客戶端
- pandas: 數據處理與分析
- markdown: Markdown 處理
- python-dotenv: 環境變數管理
- Jinja2: 模板引擎
- beautifulsoup4: HTML 解析