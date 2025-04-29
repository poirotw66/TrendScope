```
# Secure, compliant gen AI deployment with Gemini and Google Workspace.f140
[會議影片連結]()
Secure, compliant gen AI deployment with Gemini and Google Workspace.f140

## 1. 核心觀點

本次會議主要探討了組織如何安全地利用 Gemini 和 Google Workspace，同時確保符合法規和保障資料安全。核心觀點包括：

*   **安全優先的 AI 部署：** 強調在利用生成式 AI 的同時，不應犧牲安全性，並提供可配置的治理措施。
*   **隱私保護設計：** 保證使用者內容不會未經許可被分享到組織外部，也不會用於其他客戶或模型訓練。
*   **合規性：** Google Workspace 投入大量資源，提供全面的合規性認證，包括成為首批獲得 FedRAMP High 授權的生成式 AI 助理之一。
*   **資料治理：** Gemini 不會改變 Google Workspace 中資料的存取權限，而是提供工具讓客戶配置適合自身需求的資料安全態勢。
*   **AI 的企業應用：** 透過客戶案例分享，展示 Gemini 如何在實際應用中提升生產力，同時解決 Shadow AI 的風險。

## 2. 詳細內容

*   **引言：**
    *   Tim McQuinney 和 Jim Casey 作為 Google Workspace 團隊的產品經理，介紹了本次會議的主題。
    *   強調組織希望利用生成式 AI，但同時擔心隱私、安全和智慧財產權保護的問題。
    *   提到 Google Workspace 從一開始就以雲原生、零信任原則和內建的資料保護功能為基礎進行架構設計，適用於 AI 時代。
*   **Gemini 的安全與合規性：**
    *   Jim Casey 強調，目標是讓組織能夠安全地使用生成式 AI，同時保留生產力優勢。
    *   Gemini 的設計注重隱私，不會未經許可分享使用者內容，也不會用於模型訓練。
    *   Google Workspace 擁有廣泛的合規性認證，包括 FedRAMP High 授權。
*   **安全第一的原則：**
    *   Tim McQuinney 說明 Google 如何管理產品的完整生命週期，確保模型的安全開發和運營。
    *   強調 Gemini 是 Google 內部開發的模型，遵循所有 Google 產品的安全開發原則。
    *   Gemini Workspace 具有先進的威脅監控功能，可以防禦新型威脅，例如 Prompt Injection 攻擊。
*   **資料治理：**
    *   Gemini 不會改變使用者在 Google Workspace 中的資料存取權限。
    *   組織需要建立適當的資料存取和共享邊界，以符合其風險、生產力和協作需求。
    *   Google Workspace 提供工具，讓客戶可以配置適合自身需求的資料安全態勢。
*   **客戶案例分享：**
    *   邀請 Flashpoint 的 Tyler Prudel 和 Strata Prime 的 Andrew Livingstone 分享他們使用 Gemini 的經驗。
    *   Tyler Prudel 提到，Flashpoint 選擇 Gemini 的原因是它內建於 Google Workspace，並且不會使用他們的資料來訓練模型。
    *   Andrew Livingstone 強調，Gemini 只會以使用者的身份運作，簡化了管理員的工作，並降低了 Shadow AI 的風險。
    *   兩位客戶都強調了資料治理的重要性，以及 Google Workspace 提供的控制項和工具，可以幫助他們管理資料安全。
*   **實用建議：**
    *   停止建立網域範圍共享檔案，並使用群組為基礎的選項來共享檔案。
    *   使用 Drive 匯出功能和 Looker Studio 建立資料治理儀表板。
    *   使用 DLP 規則和 AI 分類來識別和保護敏感資料。
    *   為使用者提供培訓和支援，以確保他們能夠安全有效地使用 Gemini。
*   **三步流程：**
    1.  **識別和報告：** 識別和編目敏感資料。
    2.  **定義和執行：** 定義控制使用者如何共享和使用資料的政策。
    3.  **監控和追蹤：** 監控和追蹤組織中的敏感資料。
*   **新功能介紹：**
    *   Drive 清查報告：提供 Drive 項目元資料的快照。
    *   Gmail 分類標籤：將 Drive 的標籤功能擴展到 Gmail。
    *   AI 分類：支援多個 AI 分類模型，並提供隨需訓練功能。
    *   Gmail DLP：提供即時回饋，教育使用者避免違反政策。
    *   Drive IRM：限制對敏感檔案的下載、複製、列印、電子郵件和 Gemini 存取。
    *   Policy API：允許程式化管理 DLP 規則。
*   **稽核增強功能：**
    *   將套用的標籤傳遞到安全調查工具和 SecOps。
    *   擴展 Gemini 的稽核能力，包括記錄使用者互動和資料存取。

## 3. 重要結論

本次會議強調了在部署生成式 AI 時，安全性和合規性的重要性。Google Workspace 透過 Gemini 提供了一套全面的工具和控制項，幫助組織在利用 AI 的同時，保護其敏感資料並符合法規要求。透過客戶案例分享和實用建議，本次會議為組織提供了寶貴的指導，幫助他們安全有效地部署 Gemini 和 Google Workspace。
```