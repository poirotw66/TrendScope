# Secure from code to cloud with Security Command Center
[會議影片連結](https://www.youtube.com/watch?v=7keYMKlRYPU)
從程式碼到雲端的安全防護，透過 Security Command Center

## 1. 核心觀點

本次會議主要介紹 Gemini Remediation Recommender，這是一個旨在簡化和自動化安全警報修復流程的創新工具。核心觀點包括：

*   Gemini Remediation Recommender 能夠創建包含 IEC 程式碼所需確切變更的 Pull Request。
*   該工具為 DevOps 團隊提供安全背景資訊，以便他們做出充分知情的選擇。
*   透過將執行階段問題映射回其起源的 IEC 程式碼，Gemini Remediation Recommender 將修復工作提前。
*   該工具減少了安全管理員的負擔，並賦予 DevOps 團隊更多權力，同時從根本上解決問題，降低問題再次發生的機率。

## 2. 詳細內容

目前的安全警報管理流程通常包含以下步驟：安全團隊收到大量警報，然後必須確定優先順序，以確定哪些發現需要首先解決。接下來，他們需要分配負責人，以確定誰負責修復哪些發現。由於大多數部署都基於 IEC，因此修復的負責人已轉移到 DevOps 團隊。安全管理員和 DevOps 團隊之間存在大量的協作。安全團隊需要與開發團隊協作，為他們提供足夠的背景資訊。開發團隊理解背景資訊後，必須在其 IEC 程式碼（例如 Terraform）中進行實際的程式碼變更，以修復此發現。對於安全管理員和 DevOps 團隊而言，此流程存在多個痛點。

Gemini Remediation Recommender 透過以下方式運作：首先，它確定修復發現所需的確切程式碼變更。接下來，它為 DevOps 團隊新增安全背景資訊，以便他們做出充分知情的選擇。最後，它將 Pull Request 發送給正確的負責人。

Gemini Remediation Recommender 減少了安全管理員的負擔，因為他們不必擔心中斷、確定所有權以及向開發團隊提供安全背景資訊。它還賦予了開發團隊更多權力，因為他們不需要確定在哪裡修復以及修復什麼。最重要的是，它從根本上解決了問題，降低了同一類型問題再次發生的機率。

在演示中，展示了發現漏斗，其中顯示有 4,000 多個發現，其中 400 個有可用的修復程式。發現清單顯示所有這些發現都有可用的程式碼修復程式。左側有一些新的篩選器，允許您根據修復程式的可用性來篩選發現。目前正在進行的私有預覽啟動解決了所有類型的身份發現，此外還解決了開放防火牆發現。在一個身份發現的詳細資訊中，有一個「產生 PR 並發送以供審閱」按鈕。點擊該按鈕後，會將 Pull Request 排隊以供建立。建立 Pull Request 需要幾分鐘時間。完成後，刷新頁面，會看到所有 Pull Request 詳細資訊現在都已在此處填寫，包括正確的負責人、Pull Request 連結和 PR 產生時間。此時，安全管理員可以導航到詳細資訊部分，以查看將與開發團隊共用的安全背景資訊。他們還可以查看程式碼差異，其中顯示了作為 Pull Request 的一部分提出的程式碼變更。

在 GitHub 中，Pull Request 的標題包含足夠的資訊，供開發人員確定此特定 Pull Request 的審閱優先順序。它表示它是 Gemini 產生的，來自 SCC。它提到了修復特定 ID 的發現、此發現的類別以及嚴重性。它還在 PR 描述中包含足夠的描述和解釋。它討論了此 Pull Request 不會中斷您的環境。對於所有身份發現，都會發送足夠的影響分析，例如特定角色在過去 90 天內未使用，因此接受此 Pull Request 不會破壞您的環境。最後是程式碼變更，這是使用者審閱的內容。

## 3. 重要結論

Gemini Remediation Recommender 透過自動化安全警報的修復流程，顯著提升了雲端環境的安全性。它不僅簡化了安全團隊和 DevOps 團隊的工作流程，更從根本上解決了安全問題，降低了風險。
