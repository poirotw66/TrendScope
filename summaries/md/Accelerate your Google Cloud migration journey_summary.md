# Accelerate your Google Cloud migration journey
[會議影片連結](https://www.youtube.com/watch?v=RNBp0UHVw2Y)
加速您的 Google Cloud 遷移之旅

## 1. 核心觀點

本次演講主要探討如何加速 Google Cloud 遷移的旅程，講者 Scott 分享了 Datadog 在協助客戶遷移雲端的經驗，強調了事前規劃、可觀測性的重要性，以及如何利用 Google Cloud 提供的工具和服務來實現更高效、安全且具成本效益的遷移。核心觀點包括：

*   **遷移前的準備：** 充分了解現有應用程式的架構、依賴關係和效能指標，建立詳細的資產清單。
*   **可觀測性的重要性：** 利用 Datadog 等工具監控遷移過程中的系統效能、安全性和成本，及早發現並解決問題。
*   **選擇合適的遷移策略：** 根據應用程式的特性和業務需求，選擇最適合的遷移策略，例如重新託管、重新平台化、重新架構等。
*   **安全性優先：** 在遷移過程中始終將安全性放在首位，利用 Google Cloud 提供的安全工具和服務來保護資料和應用程式。
*   **成本優化：** 遷移後持續監控和優化雲端資源的使用，以降低成本並提高效率。

## 2. 詳細內容

*   **講者介紹：** Scott 介紹自己是 Datadog 的技術推廣工程師，熱愛雲端技術和狗狗。Datadog 是一個 SaaS 平台，提供可觀測性、安全性和其他統一平台服務，每天分析來自數千個客戶的數兆事件。
*   **遷移的障礙：** 應用程式的規模、複雜性和客製化程度，以及團隊的技能不足，都可能成為遷移的障礙。
*   **遷移的動機：** 遷移到 Google Cloud 的主要動機包括可擴展性、可靠性、安全性、成本優化和釋放資源。
*   **可擴展性：** Google Cloud 具有彈性，可以根據需求擴展或縮減資源。全球覆蓋範圍廣，可以將服務部署在更靠近客戶的位置。
*   **可靠性：** Google Cloud 提供高可用性的環境，具有多個資料中心和容災備援能力。
*   **安全性：** Google Cloud 提供先進的安全措施，例如 IAM，可以精細地控制存取權限。
*   **成本優化：** Google Cloud 採用隨用隨付的定價模式，可以節省基礎設施成本。
*   **遷移策略（6R/7R）：**
    *   **重新託管 (Re-host)：** 又稱「直接遷移 (Lift and Shift)」，將應用程式直接遷移到雲端，不做任何修改。這是最簡單的遷移策略，但可能不是最具成本效益的。
    *   **重新平台化 (Re-platform)：** 在遷移到雲端的過程中，對應用程式進行一些修改，例如升級作業系統或資料庫。
    *   **重新購買 (Re-purchase)：** 用雲端服務替換現有的應用程式，例如使用 SaaS 應用程式。
    *   **重新架構 (Re-architect)：** 對應用程式進行重大修改，使其更適合雲端環境，例如將應用程式轉換為微服務架構。
    *   **保留 (Retain)：** 將某些應用程式保留在現有環境中，例如由於法規或安全性的原因。
    *   **淘汰 (Retire)：** 淘汰不再需要的應用程式。
*   **Google Cloud 提供的資源：** Google Cloud 提供 Migration Center 和 Cloud Adoption Framework 等資源，可以協助客戶規劃和執行遷移。
*   **Datadog 的角色：** Datadog 可以與 Google Cloud 整合，提供可觀測性、安全性和成本監控功能，協助客戶順利遷移到雲端。
*   **Datadog 整合步驟：**
    1.  設定 Datadog 帳戶。
    2.  建立服務帳戶並將 Datadog 與 Google Cloud 整合。
    3.  建立標籤策略，例如環境、團隊等。
    4.  設定儀表板，以便視覺化監控遷移過程。
    5.  建立通訊管道，以便在發生問題時及時通知相關人員。
*   **遷移啟動：**
    1.  設定 Datadog Agent，以便收集更詳細的系統指標。
    2.  設定安全工具，例如雲端態勢管理 (Cloud Posture Management)。
    3.  建立綜合測試 (Synthetic Tests)，以便監控應用程式的可用性和效能。
    4.  設定服務等級目標 (SLO)，以便衡量應用程式的可靠性。
*   **持續監控和改進：** 在遷移後持續監控系統效能、安全性和成本，並根據需要進行調整。

## 3. 重要結論

成功遷移到 Google Cloud 需要充分的準備、合適的策略和持續的監控。Datadog 等可觀測性工具可以協助客戶順利遷移到雲端，並確保應用程式的效能、安全性和成本效益。講者強調，每個組織的遷移需求都不同，因此需要根據具體情況制定客製化的遷移計畫。
