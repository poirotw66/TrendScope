# Support disaster resilience with integrated AI-driven geospatial analytics

[會議影片連結](https://www.youtube.com/watch?v=N71tiXvLvrM)
以整合式 AI 驅動的地理空間分析來支援災害復原能力

## 1. 核心觀點

本次會議主要探討如何利用 Google 的地理空間技術，特別是 Earth Engine 和 BigQuery，結合 AI 模型（如 Weather Next），來提升災害生命週期各階段的應對能力，從災害風險評估、應急響應到災後重建。核心觀點包括：

*   地理空間技術在災害管理中的重要性：強調利用地理空間技術改善災害預測和應對流程。
*   Earth Engine 和 BigQuery 的整合應用：展示如何結合這兩個平台的強大功能，進行向量和柵格數據分析。
*   AI 模型在災害預測中的作用：介紹 Weather Next 等 AI 模型如何提供高解析度的全球天氣數據，用於災害相關的應用。
*   數據驅動決策的重要性：強調利用數據分析結果來制定更有效的災害應對策略。

## 2. 詳細內容

會議首先介紹了 Google 的地理空間技術基礎，包括 Earth Engine 和 BigQuery。Earth Engine 是一個雲端地理空間分析平台，提供大量的衛星影像數據，並支援大規模的柵格數據處理。BigQuery 是一個全託管的數據倉庫，提供快速的 SQL 分析能力，並與 Earth Engine 和 Vertex AI 等雲端工具無縫整合。

接著，會議重點介紹了 Earth Engine 和 BigQuery 的整合，以及新推出的 STRegionStats 地理函數。這個函數允許使用者基於柵格數據與向量數據的交集，計算特定區域的統計數據。此外，Analytics Hub 還新增了 20 個衍生數據集，涵蓋常見的永續性應用場景。

會議還介紹了 Google Research 和 Google DeepMind 推出的 Weather Next，這是一系列全球高解析度的 AI 模型，提供天氣相關的數據，可用於 Earth Engine 和 BigQuery 進行柵格分析。

隨後，會議以野火為例，展示了如何將這些工具應用於災害生命週期的各個階段。首先，利用 Analytics Hub 中的 Wildfire Risk to Communities 數據集，評估野火風險。然後，使用 STRegionStats 函數，結合建築物足跡數據，計算每個建築物的野火風險統計數據，並在 GeoViz 上以地圖形式呈現。

在應急響應階段，Earth Engine 可用於處理和鑲嵌原始衛星數據，Weather Next 可用於提供天氣模式信息。例如，在洛杉磯的野火事件中，Earth Engine 用於處理每日的衛星影像，並透過 Google Earth 提供給公眾。

在災後重建階段，Google Research 的 Open Buildings Temporal Data Set 可用於分析建築物高度的變化，了解災害影響，並指導重建工作。

## 3. 重要結論

本次會議展示了 Google 如何利用其強大的地理空間技術和 AI 模型，支援災害復原能力。Earth Engine 和 BigQuery 的整合，以及 Weather Next 等 AI 模型的應用，為災害管理提供了更精確、更高效的工具。透過數據驅動的決策，可以更好地應對自然災害，保護人民的生命和財產安全。
