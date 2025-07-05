"""
Hugo-based Static Site Generation for Batch Reports

This module replaces the traditional Markdown-to-HTML conversion with Hugo SSG,
providing a three-layer structure (homepage, topic categories, individual meeting details)
while maintaining compatibility with existing batch report functionality.
"""

import os
import sys
import json
import yaml
import shutil
import logging
import pathlib
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# 設置日誌
logger = logging.getLogger("hugo-report-generator")

@dataclass
class HugoSiteConfig:
    """Hugo 網站配置"""
    base_url: str = "/"
    language_code: str = "zh-tw"
    title: str = "TrendScope 會議報告"
    theme: str = "trendscope"
    output_dir: str = "public"
    content_dir: str = "content"
    static_dir: str = "static"
    layouts_dir: str = "layouts"
    
@dataclass
class ReportMetadata:
    """報告元數據"""
    title: str
    seminar: str
    category: str = "主題演講"
    date: str = ""
    url: str = ""
    session_id: str = ""
    analysis_mode: str = "comprehensive"
    template_style: str = "professional"
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")

class HugoReportGenerator:
    """Hugo 靜態網站生成器"""
    
    def __init__(self, hugo_binary: str = "hugo"):
        """
        初始化 Hugo 報告生成器
        
        Args:
            hugo_binary: Hugo 二進制文件路徑
        """
        self.hugo_binary = hugo_binary
        self.config = HugoSiteConfig()
        self._verify_hugo_installation()
        
    def _verify_hugo_installation(self):
        """驗證 Hugo 是否已安裝"""
        try:
            result = subprocess.run([self.hugo_binary, "version"], 
                                  capture_output=True, text=True, check=True)
            logger.info(f"Hugo 版本: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"Hugo 未安裝或無法執行: {e}")
    
    def generate_hugo_site(self, md_dir: str, output_dir: str,
                          template_style: str = "professional") -> List[str]:
        """
        生成 Hugo 靜態網站
        
        Args:
            md_dir: Markdown 文件目錄
            output_dir: 輸出目錄
            template_style: 模板樣式
            
        Returns:
            生成的 HTML 文件列表
        """
        try:
            # 創建臨時 Hugo 網站目錄
            site_dir = pathlib.Path(output_dir).parent / "hugo_site"
            
            # 初始化 Hugo 網站結構
            self._initialize_hugo_site(site_dir, template_style)
            
            # 處理 Markdown 文件並生成內容
            html_files = self._process_markdown_files(md_dir, site_dir, template_style)
            
            # 生成 Hugo 網站
            self._build_hugo_site(site_dir, output_dir)
            
            # 清理臨時目錄
            if site_dir.exists():
                shutil.rmtree(site_dir)
                
            return html_files
            
        except Exception as e:
            logger.error(f"Hugo 網站生成失敗: {e}")
            raise
    
    def _initialize_hugo_site(self, site_dir: pathlib.Path, template_style: str):
        """初始化 Hugo 網站結構"""
        # 創建基本目錄結構
        site_dir.mkdir(parents=True, exist_ok=True)
        
        # 創建必要的子目錄
        for subdir in ["content", "layouts", "static", "data", "archetypes"]:
            (site_dir / subdir).mkdir(exist_ok=True)
        
        # 創建 Hugo 配置文件
        self._create_hugo_config(site_dir, template_style)
        
        # 創建佈局模板
        self._create_hugo_layouts(site_dir, template_style)

        # 創建部分模板
        self.create_partials(site_dir / "layouts")

        # 創建靜態資源
        self._create_static_assets(site_dir, template_style)

        # 生成示例內容
        self.generate_sample_content(site_dir)
    
    def _create_hugo_config(self, site_dir: pathlib.Path, template_style: str):
        """創建 Hugo 配置文件"""
        config = {
            "baseURL": self.config.base_url,
            "languageCode": self.config.language_code,
            "title": self.config.title,
            # "theme": self.config.theme,  # 不使用外部主題，直接使用佈局
            "publishDir": self.config.output_dir,
            "contentDir": self.config.content_dir,
            "staticDir": self.config.static_dir,
            "layoutDir": self.config.layouts_dir,
            "defaultContentLanguage": "zh-tw",
            "hasCJKLanguage": True,
            "enableRobotsTXT": True,
            "enableGitInfo": False,
            "params": {
                "template_style": template_style,
                "style_config": self.get_template_style_config(template_style),
                "generator": "TrendScope Hugo Generator",
                "version": "1.0.0",
                "description": "AI 驅動的會議報告分析平台",
                "features": {
                    "block_based_design": True,
                    "responsive_layout": True,
                    "dark_mode_support": True,
                    "multi_language": True
                }
            },
            "markup": {
                "goldmark": {
                    "renderer": {
                        "unsafe": True
                    }
                }
            },
            "taxonomies": {
                "seminar": "seminars",
                "category": "categories",
                "tag": "tags"
            },
            "menu": {
                "main": [
                    {"name": "首頁", "url": "/", "weight": 10},
                    {"name": "研討會", "url": "/seminars/", "weight": 20},
                    {"name": "分類", "url": "/categories/", "weight": 30},
                    {"name": "標籤", "url": "/tags/", "weight": 40}
                ]
            }
        }
        
        # 支援多語言配置
        config["languages"] = {
            "zh-tw": {
                "languageName": "繁體中文",
                "weight": 1,
                "title": "TrendScope 會議報告"
            },
            "zh-cn": {
                "languageName": "简体中文", 
                "weight": 2,
                "title": "TrendScope 会议报告"
            },
            "en": {
                "languageName": "English",
                "weight": 3,
                "title": "TrendScope Conference Reports"
            }
        }
        
        config_file = site_dir / "hugo.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def _create_hugo_layouts(self, site_dir: pathlib.Path, template_style: str):
        """創建 Hugo 佈局模板"""
        layouts_dir = site_dir / "layouts"
        
        # 創建基礎佈局
        self._create_base_layout(layouts_dir, template_style)
        
        # 創建首頁佈局
        self._create_index_layout(layouts_dir, template_style)
        
        # 創建單頁佈局
        self._create_single_layout(layouts_dir, template_style)
        
        # 創建列表佈局
        self._create_list_layout(layouts_dir, template_style)
        
        # 創建分類佈局
        self._create_taxonomy_layouts(layouts_dir, template_style)
    
    def _create_base_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建基礎佈局模板"""
        base_layout = '''<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ if .Title }}{{ .Title }} - {{ end }}{{ .Site.Title }}</title>
    <meta name="description" content="{{ .Description | default .Site.Params.description }}">
    <meta name="generator" content="{{ .Site.Params.generator }}">
    
    <!-- CSS Styles -->
    <link rel="stylesheet" href="{{ "css/styles.css" | relURL }}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ "favicon.ico" | relURL }}">
</head>
<body class="template-{{ .Site.Params.template_style }}">
    <div class="container">
        {{ partial "header.html" . }}
        
        <main class="content">
            {{ block "main" . }}{{ end }}
        </main>
        
        {{ partial "footer.html" . }}
    </div>
    
    <!-- JavaScript -->
    <script src="{{ "js/main.js" | relURL }}"></script>
</body>
</html>'''
        
        (layouts_dir / "_default").mkdir(exist_ok=True)
        with open(layouts_dir / "_default" / "baseof.html", 'w', encoding='utf-8') as f:
            f.write(base_layout)
    
    def _create_static_assets(self, site_dir: pathlib.Path, template_style: str):
        """創建靜態資源文件"""
        static_dir = site_dir / "static"
        
        # 創建 CSS 目錄
        css_dir = static_dir / "css"
        css_dir.mkdir(exist_ok=True)
        
        # 創建 JS 目錄
        js_dir = static_dir / "js"
        js_dir.mkdir(exist_ok=True)
        
        # 創建樣式文件（基於現有的 sample_630.html 設計）
        self._create_css_styles(css_dir, template_style)
        
        # 創建 JavaScript 文件
        self._create_javascript(js_dir)

    def _create_css_styles(self, css_dir: pathlib.Path, template_style: str):
        """創建 CSS 樣式文件（基於 sample_630.html 設計）"""
        # 從現有的 batch_md_to_html 模組獲取樣式
        try:
            from src.batch_md_to_html import get_css_styles
            css_content = get_css_styles(template_style)
        except ImportError:
            # 如果無法導入，使用基本樣式
            css_content = self._get_default_css_styles(template_style)

        with open(css_dir / "styles.css", 'w', encoding='utf-8') as f:
            f.write(css_content)

    def _get_default_css_styles(self, template_style: str) -> str:
        """獲取默認 CSS 樣式"""
        return """
        /* TrendScope Hugo Theme - Default Styles */
        :root {
            --primary: #3a86ff;
            --primary-dark: #0048b3;
            --secondary: #00bfff;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #0ea5e9;
            --tech: #9333ea;
            --practical: #ec4899;
            --text: #2d3748;
            --text-light: #475569;
            --text-lighter: #94a3b8;
            --bg: #f0f4f8;
            --card: #fff;
            --border: #e2e8f0;
            --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.1);
            --transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'Roboto', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .section-block {
            background-color: var(--card);
            padding: 35px;
            border-radius: var(--radius-lg);
            margin-bottom: 40px;
            border-left: 5px solid var(--primary);
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        .section-block:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1);
        }
        """

    def _create_javascript(self, js_dir: pathlib.Path):
        """創建 JavaScript 文件"""
        js_content = """
        // TrendScope Hugo Theme JavaScript
        document.addEventListener('DOMContentLoaded', function() {
            // 初始化主題功能
            initializeTheme();
            initializeNavigation();
            initializeSearch();
        });

        function initializeTheme() {
            // 主題切換功能
            const themeToggle = document.querySelector('.theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', toggleTheme);
            }
        }

        function initializeNavigation() {
            // 導航功能
            const navToggle = document.querySelector('.nav-toggle');
            const navMenu = document.querySelector('.nav-menu');

            if (navToggle && navMenu) {
                navToggle.addEventListener('click', function() {
                    navMenu.classList.toggle('active');
                });
            }
        }

        function initializeSearch() {
            // 搜索功能
            const searchInput = document.querySelector('.search-input');
            if (searchInput) {
                searchInput.addEventListener('input', handleSearch);
            }
        }

        function toggleTheme() {
            document.body.classList.toggle('dark-theme');
            localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
        }

        function handleSearch(event) {
            const query = event.target.value.toLowerCase();
            // 實現搜索邏輯
            console.log('搜索查詢:', query);
        }
        """

        with open(js_dir / "main.js", 'w', encoding='utf-8') as f:
            f.write(js_content)

    def _create_index_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建首頁佈局"""
        index_layout = '''{{ define "main" }}
<div class="homepage">
    <section class="hero section-block">
        <h1 class="hero-title">{{ .Site.Title }}</h1>
        <p class="hero-subtitle">{{ .Site.Params.description }}</p>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.RegularPages }}</span>
                <span class="stat-label">會議報告</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.Taxonomies.seminars }}</span>
                <span class="stat-label">研討會</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.Taxonomies.categories }}</span>
                <span class="stat-label">分類</span>
            </div>
        </div>
    </section>

    <section class="recent-reports section-block">
        <h2 class="section-title">最新報告</h2>
        <div class="reports-grid">
            {{ range first 6 .Site.RegularPages }}
            <article class="report-card">
                <h3 class="report-title">
                    <a href="{{ .Permalink }}">{{ .Title }}</a>
                </h3>
                <div class="report-meta">
                    <span class="seminar">{{ .Params.seminar }}</span>
                    <span class="date">{{ .Date.Format "2006-01-02" }}</span>
                </div>
                <p class="report-excerpt">{{ .Summary | truncate 150 }}</p>
                <div class="report-tags">
                    {{ range .Params.tags }}
                    <span class="tag">{{ . }}</span>
                    {{ end }}
                </div>
            </article>
            {{ end }}
        </div>
    </section>

    <section class="seminars-overview section-block">
        <h2 class="section-title">研討會分類</h2>
        <div class="seminars-grid">
            {{ range .Site.Taxonomies.seminars }}
            <div class="seminar-card">
                <h3 class="seminar-name">
                    <a href="{{ .Page.Permalink }}">{{ .Page.Title }}</a>
                </h3>
                <span class="seminar-count">{{ .Count }} 場會議</span>
            </div>
            {{ end }}
        </div>
    </section>
</div>
{{ end }}'''

        with open(layouts_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_layout)

    def _create_single_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建單頁佈局"""
        single_layout = '''{{ define "main" }}
<article class="single-report">
    <header class="report-header section-block meeting-info">
        <h1 class="report-title">{{ .Title }}</h1>
        <div class="report-meta">
            <div class="meta-item">
                <strong>研討會：</strong> {{ .Params.seminar }}
            </div>
            <div class="meta-item">
                <strong>類型：</strong> {{ .Params.category | default "主題演講" }}
            </div>
            <div class="meta-item">
                <strong>日期：</strong> {{ .Date.Format "2006年01月02日" }}
            </div>
            {{ if .Params.url }}
            <div class="meta-item">
                <strong>來源：</strong> <a href="{{ .Params.url }}" target="_blank">{{ .Params.url }}</a>
            </div>
            {{ end }}
        </div>
        {{ if .Params.tags }}
        <div class="report-tags">
            {{ range .Params.tags }}
            <a href="{{ "/tags/" | relURL }}{{ . | urlize }}" class="tag">{{ . }}</a>
            {{ end }}
        </div>
        {{ end }}
    </header>

    <div class="report-content">
        {{ .Content }}
    </div>

    <footer class="report-footer section-block">
        <div class="report-navigation">
            {{ with .PrevInSection }}
            <a href="{{ .Permalink }}" class="nav-link prev">
                <span class="nav-label">上一篇</span>
                <span class="nav-title">{{ .Title }}</span>
            </a>
            {{ end }}

            {{ with .NextInSection }}
            <a href="{{ .Permalink }}" class="nav-link next">
                <span class="nav-label">下一篇</span>
                <span class="nav-title">{{ .Title }}</span>
            </a>
            {{ end }}
        </div>

        <div class="report-info">
            <p><em>本報告由 TrendScope 自動生成 | 生成時間：{{ .Date.Format "2006-01-02 15:04:05" }}</em></p>
        </div>
    </footer>
</article>
{{ end }}'''

        (layouts_dir / "_default").mkdir(exist_ok=True)
        with open(layouts_dir / "_default" / "single.html", 'w', encoding='utf-8') as f:
            f.write(single_layout)

    def _create_list_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建列表佈局"""
        list_layout = '''{{ define "main" }}
<div class="list-page">
    <header class="page-header section-block">
        <h1 class="page-title">{{ .Title }}</h1>
        {{ if .Content }}
        <div class="page-description">
            {{ .Content }}
        </div>
        {{ end }}
        <div class="page-stats">
            <span class="stat">共 {{ len .Pages }} 篇報告</span>
        </div>
    </header>

    <div class="reports-list">
        {{ range .Pages }}
        <article class="report-item section-block">
            <h2 class="report-title">
                <a href="{{ .Permalink }}">{{ .Title }}</a>
            </h2>
            <div class="report-meta">
                <span class="seminar">{{ .Params.seminar }}</span>
                <span class="category">{{ .Params.category | default "主題演講" }}</span>
                <span class="date">{{ .Date.Format "2006-01-02" }}</span>
            </div>
            <div class="report-excerpt">
                {{ .Summary | truncate 200 }}
            </div>
            {{ if .Params.tags }}
            <div class="report-tags">
                {{ range .Params.tags }}
                <a href="{{ "/tags/" | relURL }}{{ . | urlize }}" class="tag">{{ . }}</a>
                {{ end }}
            </div>
            {{ end }}
            <a href="{{ .Permalink }}" class="read-more">閱讀全文 →</a>
        </article>
        {{ end }}
    </div>
</div>
{{ end }}'''

        with open(layouts_dir / "_default" / "list.html", 'w', encoding='utf-8') as f:
            f.write(list_layout)

    def _create_taxonomy_layouts(self, layouts_dir: pathlib.Path, template_style: str):
        """創建分類佈局"""
        # 創建研討會分類佈局
        seminars_dir = layouts_dir / "seminars"
        seminars_dir.mkdir(exist_ok=True)

        seminar_list_layout = '''{{ define "main" }}
<div class="seminars-page">
    <header class="page-header section-block">
        <h1 class="page-title">研討會分類</h1>
        <p class="page-description">按研討會瀏覽所有會議報告</p>
    </header>

    <div class="seminars-grid">
        {{ range .Data.Terms.Alphabetical }}
        <div class="seminar-card section-block">
            <h2 class="seminar-name">
                <a href="{{ .Page.Permalink }}">{{ .Page.Title }}</a>
            </h2>
            <div class="seminar-stats">
                <span class="count">{{ .Count }} 場會議</span>
            </div>
            <div class="seminar-preview">
                {{ range first 3 .Pages }}
                <div class="preview-item">
                    <a href="{{ .Permalink }}">{{ .Title }}</a>
                </div>
                {{ end }}
            </div>
        </div>
        {{ end }}
    </div>
</div>
{{ end }}'''

        with open(seminars_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(seminar_list_layout)

        # 創建單個研討會佈局
        seminar_single_layout = '''{{ define "main" }}
<div class="seminar-single">
    <header class="page-header section-block">
        <h1 class="page-title">{{ .Title }}</h1>
        <div class="seminar-stats">
            <span class="stat">共 {{ len .Pages }} 場會議</span>
        </div>
    </header>

    <div class="reports-grid">
        {{ range .Pages }}
        <article class="report-card section-block">
            <h3 class="report-title">
                <a href="{{ .Permalink }}">{{ .Title }}</a>
            </h3>
            <div class="report-meta">
                <span class="category">{{ .Params.category | default "主題演講" }}</span>
                <span class="date">{{ .Date.Format "2006-01-02" }}</span>
            </div>
            <p class="report-excerpt">{{ .Summary | truncate 150 }}</p>
            {{ if .Params.tags }}
            <div class="report-tags">
                {{ range .Params.tags }}
                <span class="tag">{{ . }}</span>
                {{ end }}
            </div>
            {{ end }}
        </article>
        {{ end }}
    </div>
</div>
{{ end }}'''

        with open(seminars_dir / "single.html", 'w', encoding='utf-8') as f:
            f.write(seminar_single_layout)

    def _process_markdown_files(self, md_dir: str, site_dir: pathlib.Path,
                               template_style: str) -> List[str]:
        """處理 Markdown 文件並生成 Hugo 內容"""
        md_path = pathlib.Path(md_dir)
        content_dir = site_dir / "content"
        html_files = []

        if not md_path.exists():
            logger.warning(f"Markdown 目錄不存在: {md_dir}")
            return html_files

        # 處理每個 Markdown 文件
        for md_file in md_path.glob("*.md"):
            try:
                # 讀取 Markdown 內容
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 解析元數據
                metadata = self._extract_metadata_from_content(content, md_file.stem)

                # 創建 Hugo 內容文件
                hugo_content = self._create_hugo_content(content, metadata)

                # 確定輸出路徑（按研討會分組）
                seminar_slug = self._slugify(metadata.seminar)
                seminar_dir = content_dir / seminar_slug
                seminar_dir.mkdir(parents=True, exist_ok=True)

                # 保存 Hugo 內容文件
                output_file = seminar_dir / f"{md_file.stem}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(hugo_content)

                # 記錄生成的文件
                html_files.append(f"{seminar_slug}/{md_file.stem}.html")

                logger.info(f"已處理 Markdown 文件: {md_file.name}")

            except Exception as e:
                logger.error(f"處理 Markdown 文件失敗 {md_file.name}: {e}")

        return html_files

    def _extract_metadata_from_content(self, content: str, filename: str) -> ReportMetadata:
        """從內容中提取元數據"""
        import re

        # 嘗試從內容中提取標題
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename

        # 嘗試從內容中提取研討會信息
        seminar_match = re.search(r'研討會[：:]\s*\*?\*?(.+?)\*?\*?$', content, re.MULTILINE)
        seminar = seminar_match.group(1).strip() if seminar_match else "未知研討會"

        # 嘗試從內容中提取類型信息
        category_match = re.search(r'類型[：:]\s*\*?\*?(.+?)\*?\*?$', content, re.MULTILINE)
        category = category_match.group(1).strip() if category_match else "主題演講"

        # 嘗試從內容中提取 URL
        url_match = re.search(r'來源[：:]\s*\[(.+?)\]\((.+?)\)', content)
        url = url_match.group(2) if url_match else ""

        # 生成標籤
        tags = self._generate_tags_from_content(content, seminar, category)

        return ReportMetadata(
            title=title,
            seminar=seminar,
            category=category,
            url=url,
            session_id=filename,
            tags=tags
        )

    def _generate_tags_from_content(self, content: str, seminar: str, category: str) -> List[str]:
        """從內容生成標籤"""
        tags = []

        # 添加研討會作為標籤
        if seminar and seminar != "未知研討會":
            tags.append(seminar)

        # 添加類型作為標籤
        if category:
            tags.append(category)

        # 基於內容關鍵詞生成標籤
        tech_keywords = {
            "AI": ["AI", "人工智慧", "機器學習", "深度學習"],
            "雲端": ["雲端", "Cloud", "AWS", "Azure", "GCP"],
            "微服務": ["微服務", "Microservices", "容器", "Docker", "Kubernetes"],
            "前端": ["前端", "Frontend", "React", "Vue", "Angular"],
            "後端": ["後端", "Backend", "API", "服務端"],
            "數據": ["數據", "大數據", "數據分析", "數據科學"],
            "安全": ["安全", "Security", "資安", "加密"],
            "DevOps": ["DevOps", "CI/CD", "自動化", "部署"]
        }

        content_lower = content.lower()
        for tag, keywords in tech_keywords.items():
            if any(keyword.lower() in content_lower for keyword in keywords):
                tags.append(tag)

        return list(set(tags))  # 去重

    def _create_hugo_content(self, content: str, metadata: ReportMetadata) -> str:
        """創建 Hugo 內容文件"""
        # 創建 Front Matter
        front_matter = {
            "title": metadata.title,
            "date": metadata.date,
            "seminar": metadata.seminar,
            "category": metadata.category,
            "tags": metadata.tags,
            "session_id": metadata.session_id,
            "analysis_mode": metadata.analysis_mode,
            "template_style": metadata.template_style
        }

        if metadata.url:
            front_matter["url_source"] = metadata.url

        # 生成 YAML Front Matter
        yaml_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)

        # 處理內容，移除第一個標題（因為會用 Front Matter 中的 title）
        import re
        content_without_title = re.sub(r'^#\s+.+$', '', content, count=1, flags=re.MULTILINE).strip()

        # 組合完整的 Hugo 內容
        hugo_content = f"""---
{yaml_front_matter}---

{content_without_title}
"""

        return hugo_content

    def _slugify(self, text: str) -> str:
        """將文本轉換為 URL 友好的 slug"""
        import re
        import unicodedata

        # 移除特殊字符，保留中文、英文、數字
        text = re.sub(r'[^\w\s-]', '', text)
        # 替換空格為連字符
        text = re.sub(r'[-\s]+', '-', text)
        # 轉換為小寫
        text = text.lower().strip('-')

        return text or "unknown"

    def get_template_style_config(self, template_style: str) -> Dict[str, Any]:
        """獲取模板樣式配置"""
        style_configs = {
            "professional": {
                "theme_variant": "professional",
                "primary_color": "#3a86ff",
                "secondary_color": "#00bfff",
                "layout_type": "business",
                "typography": "formal"
            },
            "technical": {
                "theme_variant": "technical",
                "primary_color": "#00d4aa",
                "secondary_color": "#4fc3f7",
                "layout_type": "documentation",
                "typography": "monospace"
            },
            "concise": {
                "theme_variant": "minimal",
                "primary_color": "#6366f1",
                "secondary_color": "#a78bfa",
                "layout_type": "simple",
                "typography": "clean"
            },
            "presentation": {
                "theme_variant": "presentation",
                "primary_color": "#ec4899",
                "secondary_color": "#f472b6",
                "layout_type": "slides",
                "typography": "display"
            }
        }

        return style_configs.get(template_style, style_configs["professional"])

    def get_analysis_mode_config(self, analysis_mode: str) -> Dict[str, Any]:
        """獲取分析模式配置"""
        mode_configs = {
            "technical": {
                "focus": "技術深度",
                "sections": ["技術架構", "實現細節", "性能優化", "最佳實踐"],
                "icon": "🔧",
                "color": "#9333ea"
            },
            "business": {
                "focus": "商業價值",
                "sections": ["商業應用", "市場機會", "投資回報", "競爭優勢"],
                "icon": "💼",
                "color": "#ec4899"
            },
            "trend": {
                "focus": "技術趨勢",
                "sections": ["發展趨勢", "創新機會", "未來方向", "行業影響"],
                "icon": "📈",
                "color": "#0ea5e9"
            },
            "comprehensive": {
                "focus": "全方位分析",
                "sections": ["技術要點", "商業價值", "趨勢洞察", "實踐經驗"],
                "icon": "🎯",
                "color": "#22c55e"
            }
        }

        return mode_configs.get(analysis_mode, mode_configs["comprehensive"])

    def get_language_config(self, language: str = "zh-tw") -> Dict[str, Any]:
        """獲取語言配置"""
        language_configs = {
            "zh-tw": {
                "name": "繁體中文",
                "code": "zh-tw",
                "direction": "ltr",
                "date_format": "2006年01月02日",
                "labels": {
                    "home": "首頁",
                    "seminars": "研討會",
                    "categories": "分類",
                    "tags": "標籤",
                    "reports": "報告",
                    "latest": "最新報告",
                    "read_more": "閱讀全文",
                    "previous": "上一篇",
                    "next": "下一篇",
                    "generated_by": "本報告由 TrendScope 自動生成",
                    "generated_time": "生成時間"
                }
            },
            "zh-cn": {
                "name": "简体中文",
                "code": "zh-cn",
                "direction": "ltr",
                "date_format": "2006年01月02日",
                "labels": {
                    "home": "首页",
                    "seminars": "研讨会",
                    "categories": "分类",
                    "tags": "标签",
                    "reports": "报告",
                    "latest": "最新报告",
                    "read_more": "阅读全文",
                    "previous": "上一篇",
                    "next": "下一篇",
                    "generated_by": "本报告由 TrendScope 自动生成",
                    "generated_time": "生成时间"
                }
            },
            "en": {
                "name": "English",
                "code": "en",
                "direction": "ltr",
                "date_format": "January 2, 2006",
                "labels": {
                    "home": "Home",
                    "seminars": "Seminars",
                    "categories": "Categories",
                    "tags": "Tags",
                    "reports": "Reports",
                    "latest": "Latest Reports",
                    "read_more": "Read More",
                    "previous": "Previous",
                    "next": "Next",
                    "generated_by": "This report was automatically generated by TrendScope",
                    "generated_time": "Generated at"
                }
            }
        }

        return language_configs.get(language, language_configs["zh-tw"])

    def create_multilingual_content(self, content: str, metadata: ReportMetadata) -> Dict[str, str]:
        """創建多語言內容"""
        multilingual_content = {}

        # 主要語言（繁體中文）
        multilingual_content["zh-tw"] = self._create_hugo_content(content, metadata)

        # 可以在這裡添加自動翻譯邏輯
        # 目前只提供繁體中文版本

        return multilingual_content

    def _build_hugo_site(self, site_dir: pathlib.Path, output_dir: str):
        """構建 Hugo 靜態網站"""
        try:
            # 確保輸出目錄存在
            output_path = pathlib.Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # 設置 Hugo 構建命令 - 直接輸出到目標目錄
            cmd = [
                self.hugo_binary,
                "--destination", str(output_path),
                "--minify",
                "--gc"
            ]

            # 執行 Hugo 構建
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=str(site_dir)
            )

            logger.info(f"Hugo 網站構建成功: {result.stdout}")

            # 檢查輸出目錄是否有文件
            if output_path.exists():
                html_files = list(output_path.rglob("*.html"))
                logger.info(f"生成了 {len(html_files)} 個 HTML 文件")
            else:
                logger.warning(f"輸出目錄不存在: {output_path}")

        except subprocess.CalledProcessError as e:
            error_msg = f"Hugo 構建失敗 (返回碼: {e.returncode})"
            if e.stdout:
                error_msg += f"\n標準輸出: {e.stdout}"
            if e.stderr:
                error_msg += f"\n錯誤輸出: {e.stderr}"
            logger.error(error_msg)

            # 嘗試檢查 Hugo 網站結構
            self._debug_hugo_site_structure(site_dir)

            raise RuntimeError(error_msg)
        except Exception as e:
            logger.error(f"Hugo 構建過程中發生錯誤: {e}")
            raise

    def create_partials(self, layouts_dir: pathlib.Path):
        """創建 Hugo 部分模板"""
        partials_dir = layouts_dir / "partials"
        partials_dir.mkdir(exist_ok=True)

        # 創建頭部模板
        header_template = '''<header class="site-header">
    <nav class="navbar">
        <div class="nav-brand">
            <a href="{{ "/" | relURL }}">{{ .Site.Title }}</a>
        </div>
        <div class="nav-menu">
            {{ range .Site.Menus.main }}
            <a href="{{ .URL | relURL }}" class="nav-link">{{ .Name }}</a>
            {{ end }}
        </div>
        <div class="nav-toggle">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </nav>
</header>'''

        with open(partials_dir / "header.html", 'w', encoding='utf-8') as f:
            f.write(header_template)

        # 創建頁腳模板
        footer_template = '''<footer class="site-footer">
    <div class="footer-content">
        <div class="footer-info">
            <p>&copy; {{ now.Format "2006" }} {{ .Site.Title }}. 由 TrendScope 驅動。</p>
            <p>{{ .Site.Params.description }}</p>
        </div>
        <div class="footer-links">
            <a href="{{ "/" | relURL }}">首頁</a>
            <a href="{{ "/seminars/" | relURL }}">研討會</a>
            <a href="{{ "/categories/" | relURL }}">分類</a>
            <a href="{{ "/tags/" | relURL }}">標籤</a>
        </div>
    </div>
</footer>'''

        with open(partials_dir / "footer.html", 'w', encoding='utf-8') as f:
            f.write(footer_template)

    def generate_sample_content(self, site_dir: pathlib.Path):
        """生成示例內容（用於測試）"""
        content_dir = site_dir / "content"

        # 創建示例首頁內容
        index_content = '''---
title: "TrendScope 會議報告"
description: "AI 驅動的會議報告分析平台"
---

歡迎來到 TrendScope 會議報告平台！

這裡匯集了來自各大技術會議的深度分析報告，由 AI 自動生成，為您提供最新的技術趨勢和洞察。

## 特色功能

- **智能分析**: 使用先進的 AI 技術分析會議內容
- **多維度報告**: 提供技術、商業、趨勢等多角度分析
- **分類瀏覽**: 按研討會、類型、標籤輕鬆查找
- **響應式設計**: 支持各種設備的最佳瀏覽體驗
'''

        with open(content_dir / "_index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)

    def get_hugo_version(self) -> str:
        """獲取 Hugo 版本信息"""
        try:
            result = subprocess.run([self.hugo_binary, "version"],
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except Exception:
            return "Unknown"

    def _debug_hugo_site_structure(self, site_dir: pathlib.Path):
        """調試 Hugo 網站結構"""
        try:
            logger.info(f"調試 Hugo 網站結構: {site_dir}")

            # 檢查基本目錄結構
            for item in site_dir.iterdir():
                if item.is_dir():
                    logger.info(f"目錄: {item.name}/")
                    # 列出子目錄內容
                    for subitem in item.iterdir():
                        logger.info(f"  {subitem.name}")
                else:
                    logger.info(f"文件: {item.name}")

            # 檢查配置文件
            config_file = site_dir / "hugo.yaml"
            if config_file.exists():
                logger.info("Hugo 配置文件存在")
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_content = f.read()
                    logger.info(f"配置文件內容 (前500字符): {config_content[:500]}")
            else:
                logger.error("Hugo 配置文件不存在!")

            # 檢查內容目錄
            content_dir = site_dir / "content"
            if content_dir.exists():
                content_files = list(content_dir.rglob("*.md"))
                logger.info(f"找到 {len(content_files)} 個內容文件")
                for content_file in content_files:
                    logger.info(f"  內容文件: {content_file.relative_to(site_dir)}")
            else:
                logger.error("內容目錄不存在!")

        except Exception as e:
            logger.error(f"調試過程中發生錯誤: {e}")
