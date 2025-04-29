# How Anthropic is pushing the computing limits of AI at scale with GKE
[會議影片連結](https://www.youtube.com/watch?v=taqYKWX5vGw)
Anthropic 如何透過 GKE 將 AI 的運算能力推向極限

## 1. 核心觀點

Anthropic 與 Google 合作，利用 Kubernetes 和 GKE（Google Kubernetes Engine）推動 AI 運算極限。Anthropic 基於 Kubernetes 構建 AI 平台，並透過客製化的排程器、快取機制和工作流程優化，實現高效能和高利用率。Google 則透過 GKE 提供大規模叢集管理能力，並與 Anthropic 合作解決擴展性挑戰。本次演講重點在於分享 Anthropic 如何利用 Kubernetes 運行大規模 AI 工作負載，以及 Google 如何透過 GKE 支援這些需求。

## 2. 詳細內容

### Anthropic 的 Kubernetes 應用

*   **為何選擇 Kubernetes：** Anthropic 在 2020 年初創時，即採用容器化工作負載，並使用 CUDA。Kubernetes 提供的語意（如優先順序、命名空間、RBAC）非常適合多租戶環境，且具備豐富的 API 和擴充性，可自訂排程和編排框架。
*   **Stateful Sets 的廣泛應用：** Anthropic 幾乎所有工作負載都使用 Stateful Sets，因為它提供固定的 Pod 索引，方便分片和領導者選舉。On-delete 更新策略允許在不關閉容器的情況下修改容器內容。
*   **反向擴展模式：** Anthropic 預先協商運算資源，因此容量固定。為了充分利用資源，他們維持大量 Pending Pods，以便在有空閒容量時立即排程低優先順序工作負載，實現機會主義研究。
*   **Kubernetes 作為中繼資料儲存：** Anthropic 將 Kubernetes 作為中繼資料的儲存庫，並建立輕量級函式庫與 Kubernetes API 互動。
*   **客製化排程器：** 由於預設的 Kubernetes 排程器不支援 Gang Scheduling，Anthropic 建立了自己的排程器，確保所有 Pods 都能同時排程，並考慮拓樸結構以降低延遲。

### 擴展性挑戰與解決方案

*   **Mega Clusters 的吸引力：** GKE 的 Mega Clusters 支援 65,000 個節點，Anthropic 認為這有助於垂直擴展，簡化中繼資料管理。
*   **大型物件問題：** Anthropic 在 Labels 和 Annotations 中儲存大量資料，導致 kubectl 指令的回應過大。
*   **解決方案：**
    *   將 Python 函式庫遷移到 Protobuf，減少回應大小和延遲。
    *   開發 KCP Cache，一個位於 API 伺服器前方的快取層，可獨立擴展讀取副本，並提供專用端點，僅返回所需資訊。
*   **濫用問題：** 透過 GCP 的可觀測性工具，Anthropic 識別出濫用 API 伺服器的使用者，並逐步優化其 Kubernetes 使用方式。
*   **Kubernetes 擴展性問題：** 與 Google 工程師合作，推動 Kubernetes 和 CNCF 產品的改進。
*   **放棄網路策略：** 由於網路策略無法擴展，Anthropic 建立基於 IP Tables 和 VPC 防火牆的內部解決方案。
*   **簡化排程：** 簡化排程演算法，假設每個節點僅運行一個工作負載，並忽略節點資源，以提高排程吞吐量。
*   **TPU 生命週期管理：** 採用長時間運行的 TPU 節點池，並透過軟體方式對 TPU 切片，減少節點池的建立和刪除操作。

### GKE 的貢獻

*   **Spanner 整合：** 將 Kubernetes 控制平面整合到 Spanner 中，提高控制平面的可擴展性和可靠性。
*   **開放標準：** GKE 遵循開放標準，確保與 Kubernetes 的相容性。
*   **簡化使用：** 使用者只需遵循升級週期，即可利用 GKE 的擴展性優勢。

### 未來展望

*   **多叢集策略：** 考慮使用多個叢集，並採用聯邦機制進行管理。
*   **多區域策略：** 探索跨多個區域部署 Kubernetes 叢集，以實現容災和資源分散。

## 3. 重要結論

Anthropic 與 Google 的合作展示了如何利用 Kubernetes 和 GKE 運行大規模 AI 工作負載。透過客製化的排程器、快取機制和工作流程優化，Anthropic 實現了高效能和高利用率。Google 則透過 GKE 提供大規模叢集管理能力，並與 Anthropic 合作解決擴展性挑戰。本次演講強調了開放標準、持續創新和合作夥伴關係在推動 AI 運算極限方面的重要性。
