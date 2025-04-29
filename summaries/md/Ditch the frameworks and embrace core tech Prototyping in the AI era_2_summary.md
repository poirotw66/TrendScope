# Ditch the frameworks and embrace core tech Prototyping in the AI era_2
[會議影片連結]()
Ditch the frameworks and embrace core tech Prototyping in the AI era_2

## 1. 核心觀點

本次演講主要探討在生成式 AI 時代，如何透過捨棄框架，擁抱核心技術來進行原型設計。講者 Carl 分享了在 Google Cloud 上使用各種工具和最佳實踐，以加速原型開發的經驗。核心觀點包括：

*   **原型設計的重要性：** 強調原型設計是迭代和改進產品的關鍵，並引用「沒有什麼是一次發明和完善的」這句話來支持這一點。
*   **簡化原型設計流程：** 指出生成式 AI 的出現，大幅簡化了原型設計的流程，讓個人也能快速推進專案。
*   **框架的取捨：** 討論了在原型設計中，使用框架的優缺點，並建議在某些情況下，直接使用核心技術可能更有效。
*   **提示工程（Prompt Engineering）的重要性：** 強調在與 AI 模型互動時，提供具體明確的提示，以獲得更精確和客製化的結果。
*   **持續迭代和改進：** 強調在原型設計的各個階段，都需要不斷地收集使用者回饋，並根據回饋進行迭代和改進。

## 2. 詳細內容

*   **新創公司情境：** 講者以一個名為 "AI Praiser" 的虛構新創公司為例，該公司開發一款可以透過手機拍照來估算物品價值的應用程式。
*   **原型設計的三個階段：**
    *   **低擬真原型（Lo-Fi Prototyping）：** 著重於理解產品概念，並讓團隊成員達成共識。
    *   **早期建構（Early Build）：** 開發最小可行產品（MVP），並交付給使用者。
    *   **產品化（Production）：** 將產品擴展到更多客戶。
*   **捨棄框架的考量：**
    *   框架更新快速，AI 模型可能無法及時跟上。
    *   在某些情況下，使用核心技術可以更好地控制細節。
*   **提示工程策略：**
    *   零樣本提示（Zero-shot prompts）：直接提問。
    *   單樣本/少樣本提示（One-shot/Few-shot prompts）：提供範例。
    *   思維鏈（Chain of thought）：逐步引導模型。
    *   引導思考（Think through it）：要求模型自行思考。
*   **工具和技術：**
    *   Streamlit：用於快速建立原型的 Python 框架。
    *   Google AI Studio：用於與 Gemini 模型互動的工具。
    *   Gemini Canvas：用於即時建立和修改 Web 應用程式的工具。
    *   Figma：用於建立 UI 原型的工具。
    *   FastAPI：用於建立 Web API 的 Python 框架。
    *   get-ingest.com：用於從 GitHub 儲存庫提取程式碼的工具。
    *   Gemini Code Assist：用於在 IDE 中生成程式碼的工具。
    *   Application Design Center：Google Cloud 上的應用程式範本。
*   **MVP 階段的迭代：**
    *   根據使用者回饋，新增多幣別支援。
    *   利用 Gemini 的 Google 搜尋功能，提供更精確的估價。
*   **產品化階段的考量：**
    *   重構現有程式碼或從頭開始重建。
    *   使用元件框架或全功能框架。
    *   利用 Application Design Center 建立應用程式。
    *   生成 OpenAPI 規格。
    *   使用 Gemini Code Assist Enterprise 的程式碼客製化功能。
*   **程式碼清理：** 建議定期清理 AI 模型生成的程式碼，移除不必要的程式碼。

## 3. 重要結論

在生成式 AI 時代，原型設計變得更加快速和容易。透過善用各種工具和技術，並根據使用者回饋不斷迭代，可以快速開發出有價值的產品。講者強調，原型設計不只是一個任務，更是一個問題，而生成式 AI 可以幫助我們提出和回答這些問題。
