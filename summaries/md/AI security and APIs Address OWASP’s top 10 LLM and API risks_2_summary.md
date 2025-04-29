# AI security and APIs Address OWASP’s top 10 LLM and API risks_2
[會議影片連結]()
AI 安全與 API 解決 OWASP 的 LLM 和 API 十大風險_2

## 1. 核心觀點

本次會議主要討論了 AI 和 API 安全，以及如何應對 OWASP（開放網路應用安全專案）針對 LLM（大型語言模型）和 API 列出的十大風險。核心觀點包括：

*   AI 的發展離不開 API，API 的安全至關重要。
*   Gen AI 帶來了新的安全挑戰，例如惡意提示、敏感資料洩漏等。
*   OWASP 針對 LLM 和 API 分別制定了十大風險列表，企業應重視並採取相應措施。
*   Google Cloud 提供了多層防禦機制，包括 Google Cloud Armor、Apigee 和 Model Armor，以應對不同的安全風險。

## 2. 詳細內容

會議首先介紹了 Renault 的 AI 應用案例，展示了 AI 如何透過 API 為客戶提供新的功能和使用者體驗。同時也強調了 AI 代理與 API 管理之間的密切關係。

接著，會議深入探討了 Gen AI 帶來的安全挑戰，包括：

*   惡意提示（Hostile Prompts）
*   敏感資料洩漏（Sensitive Data Leakage）
*   互動稽核（Auditing of Interactions）
*   授權與驗證挑戰（Authorization and Authentication Challenges）
*   合規性（Compliance）
*   大規模生產環境中的 AI 工作負載執行（Running AI Workloads in Production and at Scale）

針對這些挑戰，OWASP 發布了 LLM 十大風險列表，其中重點關注了與惡意活動或文字輸入相關的風險，例如提示注入（Prompt Injection）和敏感資訊洩露（Sensitive Information Disclosure）。

Google Cloud 針對 LLM 的安全問題，推出了 Model Armor 解決方案。Model Armor 具有模型不可知（Model Agnostic）和雲端不可知（Cloud Agnostic）的特性，可以與任何模型和雲端平台搭配使用。

Google Cloud 在 AI 和 API 安全方面採用了深度防禦（Defense in Depth）策略，包括：

*   **Google Cloud Armor：** 作為 Google Cloud 的 Web 應用防火牆，主要用於緩解分散式阻斷服務攻擊（DDoS）和應用程式的 OWASP 十大風險。
*   **Apigee：** 作為 API 管理平台，主要用於解決 API 的 OWASP 十大風險。
*   **Model Armor：** 主要用於解決 LLM 的 OWASP 十大風險。

會議還詳細介紹了 API 的 OWASP 十大風險，包括身份驗證問題、授權問題、敏感資料存取、資源消耗問題、錯誤配置、庫存管理以及 API 濫用等。

Apigee 提供了強大的治理和安全功能，可以應對各種規模和用例。此外，Apigee 還提供了一個名為 Advanced API Security 的附加元件，專注於以下四個方面：

*   **API 可見性（Making Every API Visible）**
*   **確保 API 標準一致性（Ensuring Consistent Standards Across Your APIs），** 找出任何配置錯誤的 API。
*   **理解攻擊模式或可疑活動（Understand the Attack Patterns or Suspicious Activity）**
*   **採取行動以減輕攻擊（Take Action in Order to Mitigate Those Attacks）**

## 3. 重要結論

AI 和 API 安全是企業在數位轉型過程中必須重視的議題。OWASP 提供的風險列表可以幫助企業更好地了解潛在的安全威脅，並採取相應的防禦措施。Google Cloud 提供的多層防禦機制，可以為企業的 AI 和 API 應用提供全面的安全保障。
