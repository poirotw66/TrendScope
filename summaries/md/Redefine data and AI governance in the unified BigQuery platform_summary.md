# Redefine data and AI governance in the unified BigQuery platform
[會議影片連結](https://www.youtube.com/watch?v=g2LIKmswKXM)
在統一的 BigQuery 平台中重新定義資料和 AI 治理

## 1. 核心觀點

本次會議主要探討在統一的 BigQuery 平台中，如何重新定義資料和 AI 治理。核心觀點包括：

*   AI 應用快速發展，健全的資料和 AI 治理策略至關重要。
*   治理必須是通用的、智慧的且開放的。
*   BigQuery 正在演進為一個真正的統一 AI-ready 資料平台，而 BigQuery Universal Catalog 是其核心的 metadata 管理和治理層。
*   Walmart 和 Box 分享了他們在資料治理方面的實踐經驗。
*   Google 宣布了一系列新的產品功能，以加強資料和 AI 治理。

## 2. 詳細內容

**Lu Yan (Google)** 首先概述了 Google 對於在統一 BigQuery 平台中重新定義資料和 AI 治理的願景和策略。她強調，隨著 AI 應用的快速發展，健全的資料和 AI 治理策略變得至關重要。她指出，70% 的組織在 AI 用例中遇到了資料治理方面的困難，這是從試點到生產擴展 AI 的關鍵瓶頸。為了滿足這些關鍵需求，治理必須是通用的（無縫整合到端到端資料到 AI 生命週期）、智慧的（AI 驅動，自動化關鍵治理任務）且開放的（與各種儲存和計算選項相容）。

Lu Yan 介紹了 BigQuery Universal Catalog，它是 BigQuery 的核心 metadata 管理和治理層，涵蓋所有不同的計算和儲存選項。它包括 Dataplex 的所有功能，以及 BigQuery 安全性、BigQuery 共享和執行階段 Metastore 功能。Universal Catalog 提供以下關鍵價值：

*   單一視窗，用於使用自然語言發現組織內部的資料和 AI 資產，並在組織內部和跨組織共享這些資產。
*   利用 AI 驅動的智慧來增強對資料的信任，從自動產生 metadata 描述到監控資料異常，再到根據資料推薦洞察。
*   開放性，提供對 Apache Iceberg 等開放儲存格式的執行階段和治理支援，並與豐富的合作夥伴生態系統協同工作。

Universal Catalog 自動從所有不同的資料和 AI 來源收集 metadata，然後將這些 metadata 與 Google 最先進的大型語言模型相結合，以幫助使用者更主動和高效地進行治理。它完全整合到 BigQuery 環境中，許多關鍵治理功能已經在 BigQuery 體驗中可用，包括 lineage、資料剖析、資料品質、資料洞察和 GCS metadata 發現。Google 還將推出資料管理中心的治理中心體驗，這是一個專門的管理控制台體驗，供資料管理員、資料管理員和安全專業人員管理、保護和治理整個資料和 AI 環境。

**Eric Risher (Walmart Data Ventures)** 分享了 Walmart Data Ventures 如何利用 BigQuery Universal Catalog 來管理資料並確保資料的可靠性。他強調了資料品質的重要性，並介紹了 Walmart Data Ventures 如何採用 3D 方法來確保資料品質。他們使用 BigQuery Universal Catalog 來建立靈活的規則，並利用 Looker 來視覺化和修復資料。

**Asmita Kulkarni (Box)** 分享了 Box 如何使用 BigQuery Universal Catalog 來解決資料發現、資料 lineage 和資料安全方面的挑戰。她介紹了 Box 如何建立一個可擴展的多租戶資料平台，該平台基於資料網格架構，並利用 Dataplex 來實現分散式所有權和聯合治理。Box 使用 Dataplex 方面（aspects）來建立標準化的 metadata 框架，並使用資料 lineage 來追蹤資料從來源到目的地的路徑。他們還建立了一個強大的資料分類框架，利用 Dataplex 和 Google 的資料遺失防護 (DLP) 來保護敏感資料。

**Lu Yan (Google)** 回到台上，介紹了 Google 在資料治理領域的最新產品功能。這些功能涵蓋資料生命週期的四個不同階段：發現、理解、信任和使用。Google 宣布了對 Vertex AI 功能儲存、Cloud SQL 和 Dataform 的支援，以及對第三方資料來源的受管理 metadata 編目支援。Google 還宣布了即將推出的 BigQuery 內通用語義搜尋預覽版，以及對 Vertex AI pipelines、Vertex AI 功能儲存、Dataflow、Dataproc serverless 和 Hive 的 lineage 支援。此外，Google 還宣布了 Business Glossary 的 GA 版本，以及自動 metadata 產生和資料異常偵測功能。最後，Google 宣布了即將推出的資料產品，旨在幫助使用者管理、包裝和共享資料資產。

## 3. 重要結論

本次會議強調了在 AI 時代，資料治理的重要性日益增加。BigQuery Universal Catalog 提供了一個統一的平台，用於管理和治理資料和 AI 資產。Walmart 和 Box 的案例研究表明，BigQuery Universal Catalog 可以幫助組織解決資料發現、資料 lineage 和資料安全方面的挑戰。Google 宣布的一系列新產品功能將進一步加強資料和 AI 治理。
