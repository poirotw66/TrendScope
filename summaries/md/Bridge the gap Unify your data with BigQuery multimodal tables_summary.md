# Bridge the gap Unify your data with BigQuery multimodal tables

[會議影片連結](https://www.youtube.com/watch?v=hBg8FB6vCQ8)
彌合差距：使用 BigQuery 多模態表格統一您的數據

## 1. 核心觀點

本次會議主要介紹了 BigQuery 中名為 "Object Ref" 的新功能，旨在彌合結構化和非結構化數據之間的鴻溝。Object Ref 允許您在 BigQuery 表格中直接引用 Google Cloud Storage (GCS) 中的非結構化數據（例如圖像、音頻、視頻、文檔），從而可以使用 SQL 和 Python 對結構化和非結構化數據進行統一分析和機器學習。

核心觀點包括：

*   **Object Ref 的概念：** Object Ref 是一種新的數據類型，可以嵌入到 BigQuery 表格中，用於引用 GCS 中的非結構化數據對象。
*   **Object Ref 的優勢：** 簡化了 AI/ML 工作流程，允許在單個查詢中結合結構化和非結構化數據，並繼承了 BigQuery 的所有治理和安全功能。
*   **Object Ref 的應用場景：** 客戶服務、保險理賠、城市服務等，可以通過結合結構化數據和非結構化數據來獲得更深入的洞察。

## 2. 詳細內容

*   **BigQuery 處理非結構化數據的歷史：**
    *   早期 BigQuery 主要處理結構化數據。
    *   2023 年引入了 Object Tables，作為 GCS 對象的只讀元數據層，允許使用 SQL 查詢 GCS 中的非結構化數據。
    *   Object Tables 存在一些限制，例如只讀、固定 Schema、單個對象對應單行、訪問控制限制、可擴展性限制。

*   **Object Ref 的介紹：**
    *   Object Ref 是一個 struct 數據類型，包含 URI（指向 GCS 對象）、Authorizer（用於安全訪問 GCS 對象）、Version（GCS 對象的版本 ID）、Details（GCS 元數據）等字段。
    *   Object Ref 可以直接嵌入到 BigQuery 表格中，與結構化數據並存。
    *   Object Ref 支持嵌套在數組中，方便處理一對多關係（例如，一個音頻書籍有多個章節）。

*   **Object Ref 的創建方式：**
    *   通過 Object Tables 自動創建（即將推出）。
    *   使用 `obj.make_ref` 函數，手動指定 URI 和 Authorizer。

*   **Object Ref 在 AI/ML 中的應用：**
    *   BigQuery ML 函數（例如 `ml.generate_text`、`ml.generate_embedding`）現在支持 Object Ref 作為輸入。
    *   可以使用 SQL 或 Python 結合結構化數據和非結構化數據進行 AI/ML 分析。
    *   可以將多個 Object Ref 或 Object Ref 數組傳遞給 AI/ML 函數。

*   **Object Ref 的治理和安全：**
    *   Object Ref 繼承了 BigQuery 的所有治理和安全功能，例如列級別安全、行級別安全、數據脫敏。
    *   可以限制用戶對 Object Ref 列的訪問。
    *   可以使用不同的 Cloud Resource Connection 來控制對 GCS 對象的訪問。

*   **Object Ref 的應用示例：**
    *   **311 城市服務：** 結合市民提交的文本描述、圖片、音頻、視頻，使用 AI 模型自動分類問題、評估緊急程度、生成處理建議。
    *   **技術支持：** 結合用戶提交的描述、截圖、視頻，使用 AI 模型診斷問題、提供解決方案。
    *   **保險理賠：** 結合保單信息、事故照片、錄音記錄、維修估價單，使用 AI 模型驗證損壞一致性、檢測潛在欺詐。

*   **Object Ref 的 Python 支持：**
    *   可以使用 Pandas API 和 BigQuery DataFrames 創建包含 Object Ref 的多模態數據框。
    *   可以使用 Python UDF 和新的 Object 函數來訪問和處理非結構化數據。

*   **Object Ref 的未來發展方向：**
    *   簡化連接管理。
    *   提高性能和可擴展性。
    *   支持數據沿襲。
    *   支持通過 Analytics Hub 共享數據。

## 3. 重要結論

Object Ref 是 BigQuery 的一項重要創新，它極大地簡化了結構化和非結構化數據的集成和分析。通過 Object Ref，用戶可以充分利用 BigQuery 的強大功能，從多種數據源中獲得更深入的洞察，並構建更智能的應用程序。Object Ref 的推出將推動 BigQuery 在 AI/ML 領域的應用，並為用戶帶來更大的價值。
