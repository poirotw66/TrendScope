Solve real-time AI challenges Bigtable and BigQuery in Spotify’s music recommendation engine

[會議影片連結](https://www.youtube.com/watch?v=-rxMDSgsSQU)
Solve real-time AI challenges Bigtable and BigQuery in Spotify’s music recommendation engine

## 1. 核心觀點

本次會議主要探討了如何利用 Bigtable 和 BigQuery 解決 Spotify 音樂推薦引擎中的即時 AI 挑戰。核心觀點包括：

*   **Bigtable 和 BigQuery 的結合：** 強調了這兩種資料庫結合所產生的即時分析能力，以及如何滿足對資料即時性的需求。
*   **Bigtable SQL 的通用性：** 介紹了 Bigtable SQL 的通用性，使得具備 SQL 專業知識的人員也能夠輕鬆構建全託管的即時應用後端。
*   **連續具體化視圖（Continuous Materialized Views）的優勢：** 強調了連續具體化視圖在加速資料檢索和改善存取方面的作用，尤其是在需要快速存取複雜查詢結果的場景中。
*   **Spotify 的使用者理解：** 強調使用者理解在個性化推薦系統中的核心地位，以及如何透過不同層次的複雜度來實現個性化。
*   **特徵工程的重要性：** 探討了從批次推論到即時推論的演進，以及在特徵工程中需要考慮的延遲、新鮮度和複雜性之間的權衡。
*   **Goldilocks 區域模型：** 介紹了推薦系統模型的 Goldilocks 區域，強調了資料新鮮度、等待時間之間的平衡，並預測了 LLM 代理在未來推薦系統中的作用。
*   **BigQuery 數據框架（BigQuery DataFrames）：** 介紹了 BigQuery 數據框架如何簡化 Python 中的大規模資料科學，並利用 BigQuery 的分散式計算能力。
*   **AI 查詢引擎（AI Query Engine）：** 介紹了 BigQuery 的 AI 查詢引擎，它將 LLM 技術整合到核心查詢引擎中，以便從非結構化資料中獲取語義洞察。

## 2. 詳細內容

*   **Google 資料雲：** 介紹了 Google 的資料雲，這是一個全面的分析和資料庫平台，提供了多種資料庫選項，包括非關聯式資料庫 Bigtable。
*   **Bigtable SQL：** 宣布 Bigtable 現在提供 Google SQL 介面，與 BigQuery 使用相同的 SQL 方言，適用於需要大規模快取引擎的場景。Bigtable SQL 支援單一位數毫秒級回應、高 QPS、彈性架構和全球部署。
*   **連續具體化視圖：** 介紹了 Bigtable 的連續具體化視圖，它將查詢結果儲存為實體表，從而加快資料檢索速度。這種視圖非常適合詐欺偵測、即時追蹤系統和遙測系統等應用。
*   **Spotify 的推薦系統：** 描述了 Spotify 的音樂推薦引擎，該引擎使用兩階段方法：候選生成和排序。排序階段是即時 AI 挑戰的主要來源。
*   **建立個性化播放清單：** 透過建立名為 "Top Genre Daily" 的新播放清單，逐步展示了如何解決即時 AI 挑戰。
    *   **第一級：批次推論：** 使用 BigQuery 作為離線特徵儲存，每天更新一次所有使用者的預測。
    *   **第二級：線上特徵儲存：** 引入 Bigtable 作為線上特徵儲存，僅對點擊 "Top Genre Daily" 的使用者進行即時推論。
    *   **第三級：即時特徵：** 加入時間和裝置等即時特徵，但需要解決訓練服務資料偏差的問題。
    *   **第四級：日誌：** 移除 BigQuery，並將所有特徵載入到 Bigtable 中，從而消除訓練服務資料偏差。
    *   **第五級：近即時特徵：** 加入近即時特徵，例如過去 30 分鐘內聽過的藝人，以提高新鮮度和回應能力。
*   **案例研究：**
    *   **藝人偏好模型：** 使用第二級方法，透過批次管道更新特徵，並從 Bigtable 擷取特徵以進行線上推論。
    *   **使用者表示嵌入：** 使用第五級方法，建立一個基礎嵌入，可以被多個模型重複使用，從而簡化複雜性並擴展個性化。
*   **BigQuery 數據框架：** 介紹了 BigQuery 數據框架，它允許資料科學家使用熟悉的 Pandas 和 Scikit-learn API，同時利用 BigQuery 的分散式計算能力。
*   **AI 查詢引擎：** 介紹了 BigQuery 的 AI 查詢引擎，它將 LLM 技術整合到核心查詢引擎中，以便從非結構化資料中獲取語義洞察。
*   **示範：** 展示了如何使用 BigQuery 數據框架和 AI 運算子來建立播放清單，並將這些播放清單同步到 Bigtable。還展示了如何使用 Kafka 連接器將即時資料載入到 Bigtable 中，以及如何使用具體化視圖來建立即時分析儀表板。

## 3. 重要結論

Bigtable 和 BigQuery 的結合為構建即時 AI 應用程式提供了強大的解決方案。透過 Bigtable SQL、連續具體化視圖和 BigQuery 數據框架等新功能，開發人員可以更輕鬆地利用這兩種資料庫的功能。Spotify 的案例研究強調了使用者理解和特徵工程在構建個性化推薦系統中的重要性。此外，BigQuery 的 AI 查詢引擎為從非結構化資料中獲取語義洞察提供了新的可能性。總體而言，本次會議為開發人員提供了寶貴的見解和實用技巧，以解決即時 AI 挑戰並構建創新的應用程式。
