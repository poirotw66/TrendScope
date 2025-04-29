# Enhance the customer experience with Gemini 2.0, Flutter, and Firebase

[會議影片連結](https://www.youtube.com/watch?v=fuLh8B865hw)
使用 Gemini 2.0、Flutter 和 Firebase 增強客戶體驗

## 1. 核心觀點

本次演講主要介紹如何使用 Gemini 2.0、Flutter 和 Firebase 來增強客戶體驗。核心觀點包括：

*   Vertex AI 和 Firebase 產品套件可以單獨或一起使用，涵蓋應用程式的整個生命週期，包括開發、發布和使用者互動。
*   透過簡單直觀的開發者體驗，目標成為應用程式開發者利用 Google 最先進的 AI 模型的首選解決方案。
*   Live API 是一個介面，專為使用音訊和視訊串流與 Gemini 模型進行即時、持續的互動而設計。

## 2. 詳細內容

*   **Vertex AI 和 Firebase 的整合：**
    *   簡化了後端複雜性，提供客戶端 SDK，允許使用 Dart、Kotlin、Swift 和 JavaScript 等語言直接從應用程式呼叫 Gemini API。
    *   只需三行程式碼即可實例化 Gemini 模型，並使用提示詞（例如：寫一個關於魔法背包的故事）生成內容。
*   **Vertex AI 和 Firebase 的能力：**
    *   透過提示、系統指令、JSON 輸出和函數呼叫的組合，可以實現許多功能。
    *   無需處理服務層、REST API 或部署任何東西，只需從應用程式直接呼叫 Gemini API。
*   **Live API 的介紹：**
    *   允許與 Gemini 模型進行即時、連續的互動，使用音訊和視訊串流。
    *   應用程式建立與 Gemini API 的連線，並持續傳送小的音訊或視訊資料區塊。
    *   Gemini 逐步處理這些傳入的區塊，理解上下文，並同時傳送回生成的音訊、文字或基於對輸入串流的即時理解的回應。
    *   這種雙向串流 API 解鎖了需要立即分析和回應正在發生的視聽事件的使用案例，例如即時翻譯或基於攝影機的即時視訊串流提供音訊指導。

## 3. 重要結論

Vertex AI 和 Firebase 透過簡化 AI 模型的整合和提供即時互動能力，為開發者提供了強大的工具，以增強客戶體驗。Live API 的引入開闢了新的應用場景，將 AI 從工具轉變為積極的參與者。鼓勵開發者開始使用 Vertex AI 和 Firebase 進行構建，並分享回饋以改進產品。
