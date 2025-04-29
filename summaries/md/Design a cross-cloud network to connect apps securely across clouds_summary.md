# Design a cross-cloud network to connect apps securely across clouds
[會議影片連結](https://www.youtube.com/watch?v=pbnCg6X8Jek)
設計跨雲網路以安全地連接跨雲端的應用程式

## 1. 核心觀點

本次會議主要探討了如何設計和部署跨雲網路，以安全地連接分散在多個雲端和混合雲環境中的應用程式。核心觀點包括：

*   **跨雲網路的重要性：** 隨著企業採用多雲策略和生成式 AI 應用，跨雲網路變得至關重要，它能提供強大的全球連接性、可擴展性、安全性和合規性。
*   **兩種主要的部署模型：** 一種是從本地環境遷移到雲端的企業，需要強大的全球連接；另一種是雲原生企業，需要跨多個雲端的連接，以利用不同的服務和 SaaS 應用。
*   **Google Cloud 的解決方案：** Google Cloud 提供了 Cloud Interconnect、Cross-Cloud Interconnect、Network Connectivity Center (NCC) 和 Private Service Connect (PSC) 等產品，以構建安全、可擴展且高效的跨雲網路。
*   **應用程式感知能力：** 透過應用程式感知能力，客戶可以根據應用程式的優先順序來管理和優化網路流量，確保關鍵應用程式獲得足夠的頻寬。
*   **服務導向架構的演進：** 從傳統的網路架構演進到服務導向架構，可以簡化連接性，並為開發人員提供更大的自主權。

## 2. 詳細內容

*   **穩健的連接性：**
    *   **400G Interconnect：** 推出 400G Interconnect，提供更快的資料遷移速度和更低的頻寬成本，解決了客戶在構建 GenAI 應用時遇到的網路瓶頸問題。
    *   **應用程式感知能力：** 透過應用程式感知能力，客戶可以根據應用程式的優先順序來管理和優化網路流量，確保關鍵應用程式獲得足夠的頻寬。
    *   **Cross-Cloud Interconnect：** 提供跨雲的專用連接，目前已在全球 30 多個地點與 AWS 和 Azure 直接連接。
    *   **BGP 最佳路徑選擇：** 支援 BGP 最佳路徑選擇，允許客戶更精細地控制流量的進出路徑。
    *   **Interconnect 維護儀表板：** 提供 Interconnect 維護儀表板，讓客戶可以全面了解維護情況。
    *   **VPC 流量日誌：** 改善了丟包和延遲指標，客戶可以利用 VPC 流量日誌來優化混合雲基礎架構。

*   **可擴展的 VPC 架構：**
    *   **Network Connectivity Center (NCC)：** NCC 簡化了 VPC 連接，提供拓撲靈活性，並支援 IPv4 和 IPv6 子網路，實現了 10 倍的 VPC 擴展。
    *   **Inter-VPC NAT：** 透過 NCC 實現 Inter-VPC NAT，客戶可以解決 IP 位址耗盡問題，並簡化架構。
    *   **Private Service Connect (PSC)：** PSC 實現了與 SaaS 應用程式的無縫連接，無論是 Google 管理的 SaaS、合作夥伴管理的 SaaS 還是客戶自己管理的 SaaS。
    *   **PSC 傳播：** NCC 支援 PSC 傳播，允許客戶在一個 VPC 上開發 PSC，然後使用 NCC 將其擴展到任何需要存取的 VPC。
    *   **AI 管道中的 PSC：** PSC 在 AI 管道中扮演關鍵角色，用於資料準備、資料擷取、訓練和推論工作負載。

*   **安全性：**
    *   **Cloud NGFW：** Cloud NGFW 是一種分散式防火牆方法，可在主機 VM 層級強制執行精細的防火牆策略。
    *   **安全 Web Proxy：** 安全 Web Proxy 提供對 Web 流量的保護，並支援合規性目標。
    *   **整合：** Cloud NGFW 和安全 Web Proxy 可以輕鬆整合到跨雲部署架構中。

*   **服務導向架構：**
    *   **App Hub：** App Hub 透過自動化服務探索和編目，消除了生產者和消費者之間的隔閡。
    *   **服務綁定：** 服務綁定提供跨所有雲端網路產品的統一服務存取。
    *   **多叢集 PSE 服務：** 透過多叢集 PSE 服務，實現 GKE 叢集之間的直接服務到服務通訊。
    *   **Cloud NGFW 支援：** Cloud NGFW 支援內部 Proxy 負載平衡器，簡化了企業合規安全態勢的配置。

## 3. 重要結論

本次會議強調了跨雲網路在現代企業中的重要性，並展示了 Google Cloud 提供的各種解決方案，以構建安全、可擴展且高效的跨雲網路。透過採用這些解決方案，企業可以更好地利用多雲策略，並加速 GenAI 應用程式的開發和部署。此外，會議還強調了從傳統網路架構演進到服務導向架構的重要性，這可以簡化連接性，並為開發人員提供更大的自主權。
