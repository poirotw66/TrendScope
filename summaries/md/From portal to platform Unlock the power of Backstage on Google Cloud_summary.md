# From portal to platform Unlock the power of Backstage on Google Cloud
[會議影片連結](https://www.youtube.com/watch?v=T7IMd66sZxI)
從入口網站到平台，釋放 Google Cloud 上 Backstage 的力量

## 1. 核心觀點

本次會議主要探討了如何利用 Backstage 這個框架，在 Google Cloud 上構建強大的開發者平台。核心觀點包括：

*   Backstage 並非開箱即用的開發者入口網站或平台，而是一個可擴展、可客製化的框架，用於構建開發者入口網站。
*   HCA Healthcare（美國最大的營利性醫療保健系統）如何利用 Backstage 加速應用程式開發和現代化，並遷移到雲端。
*   透過標準化技術和建立黃金路徑，可以顯著減少開發者在 sprint zero 上花費的時間。
*   利用 CNCF（雲原生計算基金會）的平台架構和開源工具，可以構建可移植且可重複使用的平台。
*   GKE（Google Kubernetes Engine）多租戶服務與 Backstage 的整合，可以實現應用程式的自助服務部署。

## 2. 詳細內容

會議首先介紹了 Backstage 的基本概念和功能，包括：

*   **軟體目錄：** 作為入口網站的起點，提供 API 和下游依賴項（如元件和基礎架構）之間的關係。
*   **軟體範本：** 提供建立和公開黃金模式的方式，並執行與第三方工具整合的動作。
*   **外掛程式：** 允許深入擴展 Backstage 並將其整合到環境的其餘部分。
*   **技術文件：** 提供在 Git 儲存庫中提供一致文件的方式。

接著，會議討論了如何在 Google Cloud 上託管 Backstage，包括使用 HTTP 負載平衡器、身份識別代理 (IAP)、Artifact Registry、Cloud Storage、Cloud SQL 和 Secret Manager。

HCA Healthcare 的 Cameron Farmer 分享了他們如何使用 Backstage 和 GKE 構建多租戶自助服務平台。他們強調了標準化技術、建立黃金路徑以及利用 CNCF 工具的重要性。他們還分享了他們的平台架構，包括網路策略、IAM、基礎架構即代碼、SRE 策略和安全措施。

Ruan Badawi 深入探討了 GKE 多租戶服務的實施細節，包括如何創建基礎架構、提供企業標準應用程式 IAC 藍圖，以及創建標準 CI/CD 管道。他還討論了如何使用 Kubernetes 標籤來隔離應用程式，以及如何使用 GitOps 儲存庫來管理叢集和部署工作負載。

Cameron Farmer 進行了演示，展示了開發人員如何使用 Backstage 部署應用程式到 GKE。演示涵蓋了創建 GCP 專案、設定 GKE 環境以及部署 Hello World 應用程式的步驟。

## 3. 重要結論

本次會議強調了 Backstage 作為構建開發者平台的強大框架的潛力。透過標準化、自動化和自助服務，企業可以顯著提高開發人員的生產力，並加速應用程式開發和現代化。HCA Healthcare 的案例研究證明了 Backstage 和 GKE 的整合可以實現應用程式的快速部署和管理。會議還強調了利用 CNCF 工具和開源技術的重要性，以構建可移植且可重複使用的平台。
