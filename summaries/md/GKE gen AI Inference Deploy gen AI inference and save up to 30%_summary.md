# GKE gen AI Inference Deploy gen AI inference and save up to 30%
[會議影片連結](https://www.youtube.com/watch?v=6DWy7vd_9Fg)
GKE gen AI 推論部署 gen AI 推論並節省高達 30%

## 1. 核心觀點

本次會議主要討論了在 Kubernetes 上使用 GKE 進行 Gen AI 推論的優勢、客戶面臨的挑戰以及 Google 提供的解決方案。重點包括：

*   **GKE 的定位：** 相較於 Vertex AI，GKE 提供更高的靈活性、可移植性以及對基礎設施更細緻的控制。
*   **客戶挑戰：** 包括成本效益、加速器資源的取得、快速變化的技術堆疊以及對開放標準和可移植性的需求。
*   **GKE 解決方案：** 透過 GKE Inference Quick Start、自定義運算類別 (Custom Compute Classes, CCC)、VLLM on TPUs 等功能，簡化評估、資源獲取和效能優化。
*   **Snap 的經驗分享：** Snap 如何利用 GKE 平台，加速 Gen AI 模型的實驗和部署，並整合到其內容理解平台中。

## 2. 詳細內容

**GKE 的優勢與定位**

*   GKE 提供在 Google Cloud 上運行 Gen AI 推論的多種選擇，相較於 Vertex AI，GKE 提供了 Kubernetes 的靈活性和可移植性，讓客戶能夠跨雲端環境部署應用程式。
*   GKE 在開源 Kubernetes 和 GKE 本身都投入了大量資源，以優化成本、吞吐量和延遲等關鍵指標。
*   GKE 不僅僅是一個推論平台，也是一個可以運行各種應用程式（包括 Web 應用程式、批次處理和 AI/ML）的通用平台。

**客戶面臨的挑戰**

*   **成本效益：** Gen AI 推論需要高效能加速器，這使得成本成為一個主要考量因素。客戶希望在加速器上獲得最大的投資回報。
*   **資源取得：** 取得加速器資源（例如 GPU 和 TPU）是一個挑戰，客戶需要制定策略來確保有足夠的容量進行推論。
*   **技術堆疊的快速變化：** Gen AI 技術堆疊的各個層面（包括模型伺服器、加速器和 Kubernetes 擴展）都在快速變化，客戶需要快速學習和適應。
*   **可移植性和開放標準：** 客戶希望保持跨雲端和本地環境的可移植性，並使用開放標準。

**GKE 提供的解決方案**

*   **GKE Inference Quick Start：** 提供基準測試數據，幫助客戶根據模型和加速器的選擇做出明智的決策，並生成最佳化的 Kubernetes 部署配置。
*   **自定義運算類別 (Custom Compute Classes, CCC)：** 允許客戶指定資源獲取的優先順序，包括不同的定價方案（例如 Spot、On-demand 和 DWS）和多個加速器，從而提高資源利用率和降低成本。
*   **DWS Flex Start：** 提供一種介於 Spot 和 On-demand 之間的容量選項，具有七天的生命週期，並提供一定的折扣。
*   **VLLM on TPUs：** 透過與 Red Hat 合作，將 PyTorch XLA 優化整合到 VLLM 伺服器中，使客戶能夠輕鬆利用 TPU 的效能，而無需深入了解底層的優化細節。
*   **Inference Optimized Gateway (Inference Gateway)：** 提供高效的 AI 推論流量管理，考慮到模型特性（例如 LLM 的 token 生成），並根據 KV 快取利用率和佇列深度等指標進行智慧路由，從而提高效能和降低延遲。
*   **儲存加速：** 提供多種儲存加速選項，包括 Secondary Boot Disk、Cloud Storage FUSE、HyperDisk ML 和 Anywhere Cache，以加速模型資料的載入和推論速度。
*   **可觀測性：** 提供開箱即用的 GPU 和 TPU 監控功能，包括 NVIDIA DCGM 整合和對常見 AI 推論伺服器的應用程式級監控。

**Snap 的經驗分享**

*   Snap 使用 GKE 平台來加速 Gen AI 模型的實驗和部署，並將其整合到內容理解平台中。
*   Snap 利用 Inference Quick Start 和 DWS 進行快速評估，使用 Leader Worker Set 進行多節點推論，並使用 VLLM 和 TPUs 降低成本。
*   Snap 強調了在整個 AI/ML 工程流程中縮短反饋迴圈的重要性，並投資於可觀測性，以監控和優化成本。

## 3. 重要結論

GKE 提供了一個強大且靈活的平台，用於在 Kubernetes 上部署 Gen AI 推論工作負載。透過 GKE Inference Quick Start、自定義運算類別和 VLLM on TPUs 等功能，客戶可以簡化評估、資源獲取和效能優化。Snap 的經驗分享展示了如何利用 GKE 平台，加速 Gen AI 模型的實驗和部署，並整合到實際的業務應用中。
