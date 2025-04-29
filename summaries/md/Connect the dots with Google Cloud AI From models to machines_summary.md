# Connect the dots with Google Cloud AI From models to machines
[會議影片連結](https://www.youtube.com/watch?v=BsGbIKwnOU0)
將 Google Cloud AI 從模型連接到機器

## 1. 核心觀點

本次會議旨在闡明 Google Cloud AI 的各個層面，協助使用者了解何時該選擇哪種 Google Cloud AI 產品。Etsy 的 Derek 分享了 Etsy 如何針對不同使用案例選擇不同的 Google Cloud AI 產品。此外，會議也探討了如何利用 NVIDIA 在 Google Cloud 堆疊中加速 AI 工作負載。

## 2. 詳細內容

*   **Google Cloud AI 堆疊概覽：**
    *   AI 超級電腦層：提供最先進的 GPU 和 TPU，用於訓練和擴展使用案例。
    *   第一方模型：包括 Gemini 2.5 Pro 以及來自合作夥伴和開放社群的 200 多個模型。
    *   Vertex AI 平台：用於部署、管理和建構預測型 AI 模型、生成式 AI 模型和代理程式。
    *   AI 代理程式：利用新推出的代理程式開發套件，使用者可以運用 Google 內建的代理程式以及客戶自建的代理程式。Google 代理程式空間結合了搜尋和 AI 代理程式的優勢，以提高組織的生產力。

*   **客戶需求演進：**
    *   需要統一的端到端資料和 AI 平台，打破資料孤島。
    *   希望賦予更多人使用 AI 的能力，提供無程式碼、低程式碼和自訂程式碼選項。
    *   避免廠商鎖定，同時確保平台具有前瞻性，能夠基於創新加速發展。
    *   在正確的時間擁有正確的資料，確保所有人都可存取他們應存取的最新資料。

*   **產品選擇決策樹：**
    *   **Google 管理服務 (Vertex AI)：** 適合優先考慮託管服務、不希望對基礎架構進行細粒度控制的客戶。適用於訓練和提供自訂預測型機器學習模型、整合 Vertex 模型花園中的 AI、以及早期採用和探索。
    *   **Cloud Run：** 適用於小型模型線上推論，並可使用過期的 CUDS。
    *   **GKE (Google Kubernetes Engine)：** 適合偏好使用 Kubernetes、需要多雲可攜性、以及進行分散式訓練和推論的客戶。特別適用於模型大於 700 億參數的情況，此時時間和價值至關重要。
    *   **GCE (Google Compute Engine)：** 適合高效能運算，並需要對基礎架構進行細粒度控制的客戶。

*   **Etsy 的案例分享：**
    *   Etsy 使用 Vertex AI 進行高效且輕鬆的模型訓練，並使用 Gemini 在 Vertex AI 中進行大規模生成式 AI 生產使用案例。
    *   Etsy 使用 GKE 作為其內部模型服務平台，以各種服務框架大規模提供數百個模型。
    *   Etsy 使用 Cloud Run 進行簡單且敏捷的服務部署。
    *   透過 Vertex AI，Etsy 在短短三個月內就將一個關鍵的大規模生成式 AI 使用案例從原型轉變為生產。
    *   GKE 提高了 Etsy 的成本效益和控制力，透過自動調整基礎架構，可以顯著降低成本。
    *   Etsy 使用 Gemini Flash 為 Etsy 商品資訊產生圖片標題，以改善搜尋引擎最佳化。
    *   Etsy 的訓練和原型設計平台依賴 Google Cloud 服務，如 Vertex AI 和 Dataflow，客戶可以自由地使用他們選擇的 ML 框架進行實驗。

*   **NVIDIA 的角色：**
    *   NVIDIA 提供全面的效能優化微服務套件，涵蓋資料準備、訓練、評估、資料檢索和服務。
    *   NVIDIA 與 GKE 合作，為分散式訓練和服務工作負載提供晶片。
    *   Google 信任 NVIDIA 的工具，並認為 NVIDIA 的價格效能對於管理基礎架構至關重要。

## 3. 重要結論

Google Cloud AI 提供了一系列產品，涵蓋從託管服務到自助式基礎架構的各種需求。選擇正確的產品取決於客戶的屬性、工作負載設定檔和權衡考量。Etsy 的案例展示了如何結合使用不同的 Google Cloud AI 產品來滿足特定的業務需求。NVIDIA 在 Google Cloud AI 生態系統中扮演著關鍵角色，提供加速 AI 工作負載所需的硬體和軟體。
