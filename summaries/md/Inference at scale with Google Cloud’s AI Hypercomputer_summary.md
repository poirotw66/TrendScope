# Inference at scale with Google Cloud’s AI Hypercomputer

[會議影片連結](https://www.youtube.com/watch?v=susBrCautR8)
在 Google Cloud 的 AI Hypercomputer 上大規模推論

## 1. 核心觀點

本次會議主要介紹 Google Cloud 的 AI Hypercomputer 在大規模推論方面的進展，包括硬體加速器（TPU 和 GPU）的選擇、LLM 推論的優化方案（VLLM 和 Jetstream）、以及 Pathways 架構帶來的性能提升。同時，也邀請了 Osmos 和 Contextual AI 這兩家合作夥伴，分享他們如何利用 AI Hypercomputer 來驅動實際工作負載。

## 2. 詳細內容

*   **AI Hypercomputer 的基礎與演進：**
    *   預計 2025 年將是推論時代的開始，Google Cloud 的 AI Hypercomputer 作為基礎，支援越來越多的 AI 推論工作負載。
    *   AI 應用需求變得更加多樣和複雜，AI 代理將主動檢索和生成數據，以提供洞察和答案。
    *   AI Hypercomputer 提供靈活、高效、易用且可擴展的雲端推論基礎設施。

*   **硬體加速器的選擇：**
    *   Google Cloud 提供 TPU 和 NVIDIA GPU 兩種高性能、可擴展的 AI 加速器選擇。
    *   Google 內部的 Gemini 訓練和服務都運行在 TPU 上。
    *   與 NVIDIA 緊密合作，提供增強的可靠性和優化的函式庫。

*   **LLM 推論的優化方案：**
    *   **VLLM on TPUs：**
        *   將領先的開源推論引擎 VLLM 引入 TPU，只需幾行程式碼即可在 GPU 和 TPU 之間靈活切換。
        *   與 VLLM 社群緊密合作，優化了流行的開源模型，使其能夠在 TPU 上運行。
    *   **Jetstream：**
        *   Google 基於 Gemini 服務堆疊的 JAX 推論引擎。
        *   支援 DeepSeq R1 和 V3，並正在開發 LAMA 4 支援。
        *   支援長上下文，最高可達 256K，並針對分塊預填充、前綴快取和頁面保留進行了優化。
        *   在 LAMA 2 70B 和 Mixtrel 模型上，Trillium 的性能分別比上一代 V5e 提升了 2.9 倍和 2 倍。
    *   **Pathways：**
        *   Google 內部的架構和分散式運行時技術，用於所有 Google 內部的 AI 專案。
        *   允許可獨立擴展預填充和解碼，從而提供超低延遲服務。
        *   支援多主機，允許將工作負載分佈在多個主機上。
        *   在 LAMA 3 405b 上，Trillium 的每次推論成本降低到 1 美分/千個 token。
        *   預填充時間從約 2 秒減少到 277 毫秒，輸出 token 生成的延遲提高了 3 倍。

*   **Osmos 的案例分享：**
    *   Osmos 構建了世界第一個完全自主的數據整理器，利用 AI 代理群來自動化數據整理流程。
    *   訓練在 GKE 上使用 TPU 進行，推論則使用 Jetstream 和 VLLM。
    *   使用 Jetstream 實現了容器可靠運行數月的目標。
    *   使用 VLLM 實現了 Day Zero 模型支援、API 兼容性和零配置的優異性能。
    *   透過 TPU 和 VLLM，可以獲得與推論即服務提供商相媲美的每 token 定價。

*   **MaxDiffusion 和 Diffusion 模型：**
    *   MaxDiffusion 是一個高性能且具有成本效益的 Diffusion 模型參考實現，使用 Python 和 JAX 編寫。
    *   易於使用，可擴展，且靈活。
    *   Trillium 提供了迄今為止最佳的推論性能，比之前的 TPU 推論晶片 V5E 提高了約 3.5 倍。
    *   使用 MaxDiffusion，生成 1000 張圖像的成本可以低至 0.22 美元。
    *   HubX 使用 Trillium 和 PyTorch XLA，實現了 35% 的延遲改善和 45% 的每張圖像成本降低。

*   **GPU 推論的更新：**
    *   最新的 GPU 包括 A3 Ultra（由 H200 提供支援）和 A4（由 B200 提供支援）。
    *   在 MLPerf 推論 5.0 中，A3 Ultra H200 和 A4 VM 在各種模型上都提供了極具競爭力的性能。

*   **Contextual AI 的案例分享：**
    *   Contextual AI 構建了一個平台，利用檢索增強生成（RAG）來提供上下文相關的答案。
    *   使用動態工作負載排程器來配置 GPU 推論，並使用 GCS 儲存模型。
    *   從 A2 遷移到 A3 後，模型訓練時間減少了 60%，吞吐量提高了 30%，延遲降低了 40%。
    *   Qualcomm 使用 Contextual AI 的平台，將客戶工程問題的解決時間從一周縮短到幾分鐘。

## 3. 重要結論

Google Cloud 的 AI Hypercomputer 提供了全面的解決方案，以滿足各種規模和複雜度的 AI 推論需求。透過 TPU 和 GPU 的靈活選擇、LLM 推論的優化方案以及 Pathways 架構的性能提升，AI Hypercomputer 能夠幫助企業以更低的成本和更高的效率部署 AI 應用。同時，Osmos 和 Contextual AI 的案例也展示了 AI Hypercomputer 在實際應用中的價值。
