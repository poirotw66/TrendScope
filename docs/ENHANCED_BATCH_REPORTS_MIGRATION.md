# Enhanced Batch Report System Migration Guide
# 增強版批量報告系統遷移指南

## 🎯 遷移概述

本指南詳細說明如何從舊版 `batch_report.py` 遷移到新的增強版批量報告生成系統，該系統完全符合 `plan.md` 規範。

## 📋 遷移前檢查清單

### 1. 系統依賴檢查
```bash
# 檢查 Python 環境
python --version  # 需要 Python 3.8+

# 檢查必要的 Python 包
pip list | grep -E "(fastapi|google-cloud-bigquery|google-generativeai|pathlib)"

# 檢查 Hugo 安裝
hugo version  # 需要 Hugo 0.100+
```

### 2. 環境變量檢查
```bash
# 必要的環境變量
echo $GOOGLE_APPLICATION_CREDENTIALS  # BigQuery 憑證路徑
echo $GOOGLE_CLOUD_PROJECT           # Google Cloud 項目 ID
echo $GEMINI_API_KEY                 # Gemini API 密鑰
```

### 3. 目錄結構檢查
```
TrendScope/
├── base/
│   ├── api/
│   │   ├── modules/
│   │   │   ├── enhanced_report_generator.py  ✅
│   │   │   ├── trend_analyzer.py             ✅
│   │   │   ├── trend_recommendation_engine.py ✅
│   │   │   └── hugo_report.py                ✅
│   │   └── routes/
│   │       └── batch_reports.py              🔄 已更新
│   └── bigquery/
│       └── client.py                         ✅
└── config/
    └── config.py                             ✅
```

## 🚀 遷移步驟

### 步驟 1: 備份現有系統
```bash
# 備份舊版 batch_reports.py
cp base/api/routes/batch_reports.py base/api/routes/batch_reports.py.backup

# 備份現有報告
cp -r reports reports_backup_$(date +%Y%m%d)
```

### 步驟 2: 驗證增強模組
```bash
# 運行系統檢查腳本
python test_enhanced_batch_reports.py

# 檢查增強系統狀態
curl http://localhost:8001/reports/enhanced/status
```

### 步驟 3: 測試新功能

#### 3.1 測試趨勢分析
```bash
# 測試趨勢分析 API
curl -X POST http://localhost:8001/reports/trends/analyze \
  -H "Content-Type: application/json" \
  -d '{"seminars": null, "limit": 10}'
```

#### 3.2 測試批量報告生成
```bash
# 啟動增強版批量報告生成
curl -X POST http://localhost:8001/reports/generate-batch \
  -H "Content-Type: application/json" \
  -d '{
    "seminars": null,
    "limit": 5,
    "output_format": "markdown",
    "include_html": true,
    "analysis_mode": "comprehensive",
    "output_template": "professional",
    "enable_trend_analysis": true,
    "enable_recommendations": false
  }'
```

### 步驟 4: 驗證文件結構

生成的報告應包含以下符合 `plan.md` 的文件結構：

```
reports/batch_YYYYMMDD_HHMMSS/
├── trends-analysis.md           # 🏠 趨勢分析總覽
├── _index.md                    # 🏠 Hugo 首頁
├── trends/                      # 📂 趨勢分類層
│   ├── trend-ai-chips.md       # 🔧 AI 晶片趨勢
│   ├── trend-multimodal.md     # 🎭 多模態趨勢
│   ├── trend-llm.md            # 🧠 大型語言模型趨勢
│   ├── trend-cloud.md          # ☁️ 雲端技術趨勢
│   └── trend-data-science.md   # 📊 資料科學趨勢
└── sessions/                    # 📂 會議詳細層
    ├── session-20250710-ai-soc.md
    ├── session-20250710-multimodal.md
    └── ... (其他會議頁面)
```

## 🔧 新功能說明

### 1. 三階段工作流程

#### Phase 1: LLM 趨勢分析
- 使用 Gemini 2.5 Flash 進行深度語意理解
- 自動識別五大技術趨勢
- 生成結構化趨勢報告

#### Phase 2: 自動標記系統
- 基於 LLM 的會議內容分類
- 多重標記支持（一場會議可對應多個趨勢）
- 置信度評分和推理說明

#### Phase 3: 三階層 Hugo 網站生成
- **首頁** (`_index.md`) - 趨勢總覽和導航
- **趨勢分類頁面** (`trends/trend-*.md`) - 各趨勢詳細分析
- **會議詳細頁面** (`sessions/session-*.md`) - 個別會議報告

### 2. 新增 API 端點

```python
# 趨勢分析
POST /reports/trends/analyze

# 個性化推薦
POST /reports/recommendations/personalized

# 增強系統狀態
GET /reports/enhanced/status

# 增強功能列表
GET /reports/enhanced/features
```

### 3. 前端兼容性

所有現有的前端頁面保持完全兼容：
- ✅ `BatchReportsPage` - 批量報告生成
- ✅ `BatchReportTasksPage` - 報告管理和下載
- ✅ `TrendAnalysisPage` - 趨勢分析
- ✅ `PersonalizedRecommendationsPage` - 個性化推薦

## 🐛 故障排除

### 常見問題 1: 增強模組導入失敗
```bash
# 檢查模組是否存在
ls -la base/api/modules/

# 檢查 Python 路徑
python -c "import sys; print('\n'.join(sys.path))"

# 重新安裝依賴
pip install -r requirements.txt
```

### 常見問題 2: Gemini API 連接失敗
```bash
# 檢查 API 密鑰
echo $GEMINI_API_KEY

# 測試 API 連接
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_API_KEY')
model = genai.GenerativeModel('gemini-2.5-flash')
print('Gemini API 連接成功')
"
```

### 常見問題 3: BigQuery 連接失敗
```bash
# 檢查憑證文件
ls -la $GOOGLE_APPLICATION_CREDENTIALS

# 測試 BigQuery 連接
python -c "
from google.cloud import bigquery
client = bigquery.Client()
print('BigQuery 連接成功')
"
```

### 常見問題 4: Hugo 構建失敗
```bash
# 檢查 Hugo 版本
hugo version

# 手動測試 Hugo 構建
cd reports/batch_YYYYMMDD_HHMMSS/hugo_site
hugo --destination ../html
```

## 📊 性能監控

### 1. 任務執行時間
- 舊版系統：平均 2-5 分鐘/10個會議
- 新版系統：平均 3-8 分鐘/10個會議（包含趨勢分析）

### 2. 生成文件數量
- 舊版：N 個會議 → N 個 Markdown 文件
- 新版：N 個會議 → N+7 個文件（包含趨勢分析和分類文件）

### 3. 記憶體使用
- 建議最小記憶體：4GB
- 推薦記憶體：8GB+（用於大型數據集）

## 🎉 遷移完成驗證

運行完整測試套件：
```bash
python test_enhanced_batch_reports.py
```

預期結果：
- ✅ 系統狀態：所有組件正常
- ✅ 功能列表：80%+ 功能可用
- ✅ 趨勢分析：成功識別趨勢
- ✅ 批量報告：生成符合 plan.md 的文件結構
- ✅ 前端兼容：所有頁面正常運作

## 📞 支援聯絡

如果在遷移過程中遇到問題，請：
1. 檢查日誌文件：`logs/api_YYYYMMDD.log`
2. 運行診斷腳本：`python test_enhanced_batch_reports.py`
3. 查看詳細錯誤信息並參考故障排除部分

---

**遷移完成後，您將擁有一個完全符合 plan.md 規範的增強版批量報告生成系統！** 🚀
