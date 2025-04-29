Secure your cloud posture with built-in policy management platform

[會議影片連結](https://www.youtube.com/watch?v=ay-Di_WEP5A)
使用內建策略管理平台保護您的雲端安全

## 1. 核心觀點

本次會議主要介紹 Google Cloud 的內建策略管理功能，重點在於如何利用組織政策（Organization Policy）來確保雲端資源的安全與合規性，同時不影響開發者的效率。核心觀點包括：

*   組織政策是資源導向的治理控制，可確保環境中不存在不合規的資源。
*   Managed Constraints 和 Custom Org Policies 提供彈性和靈活性，以滿足不同的需求。
*   Google Cloud Security Baseline 提供預設啟用的安全控制，作為強大的基礎。
*   SafeRollR 工具（Simulator 和 DryRun）可安全地推出策略變更。

## 2. 詳細內容

會議首先強調了企業在擴展雲端足跡時面臨的兩個主要挑戰：確保組織滿足安全和合規性目標，以及在不影響開發者速度的情況下實現這些目標。Google Cloud 的 IAM 平台提供內建功能，允許管理員建立防護措施，使開發人員能夠在安全和合規性範圍內加速應用程式開發和創新。

組織政策（Org Policies）是一種資源導向的控制層，允許您控制組織中允許的資源配置。Constraints 是您想要強制執行的限制或規則，Google 提供內建和可自訂的防護措施。

Managed Constraints 是組織政策平台的一個進化，允許您使用 Simulator 和 DryRun 等工具來了解策略變更的影響。Custom Org Policies 提供靈活性和敏捷性，目前支援超過 60 種 Google Cloud 產品。

會議還分享了 Snap 如何利用這些控制來實現其目標的案例，包括使用網域限制共用組織政策來保護組織邊界的安全，使用服務帳戶金鑰組織政策和服務帳戶許可權政策來限制使用者服務帳戶金鑰，以及使用 Uniform Bucket Level Access 組織政策來解決 GCS 存取控制清單的問題。

Google Cloud Security Baseline 提供了六個 Google 定義的組織政策，這些政策是預設啟用的安全控制，可作為強大的基礎。這些控制側重於保護長期存在的憑證、保護組織存取以及加強網路安全。

## 3. 重要結論

本次會議強調了組織政策在確保雲端資源安全和合規性方面的重要性。透過使用 Managed Constraints、Custom Org Policies 和 Google Cloud Security Baseline，組織可以建立強大的安全態勢，同時保持開發者的效率。SafeRollR 工具可安全地推出策略變更，進一步降低風險。Google 鼓勵使用者加強其態勢，並利用 Google 的智慧建議來超越現狀。
