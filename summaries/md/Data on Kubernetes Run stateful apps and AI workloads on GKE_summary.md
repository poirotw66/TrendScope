# Data on Kubernetes Run stateful apps and AI workloads on GKE
[會議影片連結](https://www.youtube.com/watch?v=udQYLxsMGeU)
在 Kubernetes 上運行具狀態應用程式和 AI 工作負載

## 1. 核心觀點

本次會議主要探討在 Google Kubernetes Engine (GKE) 上運行具狀態應用程式和 AI 工作負載的策略，重點在於成本節省和效能提升。核心觀點包括：

*   針對不同類型的具狀態應用程式選擇合適的儲存方案，例如使用 Hyperdisk 調整 IOPS 和吞吐量，或使用 Storage Pool 共享容量和效能。
*   利用 GKE Data Cache 加速讀取密集型工作負載，降低延遲並提高交易處理量。
*   針對 AI/ML 工作負載，區分訓練和推論的不同需求，並採用相應的優化策略，例如使用 Container Preloading 加速推論啟動時間，或使用 Cloud Storage FUSE 或 Hyperdisk ML 儲存模型。
*   透過客戶案例分享，展示 Quadrant 和 Codeway 如何利用 GKE 解決方案來提升其向量資料庫和 AI 應用程式的效能和效率。

## 2. 詳細內容

會議首先介紹了針對具狀態應用程式（例如 Postgres）的儲存策略。講者強調，Hyperdisk 允許獨立於容量調整 IOPS 和吞吐量，從而實現更精確的資源配置和成本節省。此外，Storage Pool 允許在多個磁碟之間共享容量和效能，提高儲存利用率。

針對延遲問題，講者介紹了 GKE Data Cache，它使用本地 SSD 作為快取層，顯著降低讀取密集型工作負載的延遲。實驗表明，使用 Data Cache 可以降低 80% 的延遲，並提高 480% 的交易處理量。

接下來，會議轉向 AI/ML 工作負載。講者區分了訓練和推論的不同需求，並提供了相應的解決方案。對於訓練工作負載，重點在於節點故障恢復和 checkpointing。對於推論工作負載，重點在於降低啟動時間。

為了加速推論啟動時間，講者介紹了 Container Preloading，它將容器映像預先載入到啟動磁碟上，從而避免了從容器註冊表下載映像的延遲。此外，講者還介紹了 Cloud Storage FUSE 和 Hyperdisk ML，它們可以有效地儲存大型模型檔案。Cloud Storage FUSE 允許直接從物件儲存桶連接到 Pod，而 Hyperdisk ML 是一種可以連接到多達 2,500 個 Pod 的區塊儲存裝置。

會議還邀請了 Quadrant 和 Codeway 的代表分享他們使用 GKE 解決方案的經驗。Quadrant 是一家向量資料庫公司，他們利用 GKE Data Cache 來加速其讀取密集型工作負載。Codeway 是一家 AI 應用程式公司，他們利用 GKE 來構建其 AI 模型開發平台和 TalkingHead 影片生成平台。

Quadrant 的代表 Terry 介紹了向量資料庫的概念，以及 Quadrant 如何幫助客戶從非結構化資料中提取洞察。他強調了 Quadrant 的速度和可擴展性，以及與 GKE 結合使用時的成本效益。

Codeway 的代表 Volkan 和 Ur 介紹了他們的 TalkingHead 影片生成平台，該平台使用 Gaussian Splatting 技術來創建逼真的 AI 頭像。他們分享了他們如何使用 GKE 來構建一個可擴展且模組化的平台，以支援其產品 Lerna。

## 3. 重要結論

本次會議提供了在 GKE 上運行具狀態應用程式和 AI 工作負載的寶貴見解。透過選擇合適的儲存方案、利用 GKE Data Cache 和採用針對 AI/ML 工作負載的優化策略，企業可以顯著降低成本並提高效能。客戶案例分享展示了 GKE 解決方案在實際應用中的有效性。會議強調了在 Kubernetes 上運行資料密集型應用程式的潛力，並為企業提供了實現其數位轉型目標的工具和知識。
