# How video game studios use Google Cloud to power gen AI in games
[會議影片連結](https://www.youtube.com/watch?v=NwB_ZpZ67hs)
遊戲工作室如何使用 Google Cloud 來驅動遊戲中的生成式 AI

## 1. 核心觀點

本次會議主要探討了遊戲工作室如何利用 Google Cloud 平台和生成式 AI 技術，來提升遊戲開發效率、改善玩家體驗，並創造更具互動性和沉浸感的「活生生」的遊戲世界。重點包括：

*   生成式 AI 在遊戲開發和遊戲體驗中的應用。
*   Google Cloud for Games 的技術堆疊及其三大支柱。
*   Agonis on GKE 如何簡化遊戲伺服器的運行和擴展。
*   Clang Games 如何利用 Google Cloud 和生成式 AI 打造 MMO 模擬遊戲 Seed。

## 2. 詳細內容

會議首先介紹了遊戲產業的演變，從傳統的單機遊戲到現在的線上即時服務遊戲，開發者面臨著不斷更新內容和提供新體驗的壓力。生成式 AI 被視為解決這一問題的關鍵，它能讓遊戲動態地隨著玩家的體驗而演進，創造出「活生生」的遊戲。

Google Cloud for Games 的技術堆疊包含三大支柱：

1.  **遊戲伺服器：** 提供遊戲運行的基礎設施和應用服務，以更好地吸引玩家。
2.  **託管服務：** 包括 Google Kubernetes Engine (GKE)、Cloud Spanner 和 BigQuery，為玩家提供卓越的遊戲體驗，讓開發者專注於遊戲開發，無需擔心基礎設施。
3.  **生成式 AI：** 結合 Vertex AI 和 GKE，助力開發者構建「活生生」的遊戲。

Google 在 AI 領域擁有深厚的積累，包括 DeepQ、AlphaStar、AlphaGo 等研究成果。最新的 Gemini 模型系列將引領下一代「活生生」的遊戲。Vertex AI 平台提供對 Gemma 和 Gemini 等模型的訪問，並可在 Google Kubernetes Engine 上運行，與遊戲伺服器和後端並行。

生成式 AI 在遊戲中的應用分為兩大類：

1.  **提高遊戲開發效率：** 加速內容創作和簡化開發流程，包括角色、道具、音訊、影片、程式碼生成和 AI 遊戲測試。
2.  **改善玩家遊戲體驗：** 實現智慧 NPC、動態遊戲內容、客製化遊戲玩法和使用者生成內容，創造無限可能的世界。

會議展示了 Countdown Atalante City 遊戲，展示了如何與 NPC 進行即時對話，並根據玩家的要求生成新的服裝。

Agonis on GKE 簡化了遊戲伺服器的運行，可以靈活地擴展遊戲伺服器，並降低營運成本。GKE Autopilot 確保只需為運行的遊戲伺服器 Pod 付費，無需支付系統元件、作業系統開銷或未分配的容量。

會議還展示了 Home Run Gemini Coach Edition 遊戲，其中 Gemini 驅動的教練根據遊戲狀態提供建議。遊戲中的靜態資產由 Imogen 3 生成，動態資產由 VO2 生成。

Clang Games 的 CTO Adur Magnusson 分享了他們如何使用 Google Cloud 和生成式 AI 打造 MMO 模擬遊戲 Seed。Seed 模擬每個 Seedling 的詳細資訊，包括統計數據、需求、目標、關係和願望，這些細節驅動了他們的行為。Seedlings 持續存在於遊戲中，24/7 生活，不受玩家是否在線的影響。

Clang Games 使用 GKE 運行所有後端工作負載，包括使用者管理、支付和核心遊戲伺服器。他們使用 Spot VM 來最大化成本節省，並使用節點自動配置 (NAP) 來優化節點配置。他們還使用 PubSub、Dataflow 和 BigQuery 構建標準的 Google 數據管道，並使用 Vertex AI 進行 AI 模型託管。

Clang Games 將生成式 AI 整合到 Seedlings 的「感知、思考、行動」迴圈中。他們使用 RAG（檢索增強生成）動態生成豐富的、上下文感知的提示，並使用生成式 AI 模組來制定計劃。他們還允許玩家與 Seedlings 進行對話，使 Seedlings 成為完全成熟的遊戲內 AI 代理。

Adur Magnusson 還分享了使用生成式 AI 的一些挑戰，包括將模型紮根於虛構世界、缺乏成熟的提示開發和測試工具，以及需要監控 LLM 請求。他建議避免對所有任務採用一刀切的方法，並優化 Token 以降低成本和延遲。

## 3. 重要結論

遊戲工作室可以利用 Google Cloud 平台和生成式 AI 技術，來提升遊戲開發效率、改善玩家體驗，並創造更具互動性和沉浸感的「活生生」的遊戲世界。Google Cloud for Games 提供了一整套工具和服務，可以幫助遊戲開發者應對各種挑戰和機遇。
