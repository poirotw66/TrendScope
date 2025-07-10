#!/usr/bin/env python3
"""
Hugo 佈局模板和輔助方法
包含所有 Hugo 模板創建和處理方法
"""

import pathlib
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class HugoLayoutMethods:
    """Hugo 佈局模板方法"""
    
    def _create_base_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建基礎佈局模板"""
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
    <header class="site-header">
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
                <div class="nav-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            {{ block "main" . }}{{ end }}
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; {{ now.Year }} {{ .Site.Title }}. 由 TrendScope 技術趨勢分析系統生成。</p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="{{ "js/main.js" | relURL }}"></script>
</body>
</html>'''
        
        (layouts_dir / "_default").mkdir(exist_ok=True)
        with open(layouts_dir / "_default" / "baseof.html", 'w', encoding='utf-8') as f:
            f.write(base_layout)

    def _create_index_layout(self, layouts_dir: pathlib.Path, template_style: str):
        """創建首頁佈局"""
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
            <div class="trend-card">
                <h3 class="trend-title">人工智慧</h3>
                <p class="trend-description">探索 AI 技術的最新發展和應用趨勢</p>
                <div class="trend-stats">
                    <span>相關會議: 12</span>
                    <span>高重要性</span>
                </div>
            </div>
            <div class="trend-card">
                <h3 class="trend-title">雲端技術</h3>
                <p class="trend-description">雲端架構和服務的創新發展</p>
                <div class="trend-stats">
                    <span>相關會議: 8</span>
                    <span>中重要性</span>
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
            {{ if .Params.category }}
            <div class="meta-item">
                <strong>類型：</strong> {{ .Params.category }}
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
                    <span>相關會議: {{ .Count }}</span>
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
