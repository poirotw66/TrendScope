```
# Build enterprise observability at petabyte scale
[會議影片連結](https://www.youtube.com/watch?v=7OwH0dNWfro)
構建 Petabyte 級別的企業可觀測性

## 1. 核心觀點

本次會議主要探討了如何在 Google 和客戶的角度，以極大規模構建企業可觀測性。核心觀點包括：

*   Google 內部擁有極大規模的可觀測性系統，能夠處理海量的遙測數據並快速採取行動。
*   OpenTelemetry 正在成為業界標準，提供統一的檢測方式和數據可移植性。
*   將所有遙測數據集中在一個平台上（例如 BigQuery），可以更好地利用 AI 進行分析和洞察。
*   Yahoo 通過採用 Google 的可觀測性套件和 OpenTelemetry，成功地將其大規模的郵件環境遷移到 Google Cloud。
*   在 OpenTelemetry 的部署中，Sidecar 模式和 DaemonSet 模式各有優缺點，應根據具體用例選擇。

## 2. 詳細內容

會議首先介紹了 Google 在可觀測性方面的背景和規模。Google 擁有數十億用戶的業務，需要能夠以極高的速度和規模攝取和處理遙測數據。Google 的數據中心擁有驚人的頻寬，其內部可觀測性系統能夠處理數百萬億的時間序列數據，並以近乎實時的方式處理大量的日誌。

接著，會議強調了 OpenTelemetry 的重要性。OpenTelemetry 正在迅速普及，成為業界標準，它允許開發者使用通用的語義約定和協議進行一次檢測，然後在任何地方使用這些數據。Google 正在重新檢測其後端以支持 OpenTelemetry，並積極參與 OpenTelemetry 社區。

會議還討論了將所有遙測數據集中在一個平台上的好處。通過將日誌、指標和追蹤數據放在一起，可以更容易地使用 AI 進行分析和洞察。BigQuery 是一個可擴展的數據平台，可以處理任何類型的遙測數據，並允許用戶使用 SQL 查詢引擎進行近乎實時的分析。

Yahoo 的 Shariq Anwar 分享了 Yahoo 如何使用 Google 的可觀測性套件和 OpenTelemetry 將其大規模的郵件環境遷移到 Google Cloud。Yahoo Mail 擁有 130 個不同的組件，分佈在全球各地，每分鐘發送約 1.9 億個指標，每天索引 1.5 PB 的數據。Yahoo 選擇了一個中心化的可觀測性模型，以便工程師可以輕鬆地排除故障、響應事件並找到根本原因。

Yahoo 使用 OpenTelemetry Sidecar 模式來收集應用程式日誌和指標。Sidecar 模式允許應用程式擁有自己的自定義配置，並提供隔離和可擴展性。Yahoo 還與 Google 合作開發了新的 Key-Value Pair 提取功能，這使得開發人員可以更輕鬆地將日誌遷移到 GCP。

會議最後強調了 Google 對 OpenTelemetry 的承諾，並介紹了 Google 提供的各種工具和服務，以幫助客戶構建可擴展的可觀測性系統。

## 3. 重要結論

本次會議強調了可觀測性在現代企業中的重要性，並介紹了 Google 和 OpenTelemetry 如何幫助企業構建可擴展的可觀測性系統。通過採用這些技術，企業可以更好地了解其應用程式和基礎架構的性能，並快速排除故障。OpenTelemetry 的普及和 Google 的支持正在推動可觀測性領域的創新，並使企業能夠以更低的成本獲得更好的可觀測性。
```