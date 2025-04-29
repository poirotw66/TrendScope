# How BigQuery can help modernize your data platform for the AI era

[會議影片連結](https://www.youtube.com/watch?v=Qa9tw4Zfq5I)
BigQuery 如何協助您將資料平台現代化，以迎接 AI 時代

## 1. 核心觀點

本次會議主要探討資料倉儲和資料湖的現代化，以及 BigQuery 如何協助企業將資料現代化，以迎接人工智慧時代。講者分享了遷移的最佳實踐、常見的陷阱，以及 PayPal 和 Intesa Sanpaolo 的實際遷移案例。同時，也介紹了 Google 在 BigQuery 產品方面的最新發布。

## 2. 詳細內容

**開場與議程**

Osman Ali 首先介紹了講者團隊，包括來自 PayPal 的 Vishali Walia、來自 Intesa Sanpaolo 的 Davide Korda，以及來自 Google 的 Mohit Virindra。議程涵蓋遷移最佳實踐、PayPal 和 Intesa Sanpaolo 的遷移經驗，以及 BigQuery 的產品發布。

**資料現代化的挑戰**

Osman Ali 指出，企業在實現 AI 驅動轉型時，通常會遇到三個主要問題：資料孤島、缺乏 AI 準備，以及成本增加。Google Cloud Autonomous Data and AI Platform 旨在解決這些問題，提供多模型資料基礎、跨資料和 AI 的治理，以及整合的 AI 功能。

**BigQuery 遷移服務**

BigQuery 遷移服務是資料倉儲和資料湖遷移的關鍵服務，包含資料傳輸服務、評估服務、翻譯服務（支援 15 種方言到 BigQuery 方言）和資料驗證服務。該服務的年增長率約為 3 倍。

**遷移策略與原則**

Osman Ali 提出了五個主要原則：

1.  避免一次性的大規模遷移，應分階段進行。
2.  針對不同工作負載，優化 Schema 和程式碼。BigQuery 提供 SQL、ML 和 Spark 引擎，可針對特定工作負載進行優化。
3.  採用現代雲端資料擷取框架，從 ETL 轉向 ELT，將轉換函式庫更靠近業務使用者。
4.  實施 CI/CD，對程式碼和資料進行版本控制。
5.  重視資料治理，確保資料品質，並利用 BigQuery 的存取控制、CMEK 和 AEID 加密等功能。

**PayPal 的遷移故事**

Vishali Walia 分享了 PayPal 將 400PB 的分析資料從分散在多個資料倉儲和資料湖遷移到 BigQuery 的經驗。選擇 BigQuery 的原因是它是一個完全託管的雲原生資料倉儲，具有強大的功能和效能，提供熟悉的 SQL 介面，並整合了 BQML 和 Vertex AI。

PayPal 的遷移策略包括：

1.  企業一致性：將遷移作為企業優先事項。
2.  探索與分析：建立詳細的資料、使用者、工作負載和資料管線清單。
3.  策略：不繼承技術債務，解耦依賴關係，並建立執行軌道。
4.  現代化或遷移：根據具體情況決定是否進行現代化。
5.  培訓：投入大量資源進行培訓。
6.  執行：自動化一切可以自動化的事物，並使用 BigQuery 遷移服務。
7.  優化：在遷移時進行優化。

Vishali 也分享了一些經驗教訓，包括：移動目標難以追蹤、架構審查的重要性、FinOps 不能是事後才考慮的事情，以及資料協調的漫長過程。

遷移到 BigQuery 的影響包括查詢效能大幅提升、資料新鮮度提高、複雜性降低、營運負擔減輕，以及業務能力增強。

**Intesa Sanpaolo 的遷移故事**

Davide Korda 分享了 Intesa Sanpaolo 將其企業資料平台 Data Service Hub 遷移到 BigQuery 的故事。Data Service Hub 是一個複雜的資料生態系統，為公司的所有資料治理和資料使用提供單一的事實來源。

遷移的動機包括可擴展性問題、效能問題，以及對 AI 使用案例的支援不足。Intesa Sanpaolo 透過建立商業案例、進行徹底的測試，並獲得不同利害關係人的支持。

Intesa Sanpaolo 的遷移計畫包括：

1.  保證現有流程不會停止，並且不會出現回歸。
2.  啟動可以立即受益於此關鍵推動因素的新專案。
3.  現代化，嘗試改進技術，而不是僅僅進行遷移。

Davide 強調了團隊合作、規劃的重要性，以及 FinOps 的關鍵作用。

**BigQuery 產品發布**

Mohit Virindra 介紹了 BigQuery 遷移服務的最新發布，包括 Gemini 增強的批次和 API 翻譯、Gemini 支援的翻譯預覽、來源沿襲、評估燈號，以及新的資料遷移連接器。

## 3. 重要結論

本次會議深入探討了資料倉儲和資料湖的現代化，以及 BigQuery 如何協助企業將資料現代化，以迎接人工智慧時代。透過 PayPal 和 Intesa Sanpaolo 的實際案例，與會者可以更深入地了解遷移的策略、挑戰和收益。同時，BigQuery 產品的最新發布也為企業提供了更強大的工具和功能，以簡化遷移過程並實現資料的現代化。
