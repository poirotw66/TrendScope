# A master class in managing billions of Google Cloud storage objects and beyond
[會議影片連結](https://www.youtube.com/watch?v=eosO6EwNyxI)
Google Cloud Storage 物件管理大師班：管理數十億個物件及更多

## 1. 核心觀點

本次會議主要介紹了 Google Cloud Storage 的物件管理，特別是在大規模場景下的挑戰與解決方案。核心觀點包括：

*   儲存空間持續增長，尤其是在 AI 時代，新的訓練資料和 AI 生成內容不斷湧現。
*   物件儲存的規模龐大，管理困難，許多客戶擁有數千萬、數十億甚至數兆個物件。
*   自行開發儲存管理工具既困難又耗時，需要投入大量精力。
*   Google 推出了統一的儲存管理產品 Storage Intelligence，旨在幫助客戶解決儲存管理難題，讓他們能夠專注於更重要的業務問題。
*   Storage Intelligence 提供分析儲存狀態和大規模執行操作的功能，例如物件鎖定、儲存桶遷移和加密金鑰更新。

## 2. 詳細內容

會議首先闡述了儲存管理的重要性，指出儲存空間的持續增長、物件儲存的龐大規模以及自行開發工具的困難是客戶面臨的主要挑戰。客戶通常將 13% 到 24% 的雲端支出用於儲存管理和運營。

為了解決這些問題，Google 推出了 Storage Intelligence，這是一個統一的儲存管理產品，提供以下功能：

*   **分析儲存狀態：** 透過分析，可以了解儲存成本的驅動因素，例如按字首分析儲存分佈，找出快速增長的區域。
*   **大規模執行操作：** 可以對數百萬個物件執行操作，例如移動儲存桶以實現災難恢復或降低出口成本，或者更新加密金鑰。
*   **簡化儲存管理：** Storage Intelligence 提供端到端的管理流程，幫助客戶擺脫手動儲存管理，節省時間並專注於業務。

會議還介紹了 Storage Intelligence 的六種使用方式，包括：

1.  使用 insights data sets 功能了解儲存成本。
2.  使用儲存桶重新定位功能移動儲存桶。
3.  使用 patch operations 功能更新加密金鑰。

patch operations 功能可以在幾個小時內對數十億個物件執行操作，而無需編寫任何程式碼。

## 3. 重要結論

Storage Intelligence 是一個新的產品，旨在提供端到端的儲存管理解決方案，從分析儲存狀態到執行操作。Google 提供 30 天的免費試用，鼓勵使用者開始使用並解決儲存管理問題。Storage Intelligence 可以幫助客戶管理和控制儲存成本，同時避免或最大限度地減少各種安全合規問題，並設定組織範圍的策略。
