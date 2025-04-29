# LangGraph and MCP Toolbox Building generative AI agents on your databases
[會議影片連結](https://www.youtube.com/watch?v=GGn580J5UOQ)
LangGraph 和 MCP 工具箱：在您的資料庫上構建生成式 AI 代理

## 1. 核心觀點

本次演講介紹了如何使用 LangGraph 和 MCP Toolbox for Databases 來構建基於生成式 AI 的代理，以自動化複雜的實際工作流程。核心觀點包括：

*   **代理的定義與應用：** 代理是使用生成式 AI 模型進行決策的軟體應用，它們透過選擇工具（如 API 調用、資料庫查詢等）來收集資料並採取行動。
*   **LangGraph 的優勢：** LangGraph 在靈活性和可靠性之間取得了平衡，允許開發者定義 LLM 可以在不同狀態之間轉換的圖，從而在每個狀態選擇不同的工具。
*   **MCP Toolbox for Databases 的作用：** MCP Toolbox 是一個開源伺服器，簡化了代理與資料庫的連接，改善了可觀察性，並易於整合身份驗證服務，以解決資料存取問題。
*   **安全考量：** 強調了在構建 AI 代理時需要考慮的安全問題，例如防止惡意使用者欺騙代理以存取未授權的資料。
*   **模型上下文協定 (MCP)：** Toolbox 支援 MCP，這意味著它可以被任何與 MCP 相容的代理使用。

## 2. 詳細內容

*   **代理的靈活性與可靠性：** 演講比較了不同類型的代理系統，從確定性的鏈（chain）到完全自主的 React 迴圈。LangGraph 提供了中間地帶，允許開發者定義狀態圖，從而在靈活性和控制之間取得平衡。
*   **LangGraph 的功能：** 除了定義代理的圖之外，LangGraph 還支援人機迴路互動、持久性和串流。LangSmith 是一個用於部署 LangGraph 代理的託管服務，具有增強的可觀察性和測試功能。
*   **安全漏洞示例：** 演講提供了一個例子，說明惡意使用者如何欺騙客戶服務代理以洩露其他使用者的訂單資訊。
*   **MCP Toolbox 的安全機制：** 為了應對安全問題，MCP Toolbox 使用代理元件來將關鍵資訊（如使用者身份）移出 AI 的控制範圍，並強制執行確定性的存取控制。例如，代理只能設定日期範圍，而不能設定使用者 ID。
*   **MCP Toolbox 的易用性：** 演講展示了如何使用 MCP Toolbox 定義一個查詢資料庫以查找航班的工具，只需簡單的描述、SQL 查詢和參數。
*   **與 LangChain/LangGraph 的整合：** 演講展示了如何輕鬆地將 MCP Toolbox 整合到 LangChain 或 LangGraph 應用程式中。

## 3. 重要結論

生成式 AI 代理有潛力透過自動化關鍵工作流程來改變業務。這些代理需要存取資料，而許多資料都儲存在資料庫中。透過結合 LangGraph、MCP Toolbox for Databases 和 Google Cloud 的 AI-ready 資料庫產品組合，可以安全且高效地將代理連接到資料庫。MCP Toolbox 簡化了開發，改善了可觀察性，並易於整合身份驗證服務，從而解決了資料存取問題。
