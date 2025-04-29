# Build a serverless toolkit Empower developers with Cloud Run
[會議影片連結](https://www.youtube.com/watch?v=aqjg1QRVed8)
建構無伺服器工具組，賦能開發者使用 Cloud Run

## 1. 核心觀點

本次會議主要探討 Shopify 如何建構一個無伺服器工具組 ProdKit，以賦能開發者更輕鬆地在 Cloud Run 上部署應用程式。會議涵蓋了 ProdKit 的設計理念、架構、安全考量、可觀測性，以及實際應用案例。核心觀點包括：

*   **簡化 Cloud Run 部署流程：** ProdKit 旨在降低開發者使用 Cloud Run 的門檻，減少基礎設施設定和維護的負擔。
*   **自動化基礎設施管理：** ProdKit 提供自動化的基礎設施配置和持續部署解決方案，讓開發者可以專注於程式碼開發。
*   **強化安全性：** ProdKit 整合了多項安全措施，確保應用程式在 Cloud Run 上安全執行。
*   **提升可觀測性：** ProdKit 支援將應用程式指標傳送到 Shopify 的集中式可觀測性平台，方便開發者監控和除錯。
*   **實際應用案例：** Shopify 客戶行為 API 團隊分享了他們如何使用 ProdKit 將應用程式從 GKE 遷移到 Cloud Run，並在 Black Friday Cyber Monday 期間實現了穩定的效能。

## 2. 詳細內容

*   **ProdKit 簡介：**
    *   ProdKit 是一個無伺服器工具組，旨在簡化開發者在 Cloud Run 上部署應用程式的流程。
    *   ProdKit 提供了一個 CLI 工具（ProdCLI）、GitHub Action 工作流程和 Terraform 模組，方便開發者與基礎設施互動。
    *   ProdKit 使用一個自訂的 YAML 格式（prod.yaml）來定義基礎設施，並將其轉換為 Terraform 配置。

*   **ProdKit 的演進歷程：**
    *   最初，Shopify 嘗試使用 gcloud CLI 和 ClickOps 來部署應用程式，但發現這種方法不具備可重複性，並且實際上是在建立一個更差的 Terraform。
    *   接著，Shopify 嘗試讓開發者直接使用 Terraform，但發現 Terraform 的配置過於複雜，並且需要頻繁更新。
    *   最終，Shopify 選擇使用 prod.yaml，這讓他們可以完全更改基礎設施的底層實作，同時保持開發者介面的簡潔性。

*   **安全性考量：**
    *   ProdKit 整合了多項安全措施，包括軟體供應鏈安全、身份和存取管理以及秘密管理。
    *   Shopify 使用軟體物料清單（SBOM）、映像簽署和二進位授權來確保容器的安全性。
    *   Shopify 使用 Google Cloud Load Balancer 和 Identity Aware Proxy (IAP) 來保護應用程式的存取。
    *   Shopify 使用 Google Secrets Manager 來安全地管理應用程式的秘密。
    *   Shopify 使用 Security Command Center 和組織政策來監控和強制執行安全策略。
    *   Shopify 與 Google 合作，為 Cloud Run 引入了威脅偵測功能，以便在執行階段監控容器的行為。

*   **可觀測性：**
    *   ProdKit 支援將應用程式指標傳送到 Shopify 的集中式可觀測性平台。
    *   Shopify 使用 OpenTelemetry Collector Sidecar 來收集應用程式指標、日誌和追蹤資訊。
    *   Cloud Run 本身也提供了一些內建的可觀測性工具，例如指標、日誌和服務等級目標 (SLO)。

*   **實際應用案例：**
    *   Shopify 客戶行為 API 團隊分享了他們如何使用 ProdKit 將應用程式從 GKE 遷移到 Cloud Run。
    *   他們將 Ruby on Rails 應用程式遷移到 Rust，以獲得更好的記憶體管理和並發性。
    *   他們使用 ProdKit 來配置基礎設施、部署應用程式和管理秘密。
    *   他們在 Black Friday Cyber Monday 期間使用 Cloud Run 成功處理了大量的流量。

*   **經驗教訓：**
    *   Cloud Run 並不適用於所有情況，它更適合無狀態的 API 和資料處理應用程式。
    *   平衡自主性和可除錯性是一項挑戰。
    *   封裝 Terraform 是一項棘手的任務。
    *   無干擾的安全性很難實現。
    *   網路很複雜。

## 3. 重要結論

ProdKit 是一個成功的案例，展示了如何建構一個無伺服器工具組，以賦能開發者更輕鬆地在 Cloud Run 上部署應用程式。透過自動化基礎設施管理、強化安全性以及提升可觀測性，ProdKit 幫助 Shopify 提高了開發效率、降低了運營成本，並確保了應用程式的穩定性和安全性。本次會議為希望採用 Cloud Run 的企業提供了寶貴的參考。
