# Supercharge your development workflow with Gemini Code Assist tools
[會議影片連結](https://www.youtube.com/watch?v=mt_SRR58VnU)
使用 Gemini Code Assist 工具加速您的開發工作流程

## 1. 核心觀點

本次會議主要介紹 Gemini Code Assist 工具，這是一款在 IDE 中為開發者提供的 AI 助手，旨在簡化開發任務，特別是在處理繁瑣或需要集思廣益的複雜問題時。CME 集團分享了他們如何利用 Gemini Code Assist 作為加速器，提升開發效率和創新能力。會議強調了 Gemini Code Assist 工具如何透過提供相關上下文資訊、簡化流程和提高程式碼品質來改善開發體驗。

## 2. 詳細內容

CME 集團的 Kiran Panja 和 Arun 分享了他們使用 Gemini Code Assist 的經驗。他們強調，數位轉型的一大挑戰是人員的適應，而 Gemini Code Assist 在這方面提供了有效的幫助。

*   **CME 集團的應用：** 他們將 Gemini Code Assist 應用於軟體交付生命週期的各個階段，從產品負責人到 SRE，涵蓋了程式碼協作、內容創建和文件編寫等用例。
*   **成果：** CME 集團發現，使用 Gemini Code Assist 後，開發團隊的 pull request 數量增加了 45%，每位開發者每月平均節省 10.5 小時。此外，它還提高了開發者的滿意度和幸福感，減少了重複性任務的痛苦。
*   **推廣方式：** 他們從 20 位早期試用者開始，有機地成長到超過 500 位使用者。
*   **未來展望：** 他們希望透過整合企業上下文資訊，提供更精確的回應，並將其與 SDLC 工具集整合，以實現更流暢的體驗。

Google Cloud 的 Srinath 介紹了 Gemini Code Assist 工具，強調其核心價值在於將開發者所需的上下文資訊帶入 IDE 中。

*   **工具的定義：** Gemini Code Assist 工具可以從各種來源（如 Jira 票證、Google 文件等）獲取上下文資訊，避免開發者在不同工具之間切換。
*   **提高生產力：** 透過提供相關數據和簡化流程，Gemini Code Assist 可以幫助開發者專注於更重要的任務，提高程式碼品質。
*   **使用方式：** 開發者可以使用 `@` 運算符在 Gemini Code Assist 的聊天面板中調用工具，並使用 `help` 命令獲取工具的相關資訊。
*   **適用對象：** Gemini Code Assist 工具適用於所有 Gemini Code Assist 使用者，無論是標準版、企業版還是個人版。

Christine 深入探討了 Gemini Code Assist 工具的技術架構，並展示了工具的實際應用。

*   **工具類型：** 工具分為兩種類型：一種是調用 API 的工具，另一種是調用 IDE 中其他工具的工具（如 Snyk 和 Apigee）。
*   **API 工具架構：** 使用者發出請求後，Gemini Code Assist 會將其分解為一個或多個 API 調用，然後調用 API 並將結果轉換為摘要，提供給使用者。
*   **演示：** Christine 演示了如何使用 Sentry 獲取錯誤資訊，並使用 Atlassian Rovo 和 Google Docs 獲取設計文件，然後使用 Gemini Code Assist 根據設計文件生成程式碼。

## 3. 重要結論

Gemini Code Assist 工具透過提供相關上下文資訊、簡化流程和提高程式碼品質，顯著提升了開發者的生產力。CME 集團的案例表明，Gemini Code Assist 可以作為數位轉型的加速器，幫助企業提高開發效率和創新能力。Google Cloud 正在積極與合作夥伴合作，不斷擴展 Gemini Code Assist 工具的功能，並將其與代理整合，以實現更強大的問題解決能力。
