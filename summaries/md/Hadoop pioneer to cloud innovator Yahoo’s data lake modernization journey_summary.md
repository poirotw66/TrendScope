# Hadoop pioneer to cloud innovator Yahoo’s data lake modernization journey
[會議影片連結](https://www.youtube.com/watch?v=_7Oz1V1-ZiE)
Hadoop 先驅到雲端創新者 Yahoo 的資料湖現代化之旅

## 1. 核心觀點

本次會議主要探討 Yahoo 作為 Hadoop 的先驅，如何將其龐大的資料湖從傳統的內部部署環境遷移到 Google Cloud，實現雲端現代化的轉型歷程。重點在於分享 Yahoo 在此過程中遇到的挑戰、解決方案以及經驗教訓，旨在幫助其他企業在雲端轉型中節省時間和金錢。

## 2. 詳細內容

會議首先介紹了 Yahoo 的背景，強調其作為全球領先的數位媒體公司，擁有龐大且多樣化的產品組合，包括 Yahoo Finance、Yahoo Mail、Yahoo Sports 和 Yahoo Search 等。這些產品產生了海量的資料，對資料處理和分析提出了複雜的需求。

接著，會議深入探討了 Yahoo 在內部部署環境中管理資料湖所面臨的挑戰，包括：

*   **運營成本高昂：** 需要管理複雜的 Hadoop 和 Storm 集群，以及客製化的資料傳輸、治理和可觀測性解決方案。
*   **資料孤島：** 各個業務部門（verticals）擁有自己的資料，難以實現跨部門的資料共享和整合。
*   **技術債務：** 隨著時間的推移，技術債務不斷累積，導致系統複雜性增加，變更困難。
*   **重複建設：** 不同的團隊為了解決類似的問題，重複建設資料產品，造成資源浪費和使用者混淆。

為了應對這些挑戰，Yahoo 決定將其資料湖遷移到 Google Cloud，並採用資料網格（Data Mesh）架構。Google Cloud 提供了豐富的雲端原生服務，包括 BigQuery、Dataproc、Dataflow 和 Pub/Sub 等，可以幫助 Yahoo 簡化架構、降低成本、提高效率，並加速創新。

會議詳細介紹了 Yahoo 如何利用 Google Cloud 的各項服務來構建其雲端資料湖，包括：

*   **BigQuery：** 作為統一的查詢和處理層，用於資料分析和商業智慧。
*   **Dataproc：** 用於執行 Hadoop 工作負載，實現從內部部署到雲端的平滑過渡。
*   **Dataflow：** 用於批次和串流資料處理，支援複雜的資料轉換和整合。
*   **Pub/Sub：** 作為通用訊息傳遞系統，用於資料收集、傳輸和分發。
*   **Dataplex：** 用於資料治理和目錄管理，幫助使用者發現和理解資料。
*   **Vertex AI：** 作為端到端的機器學習平台，用於構建和部署 AI 模型。

此外，會議還分享了 Yahoo Mail 的雲端遷移案例，重點介紹了如何利用 Google Cloud 的服務來解決資料收集、資料湖構建和 AI 創新方面的挑戰。

最後，Google Cloud 產品經理 Dana Soltani 介紹了 BigQuery 遷移服務的最新功能，包括自動化資料湖評估和自動化資料遷移，可以幫助企業節省雲端遷移的時間和成本。

## 3. 重要結論

Yahoo 的雲端資料湖現代化之旅是一個複雜而漫長的過程，但透過與 Google Cloud 的合作，Yahoo 成功地克服了各種挑戰，實現了架構簡化、成本降低、效率提升和創新加速。本次會議分享的經驗教訓對於其他正在進行或計劃進行雲端轉型的企業具有重要的參考價值。
