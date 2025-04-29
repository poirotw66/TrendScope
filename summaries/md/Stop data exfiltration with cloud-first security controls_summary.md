# Stop data exfiltration with cloud-first security controls
[會議影片連結](https://www.youtube.com/watch?v=Qlg5890_Qrk)
使用雲端優先安全控制阻止資料外洩

## 1. 核心觀點

本次會議主要探討了當今安全專業人員面臨的資料外洩風險，並介紹了 Google Cloud Platform (GCP) 提供的工具和技術，以協助組織保護其資料。核心觀點包括：

*   資料外洩的嚴重性與日俱增，造成的損失巨大。
*   釣魚和憑證竊取是主要的攻擊途徑。
*   需要多層次的安全防護，涵蓋資源、身分、網路、應用程式和瀏覽器層。
*   VPC Service Controls (VPC SC) 是 GCP 的獨特功能，可有效防止資料外洩。
*   Identity Threat Detection and Response (ITDR) 結合 Context-Aware Access (CAA) 能夠即時偵測和應對異常使用者行為。
*   採用縱深防禦策略，結合多種安全控制，才能有效保護資料。

## 2. 詳細內容

會議首先強調了資料外洩的數位急迫性，並列舉了驚人的統計數據，例如 2024 年有 168 億條記錄被盜，資料外洩造成的損失高達 3.4 兆美元。此外，去年發送了 34 億封釣魚郵件，平均偵測和控制一次資料外洩需要 292 天，而資料外洩的平均成本為 936 萬美元。

接著，會議深入探討了資料外洩的解剖結構，包括初始攻擊向量、橫向移動、權限提升和資料外洩等階段。其中，釣魚和憑證竊取是主要的初始攻擊向量，約佔所有攻擊的 55%。

為了應對這些威脅，GCP 提供了多層次的安全防護，涵蓋以下幾個層面：

*   **資源層：** IAM 和組織政策。
*   **身分層：** Context-Aware Access (CAA) 和 Principle Access Boundary (PAB)。
*   **應用程式層：** Cloud Armor 和 Identity-Aware Proxy (IAP)。
*   **網路層：** VPC Service Controls (VPC SC) 和組織限制。
*   **瀏覽器層：** Chrome Enterprise Premium。

會議重點介紹了 VPC SC，這是一項獨特的功能，可透過在 Google 管理的服務周圍建立邊界來降低資料外洩風險。這些邊界可確保邊界內的資源可以相互通信，並阻止跨邊界的所有存取。

此外，會議還宣布推出 ITDR，這是一項結合 CAA 的新功能，可讓組織根據風險狀況設定存取條件，例如來自惡意 IP 的存取、非典型位置的存取或可疑行為。如果使用者會話被認為有風險，ITDR 可以自動採取預定的動作，例如要求 MFA、拒絕存取或強制重新驗證。

會議還邀請了 Deutsche Börse 的 CISO Christian，分享了該組織如何使用 GCP 的工具和技術來保護其資料。Christian 強調了在多個法律實體和複雜的監管環境中控制資料流的挑戰，並介紹了如何使用 PAB 和 VPC SC 來建立零信任架構，確保只有經過授權的使用者才能存取特定的資源。

Christian 還介紹了一種名為 "Atoma Zero Trust Segmentation" 的安全架構，該架構使用 VPC SC 參數來包裝每個專案，並使用 ingress 和 egress 規則來控制專案之間的資料交換。此外，他還介紹了一種名為 "dataflow registry" 的內部產品，該產品可追蹤所有 ingress 和 egress 規則，並提供組織內部通信流程的透明視圖。

## 3. 重要結論

資料外洩是一個日益嚴重的問題，需要多層次的安全防護。GCP 提供了廣泛的工具和技術，可協助組織保護其資料，包括 IAM、組織政策、CAA、PAB、VPC SC 和 ITDR。採用縱深防禦策略，結合這些安全控制，才能有效降低資料外洩的風險。此外，建立零信任架構，確保只有經過授權的使用者才能存取特定的資源，也是至關重要的。
