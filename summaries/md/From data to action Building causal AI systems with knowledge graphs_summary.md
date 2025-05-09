# From data to action Building causal AI systems with knowledge graphs

[會議影片連結](https://www.youtube.com/watch?v=M6muE9X_dgo)
從數據到行動：使用知識圖譜構建因果AI系統

## 1. 核心觀點

本次演講主要介紹如何利用因果AI和知識圖譜，從數據中提取因果關係，並應用於決策制定。核心觀點包括：

- 傳統的基於相關性的分析方法存在局限性，容易將巧合誤認為因果關係，導致錯誤的決策。
- 因果AI旨在建立理解因果關係的系統，從而做出更準確的預測和決策。
- 知識圖譜可以幫助存儲和檢索因果關係，提高決策效率。
- Gemini等大型語言模型可以利用知識圖譜中的因果關係，提供更明智的建議。

## 2. 詳細內容

演講者首先指出，許多組織在數據分析中過於關注相關性，而忽略了潛在的因果關係。例如，一個公司在某個季度增加了市場營銷支出，銷售額也隨之增加，但如果簡單地認為增加支出就能帶來更高的銷售額，可能會導致錯誤的決策。

因果AI可以幫助我們理解真正的因果關係。例如，市場營銷支出會影響網站流量，而網站流量又會影響銷售額，但這些關係都可能受到季節性因素的影響。通過使用因果AI，我們可以控制這些因素，更準確地評估市場營銷活動的效果。

演講者介紹了一種名為Causal Bird的AI工具，它可以從文本和指標中提取因果關係。這些關係可以存儲在Spanner Graph中，以便快速檢索。然後，Gemini等大型語言模型可以利用這些因果關係，提供更明智的建議。

演講者舉例說明，如果我們想知道如何在第二季度分配100萬美元的市場營銷預算，以最大化投資回報率，Gemini可以利用知識圖譜中的因果關係，建議增加電子郵件營銷預算，因為這將對銷售額產生最大的影響。

整個流程形成一個循環：我們從數據中提取因果關係，將其存儲在知識圖譜中，然後使用大型語言模型進行推理，並根據推理結果收集更多數據，從而不斷改進系統的推薦能力。

## 3. 重要結論

通過結合因果AI、知識圖譜和大型語言模型，我們可以構建更智能的決策支持系統，從而做出更明智的決策，並取得更好的結果。演講者鼓勵大家探索這些技術，並將其應用於自己的業務中。
