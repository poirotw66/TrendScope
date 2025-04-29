# Transforming your business with AI The Kubernetes advantage
[會議影片連結](https://www.youtube.com/watch?v=8lveNvUEdGk)
運用 AI 和 Kubernetes 優化您的業務

## 1. 核心觀點

本次會議主要探討如何利用現有的 Kubernetes 專業知識，在 AI 時代優化業務。Google Cloud 的 Gabe Munroy 分享了 GKE 的最新進展，以及如何透過 GKE Autopilot、Gemini Cloud Assist 和新的推論功能，節省時間和資源，專注於創新。Spotify 的 Christian Lindwall 也分享了他們如何利用 GKE 驅動 AI DJ 等功能。AnyScale 的 Robert Nishihara 宣布與 Google Cloud 建立合作夥伴關係，共同為 AI 開發人員提供最佳的 Ray 體驗。

## 2. 詳細內容

*   **GKE Autopilot：** 透過完全託管的控制平面、節點的完全自動化管理和叢集資源的自動調整大小，簡化 Kubernetes 叢集操作並提高資源效率。2024 年建立的 GKE 叢集中，有 30% 使用 Autopilot 模式。Autopilot 現在支援更快的 Pod 排程、擴展反應時間和容量調整，這些都得益於 Google Cloud 獨有的硬體功能。從第三季度開始，Autopilot 的容器優化運算平台也將提供給標準 GKE 叢集。

*   **Gemini Cloud Assist Investigations：** 透過使用者提供的症狀，分析綜合資料（日誌、配置、指標等），幫助使用者了解根本原因，從而更快地解決問題。所有這些都可以在 GKE 控制台中使用，減少故障排除時間，增加創新時間。

*   **GKE 推論功能：** 解決在 Kubernetes 上部署推論時，平台團隊面臨的兩個主要挑戰：在效能和成本之間取得平衡，以及 LLM 應用程式中負載平衡的問題。
    *   **GKE 推論快速入門：** 選擇具有所需效能特性的 AI 模型，GKE 將配置正確的基礎架構、加速器和 Kubernetes 資源來匹配。
    *   **GKE 推論閘道：** 降低服務成本 30% 以上，降低尾部延遲 60%，並將吞吐量提高 40%。它提供了一個模型感知閘道，針對智慧路由和負載平衡進行了優化，並具有用於路由到不同模型版本等高級功能。

*   **Spotify 的 AI 應用：** Spotify 的 AI DJ 功能由 GKE 提供支援。AI 平台團隊在 GKE 上構建和部署 ML 平台和 AI 平台。

*   **AnyScale 合作夥伴關係：** GKE 使用者可以存取 AnyScale 的 Ray Turbo，這是一個針對大規模 AI 構建的優化 Ray 執行時。Ray Turbo 透過更智慧的排程、更快的任務執行和更好的資源管理，提供卓越的效能。

*   **Cluster Director for GKE：** 透過自動修復基於其健康狀況的故障叢集，為大規模分散式工作負載提供卓越的效能和彈性。可以使用標準 Kubernetes API 來協調所有這些。

## 3. 重要結論

AI 為平台團隊帶來了新的挑戰，但 Kubernetes 和 GKE 等現有技術和產品可以幫助應對這些挑戰。透過 GKE Autopilot、Gemini Cloud Assist、新的推論功能、與 AnyScale 的合作夥伴關係以及 Cluster Director for GKE，Google Cloud 正在幫助客戶節省時間和資源，專注於創新，並在 AI 時代取得成功。
