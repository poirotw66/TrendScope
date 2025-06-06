# How Shopify runs their biggest business event of the year with GKE
[會議影片連結](https://www.youtube.com/watch?v=1RSgI4kwfOY)
How Shopify 使用 GKE 運行其年度最大商業活動

## 1. 核心觀點

本次會議主要探討 Shopify 如何利用 Google Kubernetes Engine (GKE) 及其新功能（如自定義運算類別）來應對其年度最大流量高峰期，即黑色星期五和網路星期一 (BFCM)。核心觀點包括：

*   **GKE 的重要性：** GKE 在 Shopify 應對 BFCM 期間的大規模流量方面扮演關鍵角色，提供所需的效能、可擴展性和可用性。
*   **自定義運算類別的優勢：** 自定義運算類別讓 Shopify 能夠根據不同區域的運算資源可用性，靈活地調整其應用程式的運算資源配置，從而優化效能和成本。
*   **自動化和簡化：** GKE 和自定義運算類別有助於簡化運營複雜性，使 Shopify 能夠更有效地服務客戶。
*   **持續創新：** Shopify 不斷探索和採用 GKE 的新功能，以改進其基礎設施並提升使用者體驗。
*   **近乎即時的運算能力：** GKE 的最新進展，例如容器優化的運算，可實現更快的 Pod 排程和更低的延遲。

## 2. 詳細內容

*   **BFCM 的規模和重要性：** BFCM 是 Shopify 年度流量最高的時期，需要提前數月進行準備和大規模測試。Shopify 會公開分享 BFCM 的相關數據，例如每分鐘的請求數 (RPM)。
*   **BFCM 地圖：** Shopify 創建了一個名為 BFCM 地圖的 3D 可視化工具，以即時顯示全球的銷售數據，讓團隊能夠監控銷售情況並確保系統正常運行。
*   **全球基礎設施：** Shopify 在全球多個區域運行 GKE，旨在儘可能地靠近使用者提供服務，並根據成本、效能和延遲等因素不斷評估和調整區域部署。
*   **自定義運算類別的使用案例：**
    *   **運算資源可用性：** Shopify 使用自定義運算類別來應對不同區域中運算資源的可用性問題，例如在首選區域的資源不可用時，自動將工作負載轉移到其他區域。
    *   **機器類型選擇：** Shopify 根據不同區域的可用性和效能需求，使用自定義運算類別來選擇不同的機器類型，例如在某些區域使用 N4 機器，而在其他區域使用 N2 機器。
    *   **GPU 資源管理：** Shopify 使用自定義運算類別來管理 GPU 資源，特別是在機器學習工作負載中，以便在升級叢集時能夠平滑地遷移應用程式。
*   **GKE 的最新進展：**
    *   **容器優化的運算：** GKE 推出了新的容器優化的運算，可顯著加快 Pod 排程速度，並降低應用程式延遲。
    *   **叢集自動調整程式：** GKE 的叢集自動調整程式已得到改進，可支援多達 500 個節點池，並更快地排程 Pod。
    *   **水平 Pod 自動調整程式：** GKE 的水平 Pod 自動調整程式 (HPA) 已得到改進，可更快地調整 Pod 數量，並提供更高的可靠性。
    *   **垂直 Pod 自動調整程式：** GKE 的垂直 Pod 自動調整程式 (VPA) 可自動調整 Pod 的資源請求和限制，從而優化資源利用率。
    *   **映像檔串流：** GKE 支援映像檔串流，可加快大型映像檔的啟動速度。
    *   **自定義指標：** GKE 正在改進其自定義指標堆疊，以便提供更精確的水平 Pod 自動調整。
    *   **嵌入式監控儀表板：** GKE 提供了新的嵌入式監控儀表板，可讓使用者輕鬆地監控叢集的效能和健康狀況。

## 3. 重要結論

Shopify 成功地利用 GKE 及其新功能來應對 BFCM 期間的大規模流量，並優化其基礎設施的效能和成本。自定義運算類別和 GKE 的最新進展為 Shopify 提供了更大的靈活性、自動化和可擴展性，使其能夠更好地服務客戶。本次會議強調了 GKE 在支援大規模、關鍵業務應用程式方面的重要性，並展示了 Shopify 如何透過不斷創新來提升其基礎設施和使用者體驗。
