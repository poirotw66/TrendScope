# Ray on GKE Building a next-generation AIML platform
[會議影片連結](https://www.youtube.com/watch?v=F3Ao10MV2-g)
Ray on GKE Building a next-generation AIML platform

## 1. 核心觀點

本次會議主要討論了在 Google Kubernetes Engine (GKE) 上使用 Ray 構建下一代 AI/ML 平台。核心觀點包括：

*   GKE 和 Ray 的結合為 AI/ML 工作負載提供了卓越的效能、可擴展性和可靠性。
*   Ray 是一個 Python 原生的 API 和生態系統，非常適合資料科學家，並且針對效能和規模進行了最佳化。
*   GKE 提供了領先業界的容器編排、生產處理和可靠的規模化能力，並持續投資於 AI/ML 工作負載的支援。
*   Ray Turbo 即將在 GKE 上推出，它將與 AnyScale 合作，進一步提升效能和效率。

## 2. 詳細內容

會議首先強調了 Kubernetes 和 GKE 在容器化領域的重要性，以及它們與 Ray 的協同效應。GKE 提供了強大的基礎設施，可以可靠地擴展 AI/ML 工作負載。Ray 則提供了一個易於使用的 Python API，簡化了分散式計算。

會議深入探討了客戶喜歡 Ray 的原因，包括其 Python 原生 API、效能和規模、加速器最佳化以及高效的排程和執行。Ray 已成為 AI/ML 從業人員的開放原始碼標準。

GKE 正在努力使 Ray 的使用更加容易，包括使用標籤選擇器進行協調排程、動態調整環境大小、原地 Pod 調整大小以提高利用率、以及對 TPU 的原生支援。

會議還介紹了 GKE 上 Ray 的 AI 最佳化功能，以及在 AI 超級電腦和叢集管理器方面所做的努力。這些功能旨在提供卓越的效能、可擴展性和可靠性，使客戶能夠更快地訓練更大的模型。

Ray Turbo 即將在 GKE 上推出，它將提供更高效的效能和擴展，並支援 GKE。Ray Turbo 承諾降低推論成本、提高 QPS 並加快大型資料集的載入速度。

GKE 透過 RDMA over Converged Ethernet、拓撲感知排程以及叢集管理器和 Ray Turbo 的支援，從基礎設施層到 GKE 層都進行了最佳化。

## 3. 重要結論

Ray 和 GKE 的結合為構建下一代 AI/ML 平台提供了一個強大的解決方案。GKE 提供了可靠且可擴展的基礎設施，而 Ray 則提供了一個易於使用的 Python API 和高效的分散式計算能力。Ray Turbo 的推出將進一步提升效能和效率，使客戶能夠以更低的成本構建和部署 AI/ML 應用程式。GKE 和 AnyScale 正在合作，使 Kubernetes 成為執行 Ray 工作負載的最佳平台。
