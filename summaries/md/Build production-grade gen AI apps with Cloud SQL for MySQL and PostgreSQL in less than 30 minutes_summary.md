# Build production-grade gen AI apps with Cloud SQL for MySQL and PostgreSQL in less than 30 minutes

[會議影片連結](https://www.youtube.com/watch?v=UJJM6Yg81pI)
使用 Cloud SQL for MySQL 和 PostgreSQL 在 30 分鐘內構建生產級 Gen AI 應用程式

## 1. 核心觀點

本次會議主要介紹了如何使用 Google Cloud SQL for MySQL 和 PostgreSQL 快速構建生產級的 Gen AI 應用程式。重點涵蓋了應用程式開發的生命週期，以及 Google Cloud 和 Cloud SQL 的最新功能，這些功能旨在簡化 Gen AI 應用程式的構建過程。會議還探討了應用程式的設計和架構、如何使用 Cloud SQL 更快地進行開發，以及 Gen AI 應用程式的運營和管理。此外，Manhattan Associates 分享了他們在 Gen AI 轉型方面的經驗。

## 2. 詳細內容

會議首先概述了 Cloud SQL 在 Google 數據庫產品組合中的定位，強調 Google 的目標是為所有數據庫產品提供最先進的 Gen AI 功能，以及一套強大的應用程式構建工具，確保無論選擇哪種數據庫，都能構建高效能、高擴展性的應用程式。

接著，會議深入探討了 Gen AI 應用程式的設計和架構。Retrieval Augmented Generation (RAG) 是一種流行的技術，但 AI 領域正在快速發展，出現了 AI 代理、Agentic RAG 和多代理系統等新趨勢。這些系統不僅可以生成回應，還可以推理、規劃和調用不同的工具來完成各種目標。Cloud SQL 支援 PostgreSQL 和 MySQL 的向量功能，允許直接從 SQL 查詢中調用 Vertex AI 中託管的 AI 模型，或者來自 OpenAI、Hugging Face 或 Anthropic 等外部平台的 AI 模型。

為了簡化應用程式的設計和部署，Google 推出了一個名為 Application Design Center (ADC) 的新產品。ADC 是一個 Gemini 輔助的可視化設計器，可以顯著簡化應用程式的設計和部署過程。透過 ADC，使用者可以從一個抽象的應用程式想法開始，在幾分鐘內設計和部署應用程式。

在開發方面，Cloud SQL 提供了內建的產品功能，以支援向量儲存和向量搜尋。Cloud SQL for PostgreSQL 支援 PG vector，而 MySQL 也推出了向量儲存和向量搜尋功能。Cloud SQL 還與 Gen AI 生態系統緊密整合，支援 Lama Index、Langchain 和 LangGraph 等流行的應用程式編排框架。此外，MCP Toolbox for Databases 簡化了應用程式與數據庫的連接。

在運營和管理方面，會議強調了效能和擴展性、可用性和災難恢復、以及應用程式健康監控的重要性。Cloud SQL 支援低停機時間的擴展、連接池、讀取池，以及基於 Axion 的機器。此外，Cloud SQL 還支援亞秒級維護、進階災難恢復、最終備份和保留備份等功能。AI 輔助的故障排除功能可以主動發現數據庫中可能發生的異常，並提供根本原因分析和改進建議。

Manhattan Associates 的 Ravi Maganti 分享了他們在 Gen AI 轉型方面的經驗，包括增強使用者體驗、加速上市時間、提高生產力以及改進數據分析和洞察力。他強調了與 Google 的合作關係，以及 Cloud SQL 在提供不間斷覆蓋和快速解決問題方面的優勢。

## 3. 重要結論

本次會議展示了 Google Cloud SQL 如何簡化 Gen AI 應用程式的構建過程，從設計、開發到部署和管理。透過 ADC、向量資料庫支援、與 Gen AI 生態系統的整合以及強大的運營和管理功能，Cloud SQL 幫助開發人員更快、更輕鬆地構建生產級的 Gen AI 應用程式。Manhattan Associates 的案例研究也證明了 Cloud SQL 在實際應用中的價值。
