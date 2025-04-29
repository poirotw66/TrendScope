# Best practices for building a lakehouse on Google Cloud_2

[會議影片連結]()
Best practices for building a lakehouse on Google Cloud_2

## 1. 核心觀點

本次會議主要探討在 Google Cloud 上構建 Lakehouse 的最佳實踐。核心觀點包括：Lakehouse 的關鍵組件、BigQuery 在資料治理中的作用、以及如何選擇合適的工具來處理資料、編排工作流程和提取資料價值。強調 BigQuery 作為統一治理平台的重要性，以及各種 Google Cloud 產品如何協同工作，從資料中提取價值。

## 2. 詳細內容

*   **Lakehouse 的關鍵組件：**
    *   **儲存層：** 優化開放表格格式，例如 Apache Iceberg，並建立一個僅使用單一資料副本的基礎架構。
    *   **資料處理層：** 使用 SQL 和其他開源處理引擎（例如 Apache Spark）執行批次和串流處理。
    *   **工作流程編排：** 使用適當的工具來管理和編排複雜且重複的工作流程。
    *   **資料分析：** 整合資料分析、AI 和機器學習模型以及商業智慧工具，以獲得資料洞察。
    *   **資料治理：** 確保安全、高品質的資料，這是所有其他組件的基礎。

*   **BigQuery 的作用：**
    *   BigQuery 是一個用於所有資料管理和治理需求的一站式商店。
    *   它涵蓋了治理生命週期的所有方面，包括：
        *   跨雲端專案發現多模式資料表。
        *   透過資料剖析和血緣等功能提供詳細的資料檢視。
        *   透過控制使用者存取和執行自動化資料品質檢查來建立對資料的信任。
        *   透過集中式中繼資料儲存庫管理組織如何使用資料。
        *   提供 AI 驅動的洞察和資料共享功能。

*   **工具選擇：**
    *   **儲存：** Cloud Storage 用於傳統資料湖，也可以管理 OpenTable 格式，並使用 BigQuery 和 Big Lake 存取資料。
    *   **資料處理：**
        *   Dataproc：用於託管的 Apache Spark 體驗，與 BigQuery 整合。
        *   Dataflow：Google 的託管 Apache Beam 產品，用於批次和串流工作負載。
        *   BigQuery：直接使用 SQL 存取資料。
        *   Big Lake：用於存取儲存資料。
        *   BigQuery tables for Apache Iceberg (預覽功能)：用於託管的 Iceberg 體驗。
    *   **工作流程編排：**
        *   Cloud Composer：建立在 Apache Airflow 之上，提供複雜的、以程式碼為中心的工作流程。
        *   Google Workflows：一個無伺服器、以 API 為中心的工具，使用宣告式 YAML。
        *   Cloud Scheduler：最輕量級的工具，支援傳統的基於 cron 的作業。
        *   Cloud Data Fusion：允許使用視覺化和無程式碼方法建立資料管道。
        *   BigQuery Scheduled Queries：允許直接在 BigQuery 內自動化 SQL 查詢。
    *   **資料價值提取：**
        *   Notebook：使用 Notebook 載入和視覺化資料，包括透過新的 Apache Spark 和 BigQuery 功能（目前為預覽版）在 BigQuery Studio 中使用 Python 和 PySpark。
        *   Vertex AI Workbench：用於託管的 Jupyter Notebook 體驗。
        *   BigQuery ML：提供基於 SQL 的工具來訓練和部署機器學習模型。
        *   Vertex AI：可以管理 MLOps 生命週期的所有方面，包括使用您選擇的框架訓練和部署機器學習模型。
        *   Looker：用於建立強大的 BI 儀表板。

*   **架構範例：**
    *   BigQuery 位於中心，作為一個統一的治理平台，管理我們的資料，並讓我們使用先前討論的許多產品從中提取價值。

## 3. 重要結論

在 Google Cloud 上構建 Lakehouse 需要仔細考慮儲存、處理、編排、分析和治理等關鍵組件。BigQuery 在資料治理方面扮演著核心角色，而各種 Google Cloud 產品提供了靈活的工具來處理資料、編排工作流程和提取資料價值。透過將這些組件整合在一起，組織可以建立一個強大的 Lakehouse，從其資料中獲得有意義的洞察。
