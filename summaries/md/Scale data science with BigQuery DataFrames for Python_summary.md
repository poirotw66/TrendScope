Scale data science with BigQuery DataFrames for Python

[會議影片連結](https://www.youtube.com/watch?v=24_ILX3wLVg)
使用 BigQuery DataFrames for Python 擴展資料科學

## 1. 核心觀點

本次會議主要介紹如何使用 BigQuery DataFrames 這個 Python 開源函式庫，在 BigQuery 上進行大規模資料科學運算。核心觀點包括：

*   **BigQuery DataFrames 的優勢：** 能夠在不離開 BigQuery 的情況下，使用熟悉的 Pandas 和 Scikit-learn API 處理大規模資料，簡化了從小型資料集到大型資料集的過渡。
*   **BigQuery DataFrames 的運作原理：** 作為一個轉譯器，將 Pandas 和 Scikit-learn API 轉換為 BigQuery SQL 和 BigQuery ML SQL，並在 BigQuery 內部執行。
*   **BigQuery DataFrames 的最新發展：** 推出 2.0 版本，包含效能優化（部分排序）、擴展的資料類型支援（陣列、結構、JSON）以及與 BigQuery Managed Python Functions 的整合。
*   **BigQuery DataFrames 的未來方向：** 支援多模態資料（結構化和非結構化資料），並整合 AI Query Engine 和向量搜尋等技術，以簡化從非結構化資料中提取語義洞察的過程。
*   **Deutsche Telekom 的案例分享：** 介紹了如何使用 BigQuery DataFrames 遷移 PySpark 程式碼，並在 BigQuery 上建立機器學習平台。

## 2. 詳細內容

*   **Python 在資料科學領域的普及：** Python 是資料科學和資料分析中最流行的語言之一，尤其是在生成式 AI 和多模態分析興起後，其受歡迎程度進一步提升。
*   **傳統資料科學工作流程的挑戰：** 當資料量或計算需求增加時，傳統的單一筆記本體驗會遇到瓶頸，需要轉向分散式運算框架，這會帶來額外的基礎設施成本和程式碼重寫工作。
*   **BigQuery DataFrames 的解決方案：** BigQuery DataFrames 允許使用者使用熟悉的 Pandas 和 Scikit-learn API，在 BigQuery 上處理大規模資料，無需學習新的基礎設施或重寫程式碼。
*   **BigQuery DataFrames 的三個子套件：**
    *   `bigframes.pandas`：模擬 Pandas 函式庫。
    *   `bigframes.ml`：模擬 Scikit-learn API，並使用 BigQuery 的無伺服器機器學習功能。
    *   LLM 擴展：提供對 Gemini 和第三方 LLM 模型的存取。
*   **BigQuery DataFrames 的成功案例：** 推出一年以來，資料處理量成長了 30 倍，全球有數千家客戶每月處理數百 PB 的資料。
*   **BigQuery DataFrames 2.0 的新功能：**
    *   **部分排序：** 透過放寬資料排序的嚴格要求，顯著提高效能並降低成本。
    *   **擴展的資料類型支援：** 支援 BigQuery 中的陣列、結構和 JSON 等進階資料類型。
    *   **與 BigQuery Managed Python Functions 的整合：** 簡化了 Python UDF 的建立和管理，提高了效能。
*   **與 DBT 的合作：** 允許 DBT 使用者在 DBT 的 BigQuery 介面中混合使用 SQL 和 Python 模型，從而在 DBT 管道中實現 SQL 和 Python 的工作流程。
*   **多模態資料框架：** 引入新的 blob 資料類型，以支援結構化和非結構化資料的混合，並利用 BigQuery 的物件參考功能來存取非結構化資料。
*   **AI Query Engine：** 將 LLM 技術整合到 BigQuery 的查詢規劃器和查詢執行引擎中，以簡化從非結構化資料中提取語義洞察的過程。
*   **與向量搜尋的整合：** 允許使用者使用資料框架生成嵌入，並使用向量搜尋技術進行相似性搜尋。
*   **串流資料框架：** 簡化了將資料從 BigQuery 等離線儲存區同步到 Bigtable 等線上儲存區的過程。
*   **程式碼生成和推薦：** BigQuery 的筆記本現在可以為 BigQuery DataFrames 生成和推薦程式碼，以降低學習曲線。
*   **Deutsche Telekom 的案例：**
    *   **One Data Ecosystem：** 一個基於 Google Cloud 的機器學習平台，旨在協調資料擷取和處理。
    *   **特徵工程：** 使用 BigQuery DataFrames 遷移 PySpark 程式碼，並建立特徵工程框架。
    *   **兩步驟遷移過程：** 首先將 PySpark 程式碼轉換為 Pandas 程式碼，然後將 Pandas 程式碼轉換為 BigQuery DataFrames 程式碼。
*   **示範：** 展示了如何使用 BigQuery DataFrames 建立一個由 GenAI 驅動的資料應用程式，該應用程式可以處理結構化和非結構化資料，並生成動態 FAQ。

## 3. 重要結論

BigQuery DataFrames 提供了一個強大的工具，可以在 BigQuery 上進行大規模資料科學運算。透過簡化資料處理流程、支援多模態資料和整合 AI 技術，BigQuery DataFrames 使資料科學家能夠更有效地從資料中提取洞察，並構建創新的應用程式。Deutsche Telekom 的案例證明了 BigQuery DataFrames 在實際應用中的價值。
