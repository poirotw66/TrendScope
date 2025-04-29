# Troubleshoot issues on Google Cloud with Gemini Cloud Assist Investigations
[會議影片連結](https://www.youtube.com/watch?v=vK_7jWNDoh8)
使用 Gemini Cloud Assist Investigations 解決 Google Cloud 上的問題

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的 Gemini Cloud Assist Investigations 如何幫助使用者更快速、更安全地解決雲端應用程式的問題。核心觀點包括：

*   傳統故障排除的挑戰：專業知識門檻高、資料分析困難、耗時。
*   Gemini Cloud Assist Investigations 的優勢：無需深厚的領域知識、保護資料安全、快速定位問題。
*   核心引擎：應用程式拓撲發現、問題相關資源識別、AI 假設生成。
*   整合現有工作流程：可直接從 GKE console 或 Dataproc 服務進行故障排除。

## 2. 詳細內容

Deepak Kalakuri 首先指出，現今雲端環境中，使用者在排除應用程式問題時面臨多重挑戰。雲端堆疊和資源的多樣性不斷增長，應用程式本身也變得越來越複雜，加上雲端和資源的新功能不斷推出，都增加了故障排除的難度。此外，使用者和 SRE 團隊需要分析大量的資料，才能找出問題的根源，這通常需要花費數小時的時間。

Gemini Cloud Assist Investigations 旨在徹底改變這種情況。它讓使用者無需深厚的領域知識，也能快速排除故障，同時保護資料安全。使用者不再需要將日誌錯誤訊息複製到 ChatGPT 或其他公開的 AI 工具中，避免將客戶資料或公司機密資料暴露於風險之中。

該工具的核心引擎包含三個部分：

1.  **應用程式拓撲發現：** 識別與問題相關的資源。
2.  **問題理解：** 收集相關資源的日誌、事件、配置變更、指標和錯誤，並將其分組。
3.  **AI 假設生成：** 基於觀察結果，AI 合成關於可能發生的情況以及如何更快排除問題的假設。

Gemini Cloud Assist Investigations 從多種資料來源提取資料，並以安全的方式進行。它代表使用者行事，使用使用者的權限集，並且不會將資料複製到使用者的專案之外。所有調查和假設都保留在使用者的專案中。

會議中展示了一個範例，說明如何使用 Gemini Cloud Assist Investigations 解決 CloudHub 中的應用程式問題。該工具自動將相關日誌訊息複製到調查表單中，並識別出從 3.4 到 3.5 的部署失敗。它還提出了一個相關的假設，即使用者可能最近進行了程式碼變更。使用者可以查看日誌中的錯誤訊息，並查看 GitHub 中的實際提交 URL，從而發現最近的程式碼變更中存在記憶體洩漏。

此外，Gemini Cloud Assist Investigations 可以整合到現有的工作流程中。使用者可以直接從 GKE console 或 Dataproc 服務進行故障排除。例如，在 GKE workloads 頁面中，使用者可以點擊 "Investigate" 按鈕，快速識別 pod 崩潰的原因。在 Dataproc 中，使用者可以直接從失敗的批次作業中啟動調查，快速獲得故障排除結果。

## 3. 重要結論

Gemini Cloud Assist Investigations 提供了一種更快速、更安全、更有效率的方式來解決 Google Cloud 上的應用程式問題。它降低了故障排除的門檻，保護了資料安全，並整合到現有的工作流程中，有助於提高應用程式的正常運行時間，並加速開發人員的開發速度。
