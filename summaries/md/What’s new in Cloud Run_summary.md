# What’s new in Cloud Run
[會議影片連結](https://www.youtube.com/watch?v=PWPvX25R6dM)
Cloud Run 最新資訊

## 1. 核心觀點

本次會議主要介紹了 Cloud Run 的最新功能和更新，涵蓋了開發者體驗、新的工作負載類型以及在 AI 應用方面的應用。重點包括：

*   **Cloud Run Functions:** 將 Cloud Run 和 Cloud Functions 合併，提供更簡化的函數部署選項，並支援單一用途函數。
*   **Cloud Storage 磁碟區掛載:** 允許將 Cloud Storage 儲存桶掛載為本地檔案系統，方便讀取大型媒體檔案和載入設定檔。
*   **Firebase App Hosting:** 與 Firebase 團隊合作，為 Angular、Next.js 和 Astro 等框架提供量身打造的部署體驗。
*   **Gemini Cloud Assist 整合:** 透過視覺化介面設計 Cloud Run 應用程式，產生 Terraform 設定和 G Cloud CLI 命令，並協助最佳化和疑難排解 Cloud Run 資源。
*   **VPC 網路改進:** 降低了 Cloud Run 服務連接到 VPC 時所需的 IP 位址數量，並增加了對 Cloud Run Jobs 的直接 VPC 支援。
*   **內建 Identity-Aware Proxy (IAP) 整合:** 透過單一核取方塊即可為內部 Cloud Run 服務啟用 IAP，簡化了身份驗證流程。
*   **Cloud Run 威脅偵測:** 持續監控執行中的容器執行個體，以偵測惡意行為和已知漏洞。
*   **多區域部署與服務健康狀態:** 結合多區域部署和服務健康狀態檢查，實現跨區域故障轉移，提高應用程式的可用性。
*   **Cloud Run Worker Pools:** 推出新的 Worker Pool 資源，用於執行持續的背景工作，例如 Kafka 消費者、PubSub 拉取和 GitHub Actions 執行器。
*   **Vertex AI Studio 整合:** 透過一鍵部署功能，將 Vertex AI Studio 中的原型部署到 Cloud Run。
*   **Cloud Run GPUs:** Cloud Run 現在支援 GPU，可用於執行 AI 推論工作負載，例如即時 LLM 推論、影像生成和媒體處理。

## 2. 詳細內容

會議首先回顧了 Cloud Run 的基本概念，強調其完全託管、可擴展、按用量計費的特性，以及在全球 Google Cloud 區域的可用性。

接著，詳細介紹了 Cloud Run Functions，強調其每個執行個體並行處理多個事件的能力，可以顯著降低延遲和成本。透過線上編輯器和 Google Code Assist，開發者可以更輕鬆地編寫和部署函數。

Cloud Storage 磁碟區掛載功能允許將 Cloud Storage 儲存桶掛載為本地檔案系統，方便讀取大型媒體檔案和載入設定檔。

Firebase App Hosting 為 Angular、Next.js 和 Astro 等框架提供量身打造的部署體驗，底層基於 Cloud Run 服務，但針對這些特定框架進行了最佳化。

Gemini Cloud Assist 整合簡化了 Cloud Run 應用程式的設計、部署、最佳化和疑難排解流程。

在網路方面，Cloud Run 降低了服務連接到 VPC 時所需的 IP 位址數量，並增加了對 Cloud Run Jobs 的直接 VPC 支援。內建 IAP 整合簡化了內部服務的身份驗證流程。

Cloud Run 威脅偵測持續監控執行中的容器執行個體，以偵測惡意行為和已知漏洞。

多區域部署與服務健康狀態檢查結合，實現跨區域故障轉移，提高應用程式的可用性。

Cloud Run Worker Pools 推出新的 Worker Pool 資源，用於執行持續的背景工作，例如 Kafka 消費者、PubSub 拉取和 GitHub Actions 執行器。

在 AI 方面，Cloud Run 與 Vertex AI Studio 整合，透過一鍵部署功能，將 Vertex AI Studio 中的原型部署到 Cloud Run。Cloud Run 也非常適合執行 AI 代理，並支援使用 Gemini API，無需擔心 API 金鑰和憑證。

Cloud Run GPUs 現在已正式推出，提供隨需、可擴展、快速啟動和按秒計費的 GPU 資源，可用於執行 AI 推論工作負載，例如即時 LLM 推論、影像生成和媒體處理。Cloud Run GPUs 支援 NVIDIA L4 GPU，並計劃在未來支援更多 GPU 類型。

Replit 和 Wayfair 的代表分享了他們使用 Cloud Run 的經驗。Replit 使用 Cloud Run 作為其平台即服務的基礎，為開發者提供快速部署和擴展應用程式的能力。Wayfair 使用 Cloud Run GPUs 來加速影像搜尋和產品發現等 AI 應用。

## 3. 重要結論

Cloud Run 持續推出新功能和更新，旨在簡化開發者體驗、擴展支援的工作負載類型，並在 AI 應用方面提供更強大的能力。Cloud Run GPUs 的正式推出，為開發者提供了在 Cloud Run 上執行 AI 推論工作負載的強大工具。透過與 Replit 和 Wayfair 等公司的合作，Cloud Run 正在成為雲端原生應用程式的首選平台。
