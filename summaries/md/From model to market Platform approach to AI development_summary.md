# From model to market Platform approach to AI development
[會議影片連結](https://www.youtube.com/watch?v=c43ZBUqeqfA)
從模型到市場：AI 開發的平台方法

## 1. 核心觀點

本次會議主要探討如何利用 Vertex AI 平台，加速 AI 模型的原型設計、迭代和部署，最終推向市場。Dialpad 公司分享了他們如何利用 Vertex AI 的 Prompt Optimizer 工具，將模型遷移到 Gemini 1.5 Flash，並在成本、延遲和可擴展性方面獲得顯著優勢的實際案例。

## 2. 詳細內容

*   **Vertex AI Studio 快速原型設計：**
    *   Vertex AI Studio 簡化了 AI 原型設計流程，使用者可以輕鬆地將想法轉化為可執行的應用程式。
    *   透過簡單的介面，使用者可以定義應用程式的需求，例如建立部落格文章的圖片產生器，並指定輸入（部落格文章文字、背景顏色）。
    *   Vertex AI Studio 會將這些需求轉換為提示詞 (Prompt)，並搭配合適的模型，使用者可以模擬輸入和輸出，快速測試想法。
    *   新的設計提升了多媒體互動和處理大型上下文視窗的能力，並提供模型選擇器，方便比較不同模型的價格、延遲和核心優勢。
    *   Google Gemini 2.5 Pro with Flash 即將推出，將提供更大的上下文視窗和原生工具，進一步加速原型設計。
    *   使用者可以利用 Google 搜尋資料增強回應，或連接自己的資料儲存庫進行處理。
    *   透過 Cloud Run 整合，使用者可以輕鬆部署應用程式原型，無需管理複雜的設定。

*   **Vertex SDK 迭代與生產：**
    *   Vertex SDK 加速了 AI 模型的迭代和生產過程。
    *   使用者可以使用 SDK 組裝提示詞組件、管理版本、標籤和註釋，並以程式方式管理和產生資產。
    *   透過測試、評估和調整的迭代迴圈，使用者可以不斷提升模型的品質。
    *   Vertex AI Studio 提供使用者介面，方便配置提示詞，包括系統指令、提示詞本身和模型參數。
    *   使用者可以比較不同的提示詞和模型，並儲存版本，以便在需要時回溯。
    *   SDK 提供程式碼片段，方便使用者將模型整合到應用程式中進行測試。

*   **Vertex AI 評估服務：**
    *   Vertex AI 提供評估服務，幫助使用者評估模型的效能。
    *   除了統計評估工具外，Vertex AI 還提供自動評分器 (Auto Raters)，利用大型語言模型 (LLM) 作為評審，評估模型的輸出。
    *   新的評估功能支援代理 (Agent) 和自動產生評分標準 (Rubric)，提高評估的一致性和透明度。

*   **Vertex Prompt Optimizer：**
    *   Vertex Prompt Optimizer 將提示詞工程從藝術轉變為科學。
    *   使用者可以將評估資料集傳遞給 Prompt Optimizer，它會迭代地重寫提示詞，並評估效能。

*   **模型優化器端點：**
    *   模型優化器端點會根據使用者設定的預算和目標（成本、品質或平衡），在 Gemini Flash 和 Pro 之間動態路由查詢。

*   **Dialpad 案例分享：**
    *   Dialpad 是一家 AI 優先的公司，利用 AI 轉變團隊協作和溝通的方式。
    *   Dialpad AI 可以自動總結通話內容，提取關鍵行動項目，並提供銷售和支援團隊的輔導見解。
    *   Dialpad 的 AI Playbooks 功能利用大型語言模型分析通話記錄，檢測特定主題是否被討論，並總結關鍵對話要點。
    *   Dialpad 使用 Vertex AI 的 Prompt Optimizer 工具，將模型從 TechSpison 遷移到 Gemini 1.5 Flash，並在精確度方面獲得顯著提升（從 68% 提升到 74%）。
    *   使用 Prompt Optimizer 工具，Dialpad 將提示詞調整時間從兩週縮短到三天，節省了 70-80% 的時間。

## 3. 重要結論

Vertex AI 平台提供了一套完整的工具和服務，幫助使用者加速 AI 模型的開發和部署。Dialpad 的案例表明，利用 Vertex AI 的 Prompt Optimizer 工具，可以有效地將模型遷移到新的架構，並在成本、延遲和可擴展性方面獲得顯著優勢。本次會議強調了建立穩固的評估流程和利用自動化工具的重要性，以確保 AI 模型的品質和效能。
