# One network Reimagine service assembly and compliance in a multicloud world
[會議影片連結](https://www.youtube.com/watch?v=upPo50w7Tks)
One network 重新構想多雲環境中的服務組裝與合規性

## 1. 核心觀點

本次會議主要介紹了 One Network 的概念，這是一種在多個應用程式之間統一應用服務和策略的方法，旨在解決組織中應用程式孤島化、運行環境異質化導致的複雜性和創新阻礙問題。One Network 是一種架構方法，而非單一產品，它可以在所有運算平台、環境和路徑上運行，並允許在網路層整合服務，以及在整個組織中統一執行策略，而無需對應用程式進行大規模重構。

## 2. 詳細內容

One Network 的架構包含兩個關鍵組件：一個代理（Proxy）和一個控制平面（Control Plane）。

*   **代理（Proxy）：** 作為應用程式資料平面中的通用構建模組。Google Cloud 使用開源的 Envoy 代理，它原生內建於 Google Cloud 的網路產品中，例如負載平衡器、服務網格和 GKE 閘道等。透過使用 Envoy Sidecar 或 gRPC 服務網格，客戶可以將 One Network 的功能擴展到本地部署、其他雲端，甚至是行動裝置，從而在組織內的服務之間延伸 One Network。

*   **控制平面（Control Plane）：** Google Cloud 內部使用 Traffic Director，它支援 XDS API。這個通用控制平面在 Google 產品之間一致地交付配置。此外，可以使用 Cloud Service Mesh 或開源的 XDS 相容產品，以在 Google Cloud 和其他環境中啟用統一的控制平面。

部署 One Network 的步驟包括：

1.  識別要應用統一策略或插入新可重用服務的相關路徑。
2.  識別要啟用 One Network 功能的基礎設施組件，例如雲端負載平衡器、服務網格、GKE 閘道和出口代理等。
3.  一旦這些組件到位並啟用了像 Envoy 這樣的通用代理，就可以在整個組織中統一協調策略。

Envoy 代理的一個強大功能是支援使用 Xproc 篩選器進行擴展。這些篩選器可以在資料路徑中執行自訂邏輯。Google Cloud 透過負載平衡器和 CDN 中提供的服務擴展功能啟用了這些功能，並且將在更多網路組件中提供。透過 Envoy 篩選器和服務擴展，網路成為應用程式層的延伸，任何服務都可以在資料路徑中運行並整合到應用程式中，包括通用可觀測性工具、多變數測試工具、DLP 和 AI 安全產品等。

會議中舉例說明，當特定區域的工作負載發生故障時，可以使用 One Network 一致地將流量從該區域轉移到另一個區域。每個符合 One Network 標準的組件都將以一致的方式執行，以將流量從故障區域轉移出去。

## 3. 重要結論

One Network 是一種架構方法，它將功能轉移到網路中，以在不同環境中啟用通用策略和服務整合。Google Cloud 的網路原生內建了 One Network 功能，並且可以使用像 Envoy 或 gRPC 這樣的開源專案來擴展它。評估 One Network 是否對組織有益的步驟包括：評估可以從這種方法中獲得哪些好處，選擇最適合組織的工具，以及進行規劃和承諾，因為實現 One Network 是一個迭代的過程。
