# From AWS to Google Cloud Expand your cloud toolkit
[會議影片連結](https://www.youtube.com/watch?v=cRK7uInlI94)
從 AWS 到 Google Cloud 擴展您的雲端工具包

## 1. 核心觀點

本次會議主要探討了從 AWS 遷移到 Google Cloud 的相關議題，包括 AWS 和 Google Cloud 的異同、遷移工具和框架，以及實際的遷移示範。核心觀點包括：

*   **AWS 與 Google Cloud 的相似與差異：** 兩者都是全球規模的雲端平台，提供類似的服務和功能，但在資源層級、網路和 IAM 方面存在顯著差異。
*   **結構化的遷移方法：** 強調遷移不僅僅是工具的使用，更需要一個結構化的方法和框架，以降低風險並加速遷移過程。
*   **多樣化的遷移工具：** Google Cloud 提供了多種遷移工具，涵蓋計算、儲存和資料庫等不同領域，可以根據不同的需求選擇合適的工具。
*   **遷移策略的靈活性：** 強調可以針對不同的工作負載採用不同的遷移策略，例如零停機遷移或簡單的遷移。
*   **遷移是多雲環境的機會：** 遷移可以作為建立多雲環境的起點，利用不同雲端平台的優勢。

## 2. 詳細內容

*   **AWS 與 Google Cloud 的比較：**
    *   **相似之處：** 全球規模、多種服務（計算、儲存、資料庫、AI/ML）、Pay-as-you-go 定價、IAM、多種互動介面（Web Console、API、CLI、IaC）。
    *   **差異之處：**
        *   **資源層級：** AWS 使用 Organizations、OUs、Accounts；Google Cloud 使用 Organizations、Folders、Projects。
        *   **網路：** AWS VPC 區域性，Subnet 綁定 AZ；Google Cloud VPC 全球性，Subnet 綁定 Region。
        *   **IAM：** AWS IAM Role 是身份，Google Cloud IAM Role 是權限。
*   **Google Cloud 遷移工具：**
    *   **計算：** Migration Center (評估)、Migrate to VMs (VM 遷移)、Migrate to Containers (VM 轉容器)。
    *   **儲存：** Storage Transfer Service (物件儲存遷移)。
    *   **資料庫：** Database Migration Service (資料庫遷移)。
*   **遷移框架：**
    *   **四個階段：** 評估 (Assessment)、規劃 (Plan)、部署 (Deploy)、最佳化 (Optimize)。
    *   **RAM 計畫：** Google Cloud 合作夥伴主導的遷移計畫，提供結構化的方法和專家支援。
*   **常見的遷移旅程：**
    *   **Amazon S3 to Cloud Storage：** 使用 Storage Transfer Service。
    *   **Amazon EC2 to Compute Engine：** 使用 Migration Center、Migrate to VMs/Containers。
    *   **Amazon EKS to GKE：** 重構 CI/CD 流程，將 Artifact 推送到 Google Cloud Artifact Registry。
    *   **Amazon RDS to Cloud SQL/AlloyDB：** 使用 Database Migration Service，但需注意資料庫引擎的差異。
*   **遷移示範：**
    *   **Symbol Bank 應用程式：** 一個零售銀行應用程式，使用 Python 和 Java 構建，運行在 AWS EKS 上，使用 RDS Postgres 資料庫。
    *   **遷移步驟：**
        1.  使用 Terraform 建立 Google Cloud 資源 (GKE 叢集、Database Migration Service Job)。
        2.  使用 Database Migration Service 將 RDS 資料庫遷移到 Cloud SQL。
        3.  重構 GitHub Actions 工作流程，將容器映像檔構建並推送到 Artifact Registry。
        4.  將應用程式部署到 GKE 叢集。
*   **遷移考量：**
    *   **零停機遷移：** 使用多叢集服務網格或流量工程。
    *   **多雲環境：** 將 AWS 環境用作災難復原環境。
    *   **傳統工作負載：** 使用 Migrate to VMs 和混合子網路遷移，即使工作負載使用硬編碼 IP。

## 3. 重要結論

從 AWS 遷移到 Google Cloud 是一個複雜的過程，需要仔細的規劃和執行。Google Cloud 提供了多種工具和服務來簡化遷移過程，但重要的是要採用結構化的方法，並考慮到特定的需求和限制。遷移也可以作為建立多雲環境的機會，利用不同雲端平台的優勢。
