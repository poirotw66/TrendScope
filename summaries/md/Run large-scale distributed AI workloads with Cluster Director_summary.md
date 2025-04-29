# Run large-scale distributed AI workloads with Cluster Director
[會議影片連結](https://www.youtube.com/watch?v=RmXW3UIxMYg)
執行大規模分散式 AI 工作負載與叢集管理器

## 1. 核心觀點

本次會議主要介紹 Google Cloud 的 AI 基礎設施和 Cluster Director，旨在幫助客戶更輕鬆地運行大規模分散式 AI 工作負載。核心觀點包括：

*   **Google Cloud 在 AI 領域的優勢：** Google 在 AI 領域擁有長久的歷史、強大的研究能力、豐富的模型、活躍的開源生態系統、大規模生產應用經驗以及全面的基礎設施。
*   **Google Cloud 強大的 GPU 產品路線圖：** 涵蓋 A3 Ultra、A4、A4X 等多個世代的 NVIDIA GPU，並將在 2025 年推出 RTX Pro 6000 Blackwell 和 GB300 等更強大的 GPU。
*   **Cluster Director 的重要性：** Cluster Director 是一個超級運算平台，提供卓越的效能和彈性，可輕鬆部署和管理數千個 GPU，解決了大規模 AI 訓練的挑戰。
*   **CrowdStrike 的成功案例：** CrowdStrike 透過使用 Cluster Director，在模型端到端訓練方面實現了 6 到 10 倍的速度提升。

## 2. 詳細內容

*   **Google Cloud 的 AI 基礎設施：**
    *   Google 從研究、模型、生態系統、大規模生產應用和基礎設施五個方面發展 AI。
    *   Google Cloud 提供多樣化的 GPU 選擇，包括 A3 Ultra (H200)、A4 (B200) 和 A4X (GB200)。
    *   A4 具有四倍的網路頻寬和十倍的非阻塞叢集規模，訓練效能是 A3 High 的兩倍。
    *   A4X 具有巨大的網路頻寬，訓練效能是 A3 Mega 的三倍，特別適合 MOE 模型和推理模型。
    *   Google Cloud 正在構建一個前瞻性和相容的網路基礎設施，以支援未來世代的 GPU 服務。
    *   Google Cloud 提供高效能的儲存解決方案，包括 Managed Luster 和 Rapid Storage。

*   **Cluster Director：**
    *   Cluster Director 是一個超級運算平台，提供卓越的效能和彈性。
    *   Cluster Director 具有以下關鍵功能：
        *   **輕鬆的叢集管理：** 透過預定義的藍圖或引導式建立，簡化叢集建立和配置。
        *   **簡化的工作負載最佳化和部署：** 提供預先配置的軟體堆疊和優化的模型配方。
        *   **全面的可觀察性：** 提供 360 度視圖的叢集健康狀態、資源使用情況和工作負載效能。
        *   **內建的彈性：** 透過多層檢查點服務、自動健康檢查和 AI 健康預測器，確保工作負載的穩定性和可靠性。
    *   Cluster Director 透過自動化叢集設定、最佳化配方、密集部署、快速檢查點和智慧型修復策略，縮短了 AI 訓練的時間。
    *   AI 健康預測器利用 Google 的 AI 技術，分析模式並識別潛在的節點故障，提前預防停機。

*   **CrowdStrike 的經驗分享：**
    *   CrowdStrike 選擇 Google Cloud 作為其 AI 基礎設施平台，因為其具有可信賴的效能、彈性和可管理性。
    *   CrowdStrike 透過使用 Cluster Director，在模型端到端訓練方面實現了 6 到 10 倍的速度提升。
    *   CrowdStrike 使用 Cluster Director 的叢集工具包來自動化部署，並根據需求擴展儲存。
    *   CrowdStrike 使用 Slurm 進行資源分配和排程，並將叢集劃分為不同的資源池，以滿足不同的工作負載需求。
    *   CrowdStrike 利用 Cluster Director 的可觀察性解決方案來監控叢集健康狀態和工作負載效能。
    *   CrowdStrike 感謝 Google 提供的支援，幫助他們解決了擴展訓練時遇到的問題。

## 3. 重要結論

Google Cloud 透過其強大的 AI 基礎設施和 Cluster Director，為客戶提供了一個高效、可靠且易於管理的平台，以運行大規模分散式 AI 工作負載。CrowdStrike 的成功案例證明了 Cluster Director 的價值，它可以幫助客戶加速 AI 模型的訓練，並更快地將其應用於實際場景中。
