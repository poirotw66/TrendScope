Serve open models on TPUs and GKE with superior portability and price-performance

[會議影片連結](https://www.youtube.com/watch?v=FoW_ub6bwsQ)
在TPU和GKE上提供具有卓越可移植性和價格效能的開放模型

## 1. 核心觀點

本次會議主要探討如何在 Google Cloud 的 TPU (Tensor Processing Unit) 和 GKE (Google Kubernetes Engine) 上，以更佳的可移植性和價格效能來服務開放模型。核心觀點包括：

*   **TPU v5e Trillium 的優勢：** 新一代 TPU Trillium 在推論吞吐量、效能和成本效益方面都有顯著提升，尤其是在影像擴散和大型語言模型 (LLM) 方面。
*   **GKE 的優化：** GKE 提供了多項優化功能，例如次要啟動磁碟、GCSFuse、HyperDisk 和推論閘道，以提高啟動速度、資料載入速度和推論效率。
*   **VLLM 的支援：** TPU 現在支援 VLLM，這是一個廣泛採用的開源 LLM 推論引擎，讓使用者更容易在 TPU 和 GPU 之間移植模型。
*   **動態工作負載排程器 (DWS)：** DWS Flex 和 Calendar 允許使用者根據需求付費，從而降低 TPU 的成本。
*   **容器運算類別：** 容器運算類別提高了可用性，允許使用者在 TPU 和 GPU 之間切換，並根據資源可用性自動調整。
*   **HubX 的案例研究：** HubX 分享了他們如何使用 TPU 和 GKE 來優化影像生成應用程式 Momo 的效能和成本。

## 2. 詳細內容

*   **AI 服務的挑戰：** 在 AI 服務中，需要同時考慮延遲、成本和可移植性。
*   **TPU Trillium 的效能：** Trillium 提供了 4.7 倍的單晶片效能、兩倍的 HBM 和兩倍的晶片間互連，從而提高了訓練和推論的效能。
*   **儲存效能的優化：** 次要啟動磁碟、GCSFuse 和 HyperDisk 都有助於加快資料載入速度和提高啟動效率。
*   **GKE 推論閘道：** 推論閘道使用自訂指標（例如 KV 快取利用率和佇列深度）來路由流量，從而提高推論效率。
*   **VLLM 和 Jetstream：** VLLM 是一個開源 LLM 推論引擎，易於使用且可在 GPU 和 TPU 之間移植。Jetstream 是 Google 自己的高效能推論引擎，專為 TPU 上的 JAX 而建。
*   **PyTorch XLA：** OpenXLA 專案中的 PyTorch XLA 讓使用者可以輕鬆地在 GPU 和 TPU 之間切換。
*   **動態工作負載排程器 (DWS)：** DWS Flex 和 Calendar 允許使用者根據需求付費，從而降低 TPU 的成本。Calendar 允許使用者預留長達 28 天的容量，而 FlexStart 允許使用者請求長達 7 天的容量，而無需指定開始時間。
*   **容器運算類別：** 容器運算類別提高了可用性，允許使用者在 TPU 和 GPU 之間切換，並根據資源可用性自動調整。
*   **HubX 的案例研究：** HubX 使用 TPU 和 GKE 來優化影像生成應用程式 Momo 的效能和成本。他們使用次要啟動磁碟和 FileStore 來管理模型 I/O，並調整注意力區塊大小以利用 Trillium 硬體快取。

## 3. 重要結論

Google Cloud 提供了多種工具和技術，可協助使用者在 TPU 和 GKE 上以更佳的可移植性和價格效能來服務開放模型。TPU Trillium、GKE 的優化、VLLM 的支援、DWS 和容器運算類別都有助於降低成本、提高效能和提高可用性。HubX 的案例研究證明了這些技術在實際應用中的有效性。
