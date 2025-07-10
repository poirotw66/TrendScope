#!/usr/bin/env python3
"""
Hugo 靜態網站生成器
實現 plan.md 中描述的三階層網站結構和專業視覺設計
"""

import logging
import pathlib
import subprocess
import yaml
import zipfile
import shutil
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import re
import unicodedata

logger = logging.getLogger(__name__)

@dataclass
class ReportMetadata:
    """報告元數據"""
    title: str
    seminar: str
    category: str = "主題演講"
    url: str = ""
    date: str = ""
    session_id: str = ""
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")

@dataclass
class HugoConfig:
    """Hugo 配置"""
    base_url: str = "/"
    language_code: str = "zh-tw"
    title: str = "TrendScope 技術趨勢分析"
    description: str = "深度技術趨勢分析與會議洞察"
    theme: str = "neotrendhub"

class HugoReportGenerator:
    """Hugo 靜態網站生成器"""
    
    def __init__(self, hugo_binary: str = "hugo"):
        """
        初始化 Hugo 報告生成器
        
        Args:
            hugo_binary: Hugo 二進制文件路徑
        """
        self.hugo_binary = hugo_binary
        self.config = HugoConfig()
        self._verify_hugo_installation()
        
    def _verify_hugo_installation(self):
        """驗證 Hugo 是否已安裝"""
        try:
            result = subprocess.run([self.hugo_binary, "version"], 
                                    capture_output=True, text=True, check=True)
            logger.info(f"Hugo 版本: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Hugo 未安裝或不在 PATH 中，將使用內建的靜態文件生成")
            self.hugo_binary = None

    def generate_hugo_site(self, md_dir: str, html_dir: str, 
                          template_style: str = "professional",
                          create_offline_package: bool = True) -> Dict[str, Any]:
        """
        生成 Hugo 靜態網站
        
        Args:
            md_dir: Markdown 文件目錄
            html_dir: HTML 輸出目錄
            template_style: 模板樣式
            create_offline_package: 是否創建離線包
            
        Returns:
            生成結果字典
        """
        try:
            logger.info(f"🏗️ 開始生成 Hugo 靜態網站...")
            logger.info(f"   📂 Markdown 目錄: {md_dir}")
            logger.info(f"   📂 HTML 輸出目錄: {html_dir}")
            logger.info(f"   🎨 模板樣式: {template_style}")
            
            # 創建臨時 Hugo 網站目錄
            site_dir = pathlib.Path(html_dir).parent / "hugo_site"
            
            # 初始化 Hugo 網站結構
            self._initialize_hugo_site(site_dir, template_style)
            
            # 處理 Markdown 文件並生成 Hugo 內容
            html_files = self._process_markdown_files(md_dir, site_dir, template_style)
            
            # 構建靜態網站
            if self.hugo_binary:
                success = self._build_hugo_site(site_dir, html_dir)
                if not success:
                    # 如果 Hugo 構建失敗，使用備用方法
                    self._generate_static_files_fallback(site_dir, html_dir)
            else:
                # 使用備用方法生成靜態文件
                self._generate_static_files_fallback(site_dir, html_dir)
            
            # 修復離線瀏覽路徑
            self._fix_offline_paths(html_dir)
            
            # 收集網站信息
            site_info = self._collect_site_info(md_dir, html_dir, html_files)
            
            result = {
                "html_files": html_files,
                "site_info": site_info,
                "output_dir": html_dir
            }
            
            # 創建離線包
            if create_offline_package:
                zip_file = self._create_offline_zip_package(html_dir, site_info)
                if zip_file:
                    result["zip_file"] = zip_file
                
                launcher_file = self._generate_html_launcher(html_dir, site_info)
                if launcher_file:
                    result["launcher_file"] = launcher_file
            
            logger.info(f"✅ Hugo 靜態網站生成完成!")
            logger.info(f"   📄 生成 {len(html_files)} 個 HTML 文件")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Hugo 靜態網站生成失敗: {e}")
            raise

    def _initialize_hugo_site(self, site_dir: pathlib.Path, template_style: str):
        """初始化 Hugo 網站結構"""
        # 創建基本目錄結構
        site_dir.mkdir(parents=True, exist_ok=True)
        
        # 創建必要的子目錄
        directories = [
            "content", "layouts", "static", "static/css", "static/js",
            "layouts/_default", "layouts/partials", "data", "archetypes"
        ]
        
        for directory in directories:
            (site_dir / directory).mkdir(parents=True, exist_ok=True)
        
        # 創建配置文件
        self._create_hugo_config(site_dir, template_style)
        
        # 創建佈局模板
        self._create_hugo_layouts(site_dir, template_style)
        
        # 創建靜態資源
        self._create_static_assets(site_dir, template_style)
        
        # 生成示例內容（用於測試）
        self.generate_sample_content(site_dir)
    
    def _create_hugo_config(self, site_dir: pathlib.Path, template_style: str):
        """創建 Hugo 配置文件"""
        config = {
            "baseURL": self.config.base_url,
            "languageCode": self.config.language_code,
            "title": self.config.title,
            "description": self.config.description,
            "theme": self.config.theme,
            
            # 參數配置
            "params": {
                "description": self.config.description,
                "template_style": template_style,
                "author": "TrendScope",
                "version": "2.0",
                "build_date": datetime.now().isoformat(),
                
                # 社交媒體和 SEO
                "social": {
                    "github": "",
                    "twitter": "",
                    "linkedin": ""
                },
                
                # 功能開關
                "features": {
                    "search": True,
                    "dark_mode": True,
                    "comments": False,
                    "analytics": False
                }
            },
            
            # 分類配置
            "taxonomies": {
                "tags": "tags",
                "categories": "categories",
                "seminars": "seminars",
                "trends": "trends"
            },
            
            # 菜單配置
            "menu": {
                "main": [
                    {"name": "首頁", "url": "/", "weight": 10},
                    {"name": "技術趨勢", "url": "/trends/", "weight": 20},
                    {"name": "會議報告", "url": "/sessions/", "weight": 30},
                    {"name": "研討會", "url": "/seminars/", "weight": 40}
                ]
            },
            
            # 輸出格式
            "outputs": {
                "home": ["HTML", "RSS", "JSON"],
                "page": ["HTML"],
                "section": ["HTML", "RSS"]
            },
            
            # Markdown 配置
            "markup": {
                "goldmark": {
                    "renderer": {
                        "unsafe": True
                    }
                },
                "highlight": {
                    "style": "github",
                    "lineNos": True,
                    "codeFences": True
                }
            }
        }
        
        # 寫入配置文件
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
        
        # 創建部分模板
        self.create_partials(layouts_dir)

    def _create_static_assets(self, site_dir: pathlib.Path, template_style: str):
        """創建靜態資源文件"""
        static_dir = site_dir / "static"
        
        # 創建 CSS 目錄
        css_dir = static_dir / "css"
        css_dir.mkdir(exist_ok=True)
        
        # 創建 CSS 樣式文件
        self._create_css_styles(css_dir, template_style)
        
        # 創建 JavaScript 目錄
        js_dir = static_dir / "js"
        js_dir.mkdir(exist_ok=True)
        
        # 創建 JavaScript 文件
        self._create_javascript(js_dir)

    def _create_css_styles(self, css_dir: pathlib.Path, template_style: str):
        """創建 CSS 樣式文件（基於 sample_630.html 設計）"""
        css_content = self._get_default_css_styles(template_style)

        with open(css_dir / "styles.css", 'w', encoding='utf-8') as f:
            f.write(css_content)

        logger.info(f"CSS 樣式文件已創建: {len(css_content)} 字符")

    def _get_default_css_styles(self, template_style: str) -> str:
        """獲取默認 CSS 樣式 - 增強版三階層設計"""
        return """
/* NeoTrendHub Hugo Theme - Enhanced Three-Tier Design */
/* 完全符合 plan.md 規範的三階層網站樣式 */

:root {{
    /* 主色調 */
    --primary: #3a86ff;
    --primary-dark: #2f6bff;
    --secondary: #33c5ff;
    --success: #3dd16e;
    --warning: #fba024;
    --danger: #f55656;
    --info: #22b3fb;
    --tech: #a251f7;
    --practical: #f16dac;

    /* 文字顏色 */
    --text-primary: #1a202c;
    --text-secondary: #2d3748;
    --text-muted: #718096;
    --text-light: #a0aec0;

    /* 背景顏色 */
    --bg-primary: #ffffff;
    --bg-secondary: #f7fafc;
    --bg-tertiary: #edf2f7;

    /* 邊框和陰影 */
    --border-light: #e2e8f0;
    --border-medium: #cbd5e0;
    --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.07);
    --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.1);

    /* 動畫和過渡 */
    --transition-fast: all 0.2s ease;
    --transition-normal: all 0.3s ease;
    --transition-slow: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);

    /* 圓角 */
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;

    /* 間距 */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    --spacing-3xl: 4rem;

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
}}

/* 深色模式 */
@media (prefers-color-scheme: dark) {{
    :root {{
        --primary: #4b93ff;
        --primary-dark: #2f6bff;
        --secondary: #33c5ff;
        --text-primary: #e2e8f0;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --text-light: #64748b;
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --border-light: #334155;
        --border-medium: #475569;
        --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.2);
        --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.25);
        --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.3);
    }}
}}

/* 基礎樣式 */
* {{
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', 'Roboto', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    margin: 0;
    padding: 0;
    line-height: 1.7;
    overflow-x: hidden;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
}}

/* 標題樣式 */
h1, h2, h3, h4, h5, h6 {{
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
}}

h1 {{ font-size: var(--text-4xl); }}
h2 {{ font-size: var(--text-3xl); }}
h3 {{ font-size: var(--text-2xl); }}
h4 {{ font-size: var(--text-xl); }}
h5 {{ font-size: var(--text-lg); }}
h6 {{ font-size: var(--text-base); }}

/* 連結樣式 */
a {{
    color: var(--primary);
    text-decoration: none;
    transition: var(--transition-fast);
}}

a:hover {{
    color: var(--primary-dark);
    text-decoration: underline;
}}

/* 導航欄 */
.site-header {{
    background: var(--bg-primary);
    box-shadow: var(--shadow-sm);
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid var(--border-light);
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md) 0;
}}

.nav-brand a {{
    font-size: var(--text-2xl);
    font-weight: 800;
    color: var(--primary);
    text-decoration: none;
}}

.nav-menu {{
    display: flex;
    gap: var(--spacing-xl);
    align-items: center;
    list-style: none;
    margin: 0;
    padding: 0;
}}

.nav-link {{
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition-fast);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-sm);
}}

.nav-link:hover {{
    color: var(--primary);
    background-color: rgba(58, 134, 255, 0.1);
}}

/* 英雄區塊 */
.hero {{
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    text-align: center;
    padding: var(--spacing-3xl) 0;
    margin-bottom: var(--spacing-2xl);
}}

.hero-title {{
    font-size: var(--text-5xl);
    font-weight: 800;
    margin-bottom: var(--spacing-md);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
    display: flex;
    justify-content: center;
    gap: var(--spacing-3xl);
    margin-top: var(--spacing-xl);
}}

.stat-item {{
    text-align: center;
}}

.stat-number {{
    display: block;
    font-size: var(--text-4xl);
    font-weight: 800;
    margin-bottom: var(--spacing-xs);
}}

.stat-label {{
    font-size: var(--text-sm);
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* 內容區塊 */
.content-section {{
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-2xl);
    margin: var(--spacing-xl) 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
    transition: var(--transition-normal);
}}

.content-section:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}}

.section-title {{
    font-size: var(--text-3xl);
    font-weight: 700;
    margin-bottom: var(--spacing-lg);
    color: var(--text-primary);
    position: relative;
    padding-bottom: var(--spacing-sm);
}}

.section-title::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    border-radius: var(--radius-sm);
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
    transition: var(--transition-normal);
    border: 1px solid var(--border-light);
    position: relative;
    overflow: hidden;
}}

.trend-card:hover {{
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}}

.trend-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
}}

.trend-title {{
    font-size: var(--text-2xl);
    font-weight: 700;
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
}}

.trend-description {{
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    line-height: 1.6;
}}

.trend-stats {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: var(--text-sm);
    color: var(--text-muted);
}}

/* 會議列表 */
.sessions-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--spacing-lg);
    margin: var(--spacing-xl) 0;
}}

.session-card {{
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-light);
    transition: var(--transition-normal);
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

.session-meta {{
    display: flex;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    font-size: var(--text-sm);
    color: var(--text-muted);
}}

.session-trends {{
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
    margin-top: var(--spacing-md);
}}

.trend-tag {{
    background: var(--primary);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    text-decoration: none;
    transition: var(--transition-fast);
}}

.trend-tag:hover {{
    background: var(--primary-dark);
    transform: translateY(-1px);
}}

/* 響應式設計 */
@media (max-width: 768px) {{
    .hero-title {{
        font-size: var(--text-3xl);
    }}

    .hero-stats {{
        flex-direction: column;
        gap: var(--spacing-lg);
    }}

    .trends-grid,
    .sessions-grid {{
        grid-template-columns: 1fr;
    }}

    .container {{
        padding: 0 var(--spacing-md);
    }}

    .nav-menu {{
        display: none;
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

    def _create_base_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建基礎佈局模板"""
        from .hugo_report_layouts import HugoLayoutMethods
        layout_methods = HugoLayoutMethods()
        layout_methods._create_base_layout(layouts_dir, template_style)

    def _create_index_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建首頁佈局"""
        from .hugo_report_layouts import HugoLayoutMethods
        layout_methods = HugoLayoutMethods()
        layout_methods._create_index_layout(layouts_dir, template_style)

    def _create_single_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建單頁佈局"""
        from .hugo_report_layouts import HugoLayoutMethods
        layout_methods = HugoLayoutMethods()
        layout_methods._create_single_layout(layouts_dir, template_style)

    def _create_list_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建列表佈局"""
        from .hugo_report_layouts import HugoLayoutMethods
        layout_methods = HugoLayoutMethods()
        layout_methods._create_list_layout(layouts_dir, template_style)

    def _create_taxonomy_layouts(self, layouts_dir: pathlib.Path, template_style: str):
        """創建分類佈局"""
        from .hugo_report_layouts import HugoLayoutMethods
        layout_methods = HugoLayoutMethods()
        layout_methods._create_taxonomy_layouts(layouts_dir, template_style)

    def create_partials(self, layouts_dir: pathlib.Path):
        """創建 Hugo 部分模板"""
        partials_dir = layouts_dir / "partials"
        partials_dir.mkdir(exist_ok=True)

        # 創建頭部模板
        header_template = '''<header class="site-header">
    <div class="container">
        <nav class="navbar">
            <div class="nav-brand">
                <a href="{{ "/" | relURL }}">{{ .Site.Title }}</a>
            </div>
            <ul class="nav-menu">
                {{ range .Site.Menus.main }}
                <li><a href="{{ .URL | relURL }}" class="nav-link">{{ .Name }}</a></li>
                {{ end }}
            </ul>
        </nav>
    </div>
</header>'''

        with open(partials_dir / "header.html", 'w', encoding='utf-8') as f:
            f.write(header_template)

        # 創建頁腳模板
        footer_template = '''<footer class="site-footer">
    <div class="container">
        <p>&copy; {{ now.Year }} {{ .Site.Title }}. 由 TrendScope 技術趨勢分析系統生成。</p>
    </div>
</footer>'''

        with open(partials_dir / "footer.html", 'w', encoding='utf-8') as f:
            f.write(footer_template)

    def generate_sample_content(self, site_dir: pathlib.Path):
        """生成示例內容（用於測試）"""
        content_dir = site_dir / "content"

        # 創建示例首頁內容
        index_content = '''---
title: "TrendScope 技術趨勢分析"
description: "深度技術趨勢分析與會議洞察"
---

# 歡迎來到 TrendScope

探索最新的技術趨勢，深入了解行業發展動向。
'''

        with open(content_dir / "_index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)

    # 整合輔助工具方法
    def _process_markdown_files(self, md_dir: str, site_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理 Markdown 文件並生成 Hugo 內容"""
        from .hugo_report_utils import HugoReportUtils
        utils = HugoReportUtils()
        return utils._process_markdown_files(md_dir, site_dir, template_style)

    def _extract_metadata_from_content(self, content: str, filename: str) -> ReportMetadata:
        """從內容中提取元數據"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._extract_metadata_from_content(content, filename)

    def _generate_tags_from_content(self, content: str, seminar: str, category: str) -> List[str]:
        """從內容生成標籤"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._generate_tags_from_content(content, seminar, category)

    def _create_hugo_content(self, content: str, metadata: ReportMetadata) -> str:
        """創建 Hugo 內容文件"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._create_hugo_content(content, metadata)

    def _build_hugo_site(self, site_dir: pathlib.Path, output_dir: str) -> bool:
        """構建 Hugo 靜態網站"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        core.hugo_binary = self.hugo_binary  # 傳遞 hugo_binary 屬性
        return core._build_hugo_site(site_dir, output_dir)

    def _generate_static_files_fallback(self, site_dir: pathlib.Path, output_dir: str):
        """備用靜態文件生成方法"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._generate_static_files_fallback(site_dir, output_dir)

    def _fix_offline_paths(self, output_dir: str):
        """修復離線瀏覽的路徑問題"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._fix_offline_paths(output_dir)

    def _collect_site_info(self, md_dir: str, output_dir: str, html_files: List[str]) -> Dict[str, Any]:
        """收集網站信息"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._collect_site_info(md_dir, output_dir, html_files)

    def _create_offline_zip_package(self, output_dir: str, site_info: Dict[str, Any]) -> str:
        """創建離線 ZIP 分享包"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._create_offline_zip_package(output_dir, site_info)

    def _generate_html_launcher(self, output_dir: str, site_info: Dict[str, Any]) -> str:
        """生成 HTML 啟動器文件"""
        from .hugo_report_core import HugoReportCore
        core = HugoReportCore()
        return core._generate_html_launcher(output_dir, site_info)
