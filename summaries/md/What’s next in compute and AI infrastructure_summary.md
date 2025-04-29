# What’s next in compute and AI infrastructure
[會議影片連結](https://www.youtube.com/watch?v=2LPUgszg_jk)
AI 運算基礎設施的下一步

## 1. 核心觀點

本次會議主要探討 Google 在運算和 AI 基礎設施方面的最新進展，旨在幫助企業創新並釋放業務價值。Google 強調以工作負載優化的基礎設施為中心，並在 AI 領域提供端到端的整合系統，包括 AI 優化的硬體、軟體和消費模式，稱之為 AI 超級電腦。重點包括新一代 TPU（Ironwood）、GPU 策略、Cluster Director 軟體、HyperDisk EXA pools、GKE Inference Gateway 以及 Pathways 的應用。同時也關注通用計算資源的優化，以及如何幫助客戶遷移企業工作負載到 Google Cloud。

## 2. 詳細內容

*   **AI 超級電腦：** Google 致力於提供端到端的 AI 解決方案，涵蓋硬體、軟體和消費模式。
*   **Ironwood TPU：** Google 發布了第七代 TPU Ironwood，具有更強大的效能和能源效率，並針對 PyTorch 和 Jaxx 進行了優化。Ironwood Pod 可以擴展到 9,216 個晶片，組成單一互連網路結構。
*   **GPU 策略：** Google 的 GPU 策略是成為 NVIDIA GPU 的首選和最佳選擇。他們推出了基於 NVIDIA H200 的 A3 Ultra，以及基於 NVIDIA B200 的 A4 VM，並且是首家提供 B200 和 GB200 給客戶的雲端供應商。
*   **Cluster Director：** 為了應對訓練工作負載的挑戰，Google 推出了 Cluster Director 軟體，可以輕鬆部署和管理加速器群組，並支援 Google Kubernetes Engine 和 Slurm。
*   **HyperDisk EXA pools：** 針對大型 AI 訓練工作負載，Google 預覽了 HyperDisk EXA pools。
*   **GKE Inference Gateway：** 為了降低服務成本、減少尾部延遲和提高吞吐量，Google 推出了 GKE Inference Gateway。
*   **Pathways：** Google 將內部使用的分散式執行環境 Pathways 提供給客戶使用，並推出了 VLLM on TPU，方便客戶在 TPU 上使用 PyTorch 進行推論。
*   **Gen 4 計算平台：** Google 的 Gen 4 計算平台採用了 Intel、AMD 和 ARM 的最新處理器，效能提升了 30% 到 40%。
*   **C4A VM：** Google 的 C4A VM 採用了 Google 的 Axion 處理器，在價格效能方面樹立了新標準。
*   **企業工作負載遷移：** Google 提供了工具和服務，幫助客戶將企業工作負載從本地環境遷移到 Google Cloud，並優化成本。
*   **Titanium ML adapter：** Titanium ML adapter 安全地整合 NVIDIA Nix，以提供更快的 GPU 到 GPU 通訊。
*   **H4D VM：** Google 推出了 H4D，這是他們首款高效能運算 VM，提供 200 Gbps 的 RDMA。
*   **量子計算：** Google Quantum AI 發布了最新的量子晶片 Willow。

## 3. 重要結論

Google 正在不斷創新和優化其運算和 AI 基礎設施，以滿足客戶不斷變化的需求。從新一代 TPU 到 GPU 策略，再到 Cluster Director 和 HyperDisk EXA pools，Google 正在構建一個強大而靈活的平台，幫助企業在 AI 時代取得成功。同時，Google 也關注通用計算資源的優化，以及如何幫助客戶遷移企業工作負載到 Google Cloud，提供全面的雲端解決方案。
