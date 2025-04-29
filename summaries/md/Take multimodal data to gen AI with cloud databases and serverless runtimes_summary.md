# Take multimodal data to gen AI with cloud databases and serverless runtimes
[會議影片連結](https://www.youtube.com/watch?v=20THk0ZzNBA)
將多模態數據導入生成式 AI，使用雲端資料庫和無伺服器運行環境

## 1. 核心觀點

本次演講介紹如何使用 Google Cloud 的服務，包括 AlloyDB、Gemini、Imagine 和 Cloud Run，建立一個個人造型師 App。核心觀點是利用 AlloyDB 儲存衣櫃數據的向量表示，並結合 Gemini 生成圖像描述和個人化建議，最後使用 Imagine 產生視覺化的穿搭推薦。整個應用程式使用 Java Spring Boot 框架和 Gemini Java SDK 構建，並以無伺服器方式託管在 Cloud Run 上。

## 2. 詳細內容

首先，講者介紹了 AlloyDB，它是 Google Cloud 針對 Postgres 相容的資料庫，經過完整優化，可處理低延遲和高吞吐量的高需求工作負載。使用者上傳一張穿搭照片（例如上衣的自拍照），Gemini 會生成該圖像的描述。然後，使用 AlloyDB 向量擴充功能，將此描述轉換為向量嵌入，並使用 text embedding 005 模型。AlloyDB 透過其快速掃描索引演算法，從衣櫃資料庫中找到最接近的鄰居，這些資料庫已經包含穿搭推薦的嵌入。接著，Gemini 會為搜尋結果產生個人化建議，並允許使用者新增個人化設定，例如「添加一個可愛的白色盒子包」或「添加太陽眼鏡」。整個個人化過程隨後會被發送到 Imagine，以建立視覺化表示。

應用程式的示範展示了如何上傳服裝圖片，然後讓 Gemini 生成服裝描述，並從衣櫃資料庫中找到匹配的服裝。使用者還可以新增個人化設定，例如「添加耳環」或「添加卡其色褲子」。點擊「顯示」後，Imagine 會生成出色的服裝推薦，並包含使用者要求的個人化設定。

整個應用程式使用 Java Spring Boot 框架和 Gemini Java SDK 構建，並以無伺服器方式託管在 Cloud Run 上。

## 3. 重要結論

本次演講展示了如何利用 Google Cloud 的多種服務，快速構建一個基於 AI 的應用程式。講者鼓勵大家嘗試這個 lab hands-on，並擴展其功能，並將任何有趣的功能擴展提交到程式碼實驗室中連結的 GitHub 儲存庫。
