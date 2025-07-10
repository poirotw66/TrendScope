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
import zipfile
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
    title: str = "NeoTrendHub 會議報告"
    theme: str = "NeoTrendHub"
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
                           template_style: str = "professional",
                           create_offline_package: bool = True) -> Dict[str, Any]:
        """
        生成 Hugo 靜態網站並創建離線分享包

        Args:
            md_dir: Markdown 文件目錄
            output_dir: 輸出目錄
            template_style: 模板樣式
            create_offline_package: 是否創建離線分享包

        Returns:
            包含生成結果的字典：
            {
                'html_files': List[str],  # 生成的 HTML 文件列表
                'zip_file': str,          # ZIP 檔案路徑（如果創建）
                'launcher_file': str,     # 啟動器文件路徑
                'instructions_file': str, # 使用說明文件路徑
                'total_pages': int,       # 總頁面數
                'site_info': Dict         # 網站信息
            }
        """
        try:
            # 創建臨時 Hugo 網站目錄
            site_dir = pathlib.Path(output_dir).parent / "hugo_site"
            output_path = pathlib.Path(output_dir)

            logger.info(f"開始生成 Hugo 網站: {md_dir} -> {output_dir}")

            # 初始化 Hugo 網站結構
            logger.info("初始化 Hugo 網站結構...")
            self._initialize_hugo_site(site_dir, template_style)

            # 處理 Markdown 文件並生成內容
            logger.info("處理 Markdown 文件...")
            html_files = self._process_markdown_files(md_dir, site_dir, template_style)
            logger.info(f"處理了 {len(html_files) if html_files else 0} 個 Markdown 文件")

            # 生成 Hugo 網站
            logger.info("執行 Hugo 構建...")
            build_success = self._build_hugo_site(site_dir, output_dir)

            if not build_success:
                logger.error("Hugo 構建失敗")
                raise Exception("Hugo 構建失敗")

            # 驗證輸出文件
            if not output_path.exists():
                logger.error(f"輸出目錄不存在: {output_path}")
                raise Exception(f"輸出目錄不存在: {output_path}")

            generated_html_files = list(output_path.rglob("*.html"))
            logger.info(f"Hugo 構建生成了 {len(generated_html_files)} 個 HTML 文件")

            if len(generated_html_files) == 0:
                logger.error("Hugo 構建沒有生成任何 HTML 文件")
                raise Exception("Hugo 構建沒有生成任何 HTML 文件")

            # 修復離線瀏覽路徑問題
            logger.info("修復離線瀏覽路徑...")
            self._fix_offline_paths(output_dir)

            # 收集網站信息
            logger.info("收集網站信息...")
            site_info = self._collect_site_info(md_dir, output_dir, [str(f) for f in generated_html_files])

            result = {
                'html_files': html_files,
                'zip_file': None,
                'launcher_file': None,
                'instructions_file': None,
                'total_pages': len(html_files) if html_files else 0,
                'site_info': site_info
            }

            if create_offline_package:
                # 生成 HTML 啟動器
                launcher_file = self._generate_html_launcher(output_dir, site_info, template_style)
                result['launcher_file'] = launcher_file

                # 生成使用說明文件
                instructions_file = self._generate_instructions_file(output_dir, site_info)
                result['instructions_file'] = instructions_file

                # 創建 ZIP 離線包
                zip_file = self._create_offline_zip_package(output_dir, site_info)
                result['zip_file'] = zip_file

                logger.info(f"離線分享包已創建: {zip_file}")

            # 清理臨時目錄
            if site_dir.exists():
                shutil.rmtree(site_dir)

            return result
            
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
                "generator": "NeoTrendHub Hugo Generator",
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
            },
            "permalinks": {
                "posts": "/posts/:slug/"
            },
            "disableKinds": []  # 確保不禁用任何內容類型
        }
        
        # 支援多語言配置
        config["languages"] = {
            "zh-tw": {
                "languageName": "繁體中文",
                "weight": 1,
                "title": "NeoTrendHub 會議報告"
            },
            "zh-cn": {
                "languageName": "简体中文", 
                "weight": 2,
                "title": "NeoTrendHub 会议报告"
            },
            "en": {
                "languageName": "English",
                "weight": 3,
                "title": "NeoTrendHub Conference Reports"
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
<html lang="{{ .Site.LanguageCode }}" class="no-js">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <title>{{ if .Title }}{{ .Title }} - {{ end }}{{ .Site.Title }}</title>
    <meta name="description" content="{{ .Description | default .Site.Params.description }}">
    <meta name="generator" content="Hugo {{ hugo.Version }} - NeoTrendHub">
    <meta name="author" content="NeoTrendHub AI">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
    <meta property="og:url" content="{{ .Permalink }}">
    <meta property="og:title" content="{{ .Title }} - {{ .Site.Title }}">
    <meta property="og:description" content="{{ .Description | default .Site.Params.description }}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{{ .Permalink }}">
    <meta property="twitter:title" content="{{ .Title }} - {{ .Site.Title }}">
    <meta property="twitter:description" content="{{ .Description | default .Site.Params.description }}">

    <!-- CSS Styles -->
    <link rel="stylesheet" href="{{ "css/styles.css" | relURL }}">
    <link rel="preload" href="{{ "css/styles.css" | relURL }}" as="style">

    <!-- SEO -->
    <link rel="canonical" href="{{ .Permalink }}">
    {{ if .Site.Params.rss }}
    <link rel="alternate" type="application/rss+xml" title="{{ .Site.Title }}" href="{{ "index.xml" | relURL }}">
    {{ end }}

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ "favicon.ico" | relURL }}">

    <!-- Theme Color -->
    <meta name="theme-color" content="#3a86ff">
    <meta name="msapplication-TileColor" content="#3a86ff">
