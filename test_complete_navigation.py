#!/usr/bin/env python3
"""
測試完整的 Hugo 三階層導航系統 - 手動生成完整結構
"""

import os
import sys
import pathlib
import logging
from datetime import datetime

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
# 測試檔案可以保留路徑設置以便獨立運行
project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.append(project_root)

from base.api.modules.hugo_navigation_layouts import HugoNavigationLayouts

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_complete_hugo_site():
    """創建完整的 Hugo 三階層導航網站"""
    logger.info("🚀 開始創建完整的 Hugo 三階層導航網站...")
    
    # 創建輸出目錄
    output_dir = pathlib.Path.home() / "Desktop" / "hugo_complete_navigation"
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True)
    
    # 創建基本目錄結構
    directories = [
        "css", "js", "trends", "seminars", "sessions", "posts"
    ]
    
    for directory in directories:
        (output_dir / directory).mkdir(parents=True, exist_ok=True)
    
    # 創建 CSS 文件
    create_css_file(output_dir / "css" / "styles.css")
    
    # 創建 JavaScript 文件
    create_js_file(output_dir / "js" / "main.js")
    
    # 創建首頁
    create_homepage(output_dir / "index.html")
    
    # 創建技術趨勢頁面
    create_trends_pages(output_dir)
    
    # 創建研討會頁面
    create_seminars_pages(output_dir)
    
    # 創建會議報告頁面
    create_sessions_pages(output_dir)
    
    # 創建個別會議詳細頁面
    create_individual_session_pages(output_dir)
    
    logger.info(f"✅ 完整的 Hugo 三階層導航網站已創建: {output_dir}")
    return output_dir

