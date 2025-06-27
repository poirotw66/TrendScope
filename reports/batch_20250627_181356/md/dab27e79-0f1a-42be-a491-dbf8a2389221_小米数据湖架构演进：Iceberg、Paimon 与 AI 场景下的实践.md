小米数据湖架构演进：Iceberg、Paimon 与 AI 场景下的实践
主題演講
[會議影片連結](https://qcon.infoq.cn/2025/beijing/presentation/6333)
小米數據湖架構演進：Iceberg、Paimon 與 AI 場景下的實踐

**1. 核心觀點**

本次演講深入探討了小米數據湖架構的演進之路，重點展示了如何從傳統離線湖倉向實時湖倉轉型，並將數據湖技術應用於多元化的 AI 場景。核心觀點包括：第一，小米已將 Iceberg 作為集團數倉標準，並成功推動數據湖上雲，以應對成本、容量和性能的挑戰。第二，針對 Iceberg 在實時主鍵更新和 Flink `changelog` 消費上的不足，引入 Apache Paimon 作為實時湖倉的核心組件，顯著簡化了複雜的實時聚合與特徵工程。第三，為了解決 AI 場景下非表格數據的管理難題，小米創新性地採用 Gravitino Fileset 結合 `gvfs` 虛擬文件系統，實現了統一的數據管理、治理和訪問。最後，Paimon 在大模型訓練數據預處理和動態標籤挖掘等 AI 場景中發揮了關鍵作用。

**2. 詳細內容**

**數據湖架構與上雲實踐**
小米集團擁有手機、新零售、IoT、互聯網應用、汽車及 AI 等多元業務場景，對數據平台提出極高要求。小米的湖倉架構涵蓋數據工場平台、Flink/Spark/Trino 等計算引擎、Gravitino 元數據管理、Hive/Iceberg/Paimon/Fileset 數據湖以及 HDFS/JuiceFS 存儲層。目前 Iceberg 已是集團數倉標準，管理超過 7 萬張表和 100PB 數據。為應對 IDC 環境下的高成本、容量限制及 HDFS 慢節點/小文件問題，小米積極推進數據湖上雲。在存儲選型上，JuiceFS（自建）因其在 QPS、讀性能、Bucket 帶寬和租戶隔離方面的優勢，被選為上雲核心存儲方案。Iceberg 上雲方案針對溫數據採用異步轉儲，熱數據則通過 JuiceFS Cache 直寫雲上對象存儲。雲上認證鑑權則透過 Spark、Gravitino、Ranger 和 Secret Management 實現統一管理。

**從離線湖倉到實時湖倉**
儘管 Iceberg 在離線數據倉儲中表現卓越，但在實時湖倉場景下面臨挑戰。Iceberg 在主鍵更新時難以保證並發唯一性，`upsert` 會生成過多 `equality delete` 記錄導致查詢緩慢。此外，其 Flink 流式消費 `changelog` 存在不完整（-D 記錄僅含主鍵）、缺少 -U/+U 操作、無效 `equality delete` 導致聚合錯誤以及數據亂序等問題。
為了解決這些痛點，小米引入 Apache Paimon，其核心理念是「把複雜留給自己, 把簡單留給用戶」。Paimon 的聚合模型允許用戶透過簡單的 SQL 配置實現複雜的聚合邏輯，無需手動編寫繁瑣的 `collect_list` 和 `sum`。在特徵工程的典型應用中，Paimon 結合 Flink 將傳統天級延遲、高重試成本的離線鏈路轉變為分鐘級延遲、增量計算、無需 Join（由 Paimon 內部聚合）的實時鏈路，大幅提升了數據處理效率和實時性。

**數據湖在 AI 場景的實踐**
數據湖在 AI 場景的應用主要體現在非表格數據管理、大模型訓練數據預處理和 AI 場景數據挖掘。然而，非表格數據（如圖像、音頻、文本文件）的管理和治理面臨缺乏資產定義、生命週期治理困難、審計與共享困難等挑戰。
為此，小米提出 Gravitino Fileset 解決方案。Fileset 提供統一的資產標識和虛擬訪問目錄 (`gvfs://`)，屏蔽了底層存儲細節，使 Spark、Flink、PyTorch 等不同計算框架能透過統一接口訪問 HDFS、JuiceFS 等實際存儲。這實現了 AI 數據的資產管理、生命週期治理、統一認證鑑權，並支持無需入湖即可直接分析。
在大模型訓練數據預處理方面，小米建立了網頁抽取 -> 數據過濾 -> URL 去重 -> 文本相似度去重的流程。其中，網頁抽取利用 PySpark 結合 `gvfs` 將數據存儲到 JuiceFS 的 Fileset 中；數據過濾採用 Hugging Face 的 `datatrove` 庫，其 `fsspec` 模塊與 `fileset` 良好集成；URL 去重則巧妙利用 Paimon 的主鍵表特性，並通過 `sequence.field` 保留長度最長的文檔；文本相似度去重則結合 Paimon、Iceberg 和 JuiceFS，通過多階段 Spark 任務高效完成。
在 AI 場景數據挖掘方面，對於自動駕駛幀數據標籤挖掘，面對上千個動態標籤列和實時入湖需求，Paimon 的聚合模型結合 `merge_map` 函數，能夠高效處理動態標籤的實時更新，優於 Iceberg 的 `merge into`。對於多模態大模型標籤挖掘，Paimon 因其在 Parquet 格式下支持 binary 存儲和隨機訪問性能，在圖片、文本混合存儲方面展現出優勢，同時其 schema evolution 特性便於擴展圖片元數據。

**3. 重要結論**

小米在數據湖領域的實踐證明，通過 Iceberg 和 Paimon 的協同作用，數據湖架構能夠高效支撐離線與實時的業務需求。Paimon 作為實時湖倉的核心，成功解決了 Iceberg 在高併發主鍵更新和實時 `changelog` 消費上的挑戰，極大地簡化了實時數據處理和特徵工程的複雜性。此外，Gravitino Fileset 的引入，為非表格數據（特別是 AI 訓練數據）的管理和治理提供了統一且高效的解決方案，推動了 AI 數據在數據湖上的深度應用。未來，小米將持續發力於雲原生湖倉、元數據統一和多模態數據湖的建設，以適應不斷演進的業務和技術需求。