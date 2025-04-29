# Productionizing OSS agents Best practices for agent frameworks and Vertex AI
[會議影片連結](https://www.youtube.com/watch?v=piz7XImNLfk)
Productionizing OSS agents Best practices for agent frameworks and Vertex AI

## 1. 核心觀點

本次會議主要探討了如何將開源（OSS）代理程式投入生產環境，並分享了代理程式框架和 Vertex AI 的最佳實踐。講者們來自 Google Cloud、Latam Airlines 和 Walmart，分別從不同角度分享了他們在代理程式開發、部署和應用方面的經驗。

核心觀點包括：

*   **代理程式框架選擇：** 選擇合適的框架至關重要，需要考慮工具、記憶體管理、可觀測性、學習曲線等因素。
*   **模型選擇：** 根據代理程式的任務選擇合適的模型，考慮長上下文、多模態等因素。
*   **部署挑戰：** 將代理程式從本地環境部署到生產環境面臨諸多挑戰，包括依賴管理、狀態管理、安全等。
*   **Agent Engine：** Google Cloud 的 Agent Engine 旨在簡化代理程式的部署流程，提供框架無關、可擴展、安全的運行環境。
*   **多代理程式框架：** Walmart 分享了他們使用多代理程式框架解決複雜問題的經驗，強調任務分解、上下文管理和工具支援的重要性。
*   **評估的重要性：** Latam Airlines 強調在代理程式開發過程中進行評估的重要性，並分享了他們使用黃金數據集進行評估的經驗。

## 2. 詳細內容

**Chris Overholt (Google Cloud)：**

*   強調代理程式開發的複雜性，指出框架的選擇會影響到生產環境。
*   Google Cloud 的目標是幫助開發者專注於代理程式邏輯，而不是底層的基礎設施。
*   介紹了 Agent Development Kit (ADK) 以及與 Langchain、AG2、Crew AI 等框架的整合。
*   強調了模型選擇、工具和函數定義、記憶體和狀態管理的重要性。

**Catalina & Matias (Latam Airlines)：**

*   分享了他們開發 AI 旅行規劃助手 Concert 的經驗。
*   Concert 旨在幫助用戶規劃和預訂行程，並提供個性化的推薦。
*   介紹了 Concert 的架構，包括目的地、活動和航班價格工具。
*   分享了他們在使用 LangGraph 框架時遇到的挑戰和學習經驗，包括版本迭代、評估和部署。
*   強調了建立可信賴的黃金數據集的重要性，以便自動評估代理程式的性能。

**Polong (Google Cloud)：**

*   探討了代理程式部署的挑戰，包括依賴管理、狀態管理和安全。
*   介紹了 Agent Engine，旨在簡化代理程式的部署流程，提供框架無關、可擴展、安全的運行環境。
*   Agent Engine 基於 Cloud Run，提供會話管理、可觀測性和其他代理程式特定的功能。
*   Agent Engine 與 Vertex AI 生態系統整合，包括 CICD、監控和評估服務。
*   介紹了使用 Agent Engine 的開發流程，包括本地開發、部署和管理。

**Jason Cho (Walmart)：**

*   分享了 Walmart 從提示工程到多代理程式框架的演進過程。
*   強調了在滿足產品目標、品牌指南和業務 KPI 方面的挑戰。
*   介紹了他們使用 Autogen 框架開發 Evil Town 的經驗，Evil Town 是一個多代理程式框架，旨在解決複雜的任務。
*   Evil Town 包括 Planner Agent、Debate Moderator 和 Arbitrator Agent，用於任務分解、上下文管理和結果評估。
*   分享了 Evil Town 在產品推薦、營銷材料生成和客戶理解方面的應用。
*   強調了任務分解、上下文管理和工具支援的重要性。

## 3. 重要結論

本次會議提供了關於將開源代理程式投入生產環境的寶貴見解。講者們強調了選擇合適的框架、模型和工具的重要性，並分享了他們在部署、評估和應用代理程式方面的經驗。Agent Engine 的推出有望簡化代理程式的部署流程，降低開發者的運營負擔。多代理程式框架為解決複雜問題提供了新的思路，但需要仔細考慮任務分解、上下文管理和協作模式。總體而言，本次會議為希望在生產環境中使用代理程式的開發者提供了有價值的指導。
