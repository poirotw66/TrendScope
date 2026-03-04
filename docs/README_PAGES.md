# GitHub Pages 部署說明（TrendScope 示範站）

## 本專案獨立發布（建議）

1. GitHub → 本 repo **Settings** → **Pages**
2. **Source**: Deploy from a branch  
3. **Branch**: `main`（或 `master`）  
4. **Folder**: `/docs`  
5. 儲存後，示範站網址為：
   - **https://\<你的 GitHub 帳號>.github.io/TrendScope/**
   - 首頁會自動導向 `example-site/`（技術趨勢報告示範）

若自訂網域已給其他專案（例如 www.bloss0m.xyz），請直接使用上述 `*.github.io/TrendScope/` 連結分享本示範，不會 404。

---

## 若要放在主站子路徑（例如 www.bloss0m.xyz/TrendScope/）

需在**主站的那個 repo** 裡新增路徑並放入本示範內容：

1. 在主站 repo 建立資料夾，例如 `TrendScope`
2. 將本 repo 的 **docs/example-site/** 底下所有檔案複製到主站的 `TrendScope/`（含 `index.html`、`trends/`、`sessions/`、`trends-analysis.html` 等）
3. 若主站有設定 base URL，需讓靜態資源與連結使用前綴 `/TrendScope/`（或依主站框架設定）

這樣訪問 **http://www.bloss0m.xyz/TrendScope/** 就會由主站提供檔案。
