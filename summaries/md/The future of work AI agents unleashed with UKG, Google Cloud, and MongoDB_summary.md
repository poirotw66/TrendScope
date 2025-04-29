# The future of work AI agents unleashed with UKG, Google Cloud, and MongoDB
[會議影片連結](https://www.youtube.com/watch?v=ZpSN1F9ESvQ)
The future of work AI agents unleashed with UKG, Google Cloud, and MongoDB

## 1. 核心觀點

本次會議主要探討了 UKG 如何利用 AI 代理（AI Agents）來改善人力資源、薪資和勞動力管理解決方案，並結合 Google Cloud 和 MongoDB 的技術，打造 Bright AI 平台。核心觀點包括：

*   **AI 在人力資源管理中的應用：** AI 可以應用於員工職業生涯的各個階段，從求職、入職、排班到技能提升和晉升，提供更佳的體驗和成果。
*   **Bright AI 平台的價值：** Bright AI 旨在成為值得信賴的顧問，協助員工獲得更好的工作成果，並透過 Flex AI 代理提供各種服務，例如排班協助、員工福利查詢和提升公司晉升流程公平性建議。
*   **代理框架（Agent Framework）的重要性：** 代理框架能夠集中知識、確保安全且負責任的 AI 使用，並賦能領域團隊（例如薪資團隊）提供專業價值。
*   **檢索增強生成（Retrieval Augmented Generation, RAG）平台的必要性：** RAG 平台能夠有效搜尋企業內部文件，提供更精確、更符合情境的回應，解決大型語言模型（LLM）在靜態資料集上訓練的局限性。
*   **MongoDB Atlas Vector Search 的優勢：** MongoDB Atlas Vector Search 提供雲原生、全託管的向量資料庫，與 MongoDB 的文件模型整合，簡化了開發流程，並提供儀表板和分析功能以優化檢索效果。

## 2. 詳細內容

*   **UKG 的業務與數據：** UKG 是一家提供人力資源、薪資和勞動力管理解決方案的公司，擁有豐富的數據集，包括人員數據（績效、技能、薪資）、工作數據（時間、排班、休假）和文化數據（情感分析、調查、訊息）。這些數據使 UKG 能夠利用 AI 創造、分類、總結和搜尋洞察。
*   **Bright AI 的使用案例：** Bright AI 透過簡單的文字框接受使用者提問或指令，並提供以下使用案例：
    *   **前線協助（Frontline Assist）：** 執行排班變更等動作。
    *   **員工協助（Employee Assist）：** 回答福利查詢、薪資計算等問題，並提供相關連結以深入了解。
    *   **優良職場協助（Great Place to Work Assist）：** 針對如何提升公司晉升流程公平性等問題，提供基於 Great Place to Work 內容的建議和來源連結。
*   **Flex AI 代理架構：** Bright AI 由一套 Flex AI 代理驅動，採用分層架構，包含代理協調器和多個子代理，例如薪資代理，每個子代理又可以包含更細分的代理。
*   **代理框架的技術細節：**
    *   **功能呼叫（Function Calling）：** 代理框架的核心是功能呼叫，應用程式將可用動作列表和提示傳送給 LLM，LLM 識別要執行的動作或提出後續問題，然後應用程式執行動作並將結果傳回 LLM，LLM 可以產生答案或觸發另一個動作。
    *   **無程式碼代理建立（No-Code Agent Creation）：** 代理被視為簡單的配置，可以快速建立。
    *   **評估與測試（Eval and Testing）：** 提供服務來評估代理的效能，並提供指標以確保代理提供價值。
    *   **監控與可觀測性（Monitoring and Observability）：** 提供指標來監控代理的幻覺、完成的任務和整體效能。
    *   **多代理協調（Multi-Agent Orchestration）：** 允許連接多個代理，使代理能夠協同工作以協助使用者。
    *   **工具與 API 整合（Tool and API Integration）：** 提供工具來連接現有的 API 到代理，並允許註冊和重複使用 API。
    *   **技術堆疊：** 代理執行時使用 LangGraph 協調器、Gemini LLM 進行推理，並使用 MongoDB 進行配置和狀態儲存。
*   **RAG 平台的技術細節：**
    *   **RAG 的流程：** RAG 平台首先檢索相關文件，將使用者查詢轉換為向量，並與資料庫中的向量進行比較，然後使用檢索到的文件來增強提示，並將增強的提示傳送給 LLM 以產生更精確的回應。
    *   **文件載入流程：** 文件載入流程包括文字提取、文字分割（分塊）、嵌入建立和索引。
    *   **檢索流程：** 檢索流程包括獲取配置、建立 Langchain 鏈、嵌入查詢、從向量儲存檢索文件，並使用增強的提示產生答案。
    *   **MongoDB Atlas Vector Search：** MongoDB Atlas Vector Search 用於儲存和檢索高維度嵌入，並提供雲原生、全託管的解決方案，與 MongoDB 的文件模型整合。

## 3. 重要結論

UKG 透過結合 AI 代理、Google Cloud 和 MongoDB 的技術，成功打造 Bright AI 平台，為人力資源管理帶來創新。代理框架和 RAG 平台解決了 LLM 在企業應用中的局限性，而 MongoDB Atlas Vector Search 提供了高效且可擴展的向量資料庫解決方案。本次會議展示了 AI 在改善員工體驗和提升企業效率方面的巨大潛力。