def create_css_file(css_file: pathlib.Path):
    """創建 CSS 文件"""
    css_content = """
/* NeoTrendHub Hugo Theme - 完整三階層導航系統 */
:root {
    --primary: #3a86ff;
    --primary-dark: #2f6bff;
    --secondary: #33c5ff;
    --success: #3dd16e;
    --warning: #fba024;
    --danger: #f55656;
    --info: #22b3fb;
    --tech: #a251f7;
    --practical: #f16dac;
    --text-primary: #1a202c;
    --text-secondary: #2d3748;
    --text-muted: #718096;
    --text-light: #a0aec0;
    --bg-primary: #ffffff;
    --bg-secondary: #f7fafc;
    --bg-tertiary: #edf2f7;
    --border-light: #e2e8f0;
    --border-medium: #cbd5e0;
    --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.07);
    --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.1);
    --transition-fast: all 0.2s ease;
    --transition-normal: all 0.3s ease;
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    --spacing-3xl: 4rem;
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 1.875rem;
    --text-4xl: 2.25rem;
    --text-5xl: 3rem;
}

* { box-sizing: border-box; }

body {
    font-family: 'Inter', 'Roboto', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    margin: 0;
    padding: 0;
    line-height: 1.7;
    overflow-x: hidden;
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
    font-size: var(--text-2xl);
    font-weight: 800;
    color: var(--primary);
    text-decoration: none;
}

.nav-menu {
    display: flex;
    gap: var(--spacing-xl);
    align-items: center;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition-fast);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-sm);
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
    gap: var(--spacing-sm);
    font-size: var(--text-sm);
    color: var(--text-muted);
}

.breadcrumb-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.breadcrumb-item:not(:last-child)::after {
    content: '›';
    color: var(--text-light);
    font-weight: bold;
}

.breadcrumb-link {
    color: var(--primary);
    text-decoration: none;
    transition: var(--transition-fast);
}

.breadcrumb-link:hover {
    color: var(--primary-dark);
    text-decoration: underline;
}

.breadcrumb-current {
    color: var(--text-primary);
    font-weight: 500;
}

/* 英雄區塊 */
.hero {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    text-align: center;
    padding: var(--spacing-3xl) 0;
    margin-bottom: var(--spacing-2xl);
}

.hero-title {
    font-size: var(--text-5xl);
    font-weight: 800;
    margin-bottom: var(--spacing-md);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
    font-size: var(--text-xl);
    opacity: 0.9;
    margin-bottom: var(--spacing-xl);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: var(--spacing-3xl);
    margin-top: var(--spacing-xl);
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: var(--text-4xl);
    font-weight: 800;
    margin-bottom: var(--spacing-xs);
}

.stat-label {
    font-size: var(--text-sm);
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* 內容區塊 */
.content-section {
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-2xl);
    margin: var(--spacing-xl) 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
    transition: var(--transition-normal);
}

.content-section:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.section-title {
    font-size: var(--text-3xl);
    font-weight: 700;
    margin-bottom: var(--spacing-lg);
    color: var(--text-primary);
    position: relative;
    padding-bottom: var(--spacing-sm);
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    border-radius: var(--radius-sm);
}

/* 趨勢分類卡片 */
.trends-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-2xl) 0;
}

.trend-card {
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-md);
    transition: var(--transition-normal);
    border: 1px solid var(--border-light);
    position: relative;
    overflow: hidden;
}

.trend-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.trend-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
}

.trend-title {
    font-size: var(--text-2xl);
    font-weight: 700;
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
}

.trend-description {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    line-height: 1.6;
}

.trend-stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: var(--text-sm);
    color: var(--text-muted);
}

/* 會議列表 */
.sessions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-xl) 0;
}

.session-card {
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
    transition: var(--transition-normal);
}

.session-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.session-title {
    font-size: var(--text-xl);
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--spacing-sm);
    line-height: 1.4;
}

.session-meta {
    display: flex;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    font-size: var(--text-sm);
    color: var(--text-muted);
}

.session-trends {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
    margin-top: var(--spacing-md);
}

.trend-tag {
    background: var(--primary);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    text-decoration: none;
    transition: var(--transition-fast);
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
    align-items: center;
    margin: var(--spacing-2xl) 0;
    padding: var(--spacing-lg) 0;
    border-top: 1px solid var(--border-light);
}

.nav-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) var(--spacing-lg);
    background: var(--primary);
    color: white;
    text-decoration: none;
    border-radius: var(--radius-md);
    font-weight: 500;
    transition: var(--transition-fast);
    box-shadow: var(--shadow-sm);
}

.nav-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    color: white;
    text-decoration: none;
}

/* 返回頂部按鈕 */
.back-to-top {
    position: fixed;
    bottom: var(--spacing-xl);
    right: var(--spacing-xl);
    width: 50px;
    height: 50px;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--text-lg);
    box-shadow: var(--shadow-md);
    transition: var(--transition-fast);
    opacity: 0;
    visibility: hidden;
    z-index: 1000;
}

.back-to-top.visible {
    opacity: 1;
    visibility: visible;
}

.back-to-top:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* 頁腳 */
.site-footer {
    background: var(--bg-primary);
    border-top: 1px solid var(--border-light);
    padding: var(--spacing-xl) 0;
    margin-top: var(--spacing-2xl);
    text-align: center;
    color: var(--text-muted);
    font-size: var(--text-sm);
}

/* 響應式設計 */
@media (max-width: 768px) {
    .hero-title {
        font-size: var(--text-3xl);
    }

    .hero-stats {
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    .trends-grid,
    .sessions-grid {
        grid-template-columns: 1fr;
    }

    .container {
        padding: 0 var(--spacing-md);
    }

    .nav-menu {
        display: none;
    }

    .nav-buttons {
        flex-direction: column;
        gap: var(--spacing-md);
    }

    .back-to-top {
        bottom: var(--spacing-md);
        right: var(--spacing-md);
        width: 45px;
        height: 45px;
    }
}

a {
    color: var(--primary);
    text-decoration: none;
    transition: var(--transition-fast);
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

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
h4 { font-size: var(--text-xl); }
h5 { font-size: var(--text-lg); }
h6 { font-size: var(--text-base); }
"""
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    logger.info("✅ CSS 文件已創建")

def create_js_file(js_file: pathlib.Path):
    """創建 JavaScript 文件"""
    js_content = """
// NeoTrendHub Hugo Theme JavaScript - 完整導航系統
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有功能
    initializeNavigation();
    initializeBackToTop();
    initializeBreadcrumbs();
    initializeActiveNavigation();

    console.log('NeoTrendHub Hugo Theme 已載入 - 完整導航系統');
});

function initializeNavigation() {
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
}

function initializeBackToTop() {
    // 創建返回頂部按鈕
    const backToTopBtn = document.createElement('button');
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.innerHTML = '↑';
    backToTopBtn.setAttribute('aria-label', '返回頂部');
    document.body.appendChild(backToTopBtn);

    // 滾動監聽
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    // 點擊返回頂部
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

function initializeBreadcrumbs() {
    // 動態生成麵包屑導航
    const breadcrumbContainer = document.querySelector('.breadcrumb-nav');
    if (!breadcrumbContainer) return;

    const path = window.location.pathname;
    const segments = path.split('/').filter(segment => segment);
    
    // 清空現有內容
    breadcrumbContainer.innerHTML = '';

    // 添加首頁
    const homeItem = createBreadcrumbItem('首頁', '/');
    breadcrumbContainer.appendChild(homeItem);

    // 添加路徑段
    let currentPath = '';
    segments.forEach((segment, index) => {
        currentPath += '/' + segment;
        const isLast = index === segments.length - 1;
        
        let title = segment;
        // 轉換路徑段為中文標題
        if (segment === 'trends') title = '技術趨勢';
        else if (segment === 'sessions') title = '會議報告';
        else if (segment === 'seminars') title = '研討會';
        
        const item = createBreadcrumbItem(title, currentPath, isLast);
        breadcrumbContainer.appendChild(item);
    });
}

function createBreadcrumbItem(title, url, isCurrent = false) {
    const item = document.createElement('div');
    item.className = 'breadcrumb-item';
    
    if (isCurrent) {
        item.innerHTML = `<span class="breadcrumb-current">${title}</span>`;
    } else {
        item.innerHTML = `<a href="${url}" class="breadcrumb-link">${title}</a>`;
    }
    
    return item;
}

function initializeActiveNavigation() {
    // 標記當前頁面的導航項目
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath || 
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
}
"""
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    logger.info("✅ JavaScript 文件已創建")

