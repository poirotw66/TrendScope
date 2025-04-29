Build event-driven apps with Cloud Run and Eventarc Advanced

[會議影片連結](https://www.youtube.com/watch?v=C5dl_D_IYgQ)
使用 Cloud Run 和 Eventarc Advanced 構建事件驅動應用程式

## 1. 核心觀點

本次會議主要介紹了 Cloud Run Functions 和 EventArc Advanced 這兩個新功能，旨在簡化和擴展事件驅動應用程式的開發和管理。Cloud Run Functions 讓開發者可以直接在 Cloud Run 內建立和管理函數，而 EventArc Advanced 則提供了一套工具，用於在企業級規模下構建事件驅動架構。

## 2. 詳細內容

首先，Cloud Run Functions 簡化了開發者建立函數的體驗，允許他們直接在 Cloud Run 內建立和管理函數。如果開發者熟悉 Cloud Functions，可以直接使用相同的程式碼，無需重寫。所有第二代函數都已升級為 Cloud Run Functions，可以立即使用 Cloud Run 的所有功能，包括 GPU。開發者可以使用 Cloud Console 在 Cloud Run Source Editor 中建立新函數，也可以找到使用 Cloud Functions 建立的現有函數。Cloud Run Functions 保留了 Functions API 和 Cloud Run API，開發者可以使用任一 API 來管理函數。無論使用哪種方式建立函數，開發者都可以使用 Cloud Run 的所有功能，包括 GPU 和直接 VPC 出口。此外，開發者還可以獨立管理事件，在單個函數上建立多個觸發器，而無需在每次管理觸發器時重新部署函數。Cloud Run Functions 還提供對運行時環境的更多控制，並提供 Google 管理的語言運行時，具有零停機時間和自動安全更新。

其次，EventArc Advanced 旨在幫助開發者在企業級規模下構建事件驅動應用程式。它解決了大型團隊和組織在擴展事件驅動架構時面臨的挑戰。對於發布者來說，很難發布需要新編排和新基礎設施的事件。對於平台管理員來說，以分散的方式做出存取控制決策很困難。對於事件的消費者來說，他們無法控制傳入訊息的格式和結構描述。EventArc Advanced 引入了三個新概念：訊息匯流排，用於發布和存取事件的單一位置，以及用於控制和觀察訊息端到端流動的單一位置；註冊，允許以精細的方式篩選來自匯流排的訊息；以及管道，提供對訊息形狀和格式的控制，然後再進行傳遞。

## 3. 重要結論

Cloud Run Functions 和 EventArc Advanced 為開發者提供了強大的工具，可以更輕鬆地構建和管理事件驅動應用程式。Cloud Run Functions 簡化了函數的開發和部署，而 EventArc Advanced 則解決了在企業級規模下構建事件驅動架構時面臨的挑戰。這些新功能將有助於開發者構建更具彈性、可擴展性和響應性的應用程式。
