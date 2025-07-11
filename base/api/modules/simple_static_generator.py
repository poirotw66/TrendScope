#!/usr/bin/env python3
"""
簡化的靜態網站生成器
實現 plan.md 三階層架構，不依賴外部 Hugo 二進制
"""

import logging
import pathlib
import zipfile
import shutil
import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import markdown
from jinja2 import Template

logger = logging.getLogger(__name__)

@dataclass
class PageMetadata:
    """頁面元數據"""
    title: str
    seminar: str = ""
    category: str = ""
    url: str = ""
    date: str = ""
    tags: List[str] = None
    trends: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.trends is None:
            self.trends = []
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")

class SimpleStaticGenerator:
    """簡化的靜態網站生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.md_processor = markdown.Markdown(extensions=['meta', 'toc', 'tables'])
        
    def generate_three_tier_site(self, md_dir: str, html_dir: str, 
                                template_style: str = "professional",
                                create_offline_package: bool = True) -> Dict[str, Any]:
        """
        生成三階層靜態網站
        
        Args:
            md_dir: Markdown 文件目錄
            html_dir: HTML 輸出目錄
            template_style: 模板樣式
            create_offline_package: 是否創建離線包
            
        Returns:
            生成結果字典
        """
        try:
            logger.info(f"🏗️ 開始生成三階層靜態網站...")
            logger.info(f"   📂 Markdown 目錄: {md_dir}")
            logger.info(f"   📂 HTML 輸出目錄: {html_dir}")
            logger.info(f"   🎨 模板樣式: {template_style}")
            
            # 1. 掃描和解析 Markdown 文件
            content_data = self._scan_and_parse_markdown_files(md_dir)
            
            # 2. 構建三階層網站結構
            site_structure = self._build_three_tier_structure(content_data)
            
            # 3. 創建輸出目錄
            html_path = pathlib.Path(html_dir)
            html_path.mkdir(parents=True, exist_ok=True)
            
            # 4. 生成靜態資源
            self._create_static_assets(html_path, template_style)
            
            # 5. 渲染並寫入 HTML 頁面
            html_files = self._render_and_write_pages(site_structure, html_path, template_style)
            
            # 6. 創建離線包
            result = {
                "html_files": html_files,
                "output_dir": str(html_path),
                "site_info": {
                    "total_pages": len(html_files),
                    "template_style": template_style,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
            if create_offline_package:
                zip_file = self._create_offline_package(html_path)
                if zip_file:
                    result["zip_file"] = zip_file
                    
                launcher_file = self._create_launcher(html_path)
                if launcher_file:
                    result["launcher_file"] = launcher_file
            
            logger.info(f"✅ 三階層靜態網站生成完成!")
            logger.info(f"   📄 生成 {len(html_files)} 個 HTML 文件")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 靜態網站生成失敗: {e}")
            raise
    
    def _scan_and_parse_markdown_files(self, md_dir: str) -> Dict[str, Any]:
        """掃描和解析 Markdown 文件"""
        md_path = pathlib.Path(md_dir)
        content_data = {
            "homepage": None,
            "trends_analysis": None,
            "trend_pages": [],
            "session_pages": [],
            "other_pages": []
        }
        
        for md_file in md_path.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析 Markdown 內容
                html_content = self.md_processor.convert(content)
                metadata = self._extract_metadata(content, md_file.name)
                
                page_data = {
                    "filename": md_file.name,
                    "metadata": metadata,
                    "content": content,
                    "html_content": html_content
                }
                
                # 根據文件名分類
                if md_file.name == "_index.md":
                    content_data["homepage"] = page_data
                elif md_file.name == "trends-analysis.md":
                    content_data["trends_analysis"] = page_data
                elif md_file.name.startswith("trend-"):
                    content_data["trend_pages"].append(page_data)
                elif md_file.name.startswith("session-"):
                    content_data["session_pages"].append(page_data)
                else:
                    content_data["other_pages"].append(page_data)
                    
            except Exception as e:
                logger.warning(f"解析 Markdown 文件失敗 {md_file}: {e}")
        
        logger.info(f"📄 解析完成: 首頁={1 if content_data['homepage'] else 0}, "
                   f"趨勢分析={1 if content_data['trends_analysis'] else 0}, "
                   f"趨勢頁面={len(content_data['trend_pages'])}, "
                   f"會議頁面={len(content_data['session_pages'])}")
        
        return content_data
    
    def _extract_metadata(self, content: str, filename: str) -> PageMetadata:
        """從內容中提取元數據"""
        # 提取標題
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename.replace('.md', '')
        
        # 提取研討會信息
        seminar_match = re.search(r'研討會[：:]\s*\*?\*?(.+?)\*?\*?$', content, re.MULTILINE)
        seminar = seminar_match.group(1).strip() if seminar_match else ""
        
        # 提取類型信息
        category_match = re.search(r'類型[：:]\s*\*?\*?(.+?)\*?\*?$', content, re.MULTILINE)
        category = category_match.group(1).strip() if category_match else ""
        
        # 提取 URL
        url_match = re.search(r'來源[：:]\s*\[(.+?)\]\((.+?)\)', content)
        url = url_match.group(2) if url_match else ""
        
        return PageMetadata(
            title=title,
            seminar=seminar,
            category=category,
            url=url
        )
    
    def _build_three_tier_structure(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """構建三階層網站結構"""
        structure = {
            "homepage": content_data["homepage"],
            "trends_analysis": content_data["trends_analysis"],
            "trend_categories": {},
            "sessions": {},
            "navigation": {
                "main_menu": [
                    {"name": "首頁", "url": "/", "active": False},
                    {"name": "技術趨勢", "url": "/trends/", "active": False},
                    {"name": "會議報告", "url": "/sessions/", "active": False}
                ],
                "trend_menu": [],
                "breadcrumbs": {}
            }
        }
        
        # 處理趨勢分類頁面
        for trend_page in content_data["trend_pages"]:
            trend_name = trend_page["filename"].replace("trend-", "").replace(".md", "")
            structure["trend_categories"][trend_name] = trend_page
            structure["navigation"]["trend_menu"].append({
                "name": trend_page["metadata"].title,
                "url": f"/trends/{trend_name}.html",
                "trend_key": trend_name
            })
        
        # 處理會議頁面
        for session_page in content_data["session_pages"]:
            session_id = session_page["filename"].replace("session-", "").replace(".md", "")
            structure["sessions"][session_id] = session_page
        
        return structure
    
    def _create_static_assets(self, html_path: pathlib.Path, template_style: str):
        """創建靜態資源文件"""
        # 創建 CSS 目錄
        css_dir = html_path / "css"
        css_dir.mkdir(exist_ok=True)
        
        # 創建主要樣式文件
        main_css = self._generate_main_css(template_style)
        with open(css_dir / "main.css", 'w', encoding='utf-8') as f:
            f.write(main_css)
        
        # 創建 JavaScript 目錄
        js_dir = html_path / "js"
        js_dir.mkdir(exist_ok=True)
        
        # 創建主要 JavaScript 文件
        main_js = self._generate_main_js()
        with open(js_dir / "main.js", 'w', encoding='utf-8') as f:
            f.write(main_js)
        
        logger.info("✅ 靜態資源文件創建完成")
    
    def _render_and_write_pages(self, site_structure: Dict[str, Any], 
                               html_path: pathlib.Path, template_style: str) -> List[str]:
        """渲染並寫入 HTML 頁面"""
        html_files = []
        
        # 1. 渲染首頁
        if site_structure["homepage"]:
            homepage_html = self._render_homepage(site_structure, template_style)
            homepage_file = html_path / "index.html"
            with open(homepage_file, 'w', encoding='utf-8') as f:
                f.write(homepage_html)
            html_files.append(str(homepage_file))
        
        # 2. 創建趨勢目錄並渲染趨勢頁面
        trends_dir = html_path / "trends"
        trends_dir.mkdir(exist_ok=True)
        
        for trend_key, trend_data in site_structure["trend_categories"].items():
            trend_html = self._render_trend_page(trend_data, site_structure, template_style)
            trend_file = trends_dir / f"{trend_key}.html"
            with open(trend_file, 'w', encoding='utf-8') as f:
                f.write(trend_html)
            html_files.append(str(trend_file))
        
        # 3. 創建會議目錄並渲染會議頁面
        sessions_dir = html_path / "sessions"
        sessions_dir.mkdir(exist_ok=True)
        
        for session_id, session_data in site_structure["sessions"].items():
            session_html = self._render_session_page(session_data, site_structure, template_style)
            session_file = sessions_dir / f"{session_id}.html"
            with open(session_file, 'w', encoding='utf-8') as f:
                f.write(session_html)
            html_files.append(str(session_file))
        
        # 4. 渲染趨勢分析頁面（如果存在）
        if site_structure["trends_analysis"]:
            analysis_html = self._render_analysis_page(site_structure["trends_analysis"], 
                                                     site_structure, template_style)
            analysis_file = html_path / "trends-analysis.html"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(analysis_html)
            html_files.append(str(analysis_file))
        
        return html_files

    def _render_homepage(self, site_structure: Dict[str, Any], template_style: str) -> str:
        """渲染首頁"""
        homepage_data = site_structure["homepage"]

        template = Template("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - TrendScope 技術趨勢分析</title>
    <link rel="stylesheet" href="css/main.css">
</head>
<body class="{{ template_style }}">
    <header class="site-header">
        <nav class="main-nav">
            <div class="nav-brand">
                <h1>TrendScope</h1>
                <p>技術趨勢分析</p>
            </div>
            <ul class="nav-menu">
                {% for item in navigation.main_menu %}
                <li><a href="{{ item.url }}" {% if item.url == '/' %}class="active"{% endif %}>{{ item.name }}</a></li>
                {% endfor %}
            </ul>
        </nav>
    </header>

    <main class="main-content">
        <section class="hero-section">
            <div class="container">
                <h1>{{ title }}</h1>
                <div class="content">
                    {{ content | safe }}
                </div>
            </div>
        </section>

        <section class="trends-section">
            <div class="container">
                <h2>技術趨勢分類</h2>
                <div class="trends-grid">
                    {% for trend in navigation.trend_menu %}
                    <div class="trend-card">
                        <h3><a href="{{ trend.url }}">{{ trend.name }}</a></h3>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TrendScope. 由 NeoTrendHub 自動生成</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
        """)

        return template.render(
            title=homepage_data["metadata"].title if homepage_data else "技術趨勢分析",
            content=homepage_data["html_content"] if homepage_data else "",
            navigation=site_structure["navigation"],
            template_style=template_style
        )

    def _render_trend_page(self, trend_data: Dict[str, Any],
                          site_structure: Dict[str, Any], template_style: str) -> str:
        """渲染趨勢分類頁面"""
        template = Template("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - TrendScope</title>
    <link rel="stylesheet" href="../css/main.css">
</head>
<body class="{{ template_style }}">
    <header class="site-header">
        <nav class="main-nav">
            <div class="nav-brand">
                <h1><a href="../">TrendScope</a></h1>
            </div>
            <ul class="nav-menu">
                {% for item in navigation.main_menu %}
                <li><a href="../{{ item.url.lstrip('/') }}" {% if '/trends/' in item.url %}class="active"{% endif %}>{{ item.name }}</a></li>
                {% endfor %}
            </ul>
        </nav>
    </header>

    <main class="main-content">
        <div class="container">
            <nav class="breadcrumb">
                <a href="../">首頁</a> > <a href="../trends/">技術趨勢</a> > {{ title }}
            </nav>

            <article class="trend-article">
                <header>
                    <h1>{{ title }}</h1>
                </header>
                <div class="content">
                    {{ content | safe }}
                </div>
            </article>

            <aside class="sidebar">
                <h3>其他趨勢</h3>
                <ul class="trend-links">
                    {% for trend in navigation.trend_menu %}
                    <li><a href="{{ trend.url.replace('/trends/', '') }}">{{ trend.name }}</a></li>
                    {% endfor %}
                </ul>
            </aside>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p><a href="../">返回首頁</a> | &copy; 2024 TrendScope</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>
        """)

        return template.render(
            title=trend_data["metadata"].title,
            content=trend_data["html_content"],
            navigation=site_structure["navigation"],
            template_style=template_style
        )

    def _render_session_page(self, session_data: Dict[str, Any],
                           site_structure: Dict[str, Any], template_style: str) -> str:
        """渲染會議詳細頁面"""
        template = Template("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - TrendScope</title>
    <link rel="stylesheet" href="../css/main.css">
</head>
<body class="{{ template_style }}">
    <header class="site-header">
        <nav class="main-nav">
            <div class="nav-brand">
                <h1><a href="../">TrendScope</a></h1>
            </div>
            <ul class="nav-menu">
                {% for item in navigation.main_menu %}
                <li><a href="../{{ item.url.lstrip('/') }}" {% if '/sessions/' in item.url %}class="active"{% endif %}>{{ item.name }}</a></li>
                {% endfor %}
            </ul>
        </nav>
    </header>

    <main class="main-content">
        <div class="container">
            <nav class="breadcrumb">
                <a href="../">首頁</a> > <a href="../sessions/">會議報告</a> > {{ title }}
            </nav>

            <article class="session-article">
                <header>
                    <h1>{{ title }}</h1>
                    {% if metadata.seminar %}
                    <p class="seminar">研討會：{{ metadata.seminar }}</p>
                    {% endif %}
                    {% if metadata.category %}
                    <p class="category">類型：{{ metadata.category }}</p>
                    {% endif %}
                </header>
                <div class="content">
                    {{ content | safe }}
                </div>
            </article>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p><a href="../">返回首頁</a> | &copy; 2024 TrendScope</p>
        </div>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>
        """)

        return template.render(
            title=session_data["metadata"].title,
            content=session_data["html_content"],
            metadata=session_data["metadata"],
            navigation=site_structure["navigation"],
            template_style=template_style
        )

    def _render_analysis_page(self, analysis_data: Dict[str, Any],
                            site_structure: Dict[str, Any], template_style: str) -> str:
        """渲染趨勢分析頁面"""
        template = Template("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - TrendScope</title>
    <link rel="stylesheet" href="css/main.css">
</head>
<body class="{{ template_style }}">
    <header class="site-header">
        <nav class="main-nav">
            <div class="nav-brand">
                <h1><a href="/">TrendScope</a></h1>
            </div>
            <ul class="nav-menu">
                {% for item in navigation.main_menu %}
                <li><a href="{{ item.url }}">{{ item.name }}</a></li>
                {% endfor %}
            </ul>
        </nav>
    </header>

    <main class="main-content">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">首頁</a> > 趨勢分析
            </nav>

            <article class="analysis-article">
                <header>
                    <h1>{{ title }}</h1>
                </header>
                <div class="content">
                    {{ content | safe }}
                </div>
            </article>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p><a href="/">返回首頁</a> | &copy; 2024 TrendScope</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
        """)

        return template.render(
            title=analysis_data["metadata"].title,
            content=analysis_data["html_content"],
            navigation=site_structure["navigation"],
            template_style=template_style
        )

    def _generate_main_css(self, template_style: str) -> str:
        """生成主要 CSS 樣式"""
        base_css = """
/* 基礎樣式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang TC', 'Microsoft JhengHei', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 頭部樣式 */
.site-header {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.main-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand h1 {
    font-size: 1.8rem;
    margin-bottom: 0.2rem;
}

.nav-brand p {
    font-size: 0.9rem;
    opacity: 0.8;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.nav-menu a:hover,
.nav-menu a.active {
    background-color: rgba(255,255,255,0.2);
}

/* 主要內容 */
.main-content {
    min-height: calc(100vh - 200px);
    padding: 2rem 0;
}

/* 英雄區塊 */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    text-align: center;
}

.hero-section h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* 趨勢網格 */
.trends-section {
    padding: 4rem 0;
}

.trends-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.trend-card {
    background: white;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
}

.trend-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.trend-card h3 a {
    color: #2c3e50;
    text-decoration: none;
    font-size: 1.3rem;
}

/* 麵包屑 */
.breadcrumb {
    margin-bottom: 2rem;
    font-size: 0.9rem;
}

.breadcrumb a {
    color: #3498db;
    text-decoration: none;
}

.breadcrumb a:hover {
    text-decoration: underline;
}

/* 文章樣式 */
.trend-article,
.session-article,
.analysis-article {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.trend-article header,
.session-article header,
.analysis-article header {
    margin-bottom: 2rem;
    border-bottom: 2px solid #3498db;
    padding-bottom: 1rem;
}

.trend-article h1,
.session-article h1,
.analysis-article h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.seminar,
.category {
    color: #7f8c8d;
    font-size: 1rem;
    margin: 0.5rem 0;
}

/* 內容樣式 */
.content h2 {
    color: #2c3e50;
    margin: 2rem 0 1rem 0;
    font-size: 1.8rem;
}

.content h3 {
    color: #34495e;
    margin: 1.5rem 0 1rem 0;
    font-size: 1.4rem;
}

.content p {
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.content ul,
.content ol {
    margin: 1rem 0 1rem 2rem;
}

.content li {
    margin-bottom: 0.5rem;
}

/* 側邊欄 */
.sidebar {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 2rem;
}

.sidebar h3 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.trend-links {
    list-style: none;
}

.trend-links li {
    margin-bottom: 0.5rem;
}

.trend-links a {
    color: #3498db;
    text-decoration: none;
    padding: 0.3rem 0;
    display: block;
}

.trend-links a:hover {
    text-decoration: underline;
}

/* 頁腳 */
.site-footer {
    background: #34495e;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 4rem;
}

.site-footer a {
    color: #3498db;
    text-decoration: none;
}

/* 響應式設計 */
@media (max-width: 768px) {
    .main-nav {
        flex-direction: column;
        gap: 1rem;
    }

    .nav-menu {
        gap: 1rem;
    }

    .hero-section h1 {
        font-size: 2rem;
    }

    .trends-grid {
        grid-template-columns: 1fr;
    }

    .container {
        padding: 0 15px;
    }
}
        """

        # 根據模板樣式添加特定樣式
        if template_style == "technical":
            base_css += """
/* 技術風格 */
.technical {
    background-color: #f8f9fa;
}

.technical .site-header {
    background: #1a252f;
}

.technical .hero-section {
    background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
}
            """
        elif template_style == "concise":
            base_css += """
/* 簡潔風格 */
.concise .trend-card,
.concise .trend-article,
.concise .session-article {
    border: none;
    box-shadow: none;
    border-left: 4px solid #3498db;
}
            """

        return base_css

    def _generate_main_js(self) -> str:
        """生成主要 JavaScript 文件"""
        return """
// 主要 JavaScript 功能
document.addEventListener('DOMContentLoaded', function() {
    // 平滑滾動
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // 返回頂部按鈕
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '↑';
    backToTop.className = 'back-to-top';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #3498db;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        display: none;
        z-index: 1000;
        font-size: 18px;
    `;

    document.body.appendChild(backToTop);

    // 顯示/隱藏返回頂部按鈕
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });

    // 返回頂部功能
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // 簡單的搜索功能（如果有搜索框）
    const searchInput = document.querySelector('#search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const articles = document.querySelectorAll('article, .trend-card');

            articles.forEach(article => {
                const text = article.textContent.toLowerCase();
                if (text.includes(query) || query === '') {
                    article.style.display = 'block';
                } else {
                    article.style.display = 'none';
                }
            });
        });
    }
});
        """

    def _create_offline_package(self, html_path: pathlib.Path) -> Optional[str]:
        """創建離線包"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"TrendScope-會議報告-{timestamp}.zip"
            zip_path = html_path.parent / zip_filename

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in html_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(html_path)
                        zipf.write(file_path, arcname)

            logger.info(f"✅ 離線包創建完成: {zip_filename}")
            return str(zip_path)

        except Exception as e:
            logger.error(f"❌ 創建離線包失敗: {e}")
            return None

    def _create_launcher(self, html_path: pathlib.Path) -> Optional[str]:
        """創建啟動器文件"""
        try:
            launcher_content = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendScope 報告啟動器</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .launcher {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        .logo {
            font-size: 2.5rem;
            color: #3498db;
            margin-bottom: 20px;
        }
        .description {
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        .launch-button {
            background: #3498db;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 1.1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s;
        }
        .launch-button:hover {
            background: #2980b9;
        }
        .instructions {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="launcher">
        <div class="logo">🚀 TrendScope</div>
        <h1>技術趨勢分析報告</h1>
        <p class="description">
            歡迎使用 TrendScope 技術趨勢分析報告。<br>
            這是一個離線版本，您可以在沒有網路連接的情況下瀏覽所有內容。
        </p>

        <a href="index.html" class="launch-button">開始瀏覽報告</a>

        <div class="instructions">
            <h3>使用說明：</h3>
            <ul>
                <li>點擊上方按鈕開始瀏覽報告</li>
                <li>使用導航菜單在不同頁面間切換</li>
                <li>所有內容都已離線化，無需網路連接</li>
                <li>建議使用現代瀏覽器以獲得最佳體驗</li>
            </ul>
        </div>
    </div>

    <script>
        // 自動檢測並跳轉
        setTimeout(function() {
            if (confirm('是否自動開啟報告？')) {
                window.location.href = 'index.html';
            }
        }, 3000);
    </script>
</body>
</html>
            """

            launcher_path = html_path / "launcher.html"
            with open(launcher_path, 'w', encoding='utf-8') as f:
                f.write(launcher_content)

            logger.info("✅ 啟動器文件創建完成")
            return str(launcher_path)

        except Exception as e:
            logger.error(f"❌ 創建啟動器失敗: {e}")
            return None
