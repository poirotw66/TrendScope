# AI security and APIs Address OWASP’s top 10 LLM and API risks
[會議影片連結](https://www.youtube.com/watch?v=U8bGoGAG5AU)
AI 安全與 API 解決 OWASP 的 LLM 和 API 十大風險

## 1. 核心觀點

本次會議主要探討了 AI 和 API 安全，特別是針對 OWASP（開放網路應用安全專案）針對大型語言模型（LLM）和 API 的十大風險。會議議程包括 Renault 集團的 API 歷程分享、LLM 和 API 的 OWASP 十大風險分析，以及相關的示範。Google 的 Model Armor 和 Apigee 被提出作為應對這些風險的解決方案。

## 2. 詳細內容

*   **Renault 集團的 API 歷程：**
    *   Murad Abbas 分享了 Renault 集團如何應對數據孤島、系統複雜性和與生態系統互動的挑戰。
    *   他們採用了 Horshoe 架構，包含由 Apigee 和混合雲管理的同步 API 管理層，以及使用 Solace 的非同步層。
    *   強調了 API 安全的重要性，並展示了從消費者到供應商的 API 安全控制流程，包括 API 金鑰驗證、存取權杖驗證、流量限制和配額管理。
    *   介紹了 Mobilize Data Solutions，一個透過 API 提供數據產品的平台，並使用 Apigee 的貨幣化模型。
    *   討論了生成式 AI（GenAI）的應用，包括 Chat at Renault 平台和 API 代理，用於改善 API 生命周期管理和數據存取。

*   **AI 和 API 安全挑戰：**
    *   Shelly 提出了 AI 工作負載的安全性考量，包括防止惡意輸入、避免洩露敏感資訊、確保適當的稽核追蹤以及實施身份驗證和授權控制。
    *   介紹了 OWASP 針對 LLM 的十大風險，重點關注提示注入、敏感數據洩露、不當輸出處理和系統提示洩露。
    *   Google 的 Model Armor 被提出作為保護 LLM 提示和回應的解決方案，它具有模型和雲端不可知的特性。
    *   Apigee 作為 Google Cloud 的 API 管理平台，可用於保護 AI 工作負載，並提供強大的治理、安全和分析功能。

*   **Model Armor 示範：**
    *   Andrew 展示了如何使用 Apigee 保護 LLM 免受無限制使用的影響，包括語義快取、速率限制和配額管理。
    *   示範了 Model Armor 如何阻止危險提示、私人資訊請求和越獄嘗試。

*   **API 安全和 Apigee Advanced API Security：**
    *   Shelly 討論了 OWASP 針對 API 的十大風險，並將其分為身份驗證和授權風險、對資源或敏感數據的無限制存取、API 安全管理以及惡意活動。
    *   Apigee 的安全方法是「建構安全」和「執行安全」，利用安全策略（如速率限制、配額、API 金鑰驗證、身份驗證策略、架構驗證和威脅緩解）。
    *   Apigee Advanced API Security 是一個附加元件，旨在提高 API 的可見性、確保一致的標準、了解每次攻擊並做出反應。

*   **Apigee Advanced API Security 示範：**
    *   Andrew 展示了 Apigee Advanced API Security 的安全風險評估功能，該功能根據安全設定檔評估 API 部署，並提供改進安全態勢的建議。
    *   示範了濫用偵測功能，該功能使用啟發式規則和機器學習來偵測可疑活動，並提供近乎即時的儀表板來顯示攻擊情況。
    *   展示了如何使用 Gemini（Google 的 AI 模型）來總結安全發現，並建議採取措施，例如封鎖惡意 IP 位址。
    *   示範了如何建立動作來允許、拒絕或標記流量，並根據偵測到的威脅採取適當的措施。

## 3. 重要結論

本次會議強調了在 AI 和 API 領域中安全性的重要性，並展示了 Google 的 Model Armor 和 Apigee 作為解決 OWASP 十大風險的有效工具。Renault 集團的案例研究突顯了 API 管理和安全在大型組織中的實際應用。會議結論是，透過結合適當的安全措施和工具，組織可以保護其 AI 和 API 資產免受各種威脅。
