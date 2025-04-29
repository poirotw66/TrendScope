# Master OpenTelemetry Scale and streamline observability pipelines
[會議影片連結](https://www.youtube.com/watch?v=F9NtBWCL3L0)
Master OpenTelemetry 規模化與簡化可觀測性管線

## 1. 核心觀點

本次會議主要討論了 OpenTelemetry (OTEL) 的規模化應用，以及如何利用 OTEL 簡化可觀測性管線。重點包括：

*   **OTEL 的重要性與普及性：** OTEL 已成為業界標準，用於生成、收集和匯出遙測數據，並在 CNCF 基金會中活躍度排名第二。
*   **OTEL 在遙測生命週期中的角色：** OTEL 涵蓋生成、收集和匯入階段，但不涉及儲存和消費，但其數據模型和規範有助於後續階段的工具更好地利用數據。
*   **OTEL Collector 的規模化：** 透過代理 (Agent) 和閘道 (Gateway) 架構，可以有效地擴展 OTEL Collector 的處理能力，應對高流量場景。
*   **Google Cloud 對 OTEL 的支持：** Google Cloud 全面擁抱 OTEL，提供原生 OTLP 端點、GKE 專用配置，並與 Cloud Trace 等服務深度整合。
*   **BindPlane 的作用：** BindPlane 是一個用於管理 OTEL 的平台，可以簡化配置、路由數據、標準化遙測數據，並提供免費的 Google Cloud 版本。

## 2. 詳細內容

*   **OTEL 的背景與現狀：**
    *   OTEL 是一個 CNCF 旗下的開源專案，旨在提供標準化的遙測數據解決方案。
    *   OTEL 擁有超過 1700 位作者，是 CNCF 中活躍度第二高的專案。
    *   超過 300 家組織為 OTEL 貢獻了至少 50 次程式碼。
*   **OTEL 在遙測生命週期中的作用：**
    *   **生成 (Generation)：** OTEL 提供 SDK 和自動檢測函式庫，用於生成應用程式和基礎設施的遙測數據。
    *   **收集 (Collection)：** OTEL Collector 用於收集、豐富和傳輸遙測數據。Google Cloud 中超過 50% 的追蹤數據來自 OTEL Collector。
    *   **匯入 (Ingestion)：** OTEL 定義了 OTLP 協議，用於傳輸遙測數據。Google Cloud 提供 telemetry.googleapis.com 端點，支援原生 OTLP 匯入。
    *   **路由 (Routing)、儲存 (Storage) 和消費 (Consumption)：** OTEL 不直接參與這些階段，但其數據模型和規範有助於相關工具更好地利用數據。
*   **OTEL 的發展方向：**
    *   OTEL Collector 正在努力達到 1.0 版本，以提供更高的穩定性。
    *   Prometheus 和 OTEL 社群正在合作，提高互操作性。
    *   Go 語言的自動檢測功能正在開發中。
    *   Profiling 正在成為 OTEL 的一個新的訊號類型。
*   **OTEL 在 Google Cloud 中的應用：**
    *   Google Cloud 推出 Vertex AI 和 Google Gen AI SDK 的函式庫，支援 OTEL。
    *   Google Cloud 提供 OTEL Operator，簡化 GKE 叢集中的自動檢測和收集。
    *   Google Cloud 提供 Google 構建的 OTEL Collector，為受監管的客戶提供安全的軟體供應鏈。
    *   Cloud Trace 使用 OTEL 數據模型，並優化使用者體驗。
    *   Google Cloud 的可觀測性分析 UI 支援基於 SQL 的查詢，可以利用 OTEL 數據模型和規範。
*   **BindPlane 的作用：**
    *   BindPlane 是一個用於管理 OTEL 的平台，可以簡化配置、路由數據、標準化遙測數據。
    *   BindPlane 支援 OpAmp 協議，用於遠端管理代理程式。
    *   BindPlane 提供視覺化的介面，用於模擬和測試配置變更。
    *   BindPlane 提供免費的 Google Cloud 版本。
*   **規模化 OTEL 的最佳實踐：**
    *   使用代理 (Agent) 和閘道 (Gateway) 架構。
    *   根據應用程式、團隊或遙測類型分離數據流。
    *   儘早減少和過濾數據。
    *   儘量減少在代理程式端進行的處理。
    *   在閘道端使用快取和持久佇列。
    *   利用 OTEL Collector 提供的 Prometheus 指標進行監控和擴展。

## 3. 重要結論

OpenTelemetry 正在成為可觀測性領域的標準，Google Cloud 正在積極擁抱 OTEL，並提供各種工具和服務來簡化 OTEL 的部署和管理。透過採用 OTEL 和 BindPlane 等工具，企業可以有效地擴展可觀測性管線，並獲得更深入的洞察力。
