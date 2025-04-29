```
# PyTorch on Google Cloud From experimentation to production
[會議影片連結](https://www.youtube.com/watch?v=mXPhQBglpP8)
PyTorch on Google Cloud 從實驗到生產

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 在支援 PyTorch 社群方面的進展，以及如何幫助客戶在 GCP 上實現效能和規模。核心觀點包括：

*   PyTorch 的快速成長及其三大支柱：模型、生態系統和效能。
*   Google 對 PyTorch 生態系統的深度投入，包括作為 PyTorch 基金會的創始成員，以及支援 VLLM 和 Ray 等 PyTorch 解決方案。
*   OpenXLA 作為一個開放原始碼的 ML 編譯器，如何橋接 PyTorch 到不同的硬體，並確保高效能，尤其是在大規模情況下。
*   PyTorch XLA 如何使 PyTorch 能夠在 XLA 裝置（尤其是 Cloud TPU）上高效運行。
*   透過最佳化檢查點、改進可見性和通知，以及基於策略的彈性訓練來提高 LLM 訓練工作負載的韌性。
*   NVIDIA 在韌性軟體方面的工作，以及與 Google Cloud 的整合。

## 2. 詳細內容

*   **PyTorch on GCP 概述：**
    *   PyTorch 的三大支柱：模型創新、生態系統擴展和效能需求。
    *   Google 對 PyTorch 生態系統的投入，包括對 VLLM 和 Ray 的支援。
    *   Google Cloud 客戶每天都依賴 PyTorch 來支援其關鍵的 AI/ML 工作負載。
    *   Google Cloud 提供對 PyTorch 的全面支援，包括在 TPU 和 GPU 等多樣化硬體上的訓練和推論。

*   **OpenXLA：**
    *   OpenXLA 是一個開放原始碼的 ML 編譯器，支援多種 AI 加速器。
    *   它提供了一個通用的編譯器堆疊，供 JAX 和 PyTorch 等框架使用，從而受益於共享的最佳化和開發工作。
    *   OpenXLA 是 Google 生產級 ML 編譯器的開放原始碼版本，已在 TPU 和 GPU 上運行了多個世界頂級基礎模型。
    *   OpenXLA 的核心元件包括 Stable HLO、Shardy、XLA、Pallas、Triton 和 PGRT。

*   **PyTorch XLA：**
    *   PyTorch XLA 是一個使 PyTorch 能夠在 XLA 裝置上高效運行的函式庫。
    *   它旨在透過將 PyTorch 操作轉換為 Stable HLO，然後饋送到 XLA 編譯器來實現規模化和最佳化效能。
    *   PyTorch XLA 作為 Torch.compile 的一個後端，允許使用者靈活地組合不同的執行策略。
    *   PyTorch XLA 的目標包括支援 PyTorch 社群、服務雲端客戶，以及促進生態系統發展。

*   **效能特點：**
    *   Pallas 是一個允許開發人員為 XLA 裝置編寫自訂核心的函式庫，從而實現高度最佳化的實作。
    *   主機卸載允許將模型、最佳化器狀態或啟動的部分卸載到主機的 CPU 記憶體，從而減少裝置記憶體壓力。
    *   Torch.compile 提供了一種簡單的方法來應用編譯器最佳化，只需最少的程式碼變更。
    *   在 Trillium（Google 最新的 TPU）上，LAMA 3.8b 的效能超過每晶片每秒 7,000 個 token，LAMA 3.405b 的效能超過每晶片每秒 113 個 token。
    *   VLLM 現在支援 TPU，允許使用者利用分頁偵測和連續批次處理等功能。

*   **韌性：**
    *   LLM 訓練工作負載的目標是在給定的基礎架構和時間範圍內，盡可能高效地訓練模型。
    *   關鍵挑戰包括頻繁的中斷、緩慢的檢查點方法以及難以識別和定位故障。
    *   1% 的 ML 良好輸出改進可以轉化為超過一百萬美元的成本節省。
    *   Google Cloud 引入了一系列技術來最大化良好輸出，包括最佳化的檢查點、改進的可見性和通知，以及基於策略的彈性訓練。
    *   非同步檢查點減少了訓練工作在檢查點儲存時的中斷時間。
    *   多層儲存允許快速檢查點還原，始終從最近的儲存還原。
    *   彈性訓練允許在發生故障時盡快恢復訓練工作，並可以自訂補救工作流程。

*   **NVIDIA 的貢獻：**
    *   NVIDIA 開發了韌性軟體，以提高其內部研究團隊的良好輸出。
    *   NVIDIA 的韌性軟體包括自動重新啟動、改進的檢查點功能以及準確的故障檢測。
    *   自動重新啟動功能可以透過在應用程式內檢測和處理故障來減少重新啟動時間。
    *   NVIDIA 已將其韌性工作整合到 NEMO 框架中。

## 3. 重要結論

Google Cloud 正在積極投資於 PyTorch 生態系統，並提供各種工具和技術來幫助客戶在 GCP 上實現高效能和規模。透過 OpenXLA、PyTorch XLA 和與 NVIDIA 的合作，Google Cloud 正在使 PyTorch 使用者能夠充分利用 TPU 和 GPU 等加速器的優勢，並提高 LLM 訓練工作負載的韌性。這些努力旨在降低成本、縮短訓練時間，並加速 AI 創新。
```