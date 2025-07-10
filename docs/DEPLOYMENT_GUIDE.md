# TrendScope 部署和使用指南

## 🚀 快速啟動

### **前置條件**
- Python 3.9+
- Node.js 16+
- npm 或 yarn
- Google Cloud 帳戶 (用於 BigQuery 和 Gemini API)

### **環境配置**
```bash
# 1. 設置 Gemini API 密鑰
export GEMINI_API_KEY="your-gemini-api-key"

# 2. 設置 Google Cloud 認證
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"

# 3. 設置其他環境變量（可選）
export GOOGLE_CLOUD_STORAGE_BUCKET="your-bucket-name"
```

## 📦 後端部署

### **1. 安裝 Python 依賴**
```bash
# 進入專案根目錄
cd /path/to/TrendScope

# 安裝必要依賴
pip3 install fastapi uvicorn python-dotenv
pip3 install google-generativeai google-cloud-bigquery google-cloud-storage
pip3 install pyyaml requests
```

### **2. 啟動後端 API 服務器**
```bash
# 方法 1: 使用 uvicorn 直接啟動
python3 -m uvicorn base.api.app:app --host 0.0.0.0 --port 8000 --reload

# 方法 2: 使用 Python 腳本啟動
cd base/api
python3 app.py
```

### **3. 驗證後端服務**
- API 文檔: http://localhost:8000/docs
- API 根端點: http://localhost:8000/
- 健康檢查: http://localhost:8000/

## 🌐 前端部署

### **1. 安裝 Node.js 依賴**
```bash
# 進入前端目錄
cd frontend

# 安裝依賴（如果需要）
npm install
# 或
yarn install
```

### **2. 啟動前端開發服務器**
```bash
# 使用 npm
npm run dev

# 使用 yarn
yarn dev

# 使用 Vite 直接啟動
npx vite
```

### **3. 訪問前端應用**
- 開發服務器: http://localhost:5173 (Vite 默認端口)
- 或根據終端顯示的實際端口

## 🎯 功能使用指南

### **1. 技術趨勢分析**
1. 在側邊欄點擊 **"智慧分析"** → **"技術趨勢分析"**
2. 選擇要分析的研討會（可選）
3. 設置分析會議數量限制
4. 點擊 **"開始趨勢分析"**
5. 查看五大技術趨勢和關聯性分析結果

### **2. 個性化推薦**
1. 在側邊欄點擊 **"智慧分析"** → **"個性化推薦"**
2. 配置個人興趣檔案：
   - 添加興趣領域（如：AI、機器學習）
   - 選擇專業程度（初學者/中級/專家）
   - 設置偏好趨勢（可選）
3. 配置數據範圍和推薦數量
4. 點擊 **"生成推薦"**
5. 查看個性化推薦結果和推薦理由

### **3. 增強批量報告生成**
1. 在側邊欄點擊 **"報告管理"** → **"報告處理"**
2. 選擇研討會和配置參數
3. **啟用增強功能**：
   - ✅ **LLM 趨勢分析** - 自動識別五大技術趨勢
   - ✅ **智慧推薦引擎** - 生成個性化推薦
4. 選擇分析模式和輸出模板
5. 點擊 **"開始生成報告"**
6. 下載生成的三階層報告結構

## 📊 報告結構說明

### **三階層報告結構 (符合 plan.md 規範)**
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
    ├── session-20250109-ai-soc.md
    ├── session-20250109-multimodal.md
    └── ... (其他會議頁面)
```

### **報告內容特色**
- **趨勢分析總覽**: 五大技術趨勢概述和關聯性分析
- **趨勢分類頁面**: 每個趨勢的詳細分析和相關會議
- **會議詳細頁面**: 單個會議的深度分析和趨勢標籤
- **Hugo 靜態網站**: 可離線瀏覽的完整網站包

## 🔧 故障排除

### **常見問題**

#### **1. API 連接失敗**
```bash
# 檢查後端服務是否運行
curl http://localhost:8000/

# 檢查端口是否被佔用
lsof -i :8000

# 重新啟動後端服務
python3 -m uvicorn base.api.app:app --host 0.0.0.0 --port 8000 --reload
```

#### **2. 前端編譯錯誤**
```bash
# 清除緩存並重新安裝依賴
rm -rf node_modules package-lock.json
npm install

# 或使用 yarn
rm -rf node_modules yarn.lock
yarn install
```

#### **3. Gemini API 錯誤**
```bash
# 檢查 API 密鑰是否正確設置
echo $GEMINI_API_KEY

# 測試 API 連接
python3 -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
print('API 連接成功')
"
```

#### **4. BigQuery 連接錯誤**
```bash
# 檢查認證文件
echo $GOOGLE_APPLICATION_CREDENTIALS
ls -la $GOOGLE_APPLICATION_CREDENTIALS

# 測試 BigQuery 連接
python3 -c "
from google.cloud import bigquery
client = bigquery.Client()
print('BigQuery 連接成功')
"
```

### **日誌查看**
```bash
# 後端日誌
tail -f logs/api.log

# 前端開發服務器日誌
# 查看終端輸出

# 系統日誌
tail -f /var/log/system.log  # macOS
tail -f /var/log/syslog      # Linux
```

## 📈 性能優化

### **後端優化**
- 使用 Redis 緩存頻繁查詢的結果
- 配置 BigQuery 查詢優化
- 啟用 FastAPI 的異步處理

### **前端優化**
- 啟用 Vite 的生產構建
- 配置 CDN 加速靜態資源
- 實現懶加載和代碼分割

## 🔒 安全配置

### **API 安全**
- 配置 CORS 白名單
- 實現 API 速率限制
- 添加身份驗證和授權

### **數據安全**
- 加密敏感環境變量
- 定期輪換 API 密鑰
- 配置 BigQuery 訪問控制

## 📚 更多資源

### **文檔**
- [API 文檔](http://localhost:8000/docs)
- [前端集成指南](./PLAN_MD_FRONTEND_INTEGRATION.md)
- [高級功能演示](./ADVANCED_FEATURES_DEMO.md)

### **支援**
- 查看 GitHub Issues
- 檢查測試結果文檔
- 參考實現文檔

---

## 🎉 開始使用

1. **配置環境變量** ✅
2. **啟動後端服務** ✅  
3. **啟動前端服務** ✅
4. **訪問應用界面** ✅
5. **體驗智慧分析功能** 🚀

現在您可以享受 plan.md 中描述的完整智慧化技術趨勢分析功能了！
