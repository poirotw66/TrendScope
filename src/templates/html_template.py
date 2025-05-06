def get_email_template():
    """返回 HTML 電子郵件樣板"""
    return """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Roboto', 'Microsoft JhengHei', sans-serif; /* 改用更現代的字體 */
            line-height: 1.7; /* 增加行高 */
            color: #444; /* 稍微柔和的文字顏色 */
            margin: 0;
            padding: 0;
            background-color: #f4f7f9; /* 稍微調整背景色 */
        }}
        header {{
            background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
            color: white;
            text-align: center;
            padding: 2.5rem 1rem; /* 增加 header 內邊距 */
            margin-bottom: 0; /* 移除 header 和 content 之間的間距 */
            border-bottom: 5px solid #3a5a9a; /* 添加一個邊框增加層次感 */
        }}
        header img {{
            max-width: 150px; /* 限制 logo 大小 */
            height: auto;
            margin-bottom: 1.5rem; /* 調整 logo 下方間距 */
        }}
        header h1 {{ /* 將 H1 移到 header 樣式內 */
            font-size: 2.0rem; /* 調整標題大小 */
            margin: 0; /* 移除 H1 的預設 margin */
            font-weight: 500; /* 調整字重 */
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2); /* 微調陰影 */
        }}
        .content-container {{
            max-width: 850px; /* 稍微縮小寬度 */
            margin: 2.5rem auto; /* 調整上下外邊距 */
            padding: 2.5rem; /* 增加內容區內邊距 */
            background-color: white;
            border-radius: 10px; /* 增加圓角 */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); /* 調整陰影 */
        }}
        h2 {{
            font-size: 1.7rem; /* 調整 H2 大小 */
            margin-top: 2.5rem; /* 增加 H2 上方間距 */
            margin-bottom: 1.2rem; /* 調整 H2 下方間距 */
            padding-bottom: 0.6rem; /* 調整 H2 底線間距 */
            border-bottom: 2px solid #e0e0e0; /* 加粗底線 */
            color: #182848; /* 使用 header 的深色 */
        }}
        h3 {{
            font-size: 1.3rem; /* 調整 H3 大小 */
            margin-top: 2rem; /* 增加 H3 上方間距 */
            margin-bottom: 1rem; /* 調整 H3 下方間距 */
            color: #4b6cb7; /* 使用 header 的淺色 */
        }}
        p {{
            margin-bottom: 1.2rem; /* 增加段落間距 */
            line-height: 1.8; /* 增加段落行高 */
            color: #555; /* 稍微調整段落顏色 */
        }}
        ul {{
            padding-left: 1.8rem; /* 調整列表縮進 */
            margin-bottom: 1.2rem; /* 增加列表下方間距 */
        }}
        li {{
            margin-bottom: 0.7rem; /* 調整列表項間距 */
            padding-left: 0.5rem; /* 增加列表項內縮進 */
        }}
        li::marker {{ /* 樣式化列表標記 */
            color: #4b6cb7;
        }}
        footer {{
            text-align: center;
            padding: 2.5rem 1rem; /* 增加 footer 內邊距 */
            margin-top: 3rem; /* 增加 footer 上方間距 */
            color: #777; /* 調整 footer 文字顏色 */
            font-size: 0.95rem; /* 調整 footer 字體大小 */
            background-color: #e9edf0; /* 添加 footer 背景色 */
            border-top: 1px solid #d1d9e0; /* 添加 footer 上邊框 */
        }}
        footer img {{
            max-width: 120px; /* 限制 footer logo 大小 */
            height: auto;
            margin-bottom: 1.2rem; /* 調整 footer logo 下方間距 */
            opacity: 0.7; /* 稍微降低透明度 */
        }}
        footer p {{
            margin: 0.5rem 0; /* 調整 footer 段落間距 */
        }}
        @media (max-width: 768px) {{
            .content-container {{
                padding: 2rem; /* 調整平板內邊距 */
                margin: 2rem auto; /* 調整平板外邊距 */
            }}
            header {{
                padding: 2rem 1rem;
            }}
            header h1 {{
                font-size: 1.8rem;
            }}
            h2 {{
                font-size: 1.5rem;
            }}
            h3 {{
                font-size: 1.2rem;
            }}
            footer {{
                padding: 2rem 1rem;
            }}
        }}
        @media (max-width: 480px) {{ /* 添加手機斷點 */
             .content-container {{
                 padding: 1.5rem;
                 margin: 1.5rem auto;
                 border-radius: 0; /* 手機上移除圓角 */
             }}
             header h1 {{
                 font-size: 1.6rem;
             }}
             h2 {{
                 font-size: 1.3rem;
             }}
             h3 {{
                 font-size: 1.1rem;
             }}
        }}
    </style>
</head>
<body>
    <header>
        <img src="https://i.imgur.com/0LXUWvj.png" alt="Google Next 圖示">
        <h1>{title}</h1>
    </header>
    <div class="content-container">
        {content}
    </div>
    <footer>
        <img src="https://i.imgur.com/0LXUWvj.png" alt="Google Next 圖示">
        <p>此摘要由 AI 輔助生成</p>
        <p>如有任何問題或需要更多詳細資訊，請聯繫 ITR 小組</p>
    </footer>
</body>
</html>
"""