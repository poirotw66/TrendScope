# TrendScope – 趨勢收集平台後台管理系統

## 🎯 目標使用者
內部技術人員（開發人員、資料工程師、分析師）

---

## 📐 介面結構

### 🔷 Layout 整體配置

- 左側固定選單（Sidebar）
  - 系統 Logo + 名稱「TrendScope」
  - 選單項目（附 icon）：
    - Dashboard（總覽）
    - Database（資料庫管理）
    - Report（報告管理）
    - Crawler Management（爬蟲管理）
    - System Settings（系統設定）
    - Log Query（日誌查詢）


- 頂部導覽列（Topbar）
  - 當前頁面標題
  - 使用者資訊（帳號、語言切換、登出按鈕）
  - 快速操作（如一鍵摘要、通知中心）

- 主內容區（Main Content）
  - 根據頁面顯示各功能模組
  - 桌機優先響應式設計，行動裝置自動縮起 Sidebar

---

## 🏠 Dashboard（儀表板）

- 系統整體狀態總覽
- 資訊卡片（Overview Cards）：
  - 目前任務數
  - 今日產生摘要數
  - 待審核報告數
  - 系統警示
- 任務狀態圖表、摘要產出趨勢圖
- 快速入口（如「建立新任務」、「上傳檔案」）

---

## 📚 Database（資料庫管理）

- 趨勢資料表格
  - 欄位：Conference、Date、Meeting、URL、Abstract、Topic、Other
  - 支援：
    - 關鍵字搜尋
    - 篩選器（分類、來源、主題）
    - 排序（時間、來源）
    - 分頁顯示
    - 批次匯出/刪除
  - 點擊可檢視詳細內容與摘要

---

## 📈 Report（報告管理）

- 報告清單檢視
  - 報告標題、日期、負責人、狀態（草稿 / 已發布）
  - 支援搜尋、篩選、排序
- 報告詳情頁
  - 支援下載 PDF / JSON
  - 顯示資料來源摘要與分析圖表
  - 報告審核與發布流程
- 新增報告流程
  1. 選擇資料範圍
  2. 設定分析模板
  3. 預覽與儲存 / 發布

---

## 🤖 Crawler Management（爬蟲管理）

- 爬蟲列表（表格呈現）
  - 欄位：名稱、來源、狀態（啟用 / 停用 / 出錯）、最後執行時間
  - 支援搜尋、篩選、排序
- 支援功能：
  - 手動觸發
  - 檢視錯誤日誌
  - 啟用/停用切換
- 新增爬蟲流程
  - 上傳 YAML / JSON
  - 或透過表單建立新任務
- AI Agent - crawler mcp
  - AI agent 輔助構建爬蟲流程

---

## 🛠️ System Settings（系統設定）

- API 金鑰與參數管理
- BigQuery/Cloud Storage 設定
- 使用者權限管理
- 系統參數調整

---

## 📝 Log Query（日誌查詢）

- 系統日誌查詢、錯誤追蹤
- 支援搜尋、篩選、下載

---

## 🧱 技術建議

- 前端框架：React + TypeScript
- 圖表：Recharts / Chart.js / ECharts
- 表格：TanStack Table（React Table）
- API 層：FastAPI
- 狀態管理：React Context / Redux Toolkit
- UI 統一風格：Ant Design / Material UI

---

## 📱 響應式設計建議

- 桌機版為主，行動裝置支援基本瀏覽
- 手機版自動縮起 Sidebar 成為漢堡選單（hamburger menu）
- 重要操作按鈕與通知在頂部導覽列顯示

---

## 💡 介面優化建議

- 支援深色模式（Dark Mode）
- 支援多語系（繁中/英文）
- 常用操作提供快捷鍵
- 重要操作提供二次確認與提示
- 各模組支援批次操作與匯出
- 介面風格現代、簡潔，重視資訊層次與可讀性