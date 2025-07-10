#!/usr/bin/env python3
"""
快速生成 Hugo 三階層導航系統演示
"""

import os
import pathlib
import logging
import shutil

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_quick_demo():
    """創建快速演示"""
    logger.info("🚀 開始創建 Hugo 三階層導航系統演示...")
    
    # 創建輸出目錄
    output_dir = pathlib.Path.home() / "Desktop" / "hugo_navigation_demo"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True)
    
    # 創建目錄結構
    directories = ["css", "js", "trends", "seminars", "sessions"]
    for directory in directories:
        (output_dir / directory).mkdir(parents=True, exist_ok=True)
    
    # 創建基本 CSS
    create_basic_css(output_dir / "css" / "styles.css")
    
    # 創建基本 JavaScript
    create_basic_js(output_dir / "js" / "main.js")
    
    # 創建首頁
    create_demo_homepage(output_dir / "index.html")
    
    # 創建技術趨勢頁面
    create_demo_trends_page(output_dir / "trends" / "index.html")
    create_demo_ai_trend_page(output_dir / "trends" / "ai.html")
    
    # 創建研討會頁面
    create_demo_seminars_page(output_dir / "seminars" / "index.html")
    create_demo_qcon_page(output_dir / "seminars" / "qcon-beijing-2024.html")
    
    # 創建會議報告頁面
    create_demo_sessions_page(output_dir / "sessions" / "index.html")
    create_demo_session_detail(output_dir / "sessions" / "ai-llm-trends.html")
    
    logger.info(f"✅ Hugo 三階層導航系統演示已創建: {output_dir}")
    logger.info(f"🌐 請打開瀏覽器訪問: file://{output_dir}/index.html")
    
    return output_dir

def create_basic_css(css_file: pathlib.Path):
    """創建基本 CSS"""
    css_content = """
:root {
    --primary: #3a86ff;
    --primary-dark: #2f6bff;
    --secondary: #33c5ff;
    --text-primary: #1a202c;
    --text-secondary: #2d3748;
    --text-muted: #718096;
    --bg-primary: #ffffff;
    --bg-secondary: #f7fafc;
    --border-light: #e2e8f0;
    --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.07);
    --radius-md: 12px;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
}

* { box-sizing: border-box; }

body {
    font-family: 'Inter', 'Microsoft JhengHei', sans-serif;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    margin: 0;
    padding: 0;
    line-height: 1.7;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
}

/* 導航欄 */
.site-header {
    background: var(--bg-primary);
    box-shadow: var(--shadow-sm);
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid var(--border-light);
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md) 0;
}

.nav-brand a {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--primary);
    text-decoration: none;
}

.nav-menu {
    display: flex;
    gap: var(--spacing-xl);
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.nav-link:hover, .nav-link.active {
    color: var(--primary);
    background-color: rgba(58, 134, 255, 0.1);
}

/* 麵包屑導航 */
.breadcrumb {
    background: var(--bg-secondary);
    padding: var(--spacing-md) 0;
    border-bottom: 1px solid var(--border-light);
}

.breadcrumb-nav {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-muted);
}

.breadcrumb-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.breadcrumb-item:not(:last-child)::after {
    content: '›';
    color: var(--text-muted);
    font-weight: bold;
}

.breadcrumb-link {
    color: var(--primary);
    text-decoration: none;
}

.breadcrumb-link:hover {
    text-decoration: underline;
}

.breadcrumb-current {
    color: var(--text-primary);
    font-weight: 500;
}

/* 內容區塊 */
.content-section {
    background: var(--bg-primary);
    border-radius: var(--radius-md);
    padding: var(--spacing-xl);
    margin: var(--spacing-xl) 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
}

.section-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--spacing-lg);
    color: var(--text-primary);
}

/* 卡片網格 */
.trends-grid, .sessions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-xl) 0;
}

.trend-card, .session-card {
    background: var(--bg-primary);
    border-radius: var(--radius-md);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-light);
    transition: all 0.3s ease;
}

.trend-card:hover, .session-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.trend-title, .session-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
}

.trend-description {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    line-height: 1.6;
}

.trend-stats, .session-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.875rem;
    color: var(--text-muted);
}

.trend-tag {
    background: var(--primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.75rem;
    text-decoration: none;
    transition: all 0.2s ease;
}

.trend-tag:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
    color: white;
    text-decoration: none;
}

/* 導航按鈕 */
.nav-buttons {
    display: flex;
    justify-content: space-between;
    margin: var(--spacing-xl) 0;
    padding: var(--spacing-lg) 0;
    border-top: 1px solid var(--border-light);
}

.nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: var(--spacing-md) var(--spacing-lg);
    background: var(--primary);
    color: white;
    text-decoration: none;
    border-radius: var(--radius-md);
    font-weight: 500;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}

.nav-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    color: white;
    text-decoration: none;
}

/* 頁腳 */
.site-footer {
    background: var(--bg-primary);
    border-top: 1px solid var(--border-light);
    padding: var(--spacing-xl) 0;
    margin-top: var(--spacing-xl);
    text-align: center;
    color: var(--text-muted);
    font-size: 0.875rem;
}

/* 響應式設計 */
@media (max-width: 768px) {
    .trends-grid, .sessions-grid {
        grid-template-columns: 1fr;
    }
    
    .nav-menu {
        display: none;
    }
    
    .nav-buttons {
        flex-direction: column;
        gap: var(--spacing-md);
    }
}

a {
    color: var(--primary);
    text-decoration: none;
    transition: all 0.2s ease;
}

a:hover {
    color: var(--primary-dark);
    text-decoration: underline;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
}
"""
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)

