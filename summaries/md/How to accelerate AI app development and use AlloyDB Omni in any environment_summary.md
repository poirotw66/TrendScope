# How to accelerate AI app development and use AlloyDB Omni in any environment
[會議影片連結](https://www.youtube.com/watch?v=fH-GG9MqpHI)
如何加速 AI 應用程式開發並在任何環境中使用 AlloyDB Omni

## 1. 核心觀點

本次會議主要探討如何利用 AlloyDB Omni 加速 AI 應用程式的開發，並將其應用於各種環境，包括雲端、地端和邊緣運算。核心觀點包括：

*   AlloyDB Omni 是一個可下載的資料庫軟體，可以在任何地方運行，包括本地端、多雲環境和邊緣設備。
*   AlloyDB Omni 基於 PostgreSQL，並加入了 Google 在 AI、效能和可擴展性方面的創新。
*   AlloyDB Omni 支援向量搜尋，可以輕鬆構建語意搜尋應用程式。
*   Ivan 提供 AlloyDB Omni 的託管服務，簡化了部署和管理。
*   Google Cloud Ready 計畫認證了與 AlloyDB 良好協作的合作夥伴解決方案。

## 2. 詳細內容

*   **AlloyDB Omni 的優勢：**
    *   **隨處運行：** 可以在任何地方下載和安裝，包括本地端、資料中心、伺服器、虛擬機器、Google 分散式雲端、混合雲、多雲環境等。
    *   **效能：** 比開源 PostgreSQL 更快，允許擴展更多，並從相同數量的資源中獲得更多交易。
    *   **分析加速器：** 具有柱狀引擎，可將分析樣式查詢速度提高 100 倍。
    *   **易於操作：** 具有自動駕駛和自動化功能。
    *   **統一資料庫：** 實際上是三個不同的資料庫合而為一，支援關聯式儲存、即時分析和向量搜尋。
*   **使用 AlloyDB Omni 構建向量搜尋應用程式：**
    *   使用嵌入模型建立內部資料的向量嵌入。
    *   將使用者問題轉換為向量嵌入。
    *   使用 AlloyDB 尋找與問題最接近的文件。
    *   將這些文件傳回大型語言模型 (LLM)，以產生回應。
*   **AlloyDB Omni 的向量搜尋功能：**
    *   `embedding()` 函數：簡化了向量嵌入的建立。
    *   PGVector 擴充功能：用於儲存向量資料類型並建立索引。
    *   SCAN 索引：一種基於 Google 搜尋和 YouTube 技術的可擴展近似最近鄰演算法索引，提供更快的查詢速度、更快的索引建立速度和更高的寫入吞吐量。
    *   查詢最佳化器：增強了最佳化器，使其能夠根據向量和 SQL 的組合自適應地選擇最佳執行計畫。
*   **Ivan for AlloyDB Omni：**
    *   在 Ivan 的平台上託管 AlloyDB Omni，提供託管服務。
    *   管理高可用性、備份、零停機時間、次要升級、修補、安全性和異地備援等功能。
    *   簡化了開發人員的工作，並提供 API 優先的方法。
    *   允許輕鬆配置柱狀資料庫的資源。
    *   提供簡化的遷移流程，例如將資料庫從 AWS 遷移到 Google Cloud。
*   **Google Cloud Ready 計畫：**
    *   正式認可與 AlloyDB 良好協作的合作夥伴產品。
    *   合作夥伴包括 PlyOps、Silk、Hitachi Vantara、Pure Storage 和 CommVault。
    *   Silk 提供軟體定義的雲端儲存，可增強 AlloyDB 部署的效能。
    *   Portworx by Pure Storage 幫助管理跨多雲和混合雲環境的 AlloyDB 環境。
    *   Hitachi Vantara 提供與 AlloyDB Omni 無縫整合的預先配置部署。
    *   Commvault 為 AlloyDB Omni 資料庫提供強大的資料保護功能。

## 3. 重要結論

AlloyDB Omni 是一個功能強大且靈活的資料庫解決方案，可以加速 AI 應用程式的開發，並將其部署在任何環境中。透過與 Ivan 和 Google Cloud Ready 計畫合作夥伴的整合，AlloyDB Omni 提供了一個完整的生態系統，可以簡化部署、管理和保護資料。
