# Build and deploy multi-agent applications with Vertex AI
[會議影片連結](https://www.youtube.com/watch?v=LBE0Q1w47lg)
使用 Vertex AI 建構和部署多代理程式應用程式

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的 Vertex AI Agent Builder，這是一個用於建構和部署多代理程式應用程式的平台。會議重點涵蓋了 Agent Builder 的三個主要組成部分：Agent Development Kit (ADK)、Agent Engine 和 Agent Garden。此外，Ford 和 Revionics 的代表分享了他們使用 Vertex AI Agent Builder 建構代理程式的經驗和演示。

## 2. 詳細內容

**AI 代理程式的演進：**

會議首先定義了 AI 代理程式，並追溯了生成式 AI 的演進歷程，從最初的 LLM 和提示，到 RAG 和 grounding，再到 LLM 作為工具使用其他服務，最終發展到多代理程式應用程式。

**Agentic 應用程式的關鍵要素：**

*   **LLM：** 用於推理和制定計畫。
*   **工具：** 外部服務的 API 和函數。
*   **代理程式定義：** 使用自然語言描述代理程式的目標、角色和行為。
*   **Agentic Orchestration：** 負責呼叫 LLM、解析計畫、執行步驟、維護狀態和記憶體的程式碼。

**Vertex AI Agent Builder：**

Vertex AI Agent Builder 旨在簡化代理程式的建構和部署，它包含以下三個主要部分：

*   **模型：** 包括 Gemini 2.5 Pro 和 Model Garden 中精選的高品質 LLM。
*   **工具和服務：** 包括 Agent Development Kit (ADK)、Agent Engine 和 Agent Garden。
*   **企業連接：** 提供將代理程式連接到企業資料、API 和 SaaS 應用程式的工具和服務。

**Agent Development Kit (ADK)：**

ADK 是一個開源的 Python SDK，用於建構多代理程式應用程式。它具有以下關鍵功能：

*   **多代理程式編排：** 處理多個代理程式之間的計畫和執行。
*   **可視化 UI：** 提供客戶端 UI，用於觀察子步驟的執行情況。
*   **確定性邏輯與 LLM 推理的交錯：** 允許在 LLM 推理中注入確定性邏輯，以處理邊緣情況。
*   **多種工具支援：** 支援非同步工具、長時間運行的工具和人機迴圈應用程式。
*   **模型不可知性：** 支援多種 LLM。
*   **MCP 協定支援：** 支援使用 MCP 協定與遠端代理程式進行通訊。

**Agent Engine：**

Agent Engine 是一個完全託管的運行時，用於簡化代理程式從開發到部署的過程。它提供以下功能：

*   **完全託管的運行時：** 提供用於執行代理程式的基礎架構。
*   **可擴展性：** 支援大規模部署代理程式。
*   **可觀察性：** 提供追蹤、日誌記錄和監控功能，以了解代理程式的行為。
*   **品質衡量和改進：** 與 Vertex AI 評估套件整合，用於衡量代理程式的品質。
*   **上下文管理：** 管理會話記憶體和範例儲存，以改善代理程式的互動。

**Agent Garden：**

Agent Garden 提供範例和工具，以幫助使用者發現和學習如何建構代理程式。它包括：

*   **代理程式範例：** 提供各種代理程式的範例程式碼，例如資料科學代理程式和客戶服務代理程式。
*   **工具：** 提供用於連接到企業 API 和 SaaS 應用程式的工具。

**Ford 和 Revionics 的案例分享：**

*   **Ford：** 使用 ADK 和 Agent Engine 建構客戶助理代理程式，以幫助客戶查找資訊並解決問題。
*   **Revionics：** 建構多代理程式定價系統，以自動化定價工作流程並提高營運效率。

## 3. 重要結論

Vertex AI Agent Builder 提供了一個全面的平台，用於建構和部署多代理程式應用程式。ADK 簡化了代理程式的開發，Agent Engine 提供了可擴展的運行時，Agent Garden 提供了學習資源。Ford 和 Revionics 的案例分享展示了 Agent Builder 在實際應用中的價值。
