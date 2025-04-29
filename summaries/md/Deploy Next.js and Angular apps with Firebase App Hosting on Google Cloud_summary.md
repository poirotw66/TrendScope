# Deploy Next.js and Angular apps with Firebase App Hosting on Google Cloud

[會議影片連結](https://www.youtube.com/watch?v=aw2YjRpvq_0)
使用 Firebase App Hosting 在 Google Cloud 上部署 Next.js 和 Angular 應用程式

## 1. 核心觀點

Firebase App Hosting 是一個以 Git 為中心的伺服器端解決方案，專為構建在 Google Cloud 上的現代 Web 框架而設計。它管理 Web 應用程式的整個堆疊，從構建管道到 CDN 和伺服器端渲染。Firebase App Hosting 現已正式發布 (GA)，支援 Angular 和 Next.js，並且也支援 Nuxt 和 Astro 應用程式（預覽版）。App Hosting 透過管理基礎設施並與 GitHub 集成以實現自動部署，從而加速開發。它還提供改進的 UX 用於除錯構建失敗、內建監控儀表板以了解應用程式效能和健康狀況，以及無需重建即可立即回滾到先前版本的功能。App Hosting 具有可擴展的基礎架構、成本效益和安全性，並與 Google Cloud Secret Manager 緊密集成，以實現企業級密鑰管理。

## 2. 詳細內容

Firebase App Hosting 使用 Cloud Build 運行框架構建，以生成靜態資源並為 Cloud Run 建立容器映像。然後，App Hosting 將該容器映像部署到 Cloud Run，Cloud Run 位於具有 CDN、負載平衡、憑證管理和 DNS 的完全託管網路層之後。

App Hosting 允許自訂底層 Cloud Run 配置以滿足應用程式的計算需求，並定義細粒度的環境配置。可以限制環境變數對構建環境或執行時環境或兩者的訪問。還可以自訂應用程式的服務區域，在美國、歐洲和亞洲提供區域，以確保未緩存的內容靠近最終使用者。

App Hosting 現在可以連接回 Google Cloud 中的 VPC 網路，以便可以使用更多後端服務來擴充應用程式的堆疊。此外，還可以自訂應用程式的構建和啟動命令。App Hosting 根據檢測到的框架提供有關如何構建和運行應用程式的智慧預設值，但如果需要自訂它們，則可以。

選擇託管解決方案時，需要考慮三個因素：基礎架構的可擴展性、成本的可擴展性以及安全性。App Hosting 透過 Cloud Run 的自動擴展、零網路定價以及與 Google Cloud Secret Manager 的緊密集成來滿足所有這些要求。

## 3. 重要結論

Firebase App Hosting 是一個功能強大且靈活的解決方案，用於部署現代 Web 應用程式。它提供了一系列功能，旨在加速開發、提高生產力並確保應用程式的可擴展性、成本效益和安全性。透過使用 Firebase App Hosting，開發人員可以專注於構建出色的應用程式，而不必擔心管理基礎架構。可以透過運行 `npm init @apphosting` 來下載範例應用程式並開始使用。
