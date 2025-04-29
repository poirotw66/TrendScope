# What’s new with Cloud Storage
[會議影片連結](https://www.youtube.com/watch?v=owvXIIl8LdU)
雲端儲存新知

## 1. 核心觀點

本次會議主要介紹 Google Cloud Storage 在 AI 時代下的最新發展與功能，涵蓋高效能儲存、AI 驅動的儲存智慧、以及簡化雲端遷移的解決方案。核心觀點包括：

- **AI 需求推動儲存創新：** AI 工作負載需要更高的吞吐量、更低的延遲和並行處理能力，促使 Google Cloud Storage 不斷創新。
- **高效能儲存解決方案：** 推出 Rapid Storage 和 Managed Lustre 等產品，滿足 AI 和資料湖分析對速度和規模的需求。
- **儲存智慧提升管理效率：** 利用 AI 自動化儲存管理，提供更深入的資料洞察和簡化的操作流程。
- **簡化雲端遷移：** 提供 Google Cloud NetApp Volumes 等解決方案，協助企業輕鬆將檔案資料遷移至雲端。
- **資料保護與備份：** 推出中央備份服務，提供跨多種工作負載的一致性備份和勒索軟體防護。

## 2. 詳細內容

**AI 與資料湖**

- **Rapid Storage：**
    - 一種低延遲、高吞吐量、高 QPS 的雲端儲存服務，專為加速 AI 工作負載而設計。
    - 基於 Google 內部的 Colossus 分散式檔案系統，提供接近區塊儲存的效能。
    - 隨機讀取延遲低於 1 毫秒，吞吐量高達 6 TB/s，IOPS 幾乎無限。
    - 與現有 Cloud Storage 功能無縫整合。

- **Managed Lustre (與 DDN 合作)：**
    - 一種可擴展的 POSIX 共用平行檔案系統，適用於高效能運算、AI 和大數據分析。
    - 可掛載到 Google Compute Engine 或 GKE 上的數千個運算系統。
    - 容量可從數 TB 擴展到 1 PB，效能高達 1 TB/s。
    - 適用於大規模資料分析、AI 模型訓練和推論。

**儲存智慧**

- **Storage Intelligence (正式發布)：**
    - 利用 AI 提供企業資料的全面視圖，包括資料分佈、中繼資料和安全性。
    - 協助使用者理解資料、管理成本和提高安全性。
    - 具備自動註解功能，可自動產生資料的意義和安全性設定。
    - 與 Gemini 整合，可透過自然語言查詢執行複雜的儲存操作。

**資料湖分析**

- **Anywhere Cache (正式發布)：**
    - 一種 SSD 快取服務，可將資料儲存在靠近運算資源的位置，降低延遲並提高效能。
    - 與 Cloud Storage API 完全整合，無需修改應用程式。
    - 可減少高達 70% 的延遲，尤其是在尾部延遲方面。
    - 僅對儲存在快取中的位元組收費，節省傳輸成本。
    - 提供建議引擎，協助使用者判斷是否適合使用 Anywhere Cache。

**雲端遷移**

- **Google Cloud NetApp Volumes：**
    - 一種與 NetApp 合作提供的第一方服務，協助企業將工作負載快速遷移至雲端。
    - 提供無縫遷移、成本優化和高效能。
    - 支援使用 SnapMirror 從內部部署環境遷移到雲端。
    - 提供 Vertex AI 連接器，允許 AI 模型直接存取 NetApp Volumes 中的資料。

- **Filestore：**
    - 一種雲端原生檔案系統，與 GKE 和 GCE 緊密整合。
    - 允許使用者自訂效能和容量，獨立選擇 IOPS (4,000 到 750,000) 和容量 (1 到 100 TB)。
    - 可根據需求獨立擴展效能和容量，優化總體擁有成本 (TCO)。

**資料保護與備份**

- **中央備份服務：**
    - 提供跨多種工作負載 (包括 Compute VM、VMware 和 Cloud SQL) 的一致性備份。
    - 提供集成的體驗、集中管理和可見性。
    - 提供勒索軟體防護，確保備份資料的不可變性。
    - 與 Google Cloud Console 完全整合。

## 3. 重要結論

Google Cloud Storage 持續創新，推出多項新功能和服務，以滿足 AI 時代對儲存的需求。Rapid Storage、Managed Lustre 和 Anywhere Cache 等產品提供高效能的儲存解決方案，Storage Intelligence 簡化儲存管理，Google Cloud NetApp Volumes 和 Filestore 協助企業輕鬆遷移至雲端，中央備份服務則提供全面的資料保護。這些創新使 Google Cloud Storage 成為企業在 AI 時代的理想儲存平台。
