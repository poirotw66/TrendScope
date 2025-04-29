# Gemini Code Assist Superpowers for building apps on Google Cloud databases

[會議影片連結](https://www.youtube.com/watch?v=sDTjVOo6M04)
Gemini Code Assist 超能力，用於在 Google Cloud 數據庫上構建應用程式

## 1. 核心觀點

本次演講主要介紹 Gemini Code Assist 如何協助開發者在 Google Cloud Databases 上構建應用程式，重點在於 Gemini 如何利用大型語言模型和數據庫上下文，提供更智能的程式碼生成和錯誤修復功能。核心觀點包括：

*   Gemini Code Assist 能夠理解數據庫和 SQL，協助開發者更有效地編寫程式碼。
*   數據庫上下文（schema、data、examples、documentation、code）對於 AI 代理理解數據庫至關重要。
*   Google Database tool 整合 Gemini Code Assist 和 Google Cloud Database，提供更便捷的開發體驗。
*   Cloud SQL AlloyDB 和 Spanner Studios 中的 Help Me Code 工具，可以使用自然語言生成 SQL 查詢。
*   開源 EvalBench 和 Context Enrichment tool，協助開發者評估和增強 AI 代理與數據庫的互動能力。

## 2. 詳細內容

演講首先介紹了 Gemini Code Assist 在軟體開發生命週期中的作用，強調了數據庫在應用程式開發中的核心地位。透過一個實際的程式碼生成演示，展示了 Gemini Code Assist 如何利用數據庫資訊和程式碼庫，自動生成包含正確表名和欄位名的 SQL 查詢和相關基礎設施程式碼。

接著，演講深入探討了 Gemini Code Assist 的兩個核心組成部分：Gemini 和數據庫上下文。強調了 Gemini 在理解數據庫和 SQL 方面的能力，以及透過不斷改進模型，在 text-to-SQL benchmark (BIRD) 上取得的優異成績。同時，詳細解釋了數據庫上下文的重要性，指出 AI 代理需要理解數據庫的 schema、data、application 和 semantics，才能生成正確的程式碼。

此外，演講還介紹了 Google Database tool，它整合了 Gemini Code Assist 和 Google Cloud Database，方便開發者在 IDE 中使用。同時，Cloud SQL AlloyDB 和 Spanner Studios 中的 Help Me Code 工具，允許開發者使用自然語言描述任務，自動生成 SQL 查詢。

最後，演講宣布開源 EvalBench 和 Context Enrichment tool。EvalBench 是一個用於評估 AI 代理與數據庫互動品質的框架，Context Enrichment tool 則利用 Gemini 分析數據庫 schema、內容和文檔，生成聚合內容，為 AI 代理提供更多相關資訊。

## 3. 重要結論

Gemini Code Assist 透過結合大型語言模型和數據庫上下文，為開發者在 Google Cloud Databases 上構建應用程式提供了強大的支援。Google Database tool 和 Help Me Code 工具簡化了開發流程，而開源的 EvalBench 和 Context Enrichment tool 則有助於提升 AI 代理與數據庫的互動能力。這些工具的發布，將有助於開發者更高效、更智能地開發基於 Google Cloud Databases 的應用程式。