def create_homepage(index_file: pathlib.Path):
    """創建首頁"""
    html_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendScope 技術趨勢分析</title>
    <meta name="description" content="深度技術趨勢分析與會議洞察">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <!-- 主導航 -->
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
            <!-- 英雄區塊 -->
            <section class="hero">
                <div class="hero-content">
                    <h1 class="hero-title">TrendScope 技術趨勢分析</h1>
                    <p class="hero-subtitle">深度技術趨勢分析與會議洞察</p>
                    <div class="hero-stats">
                        <div class="stat-item">
                            <span class="stat-number">15</span>
                            <span class="stat-label">會議報告</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">5</span>
                            <span class="stat-label">研討會</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">8</span>
                            <span class="stat-label">技術趨勢</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 技術趨勢分類 -->
            <section class="content-section">
                <h2 class="section-title">
                    <a href="trends/index.html" style="text-decoration: none; color: inherit;">
                        技術趨勢分析
                    </a>
                </h2>
                <div class="trends-grid">
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="trends/ai.html" style="text-decoration: none; color: inherit;">
                                人工智能
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
                                雲原生
                            </a>
                        </h3>
                        <p class="trend-description">Kubernetes、微服務和容器化技術的實踐經驗</p>
                        <div class="trend-stats">
                            <span>相關會議: 3</span>
                            <a href="trends/cloud-native.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="trends/frontend.html" style="text-decoration: none; color: inherit;">
                                前端開發
                            </a>
                        </h3>
                        <p class="trend-description">React、Vue.js 和現代前端框架的演進趨勢</p>
                        <div class="trend-stats">
                            <span>相關會議: 4</span>
                            <a href="trends/frontend.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="trends/database.html" style="text-decoration: none; color: inherit;">
                                數據庫技術
                            </a>
                        </h3>
                        <p class="trend-description">分佈式數據庫和 OLAP 系統的新發展</p>
                        <div class="trend-stats">
                            <span>相關會議: 3</span>
                            <a href="trends/database.html" class="trend-tag">查看詳情</a>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="trends/index.html" class="nav-btn">查看所有技術趨勢</a>
                </div>
            </section>

            <!-- 最新會議報告 -->
            <section class="content-section">
                <h2 class="section-title">
                    <a href="sessions/index.html" style="text-decoration: none; color: inherit;">
                        最新會議報告
                    </a>
                </h2>
                <div class="sessions-grid">
                    <article class="session-card">
                        <div class="session-header">
                            <h3 class="session-title">
                                <a href="sessions/ai-llm-trends.html">AI 大模型技術發展趨勢</a>
                            </h3>
                        </div>
                        <div class="session-meta">
                            <a href="seminars/qcon-beijing-2024.html" class="trend-tag" style="background: var(--secondary);">
                                QCon Beijing 2024
                            </a>
                            <span class="session-date">2024-07-10</span>
                        </div>
                        <div class="session-trends">
                            <a href="trends/ai.html" class="trend-tag">人工智能</a>
                            <a href="trends/ai.html" class="trend-tag">大語言模型</a>
                        </div>
                    </article>
                    <article class="session-card">
                        <div class="session-header">
                            <h3 class="session-title">
                                <a href="sessions/cloud-native-best-practices.html">雲原生架構最佳實踐</a>
                            </h3>
                        </div>
                        <div class="session-meta">
                            <a href="seminars/kubecon-china-2024.html" class="trend-tag" style="background: var(--secondary);">
                                KubeCon China 2024
                            </a>
                            <span class="session-date">2024-07-09</span>
                        </div>
                        <div class="session-trends">
                            <a href="trends/cloud-native.html" class="trend-tag">雲原生</a>
                            <a href="trends/cloud-native.html" class="trend-tag">Kubernetes</a>
                        </div>
                    </article>
                    <article class="session-card">
                        <div class="session-header">
                            <h3 class="session-title">
                                <a href="sessions/frontend-framework-evolution.html">前端框架演進與選型</a>
                            </h3>
                        </div>
                        <div class="session-meta">
                            <a href="seminars/jsconf-china-2024.html" class="trend-tag" style="background: var(--secondary);">
                                JSConf China 2024
                            </a>
                            <span class="session-date">2024-07-08</span>
                        </div>
                        <div class="session-trends">
                            <a href="trends/frontend.html" class="trend-tag">前端開發</a>
                            <a href="trends/frontend.html" class="trend-tag">React</a>
                        </div>
                    </article>
                </div>
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="sessions/index.html" class="nav-btn">查看所有會議報告</a>
                </div>
            </section>

            <!-- 研討會分類 -->
            <section class="content-section">
                <h2 class="section-title">
                    <a href="seminars/index.html" style="text-decoration: none; color: inherit;">
                        研討會分類
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
                    <div class="trend-card">
                        <h3 class="trend-title">
                            <a href="seminars/kubecon-china-2024.html" style="text-decoration: none; color: inherit;">
                                KubeCon China 2024
                            </a>
                        </h3>
                        <div class="trend-stats">
                            <span>會議數量: 4</span>
                            <a href="seminars/kubecon-china-2024.html" class="trend-tag">查看會議</a>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="seminars/index.html" class="nav-btn">查看所有研討會</a>
                </div>
            </section>
        </div>
    </main>

    <!-- 頁腳 -->
    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析. 由 TrendScope 技術趨勢分析系統生成。</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    logger.info("✅ 首頁已創建")

