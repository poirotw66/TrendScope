```markdown
# A beginner_s guide to assembling agents

[會議影片連結]()

A beginner_s guide to assembling agents

---

## 1. 核心觀點

本次會議主要介紹了 Google Cloud AI Agent Space，以及如何使用 Agent Space 構建和部署智能代理（Agent）。核心觀點包括：

- Agent Space 作為搜尋和代理的中心樞紐，可以連接各種數據源，讓代理能夠搜尋企業數據，並使用 Gemini 模型執行複雜任務。
- Agent Space 提供開箱即用的強大代理，例如 Deep Research 和 Idea Generation，可以作為構建自定義代理的靈感來源。
- Agent Space 提供無代碼代理設計器（No-Code Agent Designer）和代理開發者工具包（Agent Developer Kit，ADK），分別面向非技術人員和開發者，方便他們構建和部署代理。

---

## 2. 詳細內容

- **Agent Space 概述：**
    - Agent Space 是搜尋和代理的中心樞紐，旨在幫助用戶釋放代理的潛力。
    - 透過連接各種數據源，Agent Space 讓代理能夠以 Google 的品質和相關性搜尋企業數據。
    - 代理可以使用 Gemini 模型進行思考、行動和自動化複雜任務，還可以與其他代理協作。
    - Agent Space 提供安全合規的框架。

- **開箱即用的代理：**
    - **Deep Research Agent：**
        - 執行複雜的多步驟調查，整合來自內部企業數據和外部網路數據的信息。
        - 根據目標調整研究策略，並使用智能循環生成問題，直到達成目標。
        - 可以作為 API 使用，以增強現有代理或應用程式。
        - 目前以 Private GA 形式提供。
    - **Idea Generation Agent：**
        - 透過多代理的構思過程，幫助生成和完善解決方案，旨在推動企業的下一個重大創新。
        - 靈感來自 Google Research 的技術，該技術曾用於為生物醫學研究生成假設。
        - 能夠協調代理系統進行動態構思，並使用類似國際象棋的比賽來對所有想法進行排名。
        - 可以與結果協作以幫助完善所有想法。
        - 目前以 Private Preview 形式推出。

- **構建代理的工具：**
    - **No-Code Agent Designer：**
        - 幫助非技術人員構建代理，提供超過 30 種工具和操作，以及與企業數據的構建集成。
        - 可以用於自動化重複性任務和工作流程。
    - **Agent Developer Kit (ADK)：**
        - 開源框架，用於定義、測試和部署複雜的代理。
        - Agent Space 提供對 ADK 的原生支持，允許開發者使用 ADK 開發代理，並將其直接集成到 Agent Space 中。
        - Agent Space 負責集成、編排、UI 渲染，並使代理能夠調用 Agent Space 工具和訪問連接到 Agent Space 的數據。

---

## 3. 重要結論

Agent Space 提供了一個全面的平台，用於構建、部署和管理智能代理。透過連接數據源、提供開箱即用的代理、以及提供無代碼和基於程式碼的開發工具，Agent Space 旨在幫助企業利用 AI 自動化任務、改進決策並推動創新。
```