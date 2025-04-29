# GKE and AI Hypercomputer Build a scalable, secure, AI-ready container platform
[會議影片連結](https://www.youtube.com/watch?v=vMBqiwuO0Ms)
GKE 與 AI 超級電腦：建構可擴展、安全且支援 AI 的容器平台

## 1. 核心觀點

本次會議主要探討了 Google Cloud 的 AI Hypercomputer 如何與 Google Kubernetes Engine (GKE) 結合，為 AI 模型的訓練和推論提供高效、彈性且具成本效益的解決方案。核心觀點包括：

*   AI Hypercomputer 提供強大的基礎設施，包括 TPU 和 GPU，以滿足不斷增長的 AI 需求。
*   GKE 透過彈性訓練和推論，最大化資源利用率，降低成本。
*   動態工作負載排程器 (Dynamic Workload Scheduler, DWS) 和自訂運算類別 (Custom Compute Classes) 提升了 GPU 和 TPU 的可取得性。
*   GKE Autopilot 簡化了基礎設施管理，讓開發者更專注於 AI 模型的開發。
*   VLLM 的 TPU 支援，讓模型可以在 TPU 和 GPU 之間無縫移植，提高靈活性和成本效益。

## 2. 詳細內容

*   **AI Hypercomputer 的優勢：**
    *   基於 Google 數十年來運行大規模服務的經驗，提供選擇、彈性、效率和規模。
    *   提供專為 AI 設計的硬體，包括 TPU 和 NVIDIA GPU。
    *   透過彈性訓練，最大化 "good put"，減少浪費的時間和成本。
    *   透過彈性推論，在滿足延遲和吞吐量目標的同時，最小化基礎設施成本。

*   **彈性訓練 (Elastic Training)：**
    *   透過診斷服務和中央監管器，自動檢測和修復節點故障。
    *   可以原地重新啟動、熱交換節點，或智能調整任務大小，以確保訓練不中斷。
    *   GKE 可以管理大型叢集，最多可擴展到 65,000 個節點和 150,000 個加速器晶片。

*   **彈性推論 (Elastic Inference)：**
    *   透過 VLLM 的 TPU 支援，可以在 TPU 和 GPU 之間無縫移植模型。
    *   GKE 的自訂運算類別，可以根據需求自動擴展 TPU 和 GPU 資源。
    *   GKE 推論閘道 (Inference Gateway) 提高了 AI 服務效能，並最大化 GPU 和 TPU 的利用率。

*   **GPU 和 TPU 的可取得性 (Obtainability)：**
    *   自訂運算類別允許定義機器類型和佈建方法的優先順序列表。
    *   動態工作負載排程器 (DWS) 提供了一種經濟高效的方式來獲取批次或訓練工作負載的容量。
    *   DWS Calendar Mode 允許指定容量的開始和結束日期，確保在需要時可用。
    *   Google Cloud 提供靈活的 NVIDIA H100 GPU 存取，可選擇 1、2 或 4 個 H100 GPU。

*   **簡化 Day 2 運營：**
    *   GKE Autopilot 管理底層運算節點，讓開發者專注於應用程式。
    *   託管 DCGM 指標 (Managed DCGM Metrics) 提供 GPU 利用率的豐富指標，並自動建立儀表板。
    *   託管 AI 推論指標 (Managed AI Inference Metrics) 提供模型伺服器的指標，例如吞吐量。
    *   GKE 提供 Ray 附加元件，簡化 Ray 的部署和管理。

*   **Augment 的案例研究：**
    *   Augment 使用 GKE 和 AI Hypercomputer 建構了一個用於軟體工程師的應用程式。
    *   Augment 建立了一個大型程式碼庫的即時語義索引，以提供 AI 輔助的程式碼理解和修改。
    *   Augment 使用 GPU 進行推論和訓練，並根據工作負載動態調整資源。

## 3. 重要結論

Google Cloud 的 AI Hypercomputer 和 GKE 提供了一個強大且靈活的平台，用於建構和部署 AI 應用程式。透過彈性訓練、彈性推論、GPU/TPU 可取得性以及簡化的 Day 2 運營，企業可以降低成本、提高效率，並加速 AI 創新。VLLM 的 TPU 支援進一步增強了平台的靈活性和成本效益。Augment 的案例研究展示了 GKE 和 AI Hypercomputer 如何幫助企業建構創新的 AI 應用程式。
