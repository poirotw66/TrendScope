Expert techniques for deploying open models using Vertex AI
[會議影片連結](https://www.youtube.com/watch?v=RGw1yJuVvxM)
使用 Vertex AI 部署開放模型的專家技巧

## 1. 核心觀點

本次會議主要探討了在 Vertex AI 上部署開放模型的專家技巧，涵蓋模型探索、選擇、部署、監控、安全性和成本優化等方面。Yahoo! Mail 的案例研究展示了如何利用這些技巧來簡化郵件管理。

## 2. 詳細內容

**模型探索與部署：**

*   Vertex AI Model Garden 提供多樣化的模型選擇，包括 Google 模型、開源模型和第三方模型，可透過 Hugging Face 整合或自託管方式存取。
*   Vertex AI Prediction 作為後端引擎，提供可靠的模型託管、內建安全性和智慧功能。
*   Fast Deploy 功能可在兩分鐘內快速部署熱門模型，透過快取模型於高效能儲存和集叢池來提升開發者體驗和迭代速度。
*   VLM 和 Hex LLM 等優化容器可顯著提升 Vertex AI 上的效能，包括更快的載入速度、更少的等待時間以及更高的吞吐量。
*   Prefix caching 和 speculative decoding 等技術可加速 LLM 的運行速度，同時保持準確性。
*   可使用 Hugging Face 和 Axolotl 等工具在 Vertex AI Training 上進行高效的微調，並使用 VLM 等優化容器來部署這些模型。
*   使用者可以將自定義模型權重上傳到 Cloud Storage bucket，並使用 Model Garden SDK 進行部署。

**模型監控、安全與成本優化：**

*   Vertex Model Garden 在 Cloud Monitoring 中提供預建儀表板，顯示使用量、延遲和錯誤，方便快速發現問題。
*   Model Garden 的組織政策提供集中控制模型存取和操作的場所，實現細粒度的存取控制。
*   Spot VMs 提供折扣的運算資源，適用於容錯 AI 工作負載和實驗。
*   GC 預留和承諾使用折扣可跨多個 Vertex AI 產品共享 GPU 容量，最大化 GPU 投資。

**Yahoo! Mail 案例研究：**

*   Yahoo! Mail 的目標是簡化日常任務，Mail TLDR 提供長郵件的簡短摘要，提升郵件管理效率。
*   Yahoo! Mail 在模型選擇過程中考慮了規模、近乎即時的延遲和成本要求。
*   他們從 GPT-4 zero-shot prompting 開始實驗，然後轉向 Mistral 的七百萬參數微調模型，並使用 LoRa 進行優化和成本節省。
*   後續探索包括使用 Lava 和 Mistral 模型進行合成資料生成，以及使用 QAN 模型進行特定任務建模。
*   最終，Gemini 1.5 Flash 在 Vortex AI for Model Garden 上展現了成本和品質的巨大提升。
*   L4 GPUs 提供了最佳的成本效益。
*   VLM 因其簡單性、開源支援和硬體相容性而被選中。
*   Vertex AI Online Endpoint 提供了理想的託管解決方案，降低了營運開銷，並專注於模型部署和開發。
*   近乎即時的 TLDR 處理架構涉及將郵件放入事件佇列，由電子郵件處理程序處理，然後發送到 Vortex Endpoint 進行推論，並進行後處理，最後儲存在資料庫中。
*   該架構每天處理約 10 億個事件，強調透過硬體、推論工具和效能選擇實現簡單性、可擴展性和成本效益。

## 3. 重要結論

Vertex AI Model Garden 提供了一個全面的平台，用於探索、部署和管理開放模型。透過利用 Vertex AI Prediction 的強大功能、優化容器和推論優化技術，企業可以有效地部署和運行開放模型，同時確保安全性和成本效益。Yahoo! Mail 的案例研究證明了這些技術在實際應用中的價值。
