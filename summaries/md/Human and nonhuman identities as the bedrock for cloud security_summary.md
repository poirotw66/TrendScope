# Human and nonhuman identities as the bedrock for cloud security
[會議影片連結](https://www.youtube.com/watch?v=5mu43NXgVo8)
人類與非人類身分作為雲端安全的基石

## 1. 核心觀點

本次會議主要探討 Google Cloud 中人類與非人類身分的重要性，強調它們是雲端安全的核心基礎。會議涵蓋了身分優先安全模型的轉變、人類與非人類身分的具體安全措施，以及 Yahoo 在身分安全方面的實踐經驗。

## 2. 詳細內容

**身分優先安全 (Identity-First Security)**

*   業界正轉向以身分為中心的安全性模型，將身分視為安全性的基石。
*   客戶需要將核心功能嵌入人類與非人類身分堆疊中。

**人類身分 (Human Identities)**

*   **強制多重驗證 (MFA)：** 預計在 2024 年逐步強制高權限使用者啟用 MFA，以顯著降低攻擊面。
    *   經銷商：4 月 21 日開始強制執行。
    *   個別開發者：5 月 13 日開始強制執行。
    *   企業：第四季度開始強制執行。
*   **重新驗證 (Re-authentication)：** 對於敏感操作（如設定 IAM 政策、帳單和標籤修改）要求額外的身分驗證。
*   **工作階段管理 (Session Management)：** 限制工作階段長度，預設為 16 小時，以防止工作階段遭劫持。
*   **身分威脅偵測與回應 (Identity Threat Detection and Response)：** 偵測異常行為（例如，來自不尋常位置的登入），並要求重新驗證。
*   **身分識別提供者 (IDP) 支援：** 支援 Google Cloud 作為 IDP、第三方 IDP 聯合，以及混合模式。
*   **Workforce Identity Federation：** 95% 的服務和產品支援身分聯合，並將持續發展。

**非人類身分 (Non-Human Identities)**

*   **工作負載身分聯合 (Workload Identity Federation)：** 允許使用 AWS、Azure、GitHub、GitLab 等平台的原生憑證來驗證 Google Cloud，無需使用服務帳戶金鑰。
*   **X.509 憑證支援：** 擴展支援 X.509 憑證，允許使用現有的憑證授權機構 (CA) 進行驗證。
*   **工作負載對工作負載驗證 (Workload-to-Workload Authentication)：** 透過 SPIFI 身分，簡化 GKE、GCE 和 Cloud Run 工作負載之間的零信任驗證。
*   **受管理的工作負載身分 (Managed Workload Identity)：** 透過 PKI 驗證、信任網域驗證和授權策略，實現深度防禦。

**Yahoo 的實踐經驗**

*   **安全原則：** 集中式身分管理、限時驗證、稽核性、最小權限原則、強制 MFA。
*   **雅典 (Athens)：** Yahoo 開發並貢獻給 CNCF 的服務，提供工作負載身分和基於角色的授權系統。
*   **工作流程：** 使用 Workforce Identity Federation 和 Workload Identity Federation，自動化專案佈建、角色建立和身分管理。
*   **示範：** 展示了如何使用雅典進行 SSH 存取和 CI/CD 部署。

## 3. 重要結論

Google Cloud 正在積極發展以身分為中心的安全模型，提供廣泛的功能來保護人類和非人類身分。透過強制 MFA、重新驗證、工作階段管理和身分威脅偵測等措施，Google Cloud 旨在降低攻擊面並提高雲端安全性。Yahoo 的實踐經驗展示了如何利用這些功能來建立強大的身分安全框架。
