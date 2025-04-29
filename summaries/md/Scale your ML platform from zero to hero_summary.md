# Scale your ML platform from zero to hero
[會議影片連結](https://www.youtube.com/watch?v=PGXyJ2x4Nls)
從零到英雄，擴展您的機器學習平台

## 1. 核心觀點

本次演講由 Google Kubernetes Engine (GKE) 的 AI 產品團隊負責人 Nathan Beach 與 Snap 的 Liyong 共同主講，主要探討如何利用 GKE 構建和擴展機器學習 (ML) 平台。演講涵蓋了從評估、導入到生產部署的各個階段，並分享了 Snap 在 GKE 上構建 ML 平台的實踐經驗。核心觀點包括：

*   GKE 提供了豐富的工具和功能，可簡化 ML 平台的構建和擴展。
*   動態工作負載排程器 (DWS) 能夠有效提升 GPU 的可用性並降低成本。
*   Cluster Director for GKE 簡化了大規模分散式運算的管理。
*   GKE Inference Gateway 能夠顯著提升模型服務的吞吐量並降低延遲。
*   Snap 利用 GKE 實現了顯著的成本節約和穩定性提升。

## 2. 詳細內容

### 2.1 構建訓練平台

*   **評估階段：** GKE 提供了多樣化的加速器，包括 NVIDIA GPU 和 Google TPU，可滿足不同模型訓練的需求。動態工作負載排程器 (DWS) 允許用戶按需獲取計算資源，無需長期承諾。加速處理套件 (XPK) 是一個開源命令行工具，可簡化 GKE 叢集的建立和任務排程。
*   **導入階段：** Cluster Director for GKE 將數千個節點視為單一運算單元，簡化了維護、故障處理和拓撲感知排程等任務。託管 Ray 運算符減輕了平台團隊管理 Ray 的負擔。Job Set API 是一個 Kubernetes 原生 API，用於管理一組 Kubernetes 任務。
*   **生產階段：** Q 是一個作業排程系統，適用於多租戶環境，可最大化資源利用率。GKE 提供了託管 DCGM 導出器和收集器，可收集 GPU 指標並在 Cloud Console 中呈現儀表板。GKE 還提供 TPU 指標和 Job Set 的可觀察性。GKE 支援成本歸因，可按 Kubernetes 標籤分解成本。

### 2.2 構建服務平台

*   **評估階段：** GKE Inference Quick Start 是一個預覽工具，可根據用戶的延遲和吞吐量目標，提供 Kubernetes 清單，幫助用戶快速評估 GKE 的推論工作負載。DWS 經過改進，也適用於生產推論工作負載，並支援節點回收，可自動尋找新的節點來替換即將到期的節點。自訂運算類別允許用戶指定機器形狀和佈建方法的優先順序。Google Cloud 提供了具有一、二、四或八個 H100 GPU 的 VM，可提供靈活性。GKE 還支援 TPU 和 GPU 上的 VLM。
*   **導入階段：** Leader Worker Set 簡化了 Kubernetes Pod 的協調。輔助啟動磁碟可將容器映像儲存在附加磁碟上，從而顯著加快啟動時間。Google Cloud Storage Fuse 提高了從 Cloud Storage 讀取資料的速度。
*   **生產階段：** GKE Inference Gateway 能夠智慧地將請求路由到模型伺服器的副本，從而最大化吞吐量並降低延遲。GKE 提供了多個服務儀表板，可輕鬆了解應用程式服務指標。GKE Autopilot 簡化了運算資源的管理，並提供 Pod 層級的 SLA。

### 2.3 Snap 的實踐經驗

Snap 使用 GKE 獲取 CPU 和 GPU 資源，並使用 Kubeflow 實作工作管理系統。Snap 根據不同的 GPU 類型採用不同的策略。對於 T4 GPU，Snap 主要使用隨需模式。對於 A100 GPU，Snap 主要使用預留和 DWS。對於 H100 GPU，Snap 主要使用 DWS。Snap 強調 DWS 是他們最喜歡的功能之一，因為它允許他們在高峰時段輕鬆擴展資源，並在工作完成後釋放資源。Snap 還使用 Kubeflow Training Operator 管理工作，並計劃在未來支援更多類型的工作。Snap 透過 GKE 實現了顯著的成本節約和穩定性提升。

## 3. 重要結論

GKE 提供了構建和擴展機器學習平台所需的工具和功能。透過利用 GKE 的功能，企業可以簡化 ML 平台的管理，降低成本，並提高穩定性。Snap 的實踐經驗證明了 GKE 在構建大規模 ML 平台方面的有效性。