def create_trends_pages(output_dir: pathlib.Path):
    """創建技術趨勢頁面"""
    trends_dir = output_dir / "trends"

    # 創建趨勢列表頁面
    trends_index_content = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技術趨勢分析 - TrendScope</title>
    <meta name="description" content="探索最新的技術發展趨勢，深入了解行業動向">
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <!-- 主導航 -->
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

    <!-- 麵包屑導航 -->
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
            <div class="taxonomy-page">
                <header class="content-section">
                    <h1 class="section-title">技術趨勢分析</h1>
                    <p class="section-description">探索最新的技術發展趨勢，深入了解行業動向</p>

                    <div class="hero-stats">
                        <div class="stat-item">
                            <span class="stat-number">8</span>
                            <span class="stat-label">技術趨勢</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">15</span>
                            <span class="stat-label">相關會議</span>
                        </div>
                    </div>
                </header>

                <section class="content-section">
                    <div class="trends-grid">
                        <div class="trend-card">
                            <h3 class="trend-title">
                                <a href="ai.html" style="text-decoration: none; color: inherit;">
                                    人工智能
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
                                    雲原生
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
                        <div class="trend-card">
                            <h3 class="trend-title">
                                <a href="frontend.html" style="text-decoration: none; color: inherit;">
                                    前端開發
                                </a>
                            </h3>
                            <p class="trend-description">
                                React、Vue.js 和現代前端框架的演進趨勢和技術選型
                            </p>
                            <div class="trend-stats">
                                <span>相關會議: 4</span>
                                <a href="frontend.html" class="trend-tag">查看詳情</a>
                            </div>
                        </div>
                        <div class="trend-card">
                            <h3 class="trend-title">
                                <a href="database.html" style="text-decoration: none; color: inherit;">
                                    數據庫技術
                                </a>
                            </h3>
                            <p class="trend-description">
                                分佈式數據庫、OLAP 系統和數據處理技術的新發展
                            </p>
                            <div class="trend-stats">
                                <span>相關會議: 3</span>
                                <a href="database.html" class="trend-tag">查看詳情</a>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- 返回導航 -->
                <nav class="nav-buttons">
                    <div class="nav-prev">
                        <a href="../index.html" class="nav-btn">← 返回首頁</a>
                    </div>
                    <div class="nav-next">
                        <a href="../sessions/index.html" class="nav-btn">查看所有會議 →</a>
                    </div>
                </nav>
            </div>
        </div>
    </main>

    <!-- 頁腳 -->
    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope 技術趨勢分析. 由 TrendScope 技術趨勢分析系統生成。</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>"""

    with open(trends_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(trends_index_content)

    logger.info("✅ 技術趨勢列表頁面已創建")
