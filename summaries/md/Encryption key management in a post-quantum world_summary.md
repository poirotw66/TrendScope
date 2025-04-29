# Encryption key management in a post-quantum world
[會議影片連結](https://www.youtube.com/watch?v=sZRaX-Q-OVM)
後量子時代的加密金鑰管理

## 1. 核心觀點

本次會議主要探討了 Google Cloud 在金鑰和密鑰管理方面的進展，特別是在後量子密碼學（PQC）領域的應對策略。會議強調了易用性，旨在讓使用者更容易地利用 Google Cloud 提供的安全、隱私和合規性保護。核心觀點包括：

*   **簡化金鑰管理：** 透過 Cloud KMS AutoKey 等工具，簡化金鑰的建立、管理和輪換，降低使用門檻。
*   **應對量子威脅：** 積極開發和部署後量子密碼學演算法，以應對未來量子電腦帶來的安全挑戰。
*   **強化密鑰保護：** 提供多種金鑰管理選項，包括 Google 預設加密、客戶擁有的加密金鑰（Cloud KMS AutoKey）以及零權限解決方案（外部金鑰管理、單租戶 HSM）。
*   **提升Secret管理：** 透過 Secret Manager 和 Parameter Manager，集中管理和保護敏感資訊，降低配置錯誤的風險。
*   **合作夥伴關係：** 與 Talos 等安全廠商合作，提供更全面的安全解決方案。

## 2. 詳細內容

*   **金鑰管理產品組合：**
    *   **Baseline：** Google 預設加密，提供基礎的金鑰保護。
    *   **Enterprise Security and Privacy：** 客戶擁有和控制金鑰，例如 Cloud KMS AutoKey 和 Secret Manager。
    *   **Zero Privilege：** 提供更嚴格的控制，滿足合規性需求，例如外部金鑰管理和裸機 HSM。

*   **Cloud KMS AutoKey：**
    *   客戶擁有的加密金鑰，自動應用於適當的資源。
    *   由 Cloud HSM 提供 FIPS 140-2 L3 保護。
    *   金鑰自動輪換，並確保職責分離。
    *   提供免費層級，降低使用成本。
    *   整合到 Google Cloud Setup 中，簡化配置流程。

*   **後量子密碼學（PQC）：**
    *   Google 已投入 PQC 研究多年，並在傳輸層安全（ALTS）中啟用保護。
    *   Cloud KMS 提供量子安全數位簽章的預覽版，支援 NIST 標準化的演算法。
    *   PQC 遷移需要時間，建議使用者開始思考如何應對量子威脅。
    *   Google 將威脅分為四類：非對稱加密、數位簽章、對稱加密和高級密碼學。

*   **Secret Manager：**
    *   用於儲存、存取、管理和稽核密鑰的單一事實來源。
    *   提供細粒度的存取控制和生命週期管理。
    *   與 GKE 等其他 GCP 服務整合。
    *   GKE 的 Secret Manager 支援自動輪換，無需重新啟動 Pod。

*   **Parameter Manager：**
    *   用於集中管理工作負載配置參數。
    *   可以嵌入 Secret Manager 中的密鑰值，防止未經授權的存取。
    *   作為 Secret Manager 的一部分提供。

*   **零權限加密產品：**
    *   **Cloud KMS for Google Workspace CSE：** 與 Google Workspace 客戶端加密整合，提供資料機密性和細粒度的存取控制。
    *   **單租戶 HSM：** 提供更高的隔離性，適用於需要嚴格隱私和控制的使用者。客戶完全擁有和控制 HSM 叢集，Google 無法存取。需要基於仲裁的存取工作流程。

*   **Talos 合作夥伴關係：**
    *   Talos 提供應用程式、資料和身分的安全解決方案。
    *   與 Google 合作，協助客戶管理和控制其資料，滿足數位主權需求。
    *   Talos 的 HSM 產品和 CypherTrust 平台支援 PQC。

## 3. 重要結論

Google Cloud 正在積極推進金鑰和密鑰管理解決方案的發展，特別是在後量子密碼學領域。透過簡化金鑰管理、強化密鑰保護和提供多種部署選項，Google Cloud 旨在幫助使用者輕鬆應對不斷變化的安全威脅，並滿足合規性需求。Cloud KMS AutoKey、Secret Manager 和單租戶 HSM 等產品的推出，為使用者提供了更強大的安全工具。
