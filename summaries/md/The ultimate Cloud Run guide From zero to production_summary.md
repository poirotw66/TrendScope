# The ultimate Cloud Run guide From zero to production
[會議影片連結](https://www.youtube.com/watch?v=a459I_qUF3Q)
Cloud Run 終極指南：從零到生產

## 1. 核心觀點

本次演講主要介紹 Google Cloud 的無伺服器引擎 Cloud Run，涵蓋其核心功能、部署選項、定價模式以及如何在生產環境中使用。核心觀點包括：

*   Cloud Run 允許在無需管理基礎設施的情況下運行任何容器。
*   Cloud Run 提供多種部署選項，包括直接部署容器映像、從 GitHub 部署、使用 Buildpacks 從原始碼構建容器映像，以及使用 Cloud Run Functions。
*   Cloud Run 提供服務 (Services) 和任務 (Jobs) 兩種資源類型，分別適用於請求驅動的應用程式和需要運行至完成的容器。
*   Cloud Run 支援自動擴展、流量遷移、Secret Manager 集成以及 VPC 網路整合。
*   Cloud Run 提供基於請求和基於實例的兩種定價模式，並提供成本建議功能。

## 2. 詳細內容

*   **Cloud Run 簡介：** Cloud Run 是一個無伺服器引擎，允許使用者部署和運行容器，而無需管理底層的虛擬機器或叢集。
*   **Demo：** 講者展示了一個使用 Gemini API 產生基於 emoji 的短篇故事的應用程式，並示範了如何將 Nginx 容器映像部署到 Cloud Run。
*   **部署選項：** Cloud Run 提供四種部署選項：
    *   直接部署容器映像。
    *   從 GitHub 設置 CICD 並部署。
    *   使用 Buildpacks 從原始碼構建容器映像。
    *   使用 Cloud Run Functions。
*   **資源類型：** Cloud Run 提供兩種資源類型：
    *   **服務 (Services)：** 適用於請求驅動的應用程式，支援自動擴展、流量分割和 HTTPS。
    *   **任務 (Jobs)：** 適用於需要運行至完成的容器，可以手動或自動排程執行。
*   **原始碼部署：** 講者示範了如何使用 `gcloud run deploy` 命令從原始碼部署應用程式，以及 Cloud Run 如何使用 Buildpacks 將原始碼轉換為容器映像。
*   **版本控制和流量遷移：** Cloud Run 允許使用者管理多個版本，並使用流量遷移功能進行回滾或其他流量調整。
*   **Google Cloud 服務集成：** 講者介紹了如何使用 Google Cloud 客戶端函式庫進行身份驗證，以及如何使用直接 VPC 出口連接到 VPC 內部的服務。
*   **Secret Manager：** 講者示範了如何使用 Secret Manager 安全地儲存和管理 API 金鑰和其他敏感資料，並將其注入到 Cloud Run 服務中。
*   **生產環境考量：** 講者討論了生產環境中需要考慮的因素，包括公共網域、自動擴展和定價。
*   **預覽連結：** Cloud Run 允許使用者使用預覽連結在將流量切換到新版本之前預覽新版本。
*   **自動擴展：** Cloud Run 會根據流量自動調整實例數量，並支援縮放到零。使用者可以使用最小實例數來保持一定數量的實例處於 warm 狀態。
*   **私有後端服務：** 講者介紹了兩種配置私有後端服務的方法：使用 IAM 身份驗證或使用 VPC 網路。
*   **定價模式：** Cloud Run 提供基於請求和基於實例的兩種定價模式。基於請求的定價模式僅在實例處理請求時收費，而基於實例的定價模式則對所有實例收費，無論它們是否處理請求。Cloud Run 提供成本建議功能，以幫助使用者選擇最佳的定價模式。
*   **GPU 支援：** Cloud Run 支援 GPU 加速，允許使用者運行需要 GPU 的應用程式，例如 LLM 推理伺服器。

## 3. 重要結論

Cloud Run 是一個功能強大且靈活的無伺服器引擎，可以簡化容器化應用程式的部署和管理。它提供了多種部署選項、資源類型和定價模式，以滿足不同的需求。Cloud Run 還與 Google Cloud 的其他服務緊密集成，例如 Secret Manager 和 VPC 網路，從而簡化了應用程式的開發和部署。