def create_basic_js(js_file: pathlib.Path):
    """創建基本 JavaScript"""
    js_content = """
document.addEventListener('DOMContentLoaded', function() {
    console.log('Hugo 三階層導航系統已載入');
    
    // 標記當前頁面的導航項目
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath || 
            (linkPath !== '/' && currentPath.includes(linkPath))) {
            link.classList.add('active');
        }
    });
    
    // 平滑滾動
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
"""
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

def create_demo_homepage(index_file: pathlib.Path):
    """創建演示首頁"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendScope 技術趨勢分析 - 三階層導航演示</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="index.html" class="nav-link active">首頁</a></li>
                    <li><a href="trends/index.html" class="nav-link">技術趨勢</a></li>
                    <li><a href="sessions/index.html" class="nav-link">會議報告</a></li>
                    <li><a href="seminars/index.html" class="nav-link">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <section class="content-section">
                <h1 class="section-title">🌐 Hugo 三階層導航系統演示</h1>
                <p>這是一個完整的三階層導航系統演示，包含：</p>
                <ul>
                    <li><strong>第一層：</strong>首頁 - 提供整體概覽和快速導航</li>
                    <li><strong>第二層：</strong>分類頁面 - 技術趨勢、研討會、會議報告列表</li>
                    <li><strong>第三層：</strong>詳細頁面 - 具體的趨勢分析或會議報告</li>
                </ul>
            </section>

            <section class="content-section">
                <h2 class="section-title">
                    <a href="trends/index.html" style="text-decoration: none; color: inherit;">
                        🔥 技術趨勢分析
                    </a>
                </h2>
                <div class="trends-grid">
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="trends/ai.html" style="text-decoration: none; color: inherit;">
                                🤖 人工智能
                            </a>
                        </h3>
                        <p class="trend-description">探索 AI 大模型、機器學習和深度學習的最新發展</p>
                        <div class="trend-stats">
                            <span>相關會議: 5</span>
                            <a href="trends/ai.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="trends/cloud-native.html" style="text-decoration: none; color: inherit;">
                                ☁️ 雲原生
                            </a>
                        </h3>
                        <p class="trend-description">Kubernetes、微服務和容器化技術的實踐經驗</p>
                        <div class="trend-stats">
                            <span>相關會議: 3</span>
                            <a href="trends/cloud-native.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="trends/index.html" class="nav-btn">查看所有技術趨勢 →</a>
                </div>
            </section>

            <section class="content-section">
                <h2 class="section-title">
                    <a href="sessions/index.html" style="text-decoration: none; color: inherit;">
                        📊 最新會議報告
                    </a>
                </h2>
                <div class="sessions-grid">
                    <article class="session-card">
                        <h3 class="session-title">
                            <a href="sessions/ai-llm-trends.html">AI 大模型技術發展趨勢</a>
                        </h3>
                        <div class="session-meta">
                            <a href="seminars/qcon-beijing-2024.html" class="trend-tag" style="background: var(--secondary);">
                                QCon Beijing 2024
                            </a>
                            <span>2024-07-10</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <a href="trends/ai.html" class="trend-tag">人工智能</a>
                            <a href="trends/ai.html" class="trend-tag">大語言模型</a>
                        </div>
                    </article>
                </div>
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="sessions/index.html" class="nav-btn">查看所有會議報告 →</a>
                </div>
            </section>

            <section class="content-section">
                <h2 class="section-title">
                    <a href="seminars/index.html" style="text-decoration: none; color: inherit;">
                        🎯 研討會分類
                    </a>
                </h2>
                <div class="trends-grid">
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="seminars/qcon-beijing-2024.html" style="text-decoration: none; color: inherit;">
                                QCon Beijing 2024
                            </a>
                        </h3>
                        <div class="trend-stats">
                            <span>會議數量: 8</span>
                            <a href="seminars/qcon-beijing-2024.html" class="trend-tag">查看會議</a>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="seminars/index.html" class="nav-btn">查看所有研討會 →</a>
                </div>
            </section>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析 - Hugo 三階層導航系統演示</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_demo_trends_page(trends_index: pathlib.Path):
    """創建技術趨勢列表頁面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技術趨勢分析 - TrendScope</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="../index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html" class="nav-link">首頁</a></li>
                    <li><a href="index.html" class="nav-link active">技術趨勢</a></li>
                    <li><a href="../sessions/index.html" class="nav-link">會議報告</a></li>
                    <li><a href="../seminars/index.html" class="nav-link">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-nav">
                <div class="breadcrumb-item">
                    <a href="../index.html" class="breadcrumb-link">首頁</a>
                </div>
                <div class="breadcrumb-item">
                    <span class="breadcrumb-current">技術趨勢</span>
                </div>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <section class="content-section">
                <h1 class="section-title">🔥 技術趨勢分析</h1>
                <p>探索最新的技術發展趨勢，深入了解行業動向</p>

                <div class="trends-grid">
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="ai.html" style="text-decoration: none; color: inherit;">
                                🤖 人工智能
                            </a>
                        </h3>
                        <p class="trend-description">
                            探索 AI 大模型、機器學習和深度學習的最新發展和應用案例
                        </p>
                        <div class="trend-stats">
                            <span>相關會議: 5</span>
                            <a href="ai.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="cloud-native.html" style="text-decoration: none; color: inherit;">
                                ☁️ 雲原生
                            </a>
                        </h3>
                        <p class="trend-description">
                            Kubernetes、微服務和容器化技術的實踐經驗和最佳實踐
                        </p>
                        <div class="trend-stats">
                            <span>相關會議: 3</span>
                            <a href="cloud-native.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                </div>
            </section>

            <nav class="nav-buttons">
                <div class="nav-prev">
                    <a href="../index.html" class="nav-btn">← 返回首頁</a>
                </div>
                <div class="nav-next">
                    <a href="../sessions/index.html" class="nav-btn">查看所有會議 →</a>
                </div>
            </nav>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(trends_index, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_demo_ai_trend_page(ai_page: pathlib.Path):
    """創建 AI 趨勢詳細頁面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>人工智能趨勢 - TrendScope</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="../index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html" class="nav-link">首頁</a></li>
                    <li><a href="index.html" class="nav-link active">技術趨勢</a></li>
                    <li><a href="../sessions/index.html" class="nav-link">會議報告</a></li>
                    <li><a href="../seminars/index.html" class="nav-link">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-nav">
                <div class="breadcrumb-item">
                    <a href="../index.html" class="breadcrumb-link">首頁</a>
                </div>
                <div class="breadcrumb-item">
                    <a href="index.html" class="breadcrumb-link">技術趨勢</a>
                </div>
                <div class="breadcrumb-item">
                    <span class="breadcrumb-current">人工智能</span>
                </div>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <section class="content-section">
                <h1 class="section-title">🤖 人工智能趨勢分析</h1>
                <p>探索 AI 大模型、機器學習和深度學習的最新發展和應用案例</p>

                <h2>相關會議報告</h2>
                <div class="sessions-grid">
                    <article class="session-card">
                        <h3 class="session-title">
                            <a href="../sessions/ai-llm-trends.html">AI 大模型技術發展趨勢</a>
                        </h3>
                        <div class="session-meta">
                            <a href="../seminars/qcon-beijing-2024.html" class="trend-tag" style="background: var(--secondary);">
                                QCon Beijing 2024
                            </a>
                            <span>2024-07-10</span>
                        </div>
                    </article>
                </div>
            </section>

            <nav class="nav-buttons">
                <div class="nav-prev">
                    <a href="index.html" class="nav-btn">← 所有技術趨勢</a>
                </div>
                <div class="nav-next">
                    <a href="../sessions/ai-llm-trends.html" class="nav-btn">查看相關會議 →</a>
                </div>
            </nav>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(ai_page, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_demo_seminars_page(seminars_index: pathlib.Path):
    """創建研討會列表頁面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研討會分類 - TrendScope</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="../index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html" class="nav-link">首頁</a></li>
                    <li><a href="../trends/index.html" class="nav-link">技術趨勢</a></li>
                    <li><a href="../sessions/index.html" class="nav-link">會議報告</a></li>
                    <li><a href="index.html" class="nav-link active">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-nav">
                <div class="breadcrumb-item">
                    <a href="../index.html" class="breadcrumb-link">首頁</a>
                </div>
                <div class="breadcrumb-item">
                    <span class="breadcrumb-current">研討會</span>
                </div>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <section class="content-section">
                <h1 class="section-title">🎯 研討會分類</h1>
                <p>按研討會分類瀏覽技術會議和演講內容</p>

                <div class="trends-grid">
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="qcon-beijing-2024.html" style="text-decoration: none; color: inherit;">
                                QCon Beijing 2024
                            </a>
                        </h3>
                        <div class="trend-stats">
                            <span>會議數量: 8</span>
                            <a href="qcon-beijing-2024.html" class="trend-tag">查看會議</a>
                        </div>
                    </div>
                </div>
            </section>

            <nav class="nav-buttons">
                <div class="nav-prev">
                    <a href="../index.html" class="nav-btn">← 返回首頁</a>
                </div>
                <div class="nav-next">
                    <a href="../trends/index.html" class="nav-btn">查看技術趨勢 →</a>
                </div>
            </nav>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(seminars_index, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_demo_qcon_page(qcon_page: pathlib.Path):
    """創建 QCon 研討會詳細頁面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QCon Beijing 2024 - TrendScope</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="../index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html" class="nav-link">首頁</a></li>
                    <li><a href="../trends/index.html" class="nav-link">技術趨勢</a></li>
                    <li><a href="../sessions/index.html" class="nav-link">會議報告</a></li>
                    <li><a href="index.html" class="nav-link active">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-nav">
                <div class="breadcrumb-item">
                    <a href="../index.html" class="breadcrumb-link">首頁</a>
                </div>
                <div class="breadcrumb-item">
                    <a href="index.html" class="breadcrumb-link">研討會</a>
                </div>
                <div class="breadcrumb-item">
                    <span class="breadcrumb-current">QCon Beijing 2024</span>
                </div>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <section class="content-section">
                <h1 class="section-title">QCon Beijing 2024</h1>
                <p>QCon 全球軟件開發大會北京站 2024</p>

                <h2>會議報告</h2>
                <div class="sessions-grid">
                    <article class="session-card">
                        <h3 class="session-title">
                            <a href="../sessions/ai-llm-trends.html">AI 大模型技術發展趨勢</a>
                        </h3>
                        <div class="session-meta">
                            <span>主題演講</span>
                            <span>2024-07-10</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <a href="../trends/ai.html" class="trend-tag">人工智能</a>
                            <a href="../trends/ai.html" class="trend-tag">大語言模型</a>
                        </div>
                    </article>
                </div>
            </section>

            <nav class="nav-buttons">
                <div class="nav-prev">
                    <a href="index.html" class="nav-btn">← 所有研討會</a>
                </div>
                <div class="nav-next">
                    <a href="../sessions/ai-llm-trends.html" class="nav-btn">查看會議詳情 →</a>
                </div>
            </nav>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(qcon_page, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_demo_sessions_page(sessions_index: pathlib.Path):
    """創建會議報告列表頁面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>會議報告 - TrendScope</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="../index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html" class="nav-link">首頁</a></li>
                    <li><a href="../trends/index.html" class="nav-link">技術趨勢</a></li>
                    <li><a href="index.html" class="nav-link active">會議報告</a></li>
                    <li><a href="../seminars/index.html" class="nav-link">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-nav">
                <div class="breadcrumb-item">
                    <a href="../index.html" class="breadcrumb-link">首頁</a>
                </div>
                <div class="breadcrumb-item">
                    <span class="breadcrumb-current">會議報告</span>
                </div>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <section class="content-section">
                <h1 class="section-title">📊 所有會議報告</h1>
                <p>瀏覽所有技術會議和演講的深度分析報告</p>

                <div class="sessions-grid">
                    <article class="session-card">
                        <h3 class="session-title">
                            <a href="ai-llm-trends.html">AI 大模型技術發展趨勢</a>
                        </h3>
                        <div class="session-meta">
                            <a href="../seminars/qcon-beijing-2024.html" class="trend-tag" style="background: var(--secondary);">
                                QCon Beijing 2024
                            </a>
                            <span>2024-07-10</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <a href="../trends/ai.html" class="trend-tag">人工智能</a>
                            <a href="../trends/ai.html" class="trend-tag">大語言模型</a>
                        </div>
                    </article>
                </div>
            </section>

            <nav class="nav-buttons">
                <div class="nav-prev">
                    <a href="../index.html" class="nav-btn">← 返回首頁</a>
                </div>
                <div class="nav-next">
                    <a href="../trends/index.html" class="nav-btn">查看技術趨勢 →</a>
                </div>
            </nav>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(sessions_index, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_demo_session_detail(session_detail: pathlib.Path):
    """創建會議詳細頁面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 大模型技術發展趨勢 - TrendScope</title>
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="../index.html">TrendScope 技術趨勢分析</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html" class="nav-link">首頁</a></li>
                    <li><a href="../trends/index.html" class="nav-link">技術趨勢</a></li>
                    <li><a href="index.html" class="nav-link active">會議報告</a></li>
                    <li><a href="../seminars/index.html" class="nav-link">研討會</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="container">
            <div class="breadcrumb-nav">
                <div class="breadcrumb-item">
                    <a href="../index.html" class="breadcrumb-link">首頁</a>
                </div>
                <div class="breadcrumb-item">
                    <a href="index.html" class="breadcrumb-link">會議報告</a>
                </div>
                <div class="breadcrumb-item">
                    <span class="breadcrumb-current">AI 大模型技術發展趨勢</span>
                </div>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <article class="content-section">
                <header>
                    <h1 class="section-title">🤖 AI 大模型技術發展趨勢</h1>
                    <div class="session-meta" style="margin-bottom: 2rem;">
                        <strong>研討會：</strong>
                        <a href="../seminars/qcon-beijing-2024.html" class="trend-tag" style="background: var(--secondary);">
                            QCon Beijing 2024
                        </a>
                        <br><br>
                        <strong>日期：</strong> 2024年07月10日<br>
                        <strong>類型：</strong> 主題演講
                    </div>
                    <div style="margin-bottom: 2rem;">
                        <a href="../trends/ai.html" class="trend-tag">人工智能</a>
                        <a href="../trends/ai.html" class="trend-tag">大語言模型</a>
                        <a href="../trends/ai.html" class="trend-tag">機器學習</a>
                    </div>
                </header>

                <div>
                    <h2>技術背景</h2>
                    <p>大語言模型（LLM）正在重塑整個 AI 領域，從 GPT 系列到各種開源模型，技術發展日新月異。</p>

                    <h2>核心洞察</h2>
                    <ul>
                        <li><strong>模型規模持續增長</strong>：參數量從億級發展到萬億級</li>
                        <li><strong>多模態融合</strong>：文本、圖像、音頻的統一處理</li>
                        <li><strong>推理能力提升</strong>：從簡單對話到複雜推理</li>
                    </ul>

                    <h2>實踐經驗</h2>
                    <p>企業在部署大模型時需要考慮成本、效率和安全性的平衡。</p>
                </div>
            </article>

            <nav class="nav-buttons">
                <div class="nav-prev">
                    <a href="index.html" class="nav-btn">← 所有會議報告</a>
                </div>
                <div class="nav-next">
                    <a href="../trends/ai.html" class="nav-btn">查看相關趨勢 →</a>
                </div>
            </nav>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(session_detail, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    try:
        output_dir = create_quick_demo()
        print(f"\n🎉 Hugo 三階層導航系統演示創建成功！")
        print(f"📂 輸出目錄: {output_dir}")
        print(f"🌐 請打開瀏覽器訪問: file://{output_dir}/index.html")
        print(f"\n📋 演示包含以下頁面:")
        print(f"   🏠 首頁: index.html")
        print(f"   🔥 技術趨勢列表: trends/index.html")
        print(f"   🤖 AI 趨勢詳情: trends/ai.html")
        print(f"   🎯 研討會列表: seminars/index.html")
        print(f"   📅 QCon 詳情: seminars/qcon-beijing-2024.html")
        print(f"   📊 會議報告列表: sessions/index.html")
        print(f"   📄 會議詳情: sessions/ai-llm-trends.html")
        print(f"\n✨ 導航功能:")
        print(f"   • 主導航選單（頂部）")
        print(f"   • 麵包屑導航（頁面頂部）")
        print(f"   • 上一頁/下一頁按鈕（頁面底部）")
        print(f"   • 相關內容連結（卡片中）")
        print(f"   • 返回頂部按鈕（JavaScript 生成）")

    except Exception as e:
        print(f"❌ 創建演示失敗: {e}")
        import traceback
        traceback.print_exc()
