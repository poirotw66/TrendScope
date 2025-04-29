# NVIDIA’s special address at Google Cloud Next
[會議影片連結](https://www.youtube.com/watch?v=hReE7ncbVdg)
NVIDIA 在 Google Cloud Next 的特別演講

## 1. 核心觀點

NVIDIA 在 Google Cloud Next 的特別演講中，重點闡述了 AI 應用普及、AI 工廠的概念、以及 NVIDIA 與 Google 在 AI 基礎設施和軟體方面的深度合作。演講者強調了 AI 在各行各業的變革性影響，並介紹了 NVIDIA 最新的 Blackwell 架構和相關軟體工具，旨在加速 AI 的開發和部署，降低成本並提高效率。核心觀點包括：

*   AI 應用無處不在，正在改變各行各業的工作方式。
*   AI 工廠是 AI 模型生產的基礎，需要強大的基礎設施、安全環境和 AI 工具。
*   推理模型（Reasoning Models）是 AI 發展的重要方向，能夠進行更深入的思考和推理。
*   NVIDIA Blackwell 架構顯著提升了 AI 計算的效能和效率。
*   NVIDIA 與 Google 的合作旨在提供全面的 AI 解決方案，包括硬體、軟體和雲端服務。
*   NVIDIA 提供一系列軟體工具，如 NVIDIA Nemo 和 NVIDIA Blueprints，以簡化 AI 開發和部署。
*   NVIDIA Dynamo 能夠顯著提升 AI 推理的效能。

## 2. 詳細內容

演講首先概述了 AI 在交通運輸、石油天然氣、醫療保健、零售和金融等領域的廣泛應用。AI 不僅能提高效率，還能帶來創新，例如在醫療保健領域發現新藥物和療法，在金融領域做出更明智的決策。

接著，演講者深入探討了 AI 工廠的概念，將其比作一個生產汽車或 iPhone 的組裝線，但 AI 工廠生產的是「tokens」，即文字和圖像等資訊。AI 工廠需要強大的伺服器、資料中心和雲端基礎設施，以及一系列 AI 工具來微調、改進和優化模型。保護 AI 模型的智慧財產權至關重要，需要安全可靠的環境。

演講中還提到了 AI 計算的三個主要驅動因素：預訓練、後訓練和測試時擴展。預訓練是 AI 模型學習基礎知識的過程，需要大量的計算資源。後訓練則讓模型學習如何思考和推理，這是一個更複雜的過程，需要模型進行大量的迭代和測試。測試時擴展是指在實際應用中，模型需要生成大量的 tokens 來回答問題，這也需要強大的計算能力。

演講者介紹了 NVIDIA 最新的 Blackwell 架構，該架構旨在提升 AI 計算的效能和效率。Blackwell 能夠在降低成本的同時，增加 tokens 的生成數量，從而改善使用者體驗並提高 AI 工廠的整體產能。

NVIDIA 與 Google 在 AI 基礎設施方面有著長期的合作關係。Google Cloud 提供了 NVIDIA GPU 的各種實例，包括 A4 VM 和 A4X VM，這些實例基於 NVIDIA HGX B200 和 GP200，能夠滿足不同規模的 AI 工作負載需求。A4X VM 採用了 NVIDIA 的 NVL72 架構，可以在一個機架中連接 72 個 GPU，形成一個巨大的 GPU 叢集。

NVIDIA 不斷優化其軟體堆疊，以提高 AI 模型的效能。例如，通過軟體優化，Hopper GPU 在現代模型上的效能提高了 5 倍。NVIDIA 還推出了 NVIDIA Nemo，這是一個用於微調和優化 AI 模型的框架。NVIDIA Nemo 包含 Curator、Customizer 和 Guardrails 等工具，可以幫助開發者清理資料、微調模型並確保模型的安全性。

為了簡化 AI 開發和部署，NVIDIA 推出了 NVIDIA Blueprints，這是一個完整的 AI 代理範例，包含參考應用程式、範例資料、參考程式碼和部署工具。NVIDIA Blueprints 提供了多個生產就緒的範例，例如 PDF 到 Podcast 代理、客戶服務 AI 系統和容器安全漏洞分析工具。

NVIDIA Dynamo 是一個開源的 AI 推理伺服器，採用了最新的技術來提高推理效率。Dynamo 支援 PyTorch、VLMs、SGLang 和 TensorFlow 等多種框架，可以在 Blackwell 和 Hopper 等不同架構上運行。通過應用 Dynamo 的技術，Llama 等模型的效能可以提高 2 倍，DeepSeq 等推理模型的效能可以提高 30 倍。

演講者還介紹了 NVIDIA 在資料處理方面的合作夥伴關係，包括與 Google 合作加速 Apache Spark 和 AlloyDB。通過使用 NVIDIA 的 Rapids 庫，Spark 工作負載的效能可以提高 5 倍，成本可以降低 80%。NVIDIA 還與 Google 合作加速 AlloyDB 中的向量搜尋，使用 QVS 庫來提高向量化和搜尋的效率。

最後，演講者分享了 Spotify、Toyota 和 Shopify 等客戶的成功案例，展示了 NVIDIA GPU 在音樂推薦、品質控制和語義搜尋等方面的應用。

## 3. 重要結論

NVIDIA 在 Google Cloud Next 的特別演講中，展示了其在 AI 領域的領先地位和對 AI 未來的願景。NVIDIA 不僅提供強大的硬體基礎設施，還提供全面的軟體工具和雲端服務，旨在加速 AI 的開發和部署，並幫助各行各業的企業利用 AI 來提高效率、降低成本並實現創新。NVIDIA 與 Google 的深度合作將進一步推動 AI 的發展，並為使用者提供更強大、更高效的 AI 解決方案。
