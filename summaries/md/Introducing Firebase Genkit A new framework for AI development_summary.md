Introducing Firebase Genkit A new framework for AI development

[會議影片連結](https://www.youtube.com/watch?v=YgZIUlYqruQ)
Introducing Firebase Genkit A new framework for AI development

## 1. 核心觀點

GenKit 是一個由 Firebase 團隊開發的開源框架，旨在簡化開發者使用大型語言模型（LLM）的流程。它提供框架、工具和可觀測性，協助開發者構建、測試、調整、偵錯和部署 AI 應用程式。GenKit 支援多種語言（JavaScript、Go 和 Python），並提供統一的模型 API，方便開發者切換和比較不同的模型。此外，GenKit 還提供結構化輸出、函數呼叫、檢索增強生成（RAG）和對話代理等功能，並與多個模型供應商、向量儲存提供商和平台整合。

## 2. 詳細內容

- **GenKit 的主要組成部分：**
    - 開源 SDK（JavaScript、Go、Python）
    - 外掛生態系統（模型、向量儲存、平台整合）
    - 開發者工具（用於迭代、測試和偵錯）

- **開發者體驗：**
    - 易於上手，可在本地機器上運行。
    - 統一的模型 API，支援多種模型供應商（Google AI、Anthropic、Vertex Model Garden、OpenAI 等）。
    - 結構化和類型安全，使用 Zod (Node.js)、Pydantic (Python) 和 Go structs 定義 schema。
    - 函數呼叫，用於構建代理，允許 LLM 決定要呼叫哪些函數。
    - 檢索增強生成（RAG），整合向量儲存提供商（Firestore、Vertex Vector Search、PG Vector、DataStax、AstroDB、Neo4j 等）。
    - 流程（Flows），用於將多個步驟組合成一個可部署的 API 端點。
    - Prompt 管理，使用 .prompt 格式，方便迭代和協作。
    - 對話代理，提供 API 用於儲存和載入對話歷史。

- **平台整合：**
    - 支援多種模型（Gemini、Vertex Model Garden、Ollama 等）。
    - 支援多種向量儲存提供商（Firestore、Vertex Vector Search、PG Vector 等）。
    - 可部署到 Google Cloud Run、GKE、Firebase App Hosting、Cloud Functions for Firebase，以及任何支援 Python、Node.js 或 Go 容器的環境。

- **GenKit 的開源特性：**
    - Apache 2.0 授權，無供應商鎖定。
    - 活躍的社群，可透過 GitHub 和 Discord 參與。

- **示範：**
    - 使用 Python SDK 建立天氣代理，從 .env 檔案讀取 API 金鑰。
    - 使用 GenKit 裝飾器定義工具，並使用 Pydantic 定義 schema。
    - 使用本地開發者 UI 運行和偵錯流程。
    - 使用 Vertex AI 外掛程式和 Google Maps API 整合真實的天氣資料。
    - 使用多代理流程，根據天氣狀況推薦穿著。
    - 使用 Firebase Console 監控和偵錯 GenKit 應用程式。
    - 使用 GenKit by Example 探索更多範例。

## 3. 重要結論

GenKit 是一個功能強大且靈活的框架，可以簡化 AI 應用程式的開發流程。它提供統一的 API、結構化輸出、函數呼叫、RAG 和對話代理等功能，並與多個模型供應商、向量儲存提供商和平台整合。GenKit 的開源特性和活躍的社群使其成為開發者構建 AI 應用程式的理想選擇。
