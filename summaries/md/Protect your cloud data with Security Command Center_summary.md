# Protect your cloud data with Security Command Center
[會議影片連結](https://www.youtube.com/watch?v=itdSNQ9lTTI)
使用 Security Command Center 保護您的雲端資料

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的 Security Command Center 如何幫助企業保護雲端資料，以及德意志交易所（Deutsche Börse）如何利用該工具來應對資料安全挑戰。核心觀點包括：

*   資料安全的重要性：資料是企業的重要資產，但同時也帶來風險，需要在風險和收益之間取得平衡。
*   Data Security Compliance Posture Management (DSCPM)：Google Cloud 提出的解決方案，旨在將安全性帶到資料所在之處，無論是在 Google Cloud 還是其他地方。
*   DSCPM 的三個組成部分：資料探索、安全態勢評估、資料控制應用。
*   德意志交易所的應用案例：透過安全控制定義和安全狀態機，將法規要求映射到 Google Cloud 的安全策略上，實現資料安全驗證。

## 2. 詳細內容

*   **資料爆炸與資料安全挑戰：**
    *   企業收集大量資料，並利用 AI/ML 和分析來推動創新。
    *   資料既帶來收益，也帶來風險，需要平衡。
*   **Google Cloud 的 Data Security Compliance Posture Management (DSCPM)：**
    *   目標：為 Google Cloud 上的資料安全、隱私和合規性提供端到端治理。
    *   整合到 Security Command Center 中。
    *   三個組成部分：
        *   **資料探索：** 使用 Data Map 了解需要保護的資料。
        *   **安全態勢評估：** 評估資料的安全態勢。
        *   **資料控制應用：** 應用資料存取治理、流程治理、資料保護等控制措施。
        *   **監控與稽核：** 提供監控和稽核選項。
*   **德意志交易所的應用案例：**
    *   面臨大量的資料和嚴格的法規要求（如 Digital Operation New Zealand Act、EU AI Act）。
    *   **安全控制定義：** 將法規控制映射到策略，再映射到安全控制定義。
    *   **安全狀態機：**
        *   基於有限狀態機的概念，理解狀態和狀態之間的轉換。
        *   將安全控制定義應用於 Google Cloud 的預防性和偵測性控制。
        *   透過資產清單和日誌，持續監控 Google Cloud 的狀態。
        *   當狀態發生變化時（例如，有人存取檔案或建立儲存桶），檢查是否符合安全控制定義。
        *   如果不符合，則阻止或發送警報。
*   **結合 DSCPM 和安全狀態機：**
    *   實現資料安全驗證。
    *   了解資料的位置和保護方式。

## 3. 重要結論

Google Cloud 的 Security Command Center 和 Data Security Compliance Posture Management (DSCPM) 提供了一個全面的解決方案，幫助企業保護雲端資料。德意志交易所的案例展示了如何將這些工具與企業自身的安全策略相結合，以滿足特定的法規要求和安全需求。透過資料探索、安全態勢評估和資料控制應用，企業可以有效地管理資料風險，並確保資料安全。
