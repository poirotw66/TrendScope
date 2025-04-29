# Building and serving the next generation AI Models with JAX
[會議影片連結](https://www.youtube.com/watch?v=fcI9A-pjNlU)
使用 JAX 建構和提供下一代 AI 模型

## 1. 核心觀點

本次會議主要探討了如何使用 JAX 框架在 Google Cloud 上建構和部署下一代 AI 模型，特別是大型語言模型（LLM）和混合專家模型（MOE）。會議重點包括 JAX 的優勢、Google Cloud 提供的 JAX 生態系統、以及 Kakao 和 Children's Hospital of Philadelphia 等機構的實際應用案例。

## 2. 詳細內容

**JAX 框架與 Google Cloud 生態系統**

*   **JAX 簡介：** JAX 是一個高性能的機器學習框架，以編譯器為導向，模組化且完全基於 Python，使其具有高性能、可擴展性和易用性。
*   **Google Cloud 上的 JAX 堆疊：** Google Cloud 提供了針對 TPU 和 GPU 優化的 JAX 堆疊，包括 XLA 編譯器、FLAX（用於神經網路建構）、RBACs（用於檢查點）、OPTAX（用於優化器）、Grain（用於確定性資料載入）、AQT（用於量化）和 Jetstream（用於高性能推論）。
*   **MaxDiffusion 和 MaxText：** Google Cloud 提供了 MaxDiffusion（用於擴散模型）和 MaxText（用於 LLM 和 MOE 模型）的參考實現。
*   **XPK：** XPK 是一個工具，允許機器學習工程師使用機器學習語義在 GKE 上建立、管理和執行作業，而無需了解 Kubernetes。
*   **JAX AI 映像：** Google Cloud 提供了 JAX AI 映像，這些映像是 Docker 映像和工件，打包了 JAX 框架和 JAX 函式庫，以及其他工具，為在 GCP 上執行 JAX 工作負載提供了強大的基礎。
*   **優化配方：** Google Cloud 還提供了許多 MaxText 和 MaxDiffusion 模型的優化配方，以便輕鬆進行基準測試和在 Google Cloud 上使用 JAX。
*   **開發者工具：** Google Cloud 提供了用於分析、監控和日誌記錄的開發者工具，包括 Cloud Diagnostics XProf 函式庫，用於在 GCP 上輕鬆進行機器學習工作負載分析。

**Kakao 的 LLM 開發經驗**

*   **轉向 TPU 的原因：** Kakao 為了獲得更好的成本效益比，決定從 GPU 轉向雲端 TPU。
*   **JAX 堆疊的客製化：** Kakao 客製化了 JAX 堆疊，包括資料管道，以實現訓練靈活性和與 GPU 上的 Megatron LLM 的相容性。
*   **多來源混合：** Kakao 使用 Grain 的混合功能，以可配置的權重動態混合不同類型的內容，例如網路文本、程式碼和數學。
*   **Token 處理：** Kakao 客製化了 Token 處理方法，以與 Metron LLM 實作對齊，並提高訓練效率。
*   **訓練結果：** Kakao 成功地在 TPU-5E 上訓練了兩個重要的模型，包括從頭開始訓練的 Kanana 1.01 億模型，以及從現有的 8B 模型到 9.1B 架構的深度擴展。
*   **Trillium 的早期使用：** Kakao 透過 SPK 輕鬆地從 V5E 過渡到 Trillium，並看到了 2.7 倍的吞吐量提升。

**Kakao 的混合專家模型（MOE）經驗**

*   **實驗目標：** Kakao 的 MOE 實驗旨在探索是否可以透過將現有的密集模型升級為混合專家結構來擴展模型容量，並評估 TPU 和 MaxText 框架是否適合 MOE 訓練。
*   **模型架構：** Kakao 建立了一個 MOE 模型，該模型將 Kanana nanobase 模型升級為具有總共 64 個專家的結構，每個 Token 啟用 8 個專家，總共有 13.4B 個參數，其中 2.3B 個處於活動狀態。
*   **訓練設定：** 該模型使用與先前用於訓練原始密集模型的完全相同的資料（8000 億個 Token）進行訓練，以僅關注 MOE 架構本身的影響，並避免任何來自新資料混合的影響。
*   **訓練結果：** 實驗結果表明，即使活動參數的數量大致相同，也可以透過將密集模型升級為混合專家結構來擴展模型容量。
*   **MaxText 的優勢：** Kakao 發現 MaxText 具有簡單性、靈活性和高效性，使其成為 MOE 訓練的理想選擇。

**Children's Hospital of Philadelphia 的醫療 AI 助理**

*   **目標：** Children's Hospital of Philadelphia 正在使用 JAX 和 TPU 建立一個真正的兒科醫療助理，該助理可以回答有關患者的任何問題。
*   **方法：** 他們沒有主要依賴基於檢索的系統，而是預先訓練模型以盡可能多地了解患者，然後將個別患者識別給模型。
*   **資料：** 他們使用 Children's Hospital of Philadelphia 所有兒童的電子健康記錄（160 萬名兒童和 1.46 億份臨床筆記）來預先訓練模型。
*   **結果：** 該模型能夠以極快的速度推論，並存取有關患者的深入背景資訊。
*   **JAX 和 MaxText 的優勢：** JAX 和 MaxText 使研究人員能夠輕鬆地進行此類進展，並且易於控制不同加速器和平台上的並行性。

**Google Cloud 的持續改進**

*   **MaxText 的最新更新：** Google Cloud 不斷更新 MaxText，以支援最新的模型和技術，包括 Gemma 3、DeepSeq v3 和 Llama 4 Scout。
*   **擴展到後訓練：** 除了預訓練之外，MaxText 還擴展到後訓練，包括 SFT、GRPO 和 DPO。
*   **Pathways：** Google Cloud 正在將 Pathways 提供給客戶，Pathways 是 Google DeepMind 開發的一種用於訓練和提供 Gemini 模型的技術，它允許彈性訓練、多主機推論和互動式超級計算。

## 3. 重要結論

本次會議展示了 JAX 框架在 Google Cloud 上建構和部署下一代 AI 模型的強大功能和靈活性。透過 Kakao 和 Children's Hospital of Philadelphia 等機構的實際應用案例，我們可以清楚地看到 JAX 在 LLM 和 MOE 模型訓練、以及醫療 AI 助理開發方面的巨大潛力。Google Cloud 提供的 JAX 生態系統和持續改進，將進一步推動 AI 技術的發展和應用。
