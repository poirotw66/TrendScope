Agent observability 101 Evaluating output and behaviour of your agents
[會議影片連結](https://www.youtube.com/watch?v=2pTM1qGF9Ww)
Agent observability 101 評估 Agent 的輸出與行為

**1. 核心觀點**

本次會議主要探討 Agent 的可觀測性，強調在建構 Agent 時，了解其行為、評估其輸出，以及如何透過各種工具和方法來監控、除錯和改進 Agent 的效能至關重要。會議涵蓋了 Agent 可觀測性的重要性、理論基礎、實際應用，以及 Vodafone 等企業的實際案例。

**2. 詳細內容**

*   **為什麼可觀測性很重要：**
    *   Agent 的行為難以預測，可能產生不可逆的後果。
    *   原型開發快速，但後續驗證可能出現問題。
    *   真實世界的輸入難以預測，Agent 可能產生意料之外的行為。
    *   可觀測性提供控制和了解 Agent 行為的能力，降低壓力。
    *   Agent 的風險包括使用者不滿、品牌信任受損、成本浪費、安全風險等。

*   **可觀測性的關鍵支柱：**
    *   **指標 (Metrics)：** 衡量 Agent 的整體效能，例如成功率、錯誤率、回應時間、成本等。
    *   **追蹤 (Traces)：** 記錄 Agent 執行的每個步驟，包括使用的工具、輸入、輸出、推理過程等，用於詳細除錯。
    *   **使用者回饋 (Human Feedback)：** 透過使用者提供的讚或踩，以及額外的意見回饋，了解 Agent 的實際表現。
    *   **自動化評估 (Automated Evaluation)：** 模擬生產環境，自動測試 Agent 對各種情境的回應，類似於單元測試。
    *   **Agent Ops：** 將人員、流程和技術結合，建立一個結構化的方法來管理和監控 Agent。

*   **Agent Ops 的概念：**
    *   類似於 DevOps 和 MLOps，是在軟體工程和機器學習基礎上的額外層。
    *   不是取代現有的最佳實踐，而是額外的補充。

*   **工具呼叫 (Tool Calling) 的評估：**
    *   評估 Agent 是否正確選擇和使用工具。
    *   使用 Vertex AI 的 Gen AI Eval 服務，提供各種評估工具。
    *   評估 Agent 的軌跡 (Trajectory)，即呼叫工具的順序和方式。
    *   使用 LLM 作為評估者，判斷 Agent 的行為是否符合預期。

*   **可觀測性的實際應用：**
    *   使用 OpenTelemetry 標準，記錄 Agent 的行為。
    *   使用 Cloud Trace 可視化 Agent 的追蹤記錄。
    *   透過追蹤記錄，了解 Agent 的輸入、輸出、使用的模型、花費的時間等。

*   **Vodafone 的案例：**
    *   與 Google Cloud 合作，解決 Agent 的標準化、安全性和可擴展性問題。
    *   從識別良好的使用案例開始，並與業務目標對齊。

**3. 重要結論**

Agent 的可觀測性對於建構可靠、高效和安全的 Agent 至關重要。透過指標、追蹤、使用者回饋和自動化評估，可以深入了解 Agent 的行為，並不斷改進其效能。Vertex AI 提供了各種工具和服務，協助開發者建立和管理可觀測的 Agent。OpenTelemetry 和 Cloud Trace 等標準和工具，則提供了可視化和分析 Agent 行為的能力。
