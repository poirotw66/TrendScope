def get_email_template():
    """返回 HTML 電子郵件樣板"""
    return """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        header {
            background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
            color: white;
            text-align: center;
            padding: 2rem 1rem;
            margin-bottom: 2rem;
        }
        header img {
            max-width: 50%;
            height: auto;
            margin-bottom: 1rem;
        }
        .content-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            font-size: 2.2rem;
            margin-bottom: 1.5rem;
        }
        h2 {
            font-size: 1.8rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #eee;
        }
        h3 {
            font-size: 1.4rem;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
        p {
            margin-bottom: 1rem;
            line-height: 1.7;
        }
        ul {
            padding-left: 1.5rem;
        }
        li {
            margin-bottom: 0.5rem;
        }
        footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            color: #666;
            font-size: 0.9rem;
        }
        footer img {
            max-width: 30%;
            height: auto;
            margin-bottom: 1rem;
            opacity: 0.8;
        }
        @media (max-width: 768px) {
            .content-container {
                padding: 1.5rem;
            }
            h1 {
                font-size: 1.8rem;
            }
            h2 {
                font-size: 1.5rem;
            }
            h3 {
                font-size: 1.2rem;
            }
        }
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