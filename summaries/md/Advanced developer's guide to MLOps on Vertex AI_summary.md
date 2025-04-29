# Advanced developer's guide to MLOps on Vertex AI
[會議影片連結](https://www.youtube.com/watch?v=T1S45Bkt2Ao)
Advanced developer's guide to MLOps on Vertex AI

## 1. 核心觀點

本次會議主要探討了在 Vertex AI 上進行 MLOps 的進階開發者指南。講者 Chase Lyle 首先闡述了 MLOps 的定義，強調其為人員、流程和工具的整合，旨在快速且可靠地將機器學習應用程式部署到生產環境。會議重點涵蓋了 MLOps 的生命週期，從模型探索、資料策劃、開發實驗、發布部署到生產監控，並介紹了 Google Cloud 提供的相關工具和服務，以簡化和加速 MLOps 流程。此外，Block 公司的 Damien Ramuno Johnson 分享了他們如何利用 Vertex AI Training 加速 MLOps 工作負載的實例。

## 2. 詳細內容

**MLOps 生命週期：**

*   **探索 (Discovery)：** 尋找並採用最新的模型和技術，例如基礎模型和代理程式。Vertex AI Model Garden 和 Agent Garden 提供了最新的模型和代理程式，方便開發者使用。
*   **資料策劃 (Data Curation)：** 針對特定業務場景評估和調整模型，確保其適用性。資料策劃是常見的瓶頸，需要領域專家參與標記和生成提示詞。BigQuery 多模態表格可以幫助整合和分析多種資料類型。
*   **開發與實驗 (Development & Experiment)：** 透過批次預測和評估，快速迭代模型。RAG (Retrieval-Augmented Generation) 和模型客製化是常見的改進方法。全面的評估指標至關重要，應涵蓋一致性、流暢性、根據性、呈現方式和防禦性。
*   **發布與部署 (Release & Deploy)：** 進行基礎設施驗證、安全隱私審查、對抗性測試和整合測試，並使用影子部署和 Canary 部署來確保品質和安全。A/B 測試和並行部署有助於驗證模型的效能。
*   **生產與監控 (Production & Monitoring)：** 監控服務基礎設施、日誌、指標和追蹤，以確保模型和系統的效能。OpenTelemetry 的語義慣例有助於標準化 GenAI 事件和追蹤。

**Google Cloud 工具和服務：**

*   **Vertex AI Model Garden 和 Agent Garden：** 提供最新的模型和代理程式。
*   **BigQuery 多模態表格：** 整合和分析多種資料類型。
*   **Vertex AI Evaluation：** 評估模型和代理程式的效能。
*   **Vertex AI Experiments：** 追蹤和比較不同的實驗結果。
*   **Vertex AI Agent Engine：** 簡化代理程式的部署。
*   **Cloud Build：** 管理 CI/CD 流程。
*   **Cloud Logging, Cloud Monitoring, Cloud Tracing：** 監控應用程式的效能。
*   **Vertex AI Training：** 用於模型訓練。
*   **Dynamic Workload Scheduler：** 確保 GPU 資源的可用性。
*   **Cascade：** 一個開源函式庫，簡化 Vertex Training 的 API 使用。

**實際案例：**

Elia Sechi 展示了如何使用 Vertex AI 工具和服務構建和評估零售代理程式的演示。演示涵蓋了從 Model Garden 探索模型、使用 Colab Enterprise 策劃資料、使用 Vertex AI Agent Engine 部署代理程式，以及使用 Cloud Build 管理 CI/CD 流程的整個過程。

Damien Ramuno Johnson 分享了 Block 公司如何使用 Vertex AI Training 加速 MLOps 工作負載的經驗。他們使用 Vertex Workbench 進行資料探索和互動，並使用 Vertex Training 進行模型訓練。他們還開源了一個名為 Cascade 的函式庫，以簡化 Vertex Training 的 API 使用。

## 3. 重要結論

本次會議強調了 MLOps 在機器學習應用程式開發和部署中的重要性，並展示了 Google Cloud 提供的各種工具和服務，以簡化和加速 MLOps 流程。透過實際案例的分享，與會者可以更深入地了解如何在 Vertex AI 上構建和部署高效能的機器學習應用程式。會議也強調了持續監控和迭代的重要性，以確保模型在生產環境中的效能和可靠性。
