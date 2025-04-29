# What’s new with IAM and Org Policy Access risk, at-scale governance and AI
[會議影片連結](https://www.youtube.com/watch?v=Lourkw64AVM)
IAM 與 Org Policy 的最新資訊：存取風險、大規模治理與 AI

## 1. 核心觀點

本次會議主要討論了 Google Cloud Platform (GCP) 中 IAM (Identity and Access Management) 和 Org Policy 的最新發展，涵蓋了存取風險管理、資源的大規模治理，以及人工智慧 (AI) 在這些領域的應用。重點包括：

*   **安全平台：** GCP 的安全平台由資源管理、雲端治理、身分平台和存取管理組成，並透過 AI 加強。
*   **資源管理：** 資源管理正在轉向以應用程式為中心，允許使用者直接在資料夾層級管理應用程式，跨越多個專案。
*   **雲端治理：** 透過組織政策 (Org Policy) 和自訂限制 (Custom Constraints) 確保資源的安全配置，並推出 Google Cloud Security Baseline 以提供預設的安全設定。
*   **身分平台：** 強調非人類身分 (Non-Human Identities, NHI) 的重要性，並提供 Workforce Identity Federation 以簡化人類身分驗證。
*   **存取管理：** 除了傳統的允許 (Allow) 之外，還強調特權存取管理 (Privileged Access Management, PAM)、即時存取 (Just-In-Time Access, JIT)、權限管理 (Entitlement Management) 和主體存取邊界 (Principal Access Boundary, PAB) 等防禦縱深策略。
*   **存取風險：** 透過多重驗證 (Multi-Factor Authentication, MFA)、重新驗證 (Re-authentication) 和內建於 IAM 的身分威脅偵測與回應 (Identity Threat Detection and Response, ITDR) 來降低存取風險。
*   **AI 應用：** 利用 Gemini AI 協助撰寫自訂限制、選擇角色和改善整體安全態勢。

## 2. 詳細內容

*   **安全平台：**
    *   GCP 安全平台的核心是資源管理，它允許使用者組織雲端資源，並透過組織層級、部門、團隊、生產和開發環境等方式進行管理。
    *   在資源管理之上，GCP 提供了強大的治理產品，例如 Org Policy 和 Custom Constraints，以確保資源在建立或變更時具有正確的配置和安全態勢。
    *   身分平台負責管理人類和非人類身分，並提供存取管理功能，以控制哪些身分可以存取哪些資源。
    *   存取管理不斷發展，除了允許之外，還包括 PAM、JIT、權限管理和 PAB 等功能，以提供更精細的存取控制。
    *   存取風險管理透過 VPC 服務控制、身分感知代理 (Identity-Aware Proxy, IAP) 和情境感知存取 (Context-Aware Access, CAA) 等產品來追蹤使用者活動並偵測異常行為。
    *   Gemini AI 被用於增強整個安全平台，提供 AI 驅動的價值。

*   **資源管理：**
    *   GCP 透過 Cloud Resource Manager 組織資源，允許使用者根據組織結構以階層方式分配資源。
    *   資源標籤 (Resource Tags) 允許使用者以額外的方式推理資源，並可以控制誰可以使用哪些標籤鍵和標籤值。
    *   Cloud Asset Inventory 允許使用者搜尋、監控和分析資產。
    *   GCP 正在轉向以應用程式為中心，允許使用者直接在資料夾層級管理應用程式。
    *   透過啟用資料夾的應用程式啟用 (App Enablement) 功能，使用者可以管理跨越多個專案的應用程式。

*   **雲端治理：**
    *   Org Policy 提供了超過 110 個內建的組織政策，現在正在演進為 Managed Constraint，提供更多功能來安全地測試和部署組織政策。
    *   Custom Constraints 允許使用者建立和管理自己的政策，目前支援 57 個 Google Cloud 產品，並計劃在今年擴展到 100 多個。
    *   Google Cloud Security Baseline 是一組預設的安全設定，可確保最嚴重的問題不會出現在雲端環境中。

*   **身分平台：**
    *   非人類身分 (NHI) 的重要性日益增加，需要關注與自動化、雲端環境和微服務相關的風險。
    *   使用者可以使用 Google Cloud Workspace Cloud Identity 或 Identity Federation 來管理人類身分。
    *   Identity Federation 允許使用者使用現有的 IDP (EntraID、Okta) 而無需同步身分。
    *   GCP 支援超過 95% 的 Google Cloud 產品的 Identity Federation。
    *   GCP 正在努力成為非人類身分的 IDP，並投資於 keyless access 和 managed workload identity。

*   **存取管理：**
    *   傳統的 IAM 不足以解決雲端安全問題，需要針對雲端環境進行投資。
    *   GCP 透過 PAM、Deny 和 Principal Access Boundary 等功能來建立防禦縱深。
    *   PAM 允許使用者在需要時才請求權限，而不是一直擁有權限。
    *   Deny 允許使用者拒絕特定權限，即使該權限已透過角色授予。
    *   Principal Access Boundary 允許使用者限制身分的範圍，例如限制開發人員存取生產環境。
    *   Gemini 驅動的角色選擇器 (Role Picker) 透過自然語言識別執行工作所需的角色，並僅授予這些角色。

*   **存取風險：**
    *   MFA 是不可協商的，強烈建議所有使用者都啟用 MFA。
    *   自動重新驗證 (Automatic Re-authentication) 在使用者執行敏感操作時強制重新驗證。
    *   ITDR 與 CAA 結合，可以偵測身分威脅並在威脅發生時採取行動。

## 3. 重要結論

本次會議強調了 GCP 在 IAM 和 Org Policy 方面的最新發展，包括存取風險管理、資源的大規模治理和 AI 應用。透過這些新功能和策略，使用者可以更好地保護其雲端環境，並確保其資源的安全配置。會議還強調了防禦縱深策略的重要性，以及 AI 在簡化安全管理和改善安全態勢方面的潛力。
