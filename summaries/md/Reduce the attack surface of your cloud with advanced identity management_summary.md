# Reduce the attack surface of your cloud with advanced identity management
[會議影片連結](https://www.youtube.com/watch?v=6esZV_aN9Rg)
透過進階身分識別管理減少雲端攻擊面

## 1. 核心觀點

本次會議主要探討如何利用 Google Cloud 的 Security Command Center 和 Cloud Infrastructure Entitlement Management (CIEM) 解決方案，主動管理身分識別風險，並實施最小權限原則。重點在於解決多雲環境下，管理非人類身分識別和複雜權限系統所帶來的挑戰，以降低組織暴露於惡意攻擊的風險。

## 2. 詳細內容

講者 Bharat Sivaraman 首先強調了最小權限原則的重要性，指出若未遵循此原則，組織將暴露於潛在的攻擊風險中。然而，在多雲環境下，管理各種權限系統變得越來越複雜。每個雲端供應商都有其獨特的權限管理方式，加上非人類身分識別的激增，使得安全團隊難以全面了解身分識別的使用情況以及不當權限管理所帶來的風險。

為了解決這些挑戰，Google Cloud 推出了 Cloud Infrastructure Entitlement Management (CIEM) 功能，它提供以下功能：

*   **全面可見性：** 深入了解雲端基礎架構、應用程式和資料中所有身分識別及其擁有的權限。
*   **風險洞察：** 透過分析授予各種身分識別的權限與實際使用的權限，提供不當權限管理所導致的漏洞風險洞察。
*   **風險優先排序：** 根據權限範圍評估每個風險的嚴重程度，協助優先處理最重要的風險。

CIEM 能夠識別過度授權的情況，並根據嚴重程度進行分類。它還提供修復建議，目前支援 Google Cloud、Amazon Web Services，並在 Microsoft Azure 上推出預覽版。

會議中展示了 CIEM 在 Azure 環境中的實際應用。透過 Security Command Center，使用者可以查看 Google Cloud 和 Azure 的 CIEM 發現結果，並根據類別和嚴重程度進行組織。點擊特定發現結果，可以查看有關未使用權限的詳細資訊，並獲得建立新的 Azure 角色定義的建議，該角色定義僅包含使用者實際需要的權限。JSON 標籤提供了建立自訂角色所需的所有資訊。解決問題後，發現結果將自動消失，使用者也可以手動停用發現結果。

## 3. 重要結論

透過 Google Cloud 的 Security Command Center 和 Cloud Infrastructure Entitlement Management (CIEM) 解決方案，組織可以更有效地管理雲端環境中的身分識別和權限，降低攻擊面，並確保遵循最小權限原則。CIEM 提供的全面可見性、風險洞察和風險優先排序功能，有助於安全團隊主動識別和修復不當權限管理所導致的漏洞，從而提升整體雲端安全態勢。
