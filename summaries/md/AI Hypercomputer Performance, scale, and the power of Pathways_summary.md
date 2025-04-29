AI Hypercomputer Performance, scale, and the power of Pathways

[會議影片連結](https://www.youtube.com/watch?v=2yTzNwYLrKw)
AI Hypercomputer 的效能、規模及 Pathways 的強大功能

## 1. 核心觀點

本次會議主要介紹 Google Cloud 的 AI Hypercomputer，這是一個端到端的協同設計架構，旨在最大化 AI 工作負載的效能。會議重點包括：

*   **AI Hypercomputer 的架構：** 涵蓋效能優化的硬體、協調、運行時、框架和解決方案層，以及彈性的使用模型。
*   **Pathways 的引入：** 一個分散式運行時，可實現靈活的協調、整合的控制和互動式超級運算。
*   **Osmos 的案例：** 展示如何使用 Pathways 最大化 FLOPs 以進行開發。
*   **彈性訓練的重要性：** 強調在發生故障時，能夠縮減規模並在節點可用時擴展規模的能力。
*   **互動式開發的革新：** 透過 Pathways，開發人員可以使用低成本的 CPU 機器進行開發，並利用任意規模的運算資源。

## 2. 詳細內容

*   **AI Hypercomputer 的效能：**
    *   結合了雲端加速器 TPU 和 GPU 的優勢，這些加速器在資料中心進行協同設計，以最大化效能。
    *   使用 GKE 等可擴展的協調器，並支援 XLA 和 CUDA 運行時。
    *   提供 Cloud Diagnostic XProf 和 Torch Prime 等工具，以簡化實驗迭代和效能優化。
    *   提供 GPU 和 TPU recipes，以重現最先進的效能基準。
*   **傳統協調的限制：**
    *   在推論方面，傳統協調無法有效平衡預填充（pre-fill）和解碼階段，導致輸送量不佳。
    *   在訓練方面，傳統協調受限於「所有主機上的相同運算」模式，並且缺乏對故障的靈活應對能力。
*   **Pathways 的解決方案：**
    *   **推論：** 引入分離式服務，將預填充和解碼功能分開，以平衡算術強度並最大化輸送量。
    *   **訓練：** 允許在不同的切片上運行不同的運算，並在發生故障時提供彈性訓練的能力。
    *   **互動性：** 允許開發人員使用筆記本電腦在任意規模的叢集上進行實驗。
*   **Pathways 的架構：**
    *   作為 JAX 運行時的替代方案，允許單個 JAX 客戶端協調數千個加速器裝置上的細粒度運算。
    *   使用 Proxy 後端作為進入 Pathways 運行時的入口點。
    *   資源管理器負責 TPU 分配、操作的 GANG 排程和健康檢查。
*   **彈性訓練的實作：**
    *   使用 Elastic Manager 原始元件，在 JAX 訓練迴圈中實現彈性。
    *   在訓練迴圈中加入快照、重新分片和錯誤處理機制，以應對硬體故障。
*   **Osmos 的應用：**
    *   使用 AI 自動化資料擷取流程。
    *   利用 Pathways 進行線上強化學習，以動態調整運算資源。
    *   透過 Pathways 實現互動式體驗，簡化開發流程並最大化 FLOPs。

## 3. 重要結論

AI Hypercomputer 和 Pathways 提供了一個強大的平台，可以最大化 AI 工作負載的效能、規模和可靠性。Pathways 的靈活性、控制力和互動性，使開發人員能夠更快速地創新並構建更複雜的 AI 模型。Osmos 的案例展示了如何利用 Pathways 來解決實際問題並提高開發效率。透過採用 AI Hypercomputer 和 Pathways，組織可以加速其 AI 發展並獲得競爭優勢。
