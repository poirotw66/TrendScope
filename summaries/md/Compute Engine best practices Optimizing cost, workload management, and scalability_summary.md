Compute Engine best practices Optimizing cost, workload management, and scalability

[會議影片連結](https://www.youtube.com/watch?v=u3aLFageNzQ)
Compute Engine 最佳實務：最佳化成本、工作負載管理和可擴展性

## 1. 核心觀點

本次會議主要介紹了 Google Compute Engine 的最佳實務，旨在幫助客戶應對在成本管理、效能優化、可靠性保障以及新功能應用等方面遇到的常見挑戰。會議將應用程式分為三種類型：AI/ML 和高效能運算、雲原生應用程式和傳統應用程式，並針對每種類型提供不同的最佳實務建議。

## 2. 詳細內容

針對 AI/ML 工作負載，會議推薦使用 AI Hypercomputer，它是一個整合的工具套件，可以存取運行 AI 工作負載所需的所有必要工具。會議展示了動態工作負載排程器 (Dynamic Workload Scheduler, DWS) 的演示，該排程器可用於建立具有 NVIDIA GPU 的虛擬機器。DWS 提供對時間有限的專用 GPU 容量的存取。使用者只需提供所需的容量和時間，系統就會在容量可用時立即啟動。

對於雲原生應用程式，會議建議使用受管理執行個體群組 (Managed Instance Group, MIG)，這是管理大量 VM 的最佳方式，可以實現高可用性、可擴展性，並且可以在生產環境中更新應用程式。MIG 現在允許配置多種類型的執行個體，以便在不同類型的硬體上尋找容量。會議展示了如何將現有的已配置虛擬機器應用程式轉換為具有所有這些優勢的可擴展群組。

對於傳統應用程式，會議介紹了 VM Manager，它提供了一種更新 Windows 和 Linux 作業系統的方法。VM Manager 允許以適用於所有機器的方式修補機器。此外，OS Policy 提供所需的狀態配置，以確保所有 VM 都是安全可靠的。

## 3. 重要結論

無論在 Google Cloud 上運行何種類型的工作負載，都有相應的解決方案。會議鼓勵使用者探索這些解決方案，以最佳化成本、管理工作負載並提高可擴展性。
