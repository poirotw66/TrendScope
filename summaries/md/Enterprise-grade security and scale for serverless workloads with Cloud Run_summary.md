# Enterprise-grade security and scale for serverless workloads with Cloud Run
[會議影片連結](https://www.youtube.com/watch?v=EEUZtcYHi78)
適用於 Cloud Run 的企業級安全性和規模，以實現無伺服器工作負載

## 1. 核心觀點

本次會議主要介紹了 Google Cloud Run 如何為企業級應用提供安全、可擴展的無伺服器工作負載平台。Cloud Run 的核心優勢包括：簡化操作、內建安全性、廣泛的應用場景支援、以及成本效益。此外，會議還重點介紹了 Cloud Run 在 AI 應用、網路效能、身份驗證、高可用性、資料處理、管理和安全等方面的最新進展。ANZ 銀行分享了他們使用 Cloud Run 的經驗，強調了其在簡化開發、降低成本和提高可靠性方面的價值。

## 2. 詳細內容

*   **Cloud Run 簡介：** Cloud Run 是 Google 的全託管無伺服器容器平台，可讓您在 Google 的基礎架構上執行程式碼函式或容器。它能夠快速擴展以滿足流量需求，並在非高峰時段自動縮減至零。Cloud Run 與 Google Cloud 服務（如 Secret Manager、Cloud Monitoring、Cloud Storage 等）整合，並支援各種企業工作負載，包括 AI 推論、Web 服務、API 後端和資料處理。

*   **Cloud Run 的企業級功能：**
    *   **安全性與合規性：** Cloud Run 內建安全性，提供雙層沙箱、資料加密和存取控制。它符合 FedRAMP、HIPAA 和 PCI 等主要認證。
    *   **廣泛的應用場景支援：** Cloud Run 適用於各種應用，包括公用應用、私有應用、雲原生應用和傳統應用。它也支援輕量級應用和重量級 Java Spring Boot 應用。
    *   **成本效益：** Cloud Run 具有快速自動擴展和自動縮減至零的功能，讓您只需為實際使用的資源付費。它還提供區域冗餘、多種計費模式和承諾使用折扣。

*   **Cloud Run 的最新進展：**
    *   **AI 應用：** Cloud Run 支援使用 Vertex AI 託管 AI 模型，或直接在 Cloud Run 中使用 GPU 託管模型。它提供 Cloud Storage Volume Mounts 功能，可輕鬆存取 Cloud Storage 中的 AI 模型。
    *   **網路效能：** DirectVPC Egress 提供更快速、更可擴展、更可靠且成本更低的 VPC 網路連線。它還支援 IP 受限環境和 Cloud Run Jobs。
    *   **身份驗證：** Identity Aware Proxy (IAP) 現在已內建於 Cloud Run 中，可簡化最終使用者存取控制。
    *   **高可用性：** Cloud Run 是一個區域服務，提供區域複製和區域容錯移轉。它還支援使用單一 GCloud 命令將 Cloud Run 服務部署到多個區域，並即將支援跨區域容錯移轉。
    *   **資料處理：** Cloud Run Jobs 適用於排程批次作業，Cloud Run 服務適用於處理來自佇列的事件。即將推出的 Cloud Run Worker Pools 專為非基於請求的工作負載（如 Kafka 消費者）而設計。
    *   **管理和安全：** Cloud Run 具有細緻的 IAM 權限、威脅偵測、自訂組織政策、預設 URL 停用、自動基礎映像更新和多種 Assured Workloads。

*   **ANZ 銀行案例分享：** ANZ 銀行是一家雲原生數位銀行，使用 Cloud Run 執行其關鍵功能，包括客戶權益、交易歷史記錄、管理卡片和設定以及傳送推播通知。ANZ 銀行發現 Cloud Run 簡化了部署和擴展、降低了基礎架構成本，並提高了開發人員的生產力。他們還利用 Cloud Run 的多區域功能來實現高可用性。

## 3. 重要結論

Cloud Run 是一個功能強大且多功能的平台，可為企業提供安全、可擴展且經濟高效的無伺服器解決方案。透過簡化操作、內建安全性以及廣泛的應用場景支援，Cloud Run 使企業能夠專注於創新並更快地交付價值。ANZ 銀行成功使用 Cloud Run 的案例證明了其在實際應用中的價值。Cloud Run 的持續發展和新功能的推出，使其成為企業構建和部署現代應用程式的理想選擇。
