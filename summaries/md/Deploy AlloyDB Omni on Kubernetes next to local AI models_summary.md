# Deploy AlloyDB Omni on Kubernetes next to local AI models
[會議影片連結](https://www.youtube.com/watch?v=BxuozkkiNhQ)
在 Kubernetes 上部署 AlloyDB Omni 於本地 AI 模型旁

## 1. 核心觀點

本次會議主要介紹了 AlloyDB Omni 在 Kubernetes 上的部署，以及如何與本地 AI 模型整合。講者 Gleb 強調 AlloyDB Omni 作為一個與 PostgreSQL 完全相容的資料庫，具有卓越的效能價格比、完整的向量資料庫功能和即時分析能力。此外，AlloyDB Omni 可以在任何環境中運行，包括本地、資料中心和雲端。會議重點在於展示如何利用 AlloyDB Omni 搭配本地部署的 AI 模型，以實現更安全、更快速且更具成本效益的 AI 應用。

## 2. 詳細內容

會議首先介紹了 AlloyDB 的特性，包括其與 PostgreSQL 的相容性、卓越的效能價格比、向量資料庫功能和即時分析能力。AlloyDB Omni 允許使用者在本地環境中運行 AlloyDB，無需雲端帳戶。

接著，講者深入探討了在 Kubernetes 上部署 AlloyDB Omni 和本地 AI 模型（包括 BGE 嵌入模型和 GEMA 3 模型）的具體步驟。他展示了如何使用 Helm Chart 或 Kubernetes Operator 部署 AlloyDB Omni，以及如何配置節點池以支援 GPU 加速的 AI 模型。

講者詳細說明了如何將 AlloyDB Omni 與本地 AI 模型整合，包括：

*   **註冊模型：** 使用 `google_ml.create_model` 函數在 AlloyDB 中註冊本地 AI 模型的端點。
*   **建立嵌入：** 使用 `google_ml.embedding` 函數利用本地嵌入模型生成向量嵌入，並將其儲存在 AlloyDB 中。
*   **使用 AI 模型進行預測：** 使用 `google_ml.predict` 函數將資料傳送到本地 Gen AI 模型，並獲取預測結果。

講者還展示了一個實際的應用案例，其中 AlloyDB Omni 用於儲存產品目錄，而本地 BGE 模型用於生成產品描述的嵌入。然後，使用者可以使用語義搜尋來尋找與其查詢最相關的產品。此外，GEMA 3 模型用於根據產品資訊和使用者查詢生成更詳細的產品建議。

講者也提到了一些重要的考量因素，例如：

*   **硬體資源：** 確保 Kubernetes 叢集具有足夠的 CPU、記憶體和 GPU 資源來運行 AlloyDB Omni 和 AI 模型。
*   **網路配置：** 配置網路以允許 AlloyDB Omni 和 AI 模型之間的通訊。
*   **模型大小：** 根據可用的 GPU 記憶體限制 Gen AI 模型的大小。

最後，講者分享了 Codelab 和部落格文章的連結，供聽眾進一步了解 AlloyDB Omni 和本地 AI 模型的整合。

## 3. 重要結論

AlloyDB Omni 提供了一個強大的平台，可以在 Kubernetes 上部署，並與本地 AI 模型整合，從而實現安全、快速且具成本效益的 AI 應用。透過利用 AlloyDB Omni 的資料庫功能和本地 AI 模型的推論能力，開發人員可以構建各種創新的 AI 應用，例如語義搜尋、產品推薦和聊天機器人。本次會議展示了 AlloyDB Omni 在 AI 領域的潛力，並為開發人員提供了實用的指南，以開始使用 AlloyDB Omni 和本地 AI 模型。
