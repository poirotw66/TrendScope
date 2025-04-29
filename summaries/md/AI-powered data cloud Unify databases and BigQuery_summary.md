# AI-powered data cloud Unify databases and BigQuery
[會議影片連結](https://www.youtube.com/watch?v=bGlBratj1-E)
AI 驅動的數據雲統一數據庫和 BigQuery

## 1. 核心觀點

本次演講主要介紹 Mercado Libre 如何運用 Spanner 和 BigQuery 來處理其龐大的數據量，並為開發者提供更好的平台。核心觀點包括：

*   Spanner 的運營簡便性，可自動擴展和縮減節點，無需人工干預。
*   Spanner 與 BigQuery 的整合，以及 Chain Streams 和 Dataflow 的使用，簡化了數據處理流程。
*   Furi 平台作為一個平台即服務（PaaS）解決方案，旨在簡化開發者的工作，讓他們可以專注於構建微服務、訓練機器學習模型和創建 AI 解決方案。

## 2. 詳細內容

Pablo Rojo，Mercado Libre 的 NewSQL 團隊的軟體技術負責人，介紹了該團隊的使命是為數千名開發人員提供大規模、有影響力的分散式 SQL 數據庫。為了實現這個目標，他們採用了 Spanner。

Mercado Libre 是拉丁美洲最大的電子商務、金融科技和物流公司，業務遍及 18 個國家，擁有超過 1 億的活躍用戶。該公司擁有超過 9 萬名員工，每個季度在市場上售出超過 4 億件商品，並處理超過 560 億筆付款。

為了處理如此龐大的業務量，Mercado Libre 依賴於超過 35,000 個微服務，這些微服務運行在四個雲端供應商的 10 萬多台機器上。為了管理如此龐大的基礎設施，他們使用了工程平台 Furi。Furi 是一個建立在雲端供應商之上的平台即服務（PaaS）解決方案。創建 Furi 的動機是為了吸引超過 2 萬名開發人員，解決他們在運行微服務、訓練機器學習模型或創建 AI 解決方案時可能遇到的問題。

選擇 Spanner 的原因是其運營簡便性。Spanner 是一個自我管理的數據庫，採用它可以減少大量手動任務，並降低管理開銷。此外，其擴展能力非常出色，可以透明地、自動地擴展和縮減節點數量，而不會影響生產性能，並避免資源的過度配置。另外，Spanner 與 BigQuery 的簡單整合，加上 Chain Streams 和 Dataflow 等功能，使其成為與 BigQuery 和 Mercado Libre 內部不同技術整合的絕佳產品。

演講中提到了一些技術細節，但由於語音辨識的錯誤，部分內容難以理解，例如 "chwilicorn coolest is an allies could Propagonal on Prevental louder than ihop" 和 "przewerpint"。

## 3. 重要結論

Mercado Libre 透過採用 Spanner 和 BigQuery，以及構建 Furi 平台，成功地處理了其龐大的數據量，並為開發者提供了一個更有效率的開發環境。Spanner 的自動擴展能力和與 BigQuery 的整合，簡化了數據處理流程，並降低了運營成本。
