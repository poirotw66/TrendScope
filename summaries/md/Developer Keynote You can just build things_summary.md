# Developer Keynote You can just build things
[會議影片連結](https://www.youtube.com/watch?v=xLDSuXD8Mls)
Developer Keynote 你只管盡情打造

## 1. 核心觀點

本次 Google Cloud 的開發者主題演講，重點展示了如何利用 Google Cloud 和 Gemini 模型，賦能開發者構建新一代的應用程式，特別是 AI 代理（Agent）。演講涵蓋了代理的開發、部署和互動，以及如何利用 AI 輔助程式碼編寫和雲端操作。核心觀點包括：

*   **AI 代理的強大能力：** AI 代理可以規劃、推理、學習、協作和行動，代表使用者或與其他代理協同完成目標。
*   **Google Cloud 的工具和框架：** 推出 Agent Development Kit (ADK)、Agent Engine 和 Agent Space，簡化代理的開發和部署流程。
*   **Gemini 模型的關鍵作用：** Gemini 模型提供長上下文視窗和多模態支援，實現影片、圖片和語音的無縫整合，為應用程式帶來更豐富的體驗。
*   **AI 輔助開發的效率提升：** Code Assist 和 Cloud Assist 代理可以加速開發流程，簡化雲端操作，提高軟體工程師的生產力。
*   **開放性和選擇性：** 開發者可以選擇自己喜歡的 IDE 和模型，利用 Google Cloud 的工具和平台，構建符合自身需求的應用程式。

## 2. 詳細內容

*   **Gemini 模型與 AI Studio：**
    *   Gemini 模型提供長上下文視窗和雙向多模態能力，開發者可以在 AI Studio 中試用最新的模型，包括 Gemini 2.5 Pro。
    *   AI Studio 提供 UI 更新，包含最新的 Gemini 實驗模型和 Google 搜尋工具，以及原生圖像編輯和生成等新功能。
    *   透過 Gemini 模型，可以快速原型化 AI 應用程式，例如廚房改造計畫，包括生成詳細的提示詞、制定翻新計畫，以及視覺化改造後的樣貌。
    *   Gemini 模型可以利用 Google 搜尋進行資料檢索，獲取最新的材料成本和當地法規等資訊，使翻新計畫更具實用性。
    *   Gemini 模型可以根據使用者提供的圖片和提示詞，生成改造後的廚房圖像，並根據使用者的要求進行修改。

*   **AI 代理的開發與部署：**
    *   AI 代理是一種服務，可以與 AI 模型互動，使用工具和上下文資訊，執行目標導向的操作。
    *   Agent Development Kit (ADK) 是一個開源、模型不可知的工具包，可以簡化代理的開發流程。
    *   ADK 需要三個要素：指令（定義代理的目標）、工具（使代理能夠執行超出 LLM 範圍的動作）和模型（處理 LLM 任務並呼叫工具）。
    *   ADK 支援模型上下文協定 (MCP)，為 LLM 處理資料請求建立標準化的結構和格式。
    *   開發者可以使用 ADK 建立代理，例如驗證建築法規和查詢許可證的代理，並生成 PDF 提案。
    *   Vertex AI Agent Engine 可以簡化代理的部署流程，提供企業級的安全控制、生產級的監控和日誌記錄，以及評估和品質框架。
    *   Agent Space 是一個代理中心，可以讓開發者註冊使用 ADK 構建的代理，並將其提供給公司內部的員工或雲端市場上的其他公司使用。

*   **多代理系統與雲端偵錯：**
    *   複雜的流程需要多個代理協同工作，可以建立一個由多個專業代理組成的系統，例如建築提案代理、許可證和合規代理，以及材料訂購和交付代理。
    *   可以使用 ADK 構建和協調多代理系統，並將其部署到 Vertex AI Agent Engine。
    *   Agent Space 可以讓使用者與多代理系統互動，例如啟動許可證流程或查詢材料訂購狀態。
    *   Cloud Assist 提供雲端調查功能，可以幫助診斷基礎架構問題和程式碼問題，節省偵錯時間。

*   **開發者工具與模型選擇：**
    *   開發者可以使用 Gemini 模型在自己喜歡的 IDE 中進行程式碼編寫，例如 Windsor、Cursor 和 IntelliJ。
    *   Vertex AI Model Garden 提供各種模型，包括 Llama、Gemma、Anthropic 和 Mistral，開發者可以選擇最適合自己任務的模型。
    *   開發者可以將 Model Garden 中的模型部署到自己的端點或叢集，並將其整合到自己的應用程式中。
    *   Gemini Code Assist 現在支援 Android Studio，並提供 Android 專用的 AI 功能。
    *   Gemini 和 Firebase 提供完整的 AI 輔助功能，可以在全新的 Firebase Studio 中使用。

*   **AI 在各領域的應用：**
    *   MLB 使用 Google Cloud 處理每場比賽 2500 萬個資料點，計算以前難以想像的統計數據。
    *   Google Cloud MLB Hackathon 的獲獎者使用 Gemini API 和 Google Cloud 建立了一個可自訂的提示詞產生器，用於分析投球手的表現。
    *   Gemini 可以分析影片，評估投球手的動作，並提供改進建議。
    *   AI 也可以用於其他領域，例如品質控制、流程最佳化和故障排除。
    *   Google Cloud 與 Winter X Games 合作，建立了一個 AI 評論員和評分分析器，為男子超級管道比賽提供全新的觀賽體驗。

*   **資料科學代理與未來展望：**
    *   資料科學代理可以幫助使用者將原始資料轉換為資料應用程式，例如銷售預測應用程式。
    *   資料科學代理可以與使用者協同工作，使用 Spark 進行特徵工程，並使用 TimesFM 模型進行預測。
    *   使用者可以使用 BigQuery Notebooks 建立資料應用程式，並將其分享給其他人。
    *   Google Cloud 還將推出針對資料工程師、資料分析師和業務使用者的專業代理。
    *   Gemini Code Assist 將提供 Kanban 看板，讓使用者可以協調代理，協助完成軟體開發生命週期的各個方面。
    *   軟體工程代理將處理繁瑣的開發工作，讓開發者可以專注於有趣的工程問題。
    *   VO2 模型可以生成高品質的影片，並用於娛樂領域，例如修復和增強經典電影。

## 3. 重要結論

本次 Google Cloud 開發者主題演講展示了 AI 如何改變軟體開發的未來。透過 Gemini 模型、AI 代理和各種工具和框架，開發者可以更有效率地構建新一代的應用程式，並將 AI 應用於各個領域。Google Cloud 致力於提供開放和靈活的平台，讓開發者可以選擇自己喜歡的工具和模型，並將 AI 整合到自己的工作流程中。
