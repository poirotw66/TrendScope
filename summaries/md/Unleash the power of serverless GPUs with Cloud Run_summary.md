# Unleash the power of serverless GPUs with Cloud Run
[會議影片連結](https://www.youtube.com/watch?v=PKmoD3Gv31w)
使用 Cloud Run 釋放無伺服器 GPU 的力量

## 1. 核心觀點

本次演講主要介紹 Cloud Run GPU 的功能和優勢，以及如何在 Cloud Run 上使用 GPU 來構建高效能且具成本效益的 AI 應用程式。Cloud Run GPU 現已正式推出，可以在生產環境中大規模部署 AI 工作負載。它具有快速冷啟動、快速部署速度和低延遲等優勢，並支援全球多個地區。

## 2. 詳細內容

Cloud Run GPU 的主要優勢包括：

*   **隨需應變 (On-demand)：** Cloud Run 會根據流量自動擴展 GPU 實例，並在流量下降時縮減至零，以優化成本。
*   **快速冷啟動 (Fast cold start)：** Cloud Run 可以在幾秒鐘內啟動一個新的 GPU 實例，並安裝好驅動程式，這對於需要隨需應變 GPU 的線上 AI 推論工作負載至關重要。
*   **高度可擴展 (Highly scalable)：** Cloud Run 可以在幾分鐘內擴展到 100 個 GPU，以支援大規模生產 AI 工作負載。

Cloud Run GPU 的技術創新使得熱門開放模型的首次 Token 時間（cold start）低於 20 秒，包括 JAMA 3 和 DeepSeq R1 和 NAMA 3.1 等模型。如果從冷啟動時間中移除框架和模型載入，則原始 GPU 實例啟動時間（含驅動程式安裝）已優化到低於 5 秒，這在虛擬機器上通常需要幾分鐘。

演講者展示了一個演示，使用負載產生器向託管在 Cloud Run 上的穩定擴散服務發送大量提示，展示了 Cloud Run 自動擴展 GPU 實例的功能。在短短五分鐘內，Cloud Run 自動擴展了 100 個 GPU 實例來處理負載。Cloud Run 還會在流量下降時自動縮減 GPU 實例的數量至零，從而節省成本。

Wayfair、Vivo、L'Oreal、Chapter 等客戶已經在生產環境中使用 Cloud Run GPU。

## 3. 重要結論

Cloud Run GPU 提供了一個強大且具成本效益的平台，用於構建和部署 AI 應用程式。其隨需應變、快速冷啟動和高度可擴展的特性使其成為生產環境中 AI 工作負載的理想選擇。Cloud Run GPU 已經被許多客戶使用，並得到了 Olama、Nvidia 和 Hugging Face 等合作夥伴的支持。
