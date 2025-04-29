# AI Hypercomputer Master your storage infrastructure
[會議影片連結](https://www.youtube.com/watch?v=CXwFLE4Eelg)
AI Hypercomputer 掌握您的儲存基礎架構

## 1. 核心觀點

本次會議主要介紹 Google Cloud Storage 如何針對 AI 和 ML 工作負載進行優化，並推出新的儲存產品和功能，以滿足 AI Hypercomputer 對儲存基礎架構的需求。核心觀點包括：

*   **AI Hypercomputer 的重要性：** Google Cloud 提供端到端的整合 AI 系統，包括硬體、軟體和彈性的使用模式，針對 AI 工作負載進行優化。
*   **儲存是 AI 基礎架構的關鍵：** 儲存 I/O 瓶頸會嚴重影響 GPU 利用率，儲存也是資料擷取、處理、模型訓練和推論等流程的整合元件。
*   **Google Cloud Storage 的解決方案：** 透過 Anywhere Cache 和 Rapid Storage 等產品，提供高效能、低延遲、高吞吐量的儲存解決方案，以加速 AI 工作負載。
*   **平行檔案系統的優勢：** Managed Luster 提供高效能、完全託管的平行檔案系統，適用於需要低延遲和高吞吐量的 AI 工作負載。

## 2. 詳細內容

*   **Google Cloud 在 AI 基礎架構領域的領導地位：** Forrester 研究指出，Google Cloud 在 AI 基礎架構的各個方面都名列前茅，包括路線圖、願景、執行和創新。
*   **AI Hypercomputer 的架構：** Google Cloud 採用差異化的方法，專注於端到端的整合系統，包括硬體、軟體和彈性的使用模式，提供針對 AI 工作負載優化的 AI Hypercomputer。
*   **儲存系統的類型：** 常見的儲存系統類型包括物件儲存 (Google Cloud Storage) 和平行檔案系統。物件儲存提供幾乎無限的容量和具吸引力的成本結構，而平行檔案系統提供低延遲和高吞吐量。
*   **AI 工作負載的儲存需求：** AI 工作負載需要支援從 TB 到 EB 的容量，並具有高吞吐量、低延遲和處理工作負載變化的能力。
*   **Google Cloud Storage 的產品：** Google Cloud Storage 提供區域、雙區域和多區域儲存，以及標準、近線、冷線和封存等不同的儲存類別，以滿足不同的存取頻率需求。
*   **Anywhere Cache：** Anywhere Cache 允許客戶將其資料與 GPU、CPU 和 TPU 等運算資源共同放置在儲存儲體所在的任何區域中，從而解決了 GPU 容量限制的問題，並提供高達 2.5 TB/s 的額外吞吐量和高達 70% 的延遲改善。
*   **Rapid Storage：** Rapid Storage 是一種新的高效能儲存產品，提供雲端儲存系統的可擴展性和易用性，以及平行檔案系統的效能和介面。它提供亞毫秒級延遲、2000 萬 QPS 和 6 TB/s 的吞吐量。
*   **Snap 的經驗：** Snap 使用 Google Cloud Storage 來儲存和處理大量的事件資料，並利用 GCS 的耐用性和可擴展性來支援其 AI 和 ML 工作負載。
*   **平行檔案系統 (Managed Luster)：** Managed Luster 是一種完全託管的平行檔案系統，提供高達 1 TB/s 的效能和一致的亞毫秒級延遲。它適用於需要低延遲和高吞吐量的 AI 工作負載。
*   **Technology Innovation Institute 的經驗：** Technology Innovation Institute 使用 Parallel Store 來降低檢查點成本，並提高效能和降低成本。

## 3. 重要結論

Google Cloud Storage 提供一系列的儲存產品和功能，以滿足 AI Hypercomputer 對儲存基礎架構的需求。透過 Anywhere Cache、Rapid Storage 和 Managed Luster 等產品，客戶可以加速其 AI 工作負載，並降低成本。本次會議強調了儲存在 AI 基礎架構中的重要性，並展示了 Google Cloud 如何透過創新來解決 AI 工作負載的儲存挑戰。
