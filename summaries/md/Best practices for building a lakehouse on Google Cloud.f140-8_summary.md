# Best practices for building a lakehouse on Google Cloud.f140-8

[會議影片連結]()
Best practices for building a lakehouse on Google Cloud.f140-8

## 1. 核心觀點

本次會議主要探討在 Google Cloud 上構建 Lakehouse 的最佳實踐。核心觀點涵蓋了 AI 對資料應用的影響、資料治理的重要性、Lakehouse 的定義與架構，以及 Google Cloud 提供的相關工具和服務。

## 2. 詳細內容

會議首先強調了 AI 正在改變各個產業，但許多組織在擴展 AI 應用和從中獲取價值方面面臨挑戰。良好的資料治理至關重要，因為 AI 的輸出品質取決於輸入資料的品質。

接著，會議介紹了 Lakehouse 的概念，它整合了資料湖和資料倉儲的優勢，旨在打破資料孤島，讓組織能夠更輕鬆地存取和利用其資料。Lakehouse 的構建涉及多個層面，包括：

*   **儲存層：** 採用 Apache Iceberg 等開放表格格式，優化效能和 ACID 交易。
*   **資料處理層：** 使用 Apache Spark 等工具進行批次和串流處理。
*   **資料分析層：** 整合資料分析、AI/ML 模型和商業智慧工具。
*   **資料治理：** 確保資料安全、高品質和易於存取。

會議重點介紹了 BigQuery 在 Lakehouse 架構中的核心作用。BigQuery 提供了統一的治理體驗，支援管理各種資料類型，包括結構化資料、外部表格和串流資料。BigQuery Universal Catalog 簡化了資料的集中管理和探索。此外，BigQuery 還與多種開放原始碼處理引擎（如 Hive、Trino、Spark、Beam）整合，並支援 AI/ML 模型訓練和 Looker 儀表板構建。

會議還介紹了 Google Cloud 提供的其他相關服務，包括：

*   **Cloud Storage：** 用於儲存各種格式的資料。
*   **BigQuery tables for Apache Iceberg：** 提供完全託管的 Iceberg 表格體驗，具有高效能、高吞吐量和零讀取延遲等優勢。
*   **Managed Service for Apache Kafka：** 一個完全託管的 Kafka 體驗，支援 IAM 身份驗證、自動多 VPC 設定和資料加密。
*   **Dataproc：** 一個託管的 Apache Spark 服務，提供多種部署選項，包括 GKE、Hadoop 叢集和無伺服器 Spark。
*   **Dataflow：** 一個託管的 Apache Beam 服務，適用於批次和串流工作流程。
*   **Cloud Composer、Google Workflows、Cloud Scheduler、Cloud Data Fusion、BigQuery Scheduled Queries：** 用於工作流程編排。
*   **BigQuery data insights powered by Gemini：** 提供基於表格元資料的資料洞察。
*   **Vertex AI Workbench：** 用於託管 Jupyter Notebooks。
*   **BigQuery ML：** 提供基於 SQL 的機器學習模型訓練和部署工具。
*   **Vertex AI：** 提供使用任何框架訓練和部署機器學習模型的能力。
*   **Looker：** 用於構建商業智慧儀表板。

會議最後透過一個實際的架構範例，展示了如何將這些工具和服務整合到一個完整的 Lakehouse 解決方案中，包括資料來源、資料處理、資料治理、資料分析和 AI/ML 應用。

## 3. 重要結論

在 Google Cloud 上構建 Lakehouse 需要仔細規劃和選擇合適的工具和服務。資料治理是關鍵，而 BigQuery 在 Lakehouse 架構中扮演著核心角色。透過整合各種 Google Cloud 服務和開放原始碼技術，組織可以構建一個高效、安全且可擴展的 Lakehouse 解決方案，從而充分利用其資料資產。