</head>
<body class="template-{{ .Site.Params.template_style }} hugo-site">
    <div class="container">
        {{ partial "header.html" . }}

        <main class="content" id="main-content" role="main">
            {{ block "main" . }}{{ end }}
        </main>

        {{ partial "footer.html" . }}
    </div>

    <!-- JavaScript -->
    <script src="{{ "js/main.js" | relURL }}" defer></script>

    <!-- Remove no-js class -->
    <script>document.documentElement.classList.remove('no-js');</script>
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
        # 優先使用完整的默認樣式，確保包含所有必要的樣式
        css_content = self._get_default_css_styles(template_style)

        # 嘗試從現有模組獲取額外樣式（如果可用）
        try:
            from src.batch_md_to_html import get_css_styles
            additional_css = get_css_styles(template_style)
            # 合併樣式，但以默認樣式為主
            if additional_css and len(additional_css) > len(css_content):
                logger.info("使用來自 batch_md_to_html 的擴展樣式")
                css_content = additional_css
        except ImportError:
            logger.info("使用內建的完整 CSS 樣式")

        with open(css_dir / "styles.css", 'w', encoding='utf-8') as f:
            f.write(css_content)

        logger.info(f"CSS 樣式文件已創建: {len(css_content)} 字符")

    def _get_default_css_styles(self, template_style: str) -> str:
        """獲取默認 CSS 樣式 - 增強版三階層設計"""
        return f"""
/* NeoTrendHub Hugo Theme - Enhanced Three-Tier Design */
/* 完全符合 plan.md 規範的三階層網站樣式 */

:root {{
    /* 主色調 - 專業藍色系 */
    --primary: #3a86ff;
    --primary-dark: #0048b3;
    --primary-light: #6ba3ff;
    --secondary: #00bfff;
    --accent: #4f46e5;

    /* 功能色彩 */
    --success: #22c55e;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #0ea5e9;

    /* 趨勢分類色彩 */
    --trend-ai: #9333ea;
    --trend-cloud: #06b6d4;
    --trend-data: #10b981;
    --trend-security: #f59e0b;
    --trend-mobile: #ec4899;

    /* 文字色彩 */
    --text-primary: #1e293b;
    --text-secondary: #475569;
    --text-muted: #64748b;
    --text-light: #94a3b8;

    /* 背景色彩 */
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --bg-tertiary: #f1f5f9;
    --bg-accent: #e2e8f0;

    /* 邊框和分隔線 */
    --border-light: #e2e8f0;
    --border-medium: #cbd5e1;
    --border-dark: #94a3b8;

    /* 陰影效果 */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

    /* 圓角 */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;

    /* 間距 */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;

    /* 字體大小 */
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;
    --text-3xl: 1.875rem;
    --text-4xl: 2.25rem;
    --text-5xl: 3rem;

    /* 動畫 */
    --transition-fast: 150ms ease-in-out;
    --transition-normal: 250ms ease-in-out;
    --transition-slow: 350ms ease-in-out;
}}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {{
    :root {{
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --text-light: #64748b;

        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --bg-accent: #475569;

        --border-light: #334155;
        --border-medium: #475569;
        --border-dark: #64748b;

        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
    }}
}}

/* 基礎重置和字體設定 */
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html {{
    font-size: 16px;
    scroll-behavior: smooth;
}}

body {{
    font-family: 'Inter', 'SF Pro Display', 'Microsoft JhengHei', 'PingFang TC',
                 'Hiragino Sans GB', 'Noto Sans CJK SC', 'Source Han Sans SC',
                 -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                 'Helvetica Neue', Arial, sans-serif;
    font-size: var(--text-base);
    line-height: 1.6;
    color: var(--text-primary);
    background-color: var(--bg-secondary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}}

/* 中文字體優化 */
:lang(zh) {{
    font-family: 'Microsoft JhengHei', 'PingFang TC', 'Hiragino Sans GB',
                 'Noto Sans CJK TC', 'Source Han Sans TC', sans-serif;
}}

/* 容器和佈局 */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
}}

@media (max-width: 768px) {{
    .container {{
        padding: 0 var(--spacing-md);
    }}
}}

/* 三階層導航系統 */
.site-navigation {{
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-light);
    box-shadow: var(--shadow-sm);
    position: sticky;
    top: 0;
    z-index: 100;
}}

.nav-container {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md) 0;
}}

.site-logo {{
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}}

.site-logo::before {{
    content: "📊";
    font-size: var(--text-3xl);
}}

.main-nav {{
    display: flex;
    gap: var(--spacing-lg);
    list-style: none;
}}

.main-nav a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);
}}

.main-nav a:hover,
.main-nav a.active {{
    color: var(--primary);
    background-color: var(--bg-tertiary);
}}

/* 麵包屑導航 */
.breadcrumb {{
    background: var(--bg-primary);
    padding: var(--spacing-md) 0;
    border-bottom: 1px solid var(--border-light);
}}

.breadcrumb-list {{
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    list-style: none;
    font-size: var(--text-sm);
}}

.breadcrumb-item {{
    color: var(--text-muted);
}}

.breadcrumb-item:not(:last-child)::after {{
    content: "›";
    margin-left: var(--spacing-sm);
    color: var(--text-light);
}}

.breadcrumb-item a {{
    color: var(--primary);
    text-decoration: none;
}}

.breadcrumb-item a:hover {{
    text-decoration: underline;
}}

/* 首頁設計 */
.homepage {{
    min-height: calc(100vh - 200px);
}}

.hero-section {{
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    padding: var(--spacing-2xl) 0;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.hero-section::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
    opacity: 0.3;
}}

.hero-content {{
    position: relative;
    z-index: 1;
}}

.hero-title {{
    font-size: var(--text-5xl);
    font-weight: 800;
    margin-bottom: var(--spacing-md);
    letter-spacing: -0.025em;
}}

.hero-subtitle {{
    font-size: var(--text-xl);
    opacity: 0.9;
    margin-bottom: var(--spacing-xl);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}}

.hero-stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-lg);
    max-width: 800px;
    margin: 0 auto;
}}

.stat-item {{
    text-align: center;
}}

.stat-number {{
    display: block;
    font-size: var(--text-4xl);
    font-weight: 700;
    margin-bottom: var(--spacing-xs);
}}

.stat-label {{
    font-size: var(--text-sm);
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* 趨勢分類卡片 */
.trends-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-2xl) 0;
}}

.trend-card {{
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
    border: 1px solid var(--border-light);
    position: relative;
    overflow: hidden;
}}

.trend-card:hover {{
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}}

.trend-title {{
    font-size: var(--text-2xl);
    font-weight: 700;
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
}}

/* 會議列表 */
.session-card {{
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
    transition: all var(--transition-normal);
    margin-bottom: var(--spacing-lg);
}}

.session-card:hover {{
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}}

.session-title {{
    font-size: var(--text-xl);
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--spacing-sm);
    line-height: 1.4;
}}

/* 內容區塊 */
.content-section {{
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-2xl);
    margin: var(--spacing-xl) 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
}}

.section-title {{
    font-size: var(--text-3xl);
    font-weight: 700;
    margin-bottom: var(--spacing-lg);
    color: var(--text-primary);
}}

/* 響應式設計 */
@media (max-width: 768px) {{
    .trends-grid {{
        grid-template-columns: 1fr;
    }}

    .hero-title {{
        font-size: var(--text-3xl);
    }}

    .container {{
        padding: 0 var(--spacing-md);
    }}
}}

/* 頁腳 */
.site-footer {{
    background: var(--bg-primary);
    border-top: 1px solid var(--border-light);
    padding: var(--spacing-xl) 0;
    margin-top: var(--spacing-2xl);
    text-align: center;
    color: var(--text-muted);
    font-size: var(--text-sm);
}}
"""

    def _create_javascript(self, js_dir: pathlib.Path):
        """創建 JavaScript 文件"""
        js_content = """
        // NeoTrendHub Hugo Theme JavaScript
        document.addEventListener('DOMContentLoaded', function() {
            // 初始化主題功能
            initializeTheme();
            initializeNavigation();
            initializeSearch();

            // 載入完成後的處理
            console.log('NeoTrendHub Hugo Theme 已載入');
        });

        function initializeTheme() {
            // 檢查本地存儲的主題設置
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                document.body.classList.toggle('dark-theme', savedTheme === 'dark');
            }

            // 主題切換按鈕
            const themeToggle = document.querySelector('.theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', toggleTheme);
            }
        }

        function initializeNavigation() {
            // 移動端導航切換
            const navToggle = document.querySelector('.nav-toggle');
            const navMenu = document.querySelector('.nav-menu');

            if (navToggle && navMenu) {
                navToggle.addEventListener('click', function() {
                    navMenu.classList.toggle('active');
                });
            }

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
    <section class="hero-section">
        <div class="hero-content">
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
                    <span class="stat-number">5</span>
                    <span class="stat-label">技術趨勢</span>
                </div>
            </div>
        </div>
    </section>

    <section class="content-section">
        <h2 class="section-title">技術趨勢分析</h2>
        <div class="trends-grid">
            <!-- 趨勢卡片將由 Hugo 模板動態生成 -->
            <div class="trend-card ai">
                <span class="trend-icon">🤖</span>
                <h3 class="trend-title">人工智慧</h3>
                <p class="trend-description">探索 AI 技術的最新發展和應用趨勢</p>
                <div class="trend-stats">
                    <span class="trend-session-count">相關會議: 12</span>
                    <span class="trend-importance">高重要性</span>
                </div>
            </div>
            <div class="trend-card cloud">
                <span class="trend-icon">☁️</span>
                <h3 class="trend-title">雲端技術</h3>
                <p class="trend-description">雲端架構和服務的創新發展</p>
                <div class="trend-stats">
                    <span class="trend-session-count">相關會議: 8</span>
                    <span class="trend-importance">中重要性</span>
                </div>
            </div>
        </div>
    </section>

    <section class="content-section">
        <h2 class="section-title">最新會議報告</h2>
        <div class="sessions-grid">
            {{ range first 6 .Site.RegularPages }}
            <article class="session-card">
                <div class="session-header">
                    <h3 class="session-title">
                        <a href="{{ .Permalink }}">{{ .Title }}</a>
                    </h3>
                </div>
                <div class="session-meta">
                    {{ if .Params.seminar }}
                    <span class="session-seminar">{{ .Params.seminar }}</span>
                    {{ end }}
                    <span class="session-date">{{ .Date.Format "2006-01-02" }}</span>
                </div>
                {{ if .Params.trends }}
                <div class="session-trends">
                    {{ range .Params.trends }}
                    <a href="/trends/{{ . | urlize }}" class="trend-tag">{{ . }}</a>
                    {{ end }}
                </div>
                {{ end }}
            </article>
            {{ end }}
        </div>
    </section>
</div>
{{ end }}'''

        layouts_dir.mkdir(exist_ok=True)
        with open(layouts_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_layout)

    def _create_single_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建單頁佈局"""
        single_layout = '''{{ define "main" }}
<article class="single-report">
    <header class="content-section">
        <h1 class="section-title">{{ .Title }}</h1>
        <div class="session-meta">
            {{ if .Params.seminar }}
            <div class="meta-item">
                <strong>研討會：</strong> {{ .Params.seminar }}
            </div>
            {{ end }}
            {{ if .Date }}
            <div class="meta-item session-date">
                {{ .Date.Format "2006年01月02日" }}
            </div>
            {{ end }}
            {{ if .Params.speaker }}
            <div class="meta-item">
                <strong>講者：</strong> {{ .Params.speaker }}
            </div>
            {{ end }}
        </div>
        {{ if .Params.trends }}
        <div class="session-trends">
            {{ range .Params.trends }}
            <a href="/trends/{{ . | urlize }}" class="trend-tag">{{ . }}</a>
            {{ end }}
        </div>
        {{ end }}
    </header>

    <div class="content-section">
        <div class="section-content">
            {{ .Content }}
        </div>
    </div>

    <nav class="content-section">
        <h3>相關內容</h3>
        <div class="related-links">
            {{ if .PrevInSection }}
            <a href="{{ .PrevInSection.Permalink }}" class="nav-link prev">
                ← {{ .PrevInSection.Title }}
            </a>
            {{ end }}
            {{ if .NextInSection }}
            <a href="{{ .NextInSection.Permalink }}" class="nav-link next">
                {{ .NextInSection.Title }} →
            </a>
            {{ end }}
        </div>
    </nav>
</article>
{{ end }}'''

        default_dir = layouts_dir / "_default"
        default_dir.mkdir(exist_ok=True)
        with open(default_dir / "single.html", 'w', encoding='utf-8') as f:
            f.write(single_layout)

    def _create_list_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建列表佈局"""
        list_layout = '''{{ define "main" }}
<div class="list-page">
    <header class="content-section">
        <h1 class="section-title">{{ .Title }}</h1>
        {{ if .Content }}
        <div class="section-content">
            {{ .Content }}
        </div>
        {{ end }}
    </header>

    <section class="content-section">
        <div class="sessions-grid">
            {{ range .Pages }}
            <article class="session-card">
                <div class="session-header">
                    <h3 class="session-title">
                        <a href="{{ .Permalink }}">{{ .Title }}</a>
                    </h3>
                </div>
                <div class="session-meta">
                    {{ if .Params.seminar }}
                    <span class="session-seminar">{{ .Params.seminar }}</span>
                    {{ end }}
                    <span class="session-date">{{ .Date.Format "2006-01-02" }}</span>
                </div>
                {{ if .Params.trends }}
                <div class="session-trends">
                    {{ range .Params.trends }}
                    <a href="/trends/{{ . | urlize }}" class="trend-tag">{{ . }}</a>
                    {{ end }}
                </div>
                {{ end }}
                {{ if .Summary }}
                <div class="session-summary">
                    {{ .Summary }}
                </div>
                {{ end }}
            </article>
            {{ end }}
        </div>
    </section>
</div>
{{ end }}'''

        default_dir = layouts_dir / "_default"
        default_dir.mkdir(exist_ok=True)
        with open(default_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(list_layout)

    def _create_taxonomy_layouts(self, layouts_dir: pathlib.Path, template_style: str):
        """創建分類佈局"""
        # 創建趨勢分類佈局
        trends_dir = layouts_dir / "trends"
        trends_dir.mkdir(exist_ok=True)

        trend_list_layout = '''{{ define "main" }}
<div class="trends-page">
    <header class="content-section">
        <h1 class="section-title">技術趨勢分類</h1>
        <p class="section-content">探索當前最重要的技術趨勢，深入了解每個領域的發展動向。</p>
    </header>

    <section class="content-section">
        <div class="trends-grid">
            {{ range .Data.Terms }}
            <div class="trend-card">
                <h3 class="trend-title">
                    <a href="{{ .Page.Permalink }}">{{ .Page.Title }}</a>
                </h3>
                <p class="trend-description">{{ .Page.Summary }}</p>
                <div class="trend-stats">
                    <span class="trend-session-count">相關會議: {{ .Count }}</span>
                </div>
            </div>
            {{ end }}
        </div>
    </section>
</div>
{{ end }}'''

        with open(trends_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(trend_list_layout)

        # 創建單個趨勢頁面佈局
        trend_single_layout = '''{{ define "main" }}
<div class="trend-single">
    <header class="content-section">
        <h1 class="section-title">{{ .Title }}</h1>
        {{ if .Content }}
        <div class="section-content">
            {{ .Content }}
        </div>
        {{ end }}
    </header>

    <section class="content-section">
        <h2 class="section-title">相關會議報告</h2>
        <div class="sessions-grid">
            {{ range .Pages }}
            <article class="session-card">
                <div class="session-header">
                    <h3 class="session-title">
                        <a href="{{ .Permalink }}">{{ .Title }}</a>
                    </h3>
                </div>
                <div class="session-meta">
                    {{ if .Params.seminar }}
                    <span class="session-seminar">{{ .Params.seminar }}</span>
                    {{ end }}
                    <span class="session-date">{{ .Date.Format "2006-01-02" }}</span>
                </div>
            </article>
            {{ end }}
        </div>
    </section>
</div>
{{ end }}'''

        with open(trends_dir / "single.html", 'w', encoding='utf-8') as f:
            f.write(trend_single_layout)

    def _process_markdown_files(self, md_dir: str, site_dir: pathlib.Path,
                                template_style: str) -> List[str]:
        """處理 Markdown 文件並生成 Hugo 內容 - 支援三階層結構"""
        md_path = pathlib.Path(md_dir)
        content_dir = site_dir / "content"
        html_files = []

        if not md_path.exists():
            logger.warning(f"Markdown 目錄不存在: {md_dir}")
            return html_files

        logger.info(f"🔍 檢查 Markdown 目錄結構: {md_path}")

        # 檢查是否為增強版三階層結構
        has_enhanced_structure = self._check_enhanced_structure(md_path)

        if has_enhanced_structure:
            logger.info("✅ 檢測到增強版三階層結構，使用專用處理流程")
            html_files = self._process_enhanced_structure(md_path, content_dir, template_style)
        else:
            logger.info("📄 使用標準 Markdown 文件處理流程")
            html_files = self._process_standard_markdown_files(md_path, content_dir, template_style)

        return html_files

    def _check_enhanced_structure(self, md_path: pathlib.Path) -> bool:
        """檢查是否為增強版三階層結構"""
        # 檢查關鍵文件和目錄
        trends_analysis = md_path / "trends-analysis.md"
        index_file = md_path / "_index.md"
        trends_dir = md_path / "trends"
        sessions_dir = md_path / "sessions"

        has_structure = (
            trends_analysis.exists() or
            index_file.exists() or
            trends_dir.exists() or
            sessions_dir.exists()
        )

        logger.info(f"🔍 結構檢查結果:")
        logger.info(f"  📄 trends-analysis.md: {trends_analysis.exists()}")
        logger.info(f"  🏠 _index.md: {index_file.exists()}")
        logger.info(f"  📂 trends/: {trends_dir.exists()}")
        logger.info(f"  📂 sessions/: {sessions_dir.exists()}")

        return has_structure

    def _process_enhanced_structure(self, md_path: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理增強版三階層結構"""
        html_files = []

        # 1. 處理首頁文件 (_index.md 或 trends-analysis.md)
        index_file = md_path / "_index.md"
        trends_analysis_file = md_path / "trends-analysis.md"

        if index_file.exists():
            logger.info("📄 處理首頁文件: _index.md")
            self._copy_hugo_content_file(index_file, content_dir / "_index.md")
            html_files.append("index.html")
        elif trends_analysis_file.exists():
            logger.info("📄 處理趨勢分析文件作為首頁: trends-analysis.md")
            # 將 trends-analysis.md 轉換為首頁
            self._convert_trends_analysis_to_index(trends_analysis_file, content_dir / "_index.md")
            html_files.append("index.html")

        # 2. 處理趨勢分類目錄
        trends_dir = md_path / "trends"
        if trends_dir.exists():
            logger.info(f"📂 處理趨勢分類目錄: {trends_dir}")
            trends_content_dir = content_dir / "trends"
            trends_content_dir.mkdir(parents=True, exist_ok=True)

            # 創建趨勢分類索引頁
            self._create_trends_index(trends_content_dir)
            html_files.append("trends/index.html")

            # 處理每個趨勢文件
            for trend_file in trends_dir.glob("trend-*.md"):
                logger.info(f"  📄 處理趨勢文件: {trend_file.name}")
                target_file = trends_content_dir / trend_file.name
                self._copy_hugo_content_file(trend_file, target_file)
                html_files.append(f"trends/{trend_file.stem}/index.html")

        # 3. 處理會議詳細目錄
        sessions_dir = md_path / "sessions"
        if sessions_dir.exists():
            logger.info(f"📂 處理會議詳細目錄: {sessions_dir}")
            sessions_content_dir = content_dir / "sessions"
            sessions_content_dir.mkdir(parents=True, exist_ok=True)

            # 創建會議索引頁
            self._create_sessions_index(sessions_content_dir)
            html_files.append("sessions/index.html")

            # 處理每個會議文件
            for session_file in sessions_dir.glob("session-*.md"):
                logger.info(f"  📄 處理會議文件: {session_file.name}")
                target_file = sessions_content_dir / session_file.name
                self._copy_hugo_content_file(session_file, target_file)
                html_files.append(f"sessions/{session_file.stem}/index.html")

        # 4. 處理其他 Markdown 文件
        for md_file in md_path.glob("*.md"):
            if md_file.name not in ["_index.md", "trends-analysis.md"]:
                logger.info(f"📄 處理其他文件: {md_file.name}")
                self._process_single_markdown_file(md_file, content_dir, template_style)
                html_files.append(f"{md_file.stem}/index.html")

        logger.info(f"✅ 增強版結構處理完成，預期生成 {len(html_files)} 個 HTML 文件")
        return html_files

    def _process_standard_markdown_files(self, md_path: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理標準 Markdown 文件"""
        html_files = []

        # 處理每個 Markdown 文件
        for md_file in md_path.glob("*.md"):
            try:
                html_files.extend(self._process_single_markdown_file(md_file, content_dir, template_style))
            except Exception as e:
                logger.error(f"處理 Markdown 文件失敗 {md_file}: {e}")

        return html_files

    def _process_single_markdown_file(self, md_file: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理單個 Markdown 文件"""
        try:
            # 讀取 Markdown 內容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析元數據
            metadata = self._extract_metadata_from_content(content, md_file.stem)

            # 創建 Hugo 內容文件
            hugo_content = self._create_hugo_content(content, metadata)

            # 使用 Hugo Page Bundle 結構：每個報告都有自己的目錄
            posts_dir = content_dir / "posts"
            posts_dir.mkdir(parents=True, exist_ok=True)

            # 為 posts 目錄創建 _index.md（如果不存在）
            posts_index = posts_dir / "_index.md"
            if not posts_index.exists():
                with open(posts_index, 'w', encoding='utf-8') as f:
                    f.write("""---
title: 會議報告
description: 所有會議報告的列表
---

# 會議報告

這裡包含所有的會議報告。
""")

            # 生成簡短且安全的文件名
            session_id = md_file.stem

            # 提取 UUID 的前8個字符作為唯一標識
            if '_' in session_id:
                uuid_part = session_id.split('_')[0][:8]
            else:
                uuid_part = session_id[:8]

            # 使用簡短的文件名：report-UUID
            safe_filename = f"report-{uuid_part}"

            # 確保文件名是安全的（只包含字母數字和連字符）
            import re
            safe_filename = re.sub(r'[^a-zA-Z0-9-]', '', safe_filename)

            # 創建 Page Bundle 目錄結構：posts/report-xxx/index.md
            bundle_dir = posts_dir / safe_filename
            bundle_dir.mkdir(parents=True, exist_ok=True)

            # 保存為 index.md（Page Bundle 的標準文件名）
            output_file = bundle_dir / "index.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(hugo_content)

            # 記錄生成的文件（Hugo Page Bundle 會生成對應的 HTML）
            return [f"posts/{safe_filename}/index.html"]

        except Exception as e:
            logger.error(f"處理 Markdown 文件失敗 {md_file.name}: {e}")
            return []

    def _copy_hugo_content_file(self, source_file: pathlib.Path, target_file: pathlib.Path):
        """複製 Hugo 內容文件"""
        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # 讀取源文件內容
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 確保內容有正確的 Hugo front matter
            if not content.startswith('---'):
                # 如果沒有 front matter，添加基本的
                title = source_file.stem.replace('-', ' ').title()
                front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
---

"""
                content = front_matter + content

            # 寫入目標文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ 複製 Hugo 內容文件: {source_file.name} → {target_file}")

        except Exception as e:
            logger.error(f"❌ 複製 Hugo 內容文件失敗 {source_file} → {target_file}: {e}")

    def _convert_trends_analysis_to_index(self, trends_analysis_file: pathlib.Path, index_file: pathlib.Path):
        """將趨勢分析文件轉換為首頁"""
        try:
            with open(trends_analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 修改 front matter 以適合首頁
            if content.startswith('---'):
                # 找到 front matter 的結束位置
                end_pos = content.find('---', 3)
                if end_pos != -1:
                    front_matter = content[3:end_pos].strip()
                    body_content = content[end_pos + 3:].strip()

                    # 創建新的首頁 front matter
                    new_front_matter = f"""---
title: "技術趨勢分析報告"
description: "深度技術趨勢分析與會議洞察"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "homepage"
layout: "index"
---

"""
                    content = new_front_matter + body_content

            index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ 轉換趨勢分析為首頁: {trends_analysis_file.name} → {index_file.name}")

        except Exception as e:
            logger.error(f"❌ 轉換趨勢分析為首頁失敗: {e}")

    def _create_trends_index(self, trends_content_dir: pathlib.Path):
        """創建趨勢分類索引頁"""
        try:
            index_content = f"""---
title: "技術趨勢分類"
description: "探索各種技術趨勢的詳細分析"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "section"
layout: "list"
---

# 技術趨勢分類

探索當前最重要的技術趨勢，深入了解每個領域的發展動向和關鍵洞察。

{{{{< trend-list >}}}}
"""

            index_file = trends_content_dir / "_index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)

            logger.info(f"✅ 創建趨勢分類索引頁: {index_file}")

        except Exception as e:
            logger.error(f"❌ 創建趨勢分類索引頁失敗: {e}")

    def _create_sessions_index(self, sessions_content_dir: pathlib.Path):
        """創建會議索引頁"""
        try:
            index_content = f"""---
title: "會議詳細報告"
description: "所有會議的詳細分析和洞察"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "section"
layout: "list"
---

# 會議詳細報告

瀏覽所有會議的深度分析報告，獲取技術洞察和實用建議。

{{{{< session-list >}}}}
"""

            index_file = sessions_content_dir / "_index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)

            logger.info(f"✅ 創建會議索引頁: {index_file}")

        except Exception as e:
            logger.error(f"❌ 創建會議索引頁失敗: {e}")

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

        # 嘗試從內容中提取 URL 信息
        url_match = re.search(r'(?:來源|URL|網址)[：:]\s*(.+?)$', content, re.MULTILINE)
        url = url_match.group(1).strip() if url_match else ""

        # 生成標籤
        tags = self._generate_tags_from_content(content, seminar, category)

        return ReportMetadata(
            title=title,
            seminar=seminar,
            category=category,
            url=url,
            tags=tags
        )

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
}

.nav-brand a {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
    text-decoration: none;
}

.nav-menu {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-link {
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition);
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
}

.nav-link:hover {
    color: var(--primary);
    background-color: rgba(58, 134, 255, 0.1);
}

.nav-toggle {
    display: none;
    flex-direction: column;
    cursor: pointer;
}

.nav-toggle span {
    width: 25px;
    height: 3px;
    background: var(--text);
    margin: 3px 0;
    transition: var(--transition);
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    text-align: center;
    padding: 4rem 0;
    margin-bottom: 3rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    margin-bottom: 2rem;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-top: 2rem;
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.8;
}

/* Content Sections */
.section-block {
    background-color: var(--card);
    padding: 2.5rem;
    border-radius: var(--radius-lg);
    margin-bottom: 2.5rem;
    border-left: 5px solid var(--primary);
    box-shadow: var(--shadow-md);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.section-block:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.section-block h2 {
    color: var(--primary);
    margin-bottom: 1.5rem;
    font-size: 1.75rem;
    font-weight: 600;
}

.section-block h3 {
    color: var(--text);
    margin-bottom: 1rem;
    font-size: 1.25rem;
    font-weight: 600;
}

/* Lists and Content */
.content ul {
    list-style: none;
    padding: 0;
}

.content li {
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
}

.content li:last-child {
    border-bottom: none;
}

/* Tags */
.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
}

.tag {
    background: var(--primary);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.875rem;
    text-decoration: none;
    transition: var(--transition);
}

.tag:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
    .nav-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--card);
        flex-direction: column;
        padding: 1rem;
        box-shadow: var(--shadow-md);
    }

    .nav-menu.active {
        display: flex;
    }

    .nav-toggle {
        display: flex;
    }

    .hero-title {
        font-size: 2rem;
    }

    .hero-stats {
        flex-direction: column;
        gap: 1rem;
    }

    .container {
        padding: 0 1rem;
    }
}
"""

    def _create_javascript(self, js_dir: pathlib.Path):
        """創建 JavaScript 文件"""
        js_content = """
        // NeoTrendHub Hugo Theme JavaScript
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
            <p><em>本報告由 NeoTrendHub 自動生成 | 生成時間：{{ .Date.Format "2006-01-02 15:04:05" }}</em></p>
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
        """處理 Markdown 文件並生成 Hugo 內容 - 支援三階層結構"""
        md_path = pathlib.Path(md_dir)
        content_dir = site_dir / "content"
        html_files = []

        if not md_path.exists():
            logger.warning(f"Markdown 目錄不存在: {md_dir}")
            return html_files

        logger.info(f"🔍 檢查 Markdown 目錄結構: {md_path}")

        # 檢查是否為增強版三階層結構
        has_enhanced_structure = self._check_enhanced_structure(md_path)

        if has_enhanced_structure:
            logger.info("✅ 檢測到增強版三階層結構，使用專用處理流程")
            html_files = self._process_enhanced_structure(md_path, content_dir, template_style)
        else:
            logger.info("📄 使用標準 Markdown 文件處理流程")
            html_files = self._process_standard_markdown_files(md_path, content_dir, template_style)

        return html_files

    def _check_enhanced_structure(self, md_path: pathlib.Path) -> bool:
        """檢查是否為增強版三階層結構"""
        # 檢查關鍵文件和目錄
        trends_analysis = md_path / "trends-analysis.md"
        index_file = md_path / "_index.md"
        trends_dir = md_path / "trends"
        sessions_dir = md_path / "sessions"

        has_structure = (
            trends_analysis.exists() or
            index_file.exists() or
            trends_dir.exists() or
            sessions_dir.exists()
        )

        logger.info(f"🔍 結構檢查結果:")
        logger.info(f"  📄 trends-analysis.md: {trends_analysis.exists()}")
        logger.info(f"  🏠 _index.md: {index_file.exists()}")
        logger.info(f"  📂 trends/: {trends_dir.exists()}")
        logger.info(f"  📂 sessions/: {sessions_dir.exists()}")

        return has_structure

    def _process_enhanced_structure(self, md_path: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理增強版三階層結構"""
        html_files = []

        # 1. 處理首頁文件 (_index.md 或 trends-analysis.md)
        index_file = md_path / "_index.md"
        trends_analysis_file = md_path / "trends-analysis.md"

        if index_file.exists():
            logger.info("📄 處理首頁文件: _index.md")
            self._copy_hugo_content_file(index_file, content_dir / "_index.md")
            html_files.append("index.html")
        elif trends_analysis_file.exists():
            logger.info("📄 處理趨勢分析文件作為首頁: trends-analysis.md")
            # 將 trends-analysis.md 轉換為首頁
            self._convert_trends_analysis_to_index(trends_analysis_file, content_dir / "_index.md")
            html_files.append("index.html")

        # 2. 處理趨勢分類目錄
        trends_dir = md_path / "trends"
        if trends_dir.exists():
            logger.info(f"📂 處理趨勢分類目錄: {trends_dir}")
            trends_content_dir = content_dir / "trends"
            trends_content_dir.mkdir(parents=True, exist_ok=True)

            # 創建趨勢分類索引頁
            self._create_trends_index(trends_content_dir)
            html_files.append("trends/index.html")

            # 處理每個趨勢文件
            for trend_file in trends_dir.glob("trend-*.md"):
                logger.info(f"  📄 處理趨勢文件: {trend_file.name}")
                target_file = trends_content_dir / trend_file.name
                self._copy_hugo_content_file(trend_file, target_file)
                html_files.append(f"trends/{trend_file.stem}/index.html")

        # 3. 處理會議詳細目錄
        sessions_dir = md_path / "sessions"
        if sessions_dir.exists():
            logger.info(f"📂 處理會議詳細目錄: {sessions_dir}")
            sessions_content_dir = content_dir / "sessions"
            sessions_content_dir.mkdir(parents=True, exist_ok=True)

            # 創建會議索引頁
            self._create_sessions_index(sessions_content_dir)
            html_files.append("sessions/index.html")

            # 處理每個會議文件
            for session_file in sessions_dir.glob("session-*.md"):
                logger.info(f"  📄 處理會議文件: {session_file.name}")
                target_file = sessions_content_dir / session_file.name
                self._copy_hugo_content_file(session_file, target_file)
                html_files.append(f"sessions/{session_file.stem}/index.html")

        # 4. 處理其他 Markdown 文件
        for md_file in md_path.glob("*.md"):
            if md_file.name not in ["_index.md", "trends-analysis.md"]:
                logger.info(f"📄 處理其他文件: {md_file.name}")
                self._process_single_markdown_file(md_file, content_dir, template_style)
                html_files.append(f"{md_file.stem}/index.html")

        logger.info(f"✅ 增強版結構處理完成，預期生成 {len(html_files)} 個 HTML 文件")
        return html_files

    def _process_standard_markdown_files(self, md_path: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理標準 Markdown 文件"""
        html_files = []

        # 處理每個 Markdown 文件
        for md_file in md_path.glob("*.md"):
            try:
                html_files.extend(self._process_single_markdown_file(md_file, content_dir, template_style))
            except Exception as e:
                logger.error(f"處理 Markdown 文件失敗 {md_file}: {e}")

        return html_files

    def _process_single_markdown_file(self, md_file: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理單個 Markdown 文件"""
        try:
            # 讀取 Markdown 內容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析元數據
            metadata = self._extract_metadata_from_content(content, md_file.stem)

            # 創建 Hugo 內容文件
            hugo_content = self._create_hugo_content(content, metadata)

            # 使用 Hugo Page Bundle 結構：每個報告都有自己的目錄
            posts_dir = content_dir / "posts"
            posts_dir.mkdir(parents=True, exist_ok=True)

            # 為 posts 目錄創建 _index.md（如果不存在）
            posts_index = posts_dir / "_index.md"
            if not posts_index.exists():
                with open(posts_index, 'w', encoding='utf-8') as f:
                    f.write("""---
title: 會議報告
description: 所有會議報告的列表
---

# 會議報告

這裡包含所有的會議報告。
""")

            # 生成簡短且安全的文件名
            session_id = md_file.stem

            # 提取 UUID 的前8個字符作為唯一標識
            if '_' in session_id:
                uuid_part = session_id.split('_')[0][:8]
            else:
                uuid_part = session_id[:8]

            # 使用簡短的文件名：report-UUID
            safe_filename = f"report-{uuid_part}"

            # 確保文件名是安全的（只包含字母數字和連字符）
            import re
            safe_filename = re.sub(r'[^a-zA-Z0-9-]', '', safe_filename)

            # 創建 Page Bundle 目錄結構：posts/report-xxx/index.md
            bundle_dir = posts_dir / safe_filename
            bundle_dir.mkdir(parents=True, exist_ok=True)

            # 保存為 index.md（Page Bundle 的標準文件名）
            output_file = bundle_dir / "index.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(hugo_content)

            # 記錄生成的文件（Hugo Page Bundle 會生成對應的 HTML）
            return [f"posts/{safe_filename}/index.html"]

        except Exception as e:
            logger.error(f"處理 Markdown 文件失敗 {md_file.name}: {e}")
            return []

    def _copy_hugo_content_file(self, source_file: pathlib.Path, target_file: pathlib.Path):
        """複製 Hugo 內容文件"""
        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # 讀取源文件內容
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 確保內容有正確的 Hugo front matter
            if not content.startswith('---'):
                # 如果沒有 front matter，添加基本的
                title = source_file.stem.replace('-', ' ').title()
                front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
---

"""
                content = front_matter + content

            # 寫入目標文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ 複製 Hugo 內容文件: {source_file.name} → {target_file}")

        except Exception as e:
            logger.error(f"❌ 複製 Hugo 內容文件失敗 {source_file} → {target_file}: {e}")

    def _convert_trends_analysis_to_index(self, trends_analysis_file: pathlib.Path, index_file: pathlib.Path):
        """將趨勢分析文件轉換為首頁"""
        try:
            with open(trends_analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 修改 front matter 以適合首頁
            if content.startswith('---'):
                # 找到 front matter 的結束位置
                end_pos = content.find('---', 3)
                if end_pos != -1:
                    front_matter = content[3:end_pos].strip()
                    body_content = content[end_pos + 3:].strip()

                    # 創建新的首頁 front matter
                    new_front_matter = f"""---
title: "技術趨勢分析報告"
description: "深度技術趨勢分析與會議洞察"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "homepage"
layout: "index"
---

"""
                    content = new_front_matter + body_content

            index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ 轉換趨勢分析為首頁: {trends_analysis_file.name} → {index_file.name}")

        except Exception as e:
            logger.error(f"❌ 轉換趨勢分析為首頁失敗: {e}")

    def _create_trends_index(self, trends_content_dir: pathlib.Path):
        """創建趨勢分類索引頁"""
        try:
            index_content = f"""---
title: "技術趨勢分類"
description: "探索各種技術趨勢的詳細分析"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "section"
layout: "list"
---

# 技術趨勢分類

探索當前最重要的技術趨勢，深入了解每個領域的發展動向和關鍵洞察。

{{{{< trend-list >}}}}
"""

            index_file = trends_content_dir / "_index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)

            logger.info(f"✅ 創建趨勢分類索引頁: {index_file}")

        except Exception as e:
            logger.error(f"❌ 創建趨勢分類索引頁失敗: {e}")

    def _create_sessions_index(self, sessions_content_dir: pathlib.Path):
        """創建會議索引頁"""
        try:
            index_content = f"""---
title: "會議詳細報告"
description: "所有會議的詳細分析和洞察"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "section"
layout: "list"
---

# 會議詳細報告

瀏覽所有會議的深度分析報告，獲取技術洞察和實用建議。

{{{{< session-list >}}}}
"""

            index_file = sessions_content_dir / "_index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)

            logger.info(f"✅ 創建會議索引頁: {index_file}")

        except Exception as e:
            logger.error(f"❌ 創建會議索引頁失敗: {e}")

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
            "draft": False,  # 明確設置為非草稿
            "type": "posts",  # 明確設置內容類型
            "layout": "single",  # 明確設置佈局類型
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
{yaml_front_matter.strip()}
---

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
                    "generated_by": "本報告由 NeoTrendHub 自動生成",
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
                    "generated_by": "本报告由 NeoTrendHub 自动生成",
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
                    "generated_by": "This report was automatically generated by NeoTrendHub",
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

    def _fix_offline_paths(self, output_dir: str):
        """修復離線瀏覽的路徑問題 - 增強版"""
        try:
            output_path = pathlib.Path(output_dir)
            logger.info("開始修復離線瀏覽路徑...")

            # 統計修復的文件數量
            fixed_files = 0
            total_files = 0

            # 遞歸處理所有 HTML 文件
            for html_file in output_path.rglob("*.html"):
                total_files += 1

                # 計算文件相對於根目錄的深度
                relative_path = html_file.relative_to(output_path)
                depth = len(relative_path.parts) - 1

                # 跳過靜態資源目錄
                if any(part in ['css', 'js', 'images', 'static'] for part in relative_path.parts[:-1]):
                    continue

                if self._fix_html_file_paths(html_file, depth):
                    fixed_files += 1
                    logger.debug(f"修復文件: {relative_path} (深度: {depth})")

            logger.info(f"離線瀏覽路徑修復完成: 處理 {total_files} 個文件，修復 {fixed_files} 個文件")

        except Exception as e:
            logger.error(f"修復離線路徑時發生錯誤: {e}")
            raise

    def _fix_html_file_paths(self, html_file: pathlib.Path, depth: int) -> bool:
        """
        修復單個 HTML 文件的路徑 - 增強版

        Args:
            html_file: HTML 文件路徑
            depth: 文件相對於根目錄的深度

        Returns:
            bool: 修復是否成功
        """
        try:
            # 讀取文件內容
            with open(html_file, 'r', encoding='utf-8') as f:
                original_content = f.read()

            content = original_content
            import re

            # 根據目錄深度確定相對路徑前綴
            prefix = "../" * depth if depth > 0 else ""

            # 定義需要修復的路徑模式
            path_patterns = [
                # 靜態資源路徑
                (r'href=/css/', f'href={prefix}css/'),
                (r'src=/css/', f'src={prefix}css/'),
                (r'href=/js/', f'href={prefix}js/'),
                (r'src=/js/', f'src={prefix}js/'),
                (r'href=/images/', f'href={prefix}images/'),
                (r'src=/images/', f'src={prefix}images/'),
                (r'href=/static/', f'href={prefix}static/'),
                (r'src=/static/', f'src={prefix}static/'),
                (r'href=/favicon\.ico', f'href={prefix}favicon.ico'),

                # 內部頁面連結
                (r'href=/index\.html', f'href={prefix}index.html'),
                (r'href=/seminars/', f'href={prefix}seminars/'),
                (r'href=/categories/', f'href={prefix}categories/'),
                (r'href=/tags/', f'href={prefix}tags/'),
                (r'href=/sitemap\.xml', f'href={prefix}sitemap.xml'),
                (r'href=/robots\.txt', f'href={prefix}robots.txt'),

                # 多語言版本路徑
                (r'href=/zh-cn/', f'href={prefix}zh-cn/'),
                (r'href=/zh-tw/', f'href={prefix}zh-tw/'),
                (r'href=/en/', f'href={prefix}en/'),
            ]

            # 應用基本路徑修復
            for pattern, replacement in path_patterns:
                content = re.sub(pattern, replacement, content)

            # 處理根目錄連結的特殊情況
            if depth == 0:
                # 根目錄文件：href="/" -> href="./"
                content = re.sub(r'href="/"(?=\s|>)', 'href="./"', content)
                content = re.sub(r"href='/'(?=\s|>)", "href='./'", content)
            else:
                # 子目錄文件：href="/" -> href="../" 或 href="../../"
                content = re.sub(r'href="/"(?=\s|>)', f'href="{prefix}"', content)
                content = re.sub(r"href='/'(?=\s|>)", f"href='{prefix}'", content)

            # 使用高級正則表達式修復所有剩餘的內部連結
            def fix_advanced_internal_link(match):
                quote = match.group(1)  # 引號類型 (" 或 ')
                href_value = match.group(2)  # href 值

                # 保留外部連結
                if (href_value.startswith('http://') or
                        href_value.startswith('https://') or
                        href_value.startswith('//') or
                        href_value.startswith('mailto:') or
                        href_value.startswith('tel:')):
                    return match.group(0)

                # 保留錨點連結
                if href_value.startswith('#'):
                    return match.group(0)

                # 保留已經是相對路徑的連結
                if not href_value.startswith('/'):
                    return match.group(0)

                # 修復內部連結：移除開頭的 / 並添加適當的前綴
                fixed_href = prefix + href_value[1:]
                return f'href={quote}{fixed_href}{quote}'

            # 匹配所有 href 屬性，支援雙引號和單引號
            content = re.sub(r'href=(["\'])([^"\']*?)\1', fix_advanced_internal_link, content)

            # 修復 src 屬性（主要針對 JavaScript 文件）
            def fix_src_link(match):
                quote = match.group(1)
                src_value = match.group(2)

                # 保留外部資源
                if (src_value.startswith('http://') or
                        src_value.startswith('https://') or
                        src_value.startswith('//')):
                    return match.group(0)

                # 保留已經是相對路徑的資源
                if not src_value.startswith('/'):
                    return match.group(0)

                # 修復內部資源路徑
                fixed_src = prefix + src_value[1:]
                return f'src={quote}{fixed_src}{quote}'

            content = re.sub(r'src=(["\'])([^"\']*?)\1', fix_src_link, content)

            # 只有在內容確實發生變化時才寫入文件
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

            return False

        except Exception as e:
            logger.error(f"修復文件 {html_file} 路徑時發生錯誤: {e}")
            return False

    def _collect_site_info(self, md_dir: str, output_dir: str, html_files: List[str]) -> Dict[str, Any]:
        """收集網站信息"""
        try:
            md_path = pathlib.Path(md_dir)
            output_path = pathlib.Path(output_dir)

            # 統計信息
            md_files = list(md_path.glob("*.md")) if md_path.exists() else []
            html_file_paths = list(output_path.rglob("*.html")) if output_path.exists() else []

            # 提取報告信息
            reports = []
            seminars = set()
            categories = set()
            tags = set()

            for md_file in md_files:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    metadata = self._extract_metadata_from_content(content, md_file.stem)
                    reports.append({
                        'title': metadata.title,
                        'seminar': metadata.seminar,
                        'category': metadata.category,
                        'tags': metadata.tags,
                        'filename': md_file.stem
                    })

                    seminars.add(metadata.seminar)
                    categories.add(metadata.category)
                    tags.update(metadata.tags)

                except Exception as e:
                    logger.warning(f"無法解析報告文件 {md_file}: {e}")

            # 從目錄路徑中提取 batch_id
            batch_id = "unknown"
            try:
                # 假設目錄結構是 reports/batch_YYYYMMDD_HHMMSS/
                if "batch_" in md_dir:
                    batch_id = md_dir.split("batch_")[1].split("/")[0]
                elif "batch_" in output_dir:
                    batch_id = output_dir.split("batch_")[1].split("/")[0]
            except Exception:
                logger.warning("無法從路徑中提取 batch_id")

            return {
                'batch_id': batch_id,
                'total_reports': len(reports),
                'total_html_files': len(html_file_paths),
                'reports': reports,
                'seminars': list(seminars),
                'categories': list(categories),
                'tags': list(tags),
                'generation_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'main_report': reports[0] if reports else None
            }

        except Exception as e:
            logger.error(f"收集網站信息時發生錯誤: {e}")
            return {
                'total_reports': 0,
                'total_html_files': 0,
                'reports': [],
                'seminars': [],
                'categories': [],
                'tags': [],
                'generation_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'main_report': None
            }

    def _generate_html_launcher(self, output_dir: str, site_info: Dict[str, Any],
                                template_style: str) -> str:
        """生成 HTML 啟動器頁面"""
        try:
            output_path = pathlib.Path(output_dir)
            launcher_file = output_path / "啟動器.html"

            # 獲取主要報告信息
            main_report = site_info.get('main_report', {})
            total_reports = site_info.get('total_reports', 0)
            seminars = site_info.get('seminars', [])
            tags = site_info.get('tags', [])

            # 生成標籤 HTML
            tags_html = ""
            for tag in tags[:10]:  # 只顯示前10個標籤
                tags_html += f'<span class="tag">{tag}</span>\n                '

            # 生成快速導航按鈕
            nav_buttons = []
            if main_report:
                # 主報告按鈕
                main_report_filename = main_report.get('filename', '')
                if main_report_filename:
                    # 查找主報告的實際路徑
                    for report in site_info.get('reports', []):
                        if report.get('filename') == main_report_filename:
                            seminar_slug = self._slugify(report.get('seminar', ''))
                            report_path = f"{seminar_slug}/{main_report_filename}/index.html"
                            nav_buttons.append({
                                'text': '📄 直接查看主報告',
                                'href': report_path,
                                'class': 'btn-secondary'
                            })
                            break

            # 添加其他導航按鈕
            nav_buttons.extend([
                {'text': '🏠 開始瀏覽報告', 'href': 'index.html', 'class': 'btn-primary'},
                {'text': '📚 瀏覽所有研討會', 'href': 'seminars/index.html', 'class': 'btn-secondary'},
                {'text': '🏷️ 按標籤瀏覽', 'href': 'tags/index.html', 'class': 'btn-secondary'}
            ])

            # 生成按鈕 HTML
            buttons_html = ""
            for button in nav_buttons:
                buttons_html += f'''            <a href="{button['href']}" class="btn {button['class']}">
                {button['text']}
            </a>
'''

            launcher_html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeoTrendHub 會議報告 - 啟動器</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft JhengHei', 'PingFang TC', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .launcher-container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
            max-width: 800px;
            width: 100%;
            text-align: center;
        }}

        .logo {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}

        .welcome-text {{
            font-size: 1.1em;
            color: #333;
            margin-bottom: 40px;
            line-height: 1.6;
        }}

        .report-info {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }}

        .report-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}

        .report-meta {{
            color: #666;
            margin-bottom: 15px;
        }}

        .report-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }}

        .tag {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }}

        .action-buttons {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .btn {{
            display: inline-block;
            padding: 15px 25px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-secondary {{
            background: #f8f9fa;
            color: #333;
            border: 2px solid #ddd;
        }}

        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }}

        .instructions {{
            background: #e8f4fd;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            text-align: left;
        }}

        .instructions h3 {{
            color: #2c5aa0;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}

        .instructions ol {{
            color: #333;
            line-height: 1.6;
            padding-left: 20px;
        }}

        .instructions li {{
            margin-bottom: 8px;
        }}

        .footer {{
            margin-top: 30px;
            color: #999;
            font-size: 0.9em;
        }}

        @media (max-width: 600px) {{
            .launcher-container {{
                padding: 20px;
            }}

            .logo {{
                font-size: 2em;
            }}

            .action-buttons {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="launcher-container">
        <div class="logo">📊 NeoTrendHub</div>
        <div class="subtitle">AI 驅動的會議報告分析平台</div>

        <div class="welcome-text">
            歡迎使用 NeoTrendHub 會議報告系統！<br>
            這是一個離線版本，包含完整的會議報告內容，無需網路連接即可瀏覽。
        </div>

        <div class="report-info">
            <div class="report-title">📋 本次報告內容</div>
            <div class="report-meta">'''

            if main_report:
                launcher_html += f'''
                <strong>主要報告：</strong>{main_report.get('title', '未知報告')}<br>
                <strong>研討會：</strong>{main_report.get('seminar', '未知研討會')}<br>
                <strong>報告類型：</strong>{main_report.get('category', '主題演講')}<br>'''

            launcher_html += f'''
                <strong>總報告數：</strong>{total_reports} 篇<br>
                <strong>生成時間：</strong>{site_info.get('generation_time', '未知')}
            </div>
            <div class="report-tags">
                {tags_html}
            </div>
        </div>

        <div class="action-buttons">
{buttons_html}        </div>

        <div class="instructions">
            <h3>📖 使用說明</h3>
            <ol>
                <li><strong>開始瀏覽：</strong>點擊上方「開始瀏覽報告」按鈕進入主頁面</li>
                <li><strong>導航瀏覽：</strong>使用頂部導航菜單在不同頁面間切換</li>
                <li><strong>多語言：</strong>支援繁體中文、簡體中文、英文版本</li>
                <li><strong>離線使用：</strong>所有內容都已下載，無需網路連接</li>
                <li><strong>響應式設計：</strong>支援電腦、平板、手機等各種設備</li>
                <li><strong>搜索功能：</strong>可使用瀏覽器的搜索功能（Ctrl+F）查找內容</li>
            </ol>
        </div>

        <div class="footer">
            <p>🤖 由 NeoTrendHub AI 自動生成 | 📅 生成時間：{site_info.get('generation_time', '未知')}</p>
            <p>💡 如有問題，請聯繫技術支援團隊</p>
        </div>
    </div>

    <script>
        // 自動檢測並修復可能的路徑問題
        document.addEventListener('DOMContentLoaded', function() {{
            // 添加點擊統計（僅在控制台顯示）
            const buttons = document.querySelectorAll('.btn');
            buttons.forEach(button => {{
                button.addEventListener('click', function() {{
                    console.log('用戶點擊了：', this.textContent.trim());
                }});
            }});
        }});
    </script>
</body>
</html>'''

            with open(launcher_file, 'w', encoding='utf-8') as f:
                f.write(launcher_html)

            logger.info(f"HTML 啟動器已生成: {launcher_file}")
            return str(launcher_file)

        except Exception as e:
            logger.error(f"生成 HTML 啟動器時發生錯誤: {e}")
            return ""

    def _generate_instructions_file(self, output_dir: str, site_info: Dict[str, Any]) -> str:
        """生成使用說明文件"""
        try:
            output_path = pathlib.Path(output_dir)
            instructions_file = output_path / "使用說明.txt"

            main_report = site_info.get('main_report', {})
            total_reports = site_info.get('total_reports', 0)
            total_html_files = site_info.get('total_html_files', 0)
            tags = site_info.get('tags', [])

            instructions_content = f'''📊 NeoTrendHub 會議報告 - 離線版本使用說明
==============================================

🎯 快速開始
----------
1. 解壓縮 ZIP 檔案到任意資料夾
2. 雙擊「啟動器.html」檔案
3. 在瀏覽器中開始瀏覽報告

📋 檔案說明
----------
📁 主要檔案：
- 啟動器.html          ← 主要入口，請從這裡開始
- index.html           ← 網站首頁
- 使用說明.txt         ← 本說明文件

📁 重要目錄：
- css/                 ← 樣式文件
- js/                  ← JavaScript 文件
- seminars/            ← 研討會分類頁面
- tags/                ← 標籤分類頁面
- categories/          ← 內容分類頁面

🌐 多語言版本：
- zh-tw/               ← 繁體中文版本
- zh-cn/               ← 簡體中文版本
- en/                  ← 英文版本

📊 本次報告統計
--------------
- 總報告數：{total_reports} 篇
- 總頁面數：{total_html_files} 個
- 生成時間：{site_info.get('generation_time', '未知')}'''

            if main_report:
                instructions_content += f'''
- 主要報告：{main_report.get('title', '未知報告')}
- 研討會：{main_report.get('seminar', '未知研討會')}
- 報告類型：{main_report.get('category', '主題演講')}'''

            if tags:
                tags_str = '、'.join(tags[:10])
                if len(tags) > 10:
                    tags_str += f" 等 {len(tags)} 個標籤"
                instructions_content += f'''
- 主要標籤：{tags_str}'''

            instructions_content += '''

🚀 使用方法
----------
1. 【推薦】從啟動器開始：
   - 雙擊「啟動器.html」
   - 點擊「開始瀏覽報告」按鈕
   - 使用頂部導航菜單瀏覽不同頁面

2. 直接瀏覽特定內容：
   - 網站首頁：index.html
   - 研討會列表：seminars/index.html
   - 標籤瀏覽：tags/index.html

3. 多語言切換：
   - 繁體中文：直接使用根目錄檔案
   - 簡體中文：瀏覽 zh-cn/ 目錄下的檔案
   - 英文：瀏覽 en/ 目錄下的檔案

📱 支援的瀏覽器
--------------
✅ Google Chrome（推薦）
✅ Microsoft Edge
✅ Mozilla Firefox
✅ Safari
✅ 其他現代瀏覽器

📋 主要功能
----------
🏠 首頁：
- 網站概覽和統計信息
- 最新報告列表
- 快速導航連結

📄 報告頁面：
- 完整的會議報告內容
- 技術背景、核心觀點、實踐經驗
- 相關標籤和分類

🏷️ 標籤系統：
- 按技術領域分類（AI、雲端、DevOps等）
- 按會議類型分類（主題演講、技術分享等）
- 快速篩選相關內容

🔍 搜索功能：
- 使用瀏覽器內建搜索（Ctrl+F 或 Cmd+F）
- 在任何頁面搜索關鍵字
- 支援中英文搜索

📱 響應式設計：
- 自動適配電腦、平板、手機
- 觸控友好的操作界面
- 優化的閱讀體驗

🛠️ 故障排除
-----------
❓ 問題：點擊連結沒有反應
💡 解決：確保所有檔案都在同一個資料夾中，沒有被移動或刪除

❓ 問題：樣式顯示異常
💡 解決：檢查 css/ 目錄是否完整，嘗試重新整理頁面（F5）

❓ 問題：圖片或資源無法載入
💡 解決：確保整個資料夾結構完整，沒有缺少檔案

❓ 問題：中文顯示亂碼
💡 解決：確保瀏覽器編碼設定為 UTF-8

❓ 問題：無法開啟 HTML 檔案
💡 解決：右鍵點擊檔案 → 開啟方式 → 選擇瀏覽器

📞 技術支援
----------
如果遇到其他問題，請聯繫技術支援團隊：
- 提供具體的錯誤描述
- 說明使用的作業系統和瀏覽器版本
- 附上錯誤截圖（如果有的話）

🔄 更新說明
----------
版本：1.0.0
生成時間：{site_info.get('generation_time', '未知')}
包含頁面：{total_html_files} 個 HTML 頁面
支援語言：繁體中文、簡體中文、英文

💡 使用小貼士
-----------
1. 建議使用 Chrome 或 Edge 瀏覽器以獲得最佳體驗
2. 可以將啟動器.html 加入書籤，方便下次使用
3. 使用瀏覽器的縮放功能調整字體大小（Ctrl + 滾輪）
4. 可以列印任何頁面保存為 PDF
5. 支援全螢幕模式瀏覽（F11）

🎉 開始使用
----------
現在您可以雙擊「啟動器.html」開始探索 NeoTrendHub 會議報告了！

如有任何問題，請參考上述故障排除部分或聯繫技術支援。

祝您使用愉快！ 😊'''

            with open(instructions_file, 'w', encoding='utf-8') as f:
                f.write(instructions_content)

            logger.info(f"使用說明文件已生成: {instructions_file}")
            return str(instructions_file)

        except Exception as e:
            logger.error(f"生成使用說明文件時發生錯誤: {e}")
            return ""

    def _create_offline_zip_package(self, output_dir: str, site_info: Dict[str, Any]) -> str:
        """創建離線 ZIP 分享包"""
        try:
            output_path = pathlib.Path(output_dir)
            parent_dir = output_path.parent

            # 從 site_info 中獲取 batch_id
            batch_id = site_info.get('batch_id', 'unknown')

            # 生成 ZIP 檔案名（按照要求的格式）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"NeoTrendHub-會議報告-{batch_id}-{timestamp}.zip"
            zip_file_path = parent_dir / zip_filename

            logger.info(f"開始創建 ZIP 離線包: {zip_filename}")

            # 使用 Python 內建的 zipfile 模組
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 遍歷輸出目錄中的所有文件
                for file_path in output_path.rglob('*'):
                    if file_path.is_file():
                        # 跳過隱藏文件和系統文件
                        if file_path.name.startswith('.') or file_path.name == '.DS_Store':
                            continue

                        # 計算相對路徑
                        relative_path = file_path.relative_to(output_path)

                        # 添加文件到 ZIP
                        zipf.write(file_path, relative_path)
                        logger.debug(f"添加文件到 ZIP: {relative_path}")

            # 檢查 ZIP 文件是否創建成功
            if zip_file_path.exists():
                file_size = zip_file_path.stat().st_size
                file_size_mb = file_size / (1024 * 1024)
                logger.info(f"ZIP 離線包創建成功: {zip_filename} ({file_size_mb:.2f} MB)")
                return str(zip_file_path)
            else:
                logger.error("ZIP 檔案創建失敗")
                return ""

        except Exception as e:
            logger.error(f"創建 ZIP 離線包時發生錯誤: {e}")
            import traceback
            logger.error(f"詳細錯誤: {traceback.format_exc()}")
            return ""

    def _build_hugo_site(self, site_dir: pathlib.Path, output_dir: str) -> bool:
        """構建 Hugo 靜態網站"""
        try:
            # 確保輸出目錄存在
            output_path = pathlib.Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # 設置 Hugo 構建命令 - 使用絕對路徑
            cmd = [
                self.hugo_binary,
                "--destination", str(output_path.absolute()),
                "--gc",
                "--cleanDestinationDir",
                "--buildDrafts"  # 包含草稿內容，確保所有文件都被構建
            ]

            # 只在生產環境使用 minify，避免破壞 DOCTYPE
            if logger.level > 10:  # 非 DEBUG 模式
                cmd.append("--minify")

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
                return True
            else:
                logger.warning(f"輸出目錄不存在: {output_path}")
                return False

        except subprocess.CalledProcessError as e:
            error_msg = f"Hugo 構建失敗 (返回碼: {e.returncode})"
            if e.stdout:
                error_msg += f"\n標準輸出: {e.stdout}"
            if e.stderr:
                error_msg += f"\n錯誤輸出: {e.stderr}"
            logger.error(error_msg)

            # 嘗試檢查 Hugo 網站結構
            self._debug_hugo_site_structure(site_dir)

            return False
        except Exception as e:
            logger.error(f"Hugo 構建過程中發生錯誤: {e}")
            return False

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
            <p>&copy; {{ now.Format "2006" }} {{ .Site.Title }}. 由 NeoTrendHub 驅動。</p>
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
title: "NeoTrendHub 會議報告"
description: "AI 驅動的會議報告分析平台"
---

歡迎來到 NeoTrendHub 會議報告平台！

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
