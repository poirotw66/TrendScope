# Dialing In Firestore with MongoDB compatibility in Action
[會議影片連結](https://www.youtube.com/watch?v=zuinn3OkskI)
Dialing In Firestore with MongoDB compatibility in Action

## 1. 核心觀點

本次會議主要介紹了 Firestore 與 MongoDB 的兼容性，以及 Dialpad 如何利用 Firestore 構建其 AI 驅動的通訊平台。核心觀點包括：

*   **Firestore 的優勢：** 強調 Firestore 在擴展性、可靠性、開發者生產力方面的優勢，以及其簡化資料遷移的能力。
*   **MongoDB 兼容性：** 介紹了 Firestore 如何通過 MongoDB 兼容性，讓開發者可以使用熟悉的 MongoDB 驅動程式、工具和生態系統。
*   **Dialpad 的應用：** 分享了 Dialpad 如何利用 Firestore 實現低延遲、高可用性和自動擴展，以支持其 AI 通訊平台。
*   **新功能介紹：** 介紹了 Firestore 的新功能，包括查詢編輯器、索引類型、查詢解釋和查詢洞察，以及與 Database Center 的整合。
*   **成本效益：** 強調 Firestore 的定價模式簡單且具有成本效益，並提供承諾使用折扣。

## 2. 詳細內容

*   **Firestore 簡介：** Min Nguyen 介紹了 Firestore 的使命，即通過簡化、速度和信心來釋放應用程式創新。Firestore 是一個企業級文檔資料庫，完全無伺服器，並最大限度地提高開發者生產力。
*   **傳統文檔資料庫的挑戰：** 傳統文檔資料庫面臨擴展性和可靠性方面的挑戰，解決這些問題通常會增加複雜性。Firestore 通過自動、實時地重新平衡分離的計算和儲存來解決這些問題。
*   **Firestore 的架構：** Firestore 的儲存完全分片並跨不同可用性區域複製。當文檔寫入 Firestore 時，Firestore 使用 Paxos 協議來實現跨副本的領導者發起的寫入仲裁。
*   **Firestore 的計算層：** Firestore 的計算層實現了多個開發者友好的 API，包括 Firestore 與 MongoDB 兼容性 API。這些 API 調用 Firestore 的高級查詢引擎來處理請求。
*   **Firestore 的新功能：**
    *   **查詢編輯器：** 允許開發者使用 MongoDB 查詢語言編寫查詢，而無需安裝任何軟體。
    *   **索引類型：** 提供對稀疏和非稀疏索引的完全控制，以及多鍵索引以提高陣列查詢的性能。
    *   **查詢解釋：** 幫助理解查詢的詳細查詢計劃、性能指標和計費指標。
    *   **查詢洞察：** 顯示資料庫上執行的熱門查詢，以評估查詢性能並進行優化。
    *   **Database Center 整合：** 允許使用 Database Center 和 Gemini Cloud Assist 來盤點資料庫，並接收有關如何改進配置（如災難恢復、安全性和合規性）的主動建議。
*   **Symbol Direct 演示：** Patrick Costello 演示了如何在電子商務公司 Symbol Direct 中使用 Firestore。Symbol Direct 使用 Firestore 與 MongoDB 兼容性構建了其店面伺服器，並利用了開發者在 MongoDB 兼容客戶端方面的豐富經驗。
*   **Dialpad 的案例：** Dana Hoffman 分享了 Dialpad 如何使用 Firestore 構建其 AI 驅動的客戶通訊平台。Dialpad 利用 Firestore 實現低延遲、高可用性和自動擴展，以支持其語音、消息和會議服務。Dialpad 的流量模式具有獨特性，每小時的頂部和底部都會出現巨大的流量波動。Firestore 能夠始終如一地以相似的低延遲響應，而不管峰值負載如何。
*   **API 互操作性：** Firestore 將提供 Firestore 與 MongoDB 兼容性、Firestore 原生和 Firestore 與 Datastore 兼容性之間的 API 互操作性。

## 3. 重要結論

Firestore 通過其擴展性、可靠性、開發者生產力以及與 MongoDB 的兼容性，為構建現代應用程式提供了強大的解決方案。Dialpad 的案例證明了 Firestore 在支持大規模、低延遲和高可用性應用程式方面的能力。Firestore 的新功能和成本效益使其成為企業的理想選擇。
