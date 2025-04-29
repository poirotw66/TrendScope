# Master serverless gen AI with Gemini and Cloud Run
[會議影片連結](https://www.youtube.com/watch?v=SY6CkVcMNzs)
Master serverless gen AI with Gemini and Cloud Run

## 1. 核心觀點

本次會議主要探討如何結合 Gemini、Gemini Code Assist 和 Cloud Run，在整個軟體開發生命週期中構建生成式 AI 應用。核心觀點包括：

*   **設計與編碼：** 利用 Gemini Code Assist 加速應用開發。
*   **RAG 系統：** 強調資料攝取的重要性，包括資料分塊、元資料添加和選擇合適的嵌入模型。
*   **安全：** 強調在建構和部署階段，安全軟體供應鏈的重要性，例如使用多階段建構、Google 管理的基礎映像檔和漏洞掃描。
*   **可觀測性：** 強調建立服務等級目標（SLO），並利用 Cloud Trace 和 Cloud Run 的監控儀表板進行效能分析和問題檢測。
*   **GPU 加速：** 介紹 Cloud Run GPU 的使用，以及如何利用它來託管影像生成模型。

## 2. 詳細內容

會議涵蓋了軟體開發的各個階段，從設計、編碼、測試到建構、部署、營運和最佳化。

**設計與編碼：**

*   介紹了生成式 AI 應用程式的典型架構，包括客戶端、核心模型推論和 RAG 系統。
*   深入探討了 RAG 系統的資料攝取流程，包括資料分塊、添加元資料和選擇合適的嵌入模型。
*   展示了如何使用 Gemini Code Assist 自動產生程式碼、單元測試和 Dockerfile。

**建構與部署：**

*   強調了安全軟體供應鏈的重要性，包括使用多階段建構、Google 管理的基礎映像檔、漏洞掃描和二進位授權。
*   展示了如何使用 `gcloud run deploy` 命令，一鍵完成 Docker 映像檔的建構、推送和部署。

**營運與最佳化：**

*   強調了可觀測性的重要性，包括建立服務等級目標（SLO），並利用 Cloud Trace 和 Cloud Run 的監控儀表板進行效能分析和問題檢測。
*   介紹了 Cloud Run 的自動擴展功能，以及如何調整容器 CPU 大小和並行設定，以實現平穩快速的自動擴展。
*   展示了如何使用 Cloud Load Balancer 將 Cloud Run 服務部署到多個區域，以實現高可用性。

**Cloud Run GPU：**

*   介紹了 Cloud Run GPU 的使用，以及如何利用它來託管影像生成模型。
*   討論了使用 Cloud Run GPU 時的一些關鍵考量，包括選擇穩健的基礎映像檔、配置啟動探針和優化模型載入方式。
*   比較了不同的模型載入方式，包括從網際網路下載、將模型建構到容器映像檔中和從 Google Cloud Storage 載入。

**客戶案例：**

*   Cafe Financial 分享了他們如何使用 Gemini 和 Cloud Run，從法庭案件中生成信用風險報告。
*   他們使用 Google Composer 協調自動攝取法庭案件文件，並使用 Gemini 提取關鍵資料點。
*   他們選擇 Cloud Run 來部署自己的自訂模型，並使用 Vertex AI 快速建構 Gemini 模型。

## 3. 重要結論

Gemini 和 Cloud Run 是一個強大的組合，可以幫助開發人員在整個軟體開發生命週期中構建生成式 AI 應用程式。Cloud Run 提供了靈活、可擴展且安全的平台，用於託管 AI 模型和應用程式，而 Gemini 則提供了強大的 AI 功能和程式碼輔助工具。透過結合這兩種技術，開發人員可以更快、更輕鬆地構建和部署創新的 AI 解決方案。
