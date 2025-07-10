#!/usr/bin/env python3
"""
Hugo 導航佈局模板
包含完整三階層導航系統的 Hugo 模板
"""

import pathlib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HugoNavigationLayouts:
    """Hugo 導航佈局模板類"""
    
    def _create_base_layout_with_navigation(self, layouts_dir: pathlib.Path, template_style: str):
        """創建包含完整導航的基礎佈局模板"""
        base_layout = '''<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}" class="no-js">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} - {{ .Site.Title }}{{ end }}</title>
    <meta name="description" content="{{ if .Description }}{{ .Description }}{{ else }}{{ .Site.Params.description }}{{ end }}">
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ "css/styles.css" | relURL }}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ "favicon.ico" | relURL }}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }}{{ end }}">
    <meta property="og:description" content="{{ if .Description }}{{ .Description }}{{ else }}{{ .Site.Params.description }}{{ end }}">
    <meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
    <meta property="og:url" content="{{ .Permalink }}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }}{{ end }}">
    <meta name="twitter:description" content="{{ if .Description }}{{ .Description }}{{ else }}{{ .Site.Params.description }}{{ end }}">
</head>
<body>
    <!-- 主導航 -->
    {{ partial "navigation.html" . }}

    <!-- 麵包屑導航 -->
    {{ if not .IsHome }}
    {{ partial "breadcrumbs.html" . }}
    {{ end }}

    <main>
        <div class="container">
            {{ block "main" . }}{{ end }}
        </div>
    </main>

    <!-- 頁腳 -->
    {{ partial "footer.html" . }}

    <!-- JavaScript -->
    <script src="{{ "js/main.js" | relURL }}"></script>
</body>
</html>'''
        
        (layouts_dir / "_default").mkdir(exist_ok=True)
        with open(layouts_dir / "_default" / "baseof.html", 'w', encoding='utf-8') as f:
            f.write(base_layout)

    def _create_navigation_partials(self, layouts_dir: pathlib.Path):
        """創建導航組件"""
        partials_dir = layouts_dir / "partials"
        partials_dir.mkdir(exist_ok=True)

        # 主導航模板
        navigation_template = '''<header class="site-header">
    <div class="container">
        <nav class="navbar">
            <div class="nav-brand">
                <a href="{{ "/" | relURL }}">{{ .Site.Title }}</a>
            </div>
            <ul class="nav-menu">
                {{ range .Site.Menus.main }}
                <li>
                    <a href="{{ .URL | relURL }}" class="nav-link{{ if eq $.Page.RelPermalink .URL }} active{{ end }}">
                        {{ .Name }}
                    </a>
                </li>
                {{ end }}
            </ul>
            <button class="nav-toggle" aria-label="切換導航選單">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </nav>
    </div>
</header>'''

        with open(partials_dir / "navigation.html", 'w', encoding='utf-8') as f:
            f.write(navigation_template)

        # 麵包屑導航模板
        breadcrumbs_template = '''<nav class="breadcrumb">
    <div class="container">
        <div class="breadcrumb-nav">
            <div class="breadcrumb-item">
                <a href="{{ "/" | relURL }}" class="breadcrumb-link">首頁</a>
            </div>
            {{ if .Parent }}
            {{ range .Parent.Ancestors.Reverse }}
            <div class="breadcrumb-item">
                <a href="{{ .Permalink }}" class="breadcrumb-link">{{ .Title }}</a>
            </div>
            {{ end }}
            {{ if .Parent }}
            <div class="breadcrumb-item">
                <a href="{{ .Parent.Permalink }}" class="breadcrumb-link">{{ .Parent.Title }}</a>
            </div>
            {{ end }}
            {{ end }}
            <div class="breadcrumb-item">
                <span class="breadcrumb-current">{{ .Title }}</span>
            </div>
        </div>
    </div>
</nav>'''

        with open(partials_dir / "breadcrumbs.html", 'w', encoding='utf-8') as f:
            f.write(breadcrumbs_template)

        # 頁腳模板
        footer_template = '''<footer class="site-footer">
    <div class="container">
        <p>&copy; {{ now.Year }} {{ .Site.Title }}. 由 TrendScope 技術趨勢分析系統生成。</p>
        {{ if .Site.Menus.footer }}
        <nav class="footer-nav">
            {{ range .Site.Menus.footer }}
            <a href="{{ .URL | relURL }}" class="footer-link">{{ .Name }}</a>
            {{ end }}
        </nav>
        {{ end }}
    </div>
</footer>'''

        with open(partials_dir / "footer.html", 'w', encoding='utf-8') as f:
            f.write(footer_template)

        # 相關內容模板
        related_content_template = '''{{ if .Site.Params.navigation.show_related_content }}
<div class="related-content">
    <h3 class="related-title">相關內容</h3>
    <div class="related-links">
        {{ range first 6 (where .Site.RegularPages "Section" .Section) }}
        {{ if ne .Permalink $.Permalink }}
        <a href="{{ .Permalink }}" class="related-link">
            <div class="related-link-title">{{ .Title }}</div>
            <div class="related-link-meta">
                {{ if .Params.seminar }}{{ .Params.seminar }} • {{ end }}
                {{ .Date.Format "2006-01-02" }}
            </div>
        </a>
        {{ end }}
        {{ end }}
    </div>
</div>
{{ end }}'''

        with open(partials_dir / "related-content.html", 'w', encoding='utf-8') as f:
            f.write(related_content_template)

        # 上一頁/下一頁導航模板
        prev_next_template = '''{{ if .Site.Params.navigation.show_prev_next }}
<nav class="nav-buttons">
    <div class="nav-prev">
        {{ if .PrevInSection }}
        <a href="{{ .PrevInSection.Permalink }}" class="nav-btn">
            ← {{ .PrevInSection.Title }}
        </a>
        {{ else }}
        <span class="nav-btn disabled">← 沒有更多內容</span>
        {{ end }}
    </div>
    <div class="nav-next">
        {{ if .NextInSection }}
        <a href="{{ .NextInSection.Permalink }}" class="nav-btn">
            {{ .NextInSection.Title }} →
        </a>
        {{ else }}
        <span class="nav-btn disabled">沒有更多內容 →</span>
        {{ end }}
    </div>
</nav>
{{ end }}'''

        with open(partials_dir / "prev-next.html", 'w', encoding='utf-8') as f:
            f.write(prev_next_template)

    def _create_index_layout_with_links(self, layouts_dir: pathlib.Path, template_style: str):
        """創建包含趨勢分類連結的首頁佈局"""
        index_layout = '''{{ define "main" }}
<div class="homepage">
    <section class="hero">
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
                    <span class="stat-number">{{ len .Site.Taxonomies.trends }}</span>
                    <span class="stat-label">技術趨勢</span>
                </div>
            </div>
        </div>
    </section>

    <!-- 技術趨勢分類 -->
    {{ if .Site.Taxonomies.trends }}
    <section class="content-section">
        <h2 class="section-title">
            <a href="{{ "/trends/" | relURL }}" style="text-decoration: none; color: inherit;">
                技術趨勢分析
            </a>
        </h2>
        <div class="trends-grid">
            {{ range first 6 .Site.Taxonomies.trends.ByCount }}
            <div class="trend-card">
                <h3 class="trend-title">
                    <a href="{{ .Page.Permalink }}" style="text-decoration: none; color: inherit;">
                        {{ .Page.Title }}
                    </a>
                </h3>
                <p class="trend-description">{{ .Page.Summary | default "探索這個技術趨勢的最新發展" }}</p>
                <div class="trend-stats">
                    <span>相關會議: {{ .Count }}</span>
                    <a href="{{ .Page.Permalink }}" class="trend-tag clickable">查看詳情</a>
                </div>
            </div>
            {{ end }}
        </div>
        <div style="text-align: center; margin-top: 2rem;">
            <a href="{{ "/trends/" | relURL }}" class="nav-btn">查看所有技術趨勢</a>
        </div>
    </section>
    {{ end }}

    <!-- 最新會議報告 -->
    <section class="content-section">
        <h2 class="section-title">
            <a href="{{ "/sessions/" | relURL }}" style="text-decoration: none; color: inherit;">
                最新會議報告
            </a>
        </h2>
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
                    <a href="{{ printf "/seminars/%s/" (.Params.seminar | urlize) | relURL }}" class="seminar-link">
                        {{ .Params.seminar }}
                    </a>
                    {{ end }}
                    <span class="session-date">{{ .Date.Format "2006-01-02" }}</span>
                </div>
                {{ if .Params.trends }}
                <div class="session-trends">
                    {{ range .Params.trends }}
                    <a href="{{ printf "/trends/%s/" (. | urlize) | relURL }}" class="trend-tag clickable">{{ . }}</a>
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
        <div style="text-align: center; margin-top: 2rem;">
            <a href="{{ "/sessions/" | relURL }}" class="nav-btn">查看所有會議報告</a>
        </div>
    </section>

    <!-- 研討會分類 -->
    {{ if .Site.Taxonomies.seminars }}
    <section class="content-section">
        <h2 class="section-title">
            <a href="{{ "/seminars/" | relURL }}" style="text-decoration: none; color: inherit;">
                研討會分類
            </a>
        </h2>
        <div class="trends-grid">
            {{ range first 4 .Site.Taxonomies.seminars.ByCount }}
            <div class="trend-card">
                <h3 class="trend-title">
                    <a href="{{ .Page.Permalink }}" style="text-decoration: none; color: inherit;">
                        {{ .Page.Title }}
                    </a>
                </h3>
                <div class="trend-stats">
                    <span>會議數量: {{ .Count }}</span>
                    <a href="{{ .Page.Permalink }}" class="trend-tag clickable">查看會議</a>
                </div>
            </div>
            {{ end }}
        </div>
        <div style="text-align: center; margin-top: 2rem;">
            <a href="{{ "/seminars/" | relURL }}" class="nav-btn">查看所有研討會</a>
        </div>
    </section>
    {{ end }}
</div>
{{ end }}'''

        layouts_dir.mkdir(exist_ok=True)
        with open(layouts_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_layout)

    def _create_single_layout_with_navigation(self, layouts_dir: pathlib.Path, template_style: str):
        """創建包含完整導航的單頁佈局"""
        single_layout = '''{{ define "main" }}
<article class="single-report">
    <header class="content-section">
        <h1 class="section-title">{{ .Title }}</h1>
        <div class="session-meta">
            {{ if .Params.seminar }}
            <div class="meta-item">
                <strong>研討會：</strong>
                <a href="{{ printf "/seminars/%s/" (.Params.seminar | urlize) | relURL }}" class="seminar-link">
                    {{ .Params.seminar }}
                </a>
            </div>
            {{ end }}
            {{ if .Date }}
            <div class="meta-item session-date">
                {{ .Date.Format "2006年01月02日" }}
            </div>
            {{ end }}
            {{ if .Params.category }}
            <div class="meta-item">
                <strong>類型：</strong> {{ .Params.category }}
            </div>
            {{ end }}
            {{ if .Params.url }}
            <div class="meta-item">
                <strong>來源：</strong>
                <a href="{{ .Params.url }}" target="_blank" rel="noopener">查看原文 🔗</a>
            </div>
            {{ end }}
        </div>
        {{ if .Params.trends }}
        <div class="session-trends">
            {{ range .Params.trends }}
            <a href="{{ printf "/trends/%s/" (. | urlize) | relURL }}" class="trend-tag clickable">{{ . }}</a>
            {{ end }}
        </div>
        {{ end }}
        {{ if .Params.tags }}
        <div class="session-trends">
            {{ range .Params.tags }}
            <span class="trend-tag">{{ . }}</span>
            {{ end }}
        </div>
        {{ end }}
    </header>

    <div class="content-section">
        <div class="section-content">
            {{ .Content }}
        </div>
    </div>

    <!-- 上一頁/下一頁導航 -->
    {{ partial "prev-next.html" . }}

    <!-- 相關內容 -->
    {{ partial "related-content.html" . }}
</article>
{{ end }}'''

        default_dir = layouts_dir / "_default"
        default_dir.mkdir(exist_ok=True)
        with open(default_dir / "single.html", 'w', encoding='utf-8') as f:
            f.write(single_layout)

    def _create_list_layout_with_navigation(self, layouts_dir: pathlib.Path, template_style: str):
        """創建包含分類導航的列表佈局"""
        list_layout = '''{{ define "main" }}
<div class="list-page">
    <header class="content-section">
        <h1 class="section-title">{{ .Title }}</h1>
        {{ if .Content }}
        <div class="section-content">
            {{ .Content }}
        </div>
        {{ end }}

        <!-- 分類統計 -->
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">{{ len .Pages }}</span>
                <span class="stat-label">{{ if eq .Section "trends" }}相關會議{{ else if eq .Section "seminars" }}研討會{{ else }}項目{{ end }}</span>
            </div>
            {{ if .Section }}
            <div class="stat-item">
                <span class="stat-number">{{ .Section | title }}</span>
                <span class="stat-label">分類</span>
            </div>
            {{ end }}
        </div>
    </header>

    <!-- 快速導航 -->
    {{ if eq .Section "trends" }}
    <section class="content-section">
        <h3>快速導航到其他趨勢</h3>
        <div class="session-trends">
            {{ range .Site.Taxonomies.trends.ByCount }}
            {{ if ne .Page.Permalink $.Permalink }}
            <a href="{{ .Page.Permalink }}" class="trend-tag clickable">
                {{ .Page.Title }} ({{ .Count }})
            </a>
            {{ end }}
            {{ end }}
        </div>
    </section>
    {{ else if eq .Section "seminars" }}
    <section class="content-section">
        <h3>快速導航到其他研討會</h3>
        <div class="session-trends">
            {{ range .Site.Taxonomies.seminars.ByCount }}
            {{ if ne .Page.Permalink $.Permalink }}
            <a href="{{ .Page.Permalink }}" class="trend-tag clickable">
                {{ .Page.Title }} ({{ .Count }})
            </a>
            {{ end }}
            {{ end }}
        </div>
    </section>
    {{ end }}

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
                    <a href="{{ printf "/seminars/%s/" (.Params.seminar | urlize) | relURL }}" class="seminar-link">
                        {{ .Params.seminar }}
                    </a>
                    {{ end }}
                    <span class="session-date">{{ .Date.Format "2006-01-02" }}</span>
                    {{ if .Params.category }}
                    <span class="session-category">{{ .Params.category }}</span>
                    {{ end }}
                </div>
                {{ if .Params.trends }}
                <div class="session-trends">
                    {{ range .Params.trends }}
                    <a href="{{ printf "/trends/%s/" (. | urlize) | relURL }}" class="trend-tag clickable">{{ . }}</a>
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

    <!-- 返回上級導航 -->
    <nav class="nav-buttons">
        <div class="nav-prev">
            {{ if eq .Section "trends" }}
            <a href="{{ "/trends/" | relURL }}" class="nav-btn">← 所有技術趨勢</a>
            {{ else if eq .Section "seminars" }}
            <a href="{{ "/seminars/" | relURL }}" class="nav-btn">← 所有研討會</a>
            {{ else if eq .Section "sessions" }}
            <a href="{{ "/sessions/" | relURL }}" class="nav-btn">← 所有會議報告</a>
            {{ else }}
            <a href="{{ "/" | relURL }}" class="nav-btn">← 返回首頁</a>
            {{ end }}
        </div>
        <div class="nav-next">
            <a href="{{ "/" | relURL }}" class="nav-btn">返回首頁 →</a>
        </div>
    </nav>
</div>
{{ end }}'''

        default_dir = layouts_dir / "_default"
        default_dir.mkdir(exist_ok=True)
        with open(default_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(list_layout)

    def _create_taxonomy_layouts_with_navigation(self, layouts_dir: pathlib.Path, template_style: str):
        """創建包含導航的分類佈局（趨勢和研討會）"""

        # 趨勢分類佈局
        trends_layout = '''{{ define "main" }}
<div class="taxonomy-page">
    <header class="content-section">
        <h1 class="section-title">技術趨勢分析</h1>
        <p class="section-description">探索最新的技術發展趨勢，深入了解行業動向</p>

        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.Taxonomies.trends }}</span>
                <span class="stat-label">技術趨勢</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.RegularPages }}</span>
                <span class="stat-label">相關會議</span>
            </div>
        </div>
    </header>

    <section class="content-section">
        <div class="trends-grid">
            {{ range .Site.Taxonomies.trends.ByCount }}
            <div class="trend-card">
                <h3 class="trend-title">
                    <a href="{{ .Page.Permalink }}" style="text-decoration: none; color: inherit;">
                        {{ .Page.Title }}
                    </a>
                </h3>
                <p class="trend-description">
                    {{ .Page.Summary | default "探索這個技術趨勢的最新發展和應用案例" }}
                </p>
                <div class="trend-stats">
                    <span>相關會議: {{ .Count }}</span>
                    <a href="{{ .Page.Permalink }}" class="trend-tag clickable">查看詳情</a>
                </div>

                <!-- 顯示相關會議預覽 -->
                {{ if gt .Count 0 }}
                <div class="trend-sessions-preview">
                    <h4>相關會議：</h4>
                    <div class="session-trends">
                        {{ range first 3 .Pages }}
                        <a href="{{ .Permalink }}" class="trend-tag" style="background: var(--secondary);">
                            {{ .Title | truncate 30 }}
                        </a>
                        {{ end }}
                        {{ if gt .Count 3 }}
                        <a href="{{ .Page.Permalink }}" class="trend-tag" style="background: var(--text-muted);">
                            +{{ sub .Count 3 }} 更多
                        </a>
                        {{ end }}
                    </div>
                </div>
                {{ end }}
            </div>
            {{ end }}
        </div>
    </section>

    <!-- 返回導航 -->
    <nav class="nav-buttons">
        <div class="nav-prev">
            <a href="{{ "/" | relURL }}" class="nav-btn">← 返回首頁</a>
        </div>
        <div class="nav-next">
            <a href="{{ "/sessions/" | relURL }}" class="nav-btn">查看所有會議 →</a>
        </div>
    </nav>
</div>
{{ end }}'''

        # 創建趨勢分類目錄和佈局
        trends_dir = layouts_dir / "trends"
        trends_dir.mkdir(exist_ok=True)
        with open(trends_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(trends_layout)

        # 研討會分類佈局
        seminars_layout = '''{{ define "main" }}
<div class="taxonomy-page">
    <header class="content-section">
        <h1 class="section-title">研討會分類</h1>
        <p class="section-description">按研討會分類瀏覽技術會議和演講內容</p>

        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.Taxonomies.seminars }}</span>
                <span class="stat-label">研討會</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ len .Site.RegularPages }}</span>
                <span class="stat-label">會議報告</span>
            </div>
        </div>
    </header>

    <section class="content-section">
        <div class="trends-grid">
            {{ range .Site.Taxonomies.seminars.ByCount }}
            <div class="trend-card">
                <h3 class="trend-title">
                    <a href="{{ .Page.Permalink }}" style="text-decoration: none; color: inherit;">
                        {{ .Page.Title }}
                    </a>
                </h3>
                <div class="trend-stats">
                    <span>會議數量: {{ .Count }}</span>
                    <a href="{{ .Page.Permalink }}" class="trend-tag clickable">查看會議</a>
                </div>

                <!-- 顯示最新會議預覽 -->
                {{ if gt .Count 0 }}
                <div class="trend-sessions-preview">
                    <h4>最新會議：</h4>
                    <div class="session-trends">
                        {{ range first 3 (.Pages.ByDate.Reverse) }}
                        <a href="{{ .Permalink }}" class="trend-tag" style="background: var(--success);">
                            {{ .Title | truncate 30 }}
                        </a>
                        {{ end }}
                        {{ if gt .Count 3 }}
                        <a href="{{ .Page.Permalink }}" class="trend-tag" style="background: var(--text-muted);">
                            +{{ sub .Count 3 }} 更多
                        </a>
                        {{ end }}
                    </div>
                </div>
                {{ end }}

                <!-- 顯示相關技術趨勢 -->
                {{ $seminarTrends := slice }}
                {{ range .Pages }}
                    {{ range .Params.trends }}
                        {{ $seminarTrends = $seminarTrends | append . }}
                    {{ end }}
                {{ end }}
                {{ $uniqueTrends := $seminarTrends | uniq }}
                {{ if $uniqueTrends }}
                <div class="trend-sessions-preview">
                    <h4>相關技術趨勢：</h4>
                    <div class="session-trends">
                        {{ range first 4 $uniqueTrends }}
                        <a href="{{ printf "/trends/%s/" (. | urlize) | relURL }}" class="trend-tag" style="background: var(--tech);">
                            {{ . }}
                        </a>
                        {{ end }}
                    </div>
                </div>
                {{ end }}
            </div>
            {{ end }}
        </div>
    </section>

    <!-- 返回導航 -->
    <nav class="nav-buttons">
        <div class="nav-prev">
            <a href="{{ "/" | relURL }}" class="nav-btn">← 返回首頁</a>
        </div>
        <div class="nav-next">
            <a href="{{ "/trends/" | relURL }}" class="nav-btn">查看技術趨勢 →</a>
        </div>
    </nav>
</div>
{{ end }}'''

        # 創建研討會分類目錄和佈局
        seminars_dir = layouts_dir / "seminars"
        seminars_dir.mkdir(exist_ok=True)
        with open(seminars_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(seminars_layout)

        # 會議報告列表佈局
        sessions_layout = '''{{ define "main" }}
<div class="sessions-page">
    <header class="content-section">
        <h1 class="section-title">所有會議報告</h1>
        <p class="section-description">瀏覽所有技術會議和演講的深度分析報告</p>

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
                <span class="stat-number">{{ len .Site.Taxonomies.trends }}</span>
                <span class="stat-label">技術趨勢</span>
            </div>
        </div>
    </header>

    <!-- 快速篩選 -->
    <section class="content-section">
        <h3>按研討會篩選</h3>
        <div class="session-trends">
            {{ range .Site.Taxonomies.seminars.ByCount }}
            <a href="{{ .Page.Permalink }}" class="trend-tag clickable">
                {{ .Page.Title }} ({{ .Count }})
            </a>
            {{ end }}
        </div>
    </section>

    <section class="content-section">
        <h3>按技術趨勢篩選</h3>
        <div class="session-trends">
            {{ range .Site.Taxonomies.trends.ByCount }}
            <a href="{{ .Page.Permalink }}" class="trend-tag clickable">
                {{ .Page.Title }} ({{ .Count }})
            </a>
            {{ end }}
        </div>
    </section>

    <section class="content-section">
        <div class="sessions-grid">
            {{ range .Site.RegularPages.ByDate.Reverse }}
            <article class="session-card">
                <div class="session-header">
                    <h3 class="session-title">
                        <a href="{{ .Permalink }}">{{ .Title }}</a>
                    </h3>
                </div>
                <div class="session-meta">
                    {{ if .Params.seminar }}
                    <a href="{{ printf "/seminars/%s/" (.Params.seminar | urlize) | relURL }}" class="seminar-link">
                        {{ .Params.seminar }}
                    </a>
                    {{ end }}
                    <span class="session-date">{{ .Date.Format "2006-01-02" }}</span>
                    {{ if .Params.category }}
                    <span class="session-category">{{ .Params.category }}</span>
                    {{ end }}
                </div>
                {{ if .Params.trends }}
                <div class="session-trends">
                    {{ range .Params.trends }}
                    <a href="{{ printf "/trends/%s/" (. | urlize) | relURL }}" class="trend-tag clickable">{{ . }}</a>
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

    <!-- 返回導航 -->
    <nav class="nav-buttons">
        <div class="nav-prev">
            <a href="{{ "/" | relURL }}" class="nav-btn">← 返回首頁</a>
        </div>
        <div class="nav-next">
            <a href="{{ "/trends/" | relURL }}" class="nav-btn">查看技術趨勢 →</a>
        </div>
    </nav>
</div>
{{ end }}'''

        # 創建會議報告目錄和佈局
        sessions_dir = layouts_dir / "sessions"
        sessions_dir.mkdir(exist_ok=True)
        with open(sessions_dir / "list.html", 'w', encoding='utf-8') as f:
            f.write(sessions_layout)

        logger.info("✅ 分類佈局創建完成（包含完整導航）")
