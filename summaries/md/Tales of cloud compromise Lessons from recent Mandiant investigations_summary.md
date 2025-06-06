# Tales of cloud compromise Lessons from recent Mandiant investigations

[會議影片連結](https://www.youtube.com/watch?v=sXajZd8J1qg)
雲端入侵事件：近期 Mandiant 調查的經驗教訓

## 1. 核心觀點

本次會議主要探討了雲端和混合環境中，威脅行為者如何進行入侵，並從 Mandiant 的實際應對經驗中提取實用教訓，以加強安全性和恢復能力。核心觀點包括：

*   混合基礎設施的普遍性：大多數組織同時運行內部部署和雲端系統，需要將兩者視為一個整體來進行安全管理。
*   攻擊者策略的演變：從簡單的勒索軟體部署轉向多方面的勒索，包括資料竊取和多重施壓。
*   安全計畫的三個層面：人員、流程和技術，成功的攻擊往往是這三個層面系統性失效的結果。
*   機會主義目標：攻擊者主要關注機會，針對擁有敏感資訊的行業，如金融服務、商業和專業服務、高科技、零售和酒店業。
*   快速的攻擊時間：從初始存取到勒索軟體部署的時間窗口非常短，需要快速的檢測和響應。
*   常見的入侵途徑：包括弱身份驗證、資訊竊取惡意軟體、商品後門程式和針對外部可存取系統的漏洞利用。
*   法律和技術響應的重要性：需要建立全面的網路和法律響應策略，包括法律、鑑識和修復。

## 2. 詳細內容

會議首先強調了混合基礎設施的普遍性，指出大多數組織同時運行內部部署和雲端系統。一個具體的例子是，攻擊者可以利用 Active Directory 的漏洞，入侵 EDR 平台，並將其武器化，從而攻擊連接的端點、系統和伺服器。這突顯了需要以整體觀點看待系統、安全和恢復能力，而不是將內部部署和雲端視為獨立的孤島。

接著，會議討論了攻擊者策略的演變，從簡單的勒索軟體部署轉向多方面的勒索。現在，攻擊者會花費大量精力竊取憑證、入侵邊緣或網路設備、進行內部偵察、利用合法的第三方工具、刪除備份以及竊取大量敏感資料。資料竊取是多方面勒索模型的關鍵，攻擊者的籌碼不再僅僅是加密的系統，而是洩露敏感資料的威脅。

會議還介紹了 Mandiant 如何追蹤和分類威脅行為者，分為 APT（高級持續性威脅）、FIN（金融動機威脅）和 UNC（未分類）。

隨後，會議探討了攻擊的主要目標，指出金融服務、商業和專業服務、高科技、零售和酒店業等行業經常面臨更高的攻擊量。然而，攻擊者主要關注機會，針對擁有敏感資訊的組織。

會議強調了攻擊時間的快速性，指出在涉及資料竊取的事件中，從初始存取到部署的中間時間為六天，而在不涉及資料竊取的事件中，中間時間僅為兩天。在近三分之一的案例中，初始存取到部署發生在 48 小時內。

會議還討論了攻擊中常見的模式，包括利用現有資源（Living off the Land）、擴大攻擊面（針對非人類身份和邊緣網路設備）以及利用第三方整合。攻擊者試圖尋找和濫用弱點，如錯誤配置和漏洞。

會議列舉了常見的入侵途徑，包括弱身份驗證、資訊竊取惡意軟體、商品後門程式、針對外部可存取系統的漏洞利用、SIM 卡交換、電話和簡訊社交工程以及惡意搜尋引擎廣告。

會議強調，安全計畫包含人員、流程和技術三個層面，成功的攻擊往往是這三個層面系統性失效的結果。

會議分享了兩個案例研究，一個是混合環境中的入侵，另一個是純雲端環境中的勒索。這些案例研究突顯了安全配置錯誤、響應和遏制不足以及檢測能力不足等常見問題。

會議還討論了全面的網路和法律響應策略，強調了法律、鑑識和修復的重要性。法律團隊需要儘早參與，以識別風險並確保合規性。

最後，會議提供了一些實用的建議，包括建立核心安全、法律和恢復要素之間的交叉點、加強基礎監控、審查法律協議以及建立基於環境的響應和恢復計畫。

## 3. 重要結論

本次會議強調，有效降低整體攻擊面需要多層次的方法，包括有針對性的限制、強化措施、響應行動和跨身份、資源、網路和端點的檢測。此外，還需要法律、安全、IT 和恢復團隊之間的協作，以打破傳統的孤島，建立全面的分層安全框架。透過主動合作、調整政策、共享威脅情報、協調響應工作以及確保整合恢復計畫，組織可以建立真正的網路攻擊恢復能力。
