import os
import markdown
import re
from pathlib import Path
import argparse

from src.utils.logging_utils import logger
from src.utils.file_utils import FileUtils

TEMPLATE_DIR = Path(__file__).parent / "templates"
EMAIL_TEMPLATE_PATH = TEMPLATE_DIR / "email_template.html"

def get_template_css(template_style="professional"):
    """根據樣板風格返回對應的 CSS 樣式"""
    css_styles = {
        "professional": """
        /* Professional Business Style - Inspired by sample.html */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', 'Microsoft JhengHei', sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }

        .container {
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
        }

        header {
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #4b6cb7, #182848);
            color: #fff;
            position: relative;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-radius: 10px 10px 0 0;
        }

        header h1 {
            font-size: 2.2rem;
            margin: 0 0 10px 0;
            letter-spacing: 0.5px;
        }

        header p {
            font-size: 1.1rem;
            margin: 0;
            opacity: 0.9;
        }

        .content {
            background-color: #fff;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 30px;
            margin-bottom: 30px;
        }

        /* 基礎區塊樣式 */
        .section-block {
            background-color: #fff;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 5px solid #4b6cb7;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .section-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4b6cb7 0%, #3498db 50%, #2ecc71 100%);
            opacity: 0.6;
        }

        .section-block:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }

        /* 會議資訊區塊 */
        .section-block.meeting-info {
            border-left-color: #3498db;
            background: linear-gradient(135deg, #f8fcff 0%, #e3f2fd 100%);
        }

        .section-block.meeting-info::before {
            background: linear-gradient(90deg, #3498db 0%, #2196f3 100%);
        }

        /* 內容章節區塊 */
        .section-block.content-section {
            border-left-color: #2ecc71;
            background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
        }

        .section-block.content-section::before {
            background: linear-gradient(90deg, #2ecc71 0%, #4caf50 100%);
        }

        /* 技術背景區塊 */
        .section-block.tech-background {
            border-left-color: #9c27b0;
            background: linear-gradient(135deg, #faf8ff 0%, #f3e5f5 100%);
        }

        .section-block.tech-background::before {
            background: linear-gradient(90deg, #9c27b0 0%, #673ab7 100%);
        }

        /* 核心觀點區塊 */
        .section-block.core-insights {
            border-left-color: #ff9800;
            background: linear-gradient(135deg, #fffbf0 0%, #fff3e0 100%);
        }

        .section-block.core-insights::before {
            background: linear-gradient(90deg, #ff9800 0%, #f57c00 100%);
        }

        /* 實踐經驗區塊 */
        .section-block.practical-experience {
            border-left-color: #e91e63;
            background: linear-gradient(135deg, #fff8fa 0%, #fce4ec 100%);
        }

        .section-block.practical-experience::before {
            background: linear-gradient(90deg, #e91e63 0%, #c2185b 100%);
        }

        /* 區塊標題樣式 */
        .section-title {
            font-size: 1.6rem;
            margin-top: 0;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #4b6cb7;
            display: flex;
            align-items: center;
            color: #4b6cb7;
            font-weight: 700;
            position: relative;
        }

        .section-title::before {
            content: '📋';
            margin-right: 12px;
            font-size: 1.2em;
        }

        .section-block.meeting-info .section-title {
            color: #3498db;
            border-bottom-color: #3498db;
        }

        .section-block.meeting-info .section-title::before {
            content: '📊';
        }

        .section-block.content-section .section-title {
            color: #2ecc71;
            border-bottom-color: #2ecc71;
        }

        .section-block.content-section .section-title::before {
            content: '📝';
        }

        .section-block.tech-background .section-title {
            color: #9c27b0;
            border-bottom-color: #9c27b0;
        }

        .section-block.tech-background .section-title::before {
            content: '⚙️';
        }

        .section-block.core-insights .section-title {
            color: #ff9800;
            border-bottom-color: #ff9800;
        }

        .section-block.core-insights .section-title::before {
            content: '💡';
        }

        .section-block.practical-experience .section-title {
            color: #e91e63;
            border-bottom-color: #e91e63;
        }

        .section-block.practical-experience .section-title::before {
            content: '🛠️';
        }

        /* 章節內容樣式 */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            font-weight: 700;
            line-height: 1.3;
            margin-top: 0;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 2.2rem;
            text-align: center;
            margin-bottom: 30px;
        }

        h2 {
            font-size: 1.8rem;
            color: #4b6cb7;
            padding: 15px 20px;
            background: linear-gradient(135deg, #f8faff 0%, #e8f0fe 100%);
            border-radius: 8px;
            border-left: 4px solid #4b6cb7;
            margin: 25px 0 20px 0;
            position: relative;
        }

        h2::before {
            content: '🎯';
            margin-right: 10px;
            font-size: 0.9em;
        }

        h3 {
            font-size: 1.4rem;
            color: #2c3e50;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 8px;
            margin: 20px 0 15px 0;
        }

        h4 {
            font-size: 1.2rem;
            color: #495057;
            margin: 15px 0 10px 0;
        }

        p {
            margin-bottom: 18px;
            line-height: 1.8;
            color: #333;
            text-align: justify;
        }

        /* 特殊段落樣式 */
        .highlight-box {
            background: linear-gradient(135deg, #fff9e6 0%, #fff3d4 100%);
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(255, 193, 7, 0.1);
        }

        .info-box {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left: 4px solid #2196f3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
        }

        .success-box {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            border-left: 4px solid #4caf50;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
        }

        .video-link {
            display: inline-block;
            margin: 10px 0;
            padding: 8px 15px;
            background-color: rgba(255, 255, 255, 0.2);
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .video-link:hover {
            background-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .video-link i {
            margin-right: 5px;
        }

        ul {
            padding-left: 20px;
        }

        li {
            margin-bottom: 10px;
            position: relative;
            list-style-type: none;
            padding-left: 25px;
        }

        li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: #4b6cb7;
            font-size: 1.2rem;
            font-weight: bold;
        }

        .section-block.meeting-info li::before { color: #3498db; }
        .section-block.content-section li::before { color: #2ecc71; }

        strong {
            color: #2c3e50;
            font-weight: bold;
        }

        code {
            background: #f4f4f4;
            color: #e74c3c;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9em;
        }

        pre {
            background: #f8f9fa;
            color: #2c3e50;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5em 0;
            border-left: 4px solid #4b6cb7;
        }

        blockquote {
            border-left: 4px solid #4b6cb7;
            background: #f8f9fa;
            padding: 15px 20px;
            margin: 1.5em 0;
            border-radius: 0 6px 6px 0;
            color: #2c3e50;
            font-style: italic;
        }

        .video-link:hover {
            background: #2563eb;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
        }

        code {
            background: #f1f5f9;
            color: #dc2626;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9em;
            border: 1px solid #e2e8f0;
        }

        pre {
            background: #0f172a;
            color: #e2e8f0;
            padding: 24px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 2em 0;
            border: 1px solid #1e293b;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        ul, ol {
            margin: 1.5em 0;
            padding-left: 1.5em;
        }

        li {
            margin: 0.5em 0;
            color: #475569;
            line-height: 1.7;
        }

        blockquote {
            border-left: 4px solid #3b82f6;
            background: #f8fafc;
            padding: 16px 24px;
            margin: 2em 0;
            border-radius: 0 8px 8px 0;
            color: #475569;
            font-style: italic;
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        /* 其他圖標尺寸優化 */
        .meeting-icon {
            width: auto;
            height: 24px;
            max-width: 120px;
            object-fit: contain;
            opacity: 0.8;
        }

        @media (max-width: 768px) {
            body {
                padding: 16px;
                font-size: 16px;
            }
            .container { border-radius: 12px; }
            header { padding: 48px 24px; }
            header h1 { font-size: 2.25rem; }
            .content { padding: 40px 24px; }
            .meeting-item { padding: 24px; }
            h2 { font-size: 1.75rem; }
            h3 { font-size: 1.375rem; }
        }
        """,
        "technical": """
        /* Technical Documentation Style - Dark Theme Inspired by sample.html */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'JetBrains Mono', 'Roboto', 'Microsoft JhengHei', monospace;
            background-color: #1a1a1a;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }

        .container {
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
        }

        header {
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: #ecf0f1;
            position: relative;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border-radius: 10px 10px 0 0;
        }

        header h1 {
            font-size: 2rem;
            margin: 0 0 10px 0;
            letter-spacing: 0.5px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        header p {
            font-size: 1rem;
            margin: 0;
            opacity: 0.9;
        }

        .content {
            background-color: #2c2c2c;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            padding: 30px;
            margin-bottom: 30px;
        }

        /* 技術文檔區塊樣式 */
        .section-block {
            background-color: #2c3e50;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #e67e22;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .section-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #e67e22 0%, #3498db 50%, #27ae60 100%);
            opacity: 0.8;
        }

        .section-block:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        }

        /* 會議資訊區塊 */
        .section-block.meeting-info {
            border-left-color: #3498db;
            background: linear-gradient(135deg, #1e3a5f 0%, #2c3e50 100%);
        }

        .section-block.meeting-info::before {
            background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        }

        /* 內容章節區塊 */
        .section-block.content-section {
            border-left-color: #27ae60;
            background: linear-gradient(135deg, #1e4d2b 0%, #2c3e50 100%);
        }

        .section-block.content-section::before {
            background: linear-gradient(90deg, #27ae60 0%, #229954 100%);
        }

        /* 技術背景區塊 */
        .section-block.tech-background {
            border-left-color: #8e44ad;
            background: linear-gradient(135deg, #3d2a4d 0%, #2c3e50 100%);
        }

        .section-block.tech-background::before {
            background: linear-gradient(90deg, #8e44ad 0%, #7d3c98 100%);
        }

        /* 核心觀點區塊 */
        .section-block.core-insights {
            border-left-color: #f39c12;
            background: linear-gradient(135deg, #5d4e37 0%, #2c3e50 100%);
        }

        .section-block.core-insights::before {
            background: linear-gradient(90deg, #f39c12 0%, #e67e22 100%);
        }

        /* 實踐經驗區塊 */
        .section-block.practical-experience {
            border-left-color: #e74c3c;
            background: linear-gradient(135deg, #5d2c2c 0%, #2c3e50 100%);
        }

        .section-block.practical-experience::before {
            background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        }

        /* 區塊標題樣式 */
        .section-title {
            font-size: 1.5rem;
            margin-top: 0;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #e67e22;
            display: flex;
            align-items: center;
            color: #e67e22;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 700;
        }

        .section-title::before {
            content: '⚡';
            margin-right: 12px;
            font-size: 1.2em;
        }

        .section-block.meeting-info .section-title {
            color: #3498db;
            border-bottom-color: #3498db;
        }

        .section-block.meeting-info .section-title::before {
            content: '📊';
        }

        .section-block.content-section .section-title {
            color: #27ae60;
            border-bottom-color: #27ae60;
        }

        .section-block.content-section .section-title::before {
            content: '💻';
        }

        .section-block.tech-background .section-title {
            color: #8e44ad;
            border-bottom-color: #8e44ad;
        }

        .section-block.tech-background .section-title::before {
            content: '🔧';
        }

        .section-block.core-insights .section-title {
            color: #f39c12;
            border-bottom-color: #f39c12;
        }

        .section-block.core-insights .section-title::before {
            content: '🧠';
        }

        .section-block.practical-experience .section-title {
            color: #e74c3c;
            border-bottom-color: #e74c3c;
        }

        .section-block.practical-experience .section-title::before {
            content: '⚙️';
        }

        /* 技術文檔章節內容樣式 */
        h1, h2, h3, h4, h5, h6 {
            color: #ecf0f1;
            font-weight: 700;
            line-height: 1.3;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin-top: 0;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 2rem;
            text-align: center;
            margin-bottom: 30px;
            color: #3498db;
        }

        h2 {
            font-size: 1.6rem;
            color: #e67e22;
            padding: 15px 20px;
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            border-radius: 8px;
            border-left: 4px solid #e67e22;
            margin: 25px 0 20px 0;
            position: relative;
        }

        h2::before {
            content: '🔍';
            margin-right: 10px;
            font-size: 0.9em;
        }

        h3 {
            font-size: 1.3rem;
            color: #ecf0f1;
            border-bottom: 2px solid #34495e;
            padding-bottom: 8px;
            margin: 20px 0 15px 0;
        }

        h4 {
            font-size: 1.1rem;
            color: #bdc3c7;
            margin: 15px 0 10px 0;
        }

        p {
            margin-bottom: 18px;
            line-height: 1.8;
            color: #bdc3c7;
            text-align: justify;
        }

        /* 技術文檔特殊樣式 */
        .code-block {
            background: linear-gradient(135deg, #1a252f 0%, #2c3e50 100%);
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
            font-family: 'JetBrains Mono', monospace;
        }

        .warning-box {
            background: linear-gradient(135deg, #5d4037 0%, #3e2723 100%);
            border-left: 4px solid #ff9800;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(255, 152, 0, 0.2);
        }

        .success-box {
            background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
            border-left: 4px solid #4caf50;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
        }

        .video-link {
            display: inline-block;
            margin: 10px 0;
            padding: 8px 15px;
            background-color: rgba(255, 255, 255, 0.1);
            color: #ecf0f1;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .video-link:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .video-link i {
            margin-right: 5px;
        }

        ul {
            padding-left: 20px;
        }

        li {
            margin-bottom: 10px;
            position: relative;
            list-style-type: none;
            padding-left: 25px;
        }

        li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: #e67e22;
            font-size: 1.2rem;
            font-weight: bold;
        }

        .section-block.meeting-info li::before { color: #3498db; }
        .section-block.content-section li::before { color: #27ae60; }

        strong {
            color: #ecf0f1;
            font-weight: bold;
        }

        code {
            background: #34495e;
            color: #e74c3c;
            padding: 3px 6px;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9em;
        }

        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5em 0;
            border-left: 4px solid #e67e22;
        }

        blockquote {
            border-left: 4px solid #e67e22;
            background: #34495e;
            padding: 15px 20px;
            margin: 1.5em 0;
            border-radius: 0 6px 6px 0;
            color: #bdc3c7;
            font-style: italic;
        }

        .video-link:hover {
            background: linear-gradient(135deg, #2ea043 0%, #238636 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
        }

        code {
            background: #262c36;
            color: #f85149;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: inherit;
            font-size: 0.9em;
            border: 1px solid #30363d;
        }

        pre {
            background: #0d1117;
            color: #e6edf3;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 2em 0;
            border: 1px solid #21262d;
            font-size: 13px;
            line-height: 1.5;
        }

        pre code {
            background: none;
            border: none;
            padding: 0;
            color: inherit;
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        /* 其他圖標尺寸優化 */
        .meeting-icon {
            width: auto;
            height: 20px;
            max-width: 100px;
            object-fit: contain;
            opacity: 0.7;
            filter: brightness(1.2);
        }

        @media (max-width: 768px) {
            body {
                padding: 16px;
                font-size: 14px;
            }
            .container { border-radius: 8px; }
            header { padding: 32px 24px; }
            header h1 { font-size: 1.75rem; }
            .content { padding: 32px 24px; }
            .meeting-item { padding: 20px; }
            h2 { font-size: 1.75rem; }
            h3 { font-size: 1.25rem; }
        }
        """,
        "concise": """
        /* Concise Summary Style - Clean Minimalist Inspired by sample.html */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', 'Microsoft JhengHei', sans-serif;
            background-color: #fafafa;
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }

        .container {
            max-width: 800px;
            margin: 30px auto;
            padding: 0 20px;
        }

        header {
            text-align: center;
            padding: 25px 20px;
            background: linear-gradient(135deg, #95a5a6, #7f8c8d);
            color: #fff;
            position: relative;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-radius: 10px 10px 0 0;
        }

        header h1 {
            font-size: 1.8rem;
            margin: 0 0 8px 0;
            letter-spacing: 0.3px;
        }

        header p {
            font-size: 1rem;
            margin: 0;
            opacity: 0.9;
        }

        .content {
            background-color: #fff;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 25px;
            margin-bottom: 30px;
        }

        /* 簡潔摘要區塊樣式 */
        .section-block {
            background-color: #fff;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #95a5a6;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .section-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #95a5a6 0%, #3498db 50%, #2ecc71 100%);
            opacity: 0.7;
        }

        .section-block:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        }

        /* 會議資訊區塊 */
        .section-block.meeting-info {
            border-left-color: #3498db;
            background: linear-gradient(135deg, #f8fcff 0%, #e3f2fd 100%);
        }

        .section-block.meeting-info::before {
            background: linear-gradient(90deg, #3498db 0%, #2196f3 100%);
        }

        /* 內容章節區塊 */
        .section-block.content-section {
            border-left-color: #2ecc71;
            background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
        }

        .section-block.content-section::before {
            background: linear-gradient(90deg, #2ecc71 0%, #4caf50 100%);
        }

        /* 技術背景區塊 */
        .section-block.tech-background {
            border-left-color: #9c27b0;
            background: linear-gradient(135deg, #faf8ff 0%, #f3e5f5 100%);
        }

        .section-block.tech-background::before {
            background: linear-gradient(90deg, #9c27b0 0%, #673ab7 100%);
        }

        /* 核心觀點區塊 */
        .section-block.core-insights {
            border-left-color: #ff9800;
            background: linear-gradient(135deg, #fffbf0 0%, #fff3e0 100%);
        }

        .section-block.core-insights::before {
            background: linear-gradient(90deg, #ff9800 0%, #f57c00 100%);
        }

        /* 實踐經驗區塊 */
        .section-block.practical-experience {
            border-left-color: #e91e63;
            background: linear-gradient(135deg, #fff8fa 0%, #fce4ec 100%);
        }

        .section-block.practical-experience::before {
            background: linear-gradient(90deg, #e91e63 0%, #c2185b 100%);
        }

        /* 區塊標題樣式 */
        .section-title {
            font-size: 1.4rem;
            margin-top: 0;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #95a5a6;
            display: flex;
            align-items: center;
            color: #95a5a6;
            font-weight: 600;
        }

        .section-title::before {
            content: '📄';
            margin-right: 10px;
            font-size: 1.1em;
        }

        .section-block.meeting-info .section-title {
            color: #3498db;
            border-bottom-color: #3498db;
        }

        .section-block.meeting-info .section-title::before {
            content: '📋';
        }

        .section-block.content-section .section-title {
            color: #2ecc71;
            border-bottom-color: #2ecc71;
        }

        .section-block.content-section .section-title::before {
            content: '📝';
        }

        .section-block.tech-background .section-title {
            color: #9c27b0;
            border-bottom-color: #9c27b0;
        }

        .section-block.tech-background .section-title::before {
            content: '🔧';
        }

        .section-block.core-insights .section-title {
            color: #ff9800;
            border-bottom-color: #ff9800;
        }

        .section-block.core-insights .section-title::before {
            content: '💡';
        }

        .section-block.practical-experience .section-title {
            color: #e91e63;
            border-bottom-color: #e91e63;
        }

        .section-block.practical-experience .section-title::before {
            content: '🛠️';
        }

        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            font-weight: 600;
            line-height: 1.4;
        }

        h1 { font-size: 1.8rem; }
        h2 { font-size: 1.5rem; }
        h3 { font-size: 1.2rem; }

        p {
            margin-bottom: 12px;
            line-height: 1.6;
            color: #333;
            font-size: 1rem;
        }

        .video-link {
            display: inline-block;
            margin: 8px 0;
            padding: 6px 12px;
            background-color: rgba(255, 255, 255, 0.2);
            color: #fff;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .video-link:hover {
            background-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        .video-link i {
            margin-right: 4px;
        }

        ul {
            padding-left: 18px;
        }

        li {
            margin-bottom: 8px;
            position: relative;
            list-style-type: none;
            padding-left: 20px;
        }

        li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: #95a5a6;
            font-size: 1.1rem;
            font-weight: bold;
        }

        .section-block.meeting-info li::before { color: #3498db; }
        .section-block.content-section li::before { color: #2ecc71; }

        strong {
            color: #2c3e50;
            font-weight: bold;
        }

        code {
            background: #ecf0f1;
            color: #e74c3c;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85em;
        }

        pre {
            background: #f8f9fa;
            color: #2c3e50;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1.2em 0;
            border-left: 3px solid #95a5a6;
        }

        blockquote {
            border-left: 3px solid #95a5a6;
            background: #f8f9fa;
            padding: 12px 16px;
            margin: 1.2em 0;
            border-radius: 0 4px 4px 0;
            color: #2c3e50;
            font-style: italic;
        }

        .video-link:hover {
            background: #2563eb;
            transform: translateY(-1px);
        }

        code {
            background: #f3f4f6;
            color: #dc2626;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.875em;
        }

        pre {
            background: #f8fafc;
            color: #1f2937;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1.5em 0;
            border: 1px solid #e5e7eb;
            font-size: 14px;
        }

        ul, ol {
            padding-left: 1.5em;
            margin: 1em 0;
        }

        li {
            margin: 0.5em 0;
            color: #374151;
        }

        blockquote {
            border-left: 4px solid #3b82f6;
            padding-left: 16px;
            margin: 1.5em 0;
            color: #4b5563;
            font-style: italic;
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        /* 其他圖標尺寸優化 */
        .meeting-icon {
            width: auto;
            height: 20px;
            max-width: 100px;
            object-fit: contain;
            opacity: 0.8;
        }

        @media (max-width: 768px) {
            body {
                padding: 16px;
                font-size: 16px;
            }
            .container { border-radius: 6px; }
            header { padding: 36px 24px 24px; }
            header h1 { font-size: 1.875rem; }
            .content { padding: 36px 24px; }
            .meeting-item { padding: 20px; }
            h2 { font-size: 1.75rem; }
            h3 { font-size: 1.25rem; }
        }
        """,
        "presentation": """
        /* Presentation Style - Vibrant Visual Design Inspired by sample.html */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', 'Microsoft JhengHei', sans-serif;
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 950px;
            margin: 30px auto;
            padding: 0 20px;
        }

        header {
            text-align: center;
            padding: 35px 20px;
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: #fff;
            position: relative;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            border-radius: 10px 10px 0 0;
        }

        header h1 {
            font-size: 2.4rem;
            margin: 0 0 12px 0;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        header p {
            font-size: 1.1rem;
            margin: 0;
            opacity: 0.95;
        }

        .content {
            background-color: #fff;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            padding: 35px;
            margin-bottom: 30px;
        }

        .section-block {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 6px solid #e74c3c;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .section-block:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }

        .section-block.meeting-info {
            border-left-color: #f39c12;
            background: linear-gradient(135deg, #fff9e6 0%, #fff3d4 100%);
        }

        .section-block.content-section {
            border-left-color: #27ae60;
            background: linear-gradient(135deg, #f0fff4 0%, #e6ffed 100%);
        }

        .section-title {
            font-size: 1.6rem;
            margin-top: 0;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 3px solid #e74c3c;
            display: inline-block;
            color: #e74c3c;
            font-weight: 700;
        }

        .section-block.meeting-info .section-title {
            color: #f39c12;
            border-bottom-color: #f39c12;
        }

        .section-block.content-section .section-title {
            color: #27ae60;
            border-bottom-color: #27ae60;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            font-weight: 700;
            line-height: 1.3;
        }

        h1 { font-size: 2.4rem; text-align: center; }
        h2 { font-size: 1.9rem; }
        h3 { font-size: 1.5rem; }

        p {
            margin-bottom: 18px;
            line-height: 1.7;
            color: #34495e;
            font-size: 1.1rem;
            text-align: justify;
        }

        ul {
            padding-left: 22px;
        }

        li {
            margin-bottom: 12px;
            position: relative;
            list-style-type: none;
            padding-left: 28px;
        }

        li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: #e74c3c;
            font-size: 1.3rem;
            font-weight: bold;
        }

        .section-block.meeting-info li::before { color: #f39c12; }
        .section-block.content-section li::before { color: #27ae60; }

        strong {
            color: #2c3e50;
            font-weight: bold;
        }

        code {
            background: #f8f9fa;
            color: #e74c3c;
            padding: 3px 7px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9em;
            border: 1px solid #e9ecef;
        }

        pre {
            background: #f8f9fa;
            color: #2c3e50;
            padding: 25px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 2em 0;
            border-left: 6px solid #e74c3c;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        blockquote {
            border-left: 6px solid #e74c3c;
            background: linear-gradient(135deg, #fff5f5 0%, #fef2f2 100%);
            padding: 20px 25px;
            margin: 2em 0;
            border-radius: 0 8px 8px 0;
            color: #2c3e50;
            font-style: italic;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .video-link {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            margin: 24px 0;
            padding: 16px 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.125rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
        }

        .video-link::before {
            content: '▶️';
            margin-right: 4px;
            font-size: 0.9em;
        }

        .video-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.6);
        }

        code {
            background: linear-gradient(135deg, #fef7cd 0%, #fbbf24 100%);
            color: #92400e;
            padding: 4px 8px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9em;
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        pre {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: #e5e7eb;
            padding: 24px;
            border-radius: 16px;
            overflow-x: auto;
            margin: 2em 0;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border: 1px solid #374151;
        }

        ul, ol {
            padding-left: 2em;
            margin: 1.5em 0;
        }

        li {
            margin: 0.75em 0;
            color: #4a5568;
            position: relative;
        }

        ul li::before {
            content: '✨';
            position: absolute;
            left: -1.5em;
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 15px;
        }

        /* 其他圖標尺寸優化 */
        .meeting-icon {
            width: auto;
            height: 28px;
            max-width: 140px;
            object-fit: contain;
            opacity: 0.7;
        }

        @media (max-width: 768px) {
            body {
                padding: 16px;
                font-size: 16px;
            }
            .container {
                border-radius: 16px;
                margin: 16px 0;
            }
            header {
                padding: 48px 24px;
            }
            header h1 {
                font-size: 2.5rem;
            }
            .content {
                padding: 40px 24px;
            }
            .meeting-item {
                padding: 28px;
                border-radius: 12px;
            }
            h2 {
                font-size: 1.875rem;
                padding: 20px 24px;
            }
            h3 { font-size: 1.5rem; }
        }
        """
    }

    return css_styles.get(template_style, css_styles["professional"])

# Preload template content at module level
try:
    with open(EMAIL_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        EMAIL_TEMPLATE_CONTENT = f.read()
    logger.info(f"Email template loaded successfully from {EMAIL_TEMPLATE_PATH}")
except FileNotFoundError:
    logger.error(f"Template file not found: {EMAIL_TEMPLATE_PATH}")
    EMAIL_TEMPLATE_CONTENT = "Error: Email template not found."
except Exception as e:
    logger.error(f"Error reading template file {EMAIL_TEMPLATE_PATH}: {e}")
    EMAIL_TEMPLATE_CONTENT = "Error: Could not read email template."


def wrap_sections_to_columns(html):
    """Wraps H2 sections into four columns (first 3 separate, rest in 4th)."""
    parts = re.split(r'(<h2>.*?</h2>)', html)
    sections = []
    current = ""
    for part in parts:
        if part.startswith("<h2>"):
            if current:
                sections.append(current)
            current = part
        else:
            current += part
    if current:
        sections.append(current)

    columns = ["", "", "", ""]
    for i, section in enumerate(sections):
        if i < 3:
            columns[i] = f'<div class="section-card">{section}</div>'
        else:
            columns[3] += f'<div class="section-card">{section}</div>'

    html_grid = ""
    for col in columns:
        html_grid += f'<div class="column">{col}</div>'
    return html_grid

def wrap_sections_to_meeting_items(html):
    """Wraps each H2 section into a 'meeting-item' div."""
    parts = re.split(r'(<h2>.*?</h2>)', html)
    sections = []
    current = ""
    for part in parts:
        if part.startswith("<h2>"):
            if current:
                sections.append(current)
            current = part
        else:
            current += part
    if current:
        sections.append(current)

    html_meetings = ""
    for section in sections:
        html_meetings += f'<div class="meeting-item">{section}</div>'
    return html_meetings

def markdown_to_email_html(md_content, index=0, template_style="professional"):
    """Converts Markdown content to a styled HTML email format using a template.

    Args:
        md_content: Markdown content to convert
        index: Index parameter for processing
        template_style: Template style for CSS ("professional", "technical", "concise", "presentation")
    """
    # Check if template loading failed during module import
    if "Error:" in EMAIL_TEMPLATE_CONTENT:
        logger.error("Cannot generate HTML because the email template failed to load.")
        return EMAIL_TEMPLATE_CONTENT

    html_content = markdown.markdown(md_content)
    title_match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = "Conference Meeting Summary"
    if title_match:
        title = title_match.group(1)

    lines = md_content.strip().splitlines()
    content_after_index = "\n".join(lines[index:]) if len(lines) > index else ""
    if index == 3:
        content_after_index = "## " + content_after_index

    html_body_content = markdown.markdown(content_after_index)
    html_body_content = wrap_sections_to_meeting_items(html_body_content)

    html_body_content = re.sub(
        r'<h3>Key Takeaways</h3>',
        r'<h3>Key Takeaways</h3><div class="key-content">',
        html_body_content
    )
    html_body_content = re.sub(
        r'<hr />',
        r'</div></div><hr />',
        html_body_content
    )
    html_body_content = html_body_content.replace('<hr />', '')
    if not html_body_content.endswith('</div>'):
        open_divs = html_body_content.count('<div')
        close_divs = html_body_content.count('</div>')
        if open_divs > close_divs:
            html_body_content += '</div>' * (open_divs - close_divs)

    category = lines[1].strip() if len(lines) > 1 else "Presentation Category"
    url_match = re.search(r'\[.*?\]\((https?://[^\)]+)\)', md_content)
    url = url_match.group(1) if url_match else ""

    # Template is already loaded into EMAIL_TEMPLATE_CONTENT
    # Remove the try-except block for reading the template here

    header_image_html = f'<img src="https://i.imgur.com/0LXUWvj.png" alt="{title} Icon">' if title else ''
    video_link_html = f'<a href="{url}" class="video-link" target="_blank"><i>▶</i> Meeting Video Link</a>' if url else ''
    footer_image_html = f'<img src="https://i.imgur.com/0LXUWvj.png" alt="{title} Icon">' if title else ''

    # Replace placeholders using the pre-loaded template content
    email_html = EMAIL_TEMPLATE_CONTENT.replace('{{title}}', title)
    email_html = email_html.replace('{{category}}', category)
    email_html = email_html.replace('{{header_image}}', header_image_html)
    email_html = email_html.replace('{{video_link}}', video_link_html)
    email_html = email_html.replace('{{html_body_content}}', html_body_content)
    email_html = email_html.replace('{{footer_image}}', footer_image_html)

    # 根據樣板風格替換 CSS 樣式
    custom_css = get_template_css(template_style)
    # 查找並替換現有的 CSS 樣式部分
    css_pattern = r'<style>.*?</style>'
    if re.search(css_pattern, email_html, re.DOTALL):
        email_html = re.sub(css_pattern, f'<style>{custom_css}</style>', email_html, flags=re.DOTALL)
    else:
        # 如果沒有找到 style 標籤，在 head 中添加
        head_pattern = r'</head>'
        if re.search(head_pattern, email_html):
            email_html = re.sub(head_pattern, f'<style>{custom_css}</style></head>', email_html)

    return email_html

def batch_md_to_html(md_dir_str, html_dir_str, index_param=0, template_style="professional"):
    """Converts all Markdown files in a directory to HTML files.

    Args:
        md_dir_str: Path to markdown directory
        html_dir_str: Path to output HTML directory
        index_param: Index parameter for processing
        template_style: Template style ("professional", "technical", "concise", "presentation")
    """
    md_dir = Path(md_dir_str)
    html_dir = Path(html_dir_str)

    if not md_dir.is_dir():
        logger.error(f"Markdown input directory not found or is not a directory: {md_dir}")
        return

    html_dir.mkdir(parents=True, exist_ok=True)

    # Template directory check is less critical now as loading happens at import
    # if not TEMPLATE_DIR.is_dir():
    #     logger.warning(f"Template directory not found: {TEMPLATE_DIR}")

    # Check if template loading failed earlier
    if "Error:" in EMAIL_TEMPLATE_CONTENT:
        logger.error("Aborting batch conversion because the email template failed to load.")
        return

    for md_file in md_dir.glob('*.md'):
        logger.info(f"Processing Markdown file: {md_file.name}")
        md_content = FileUtils.read_file(md_file)
        if md_content is None:
            logger.warning(f"Could not read file {md_file.name}, skipping.")
            continue

        html_content = markdown_to_email_html(md_content, index=index_param, template_style=template_style)

        # Check if markdown_to_email_html returned an error string
        if isinstance(html_content, str) and "Error:" in html_content:
            logger.error(f"Skipping {md_file.name} due to template loading error.")
            continue # Skip this file if template had issues

        html_filename = md_file.stem + '.html'
        html_path = html_dir / html_filename

        if FileUtils.write_file(html_content, html_path):
            logger.info(f"Converted: {md_file.name} -> {html_path.name}")
        else:
            logger.error(f"Failed to write HTML file for: {md_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch convert Markdown files to HTML.")
    parser.add_argument("-i", "--input", default="../output/md", help="Input directory containing Markdown files.")
    parser.add_argument("-o", "--output", default="../output/html", help="Output directory for HTML files.")
    parser.add_argument("--index", type=int, default=0, help="Index parameter for markdown_to_email_html function (default: 0).")

    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output

    batch_md_to_html(input_dir, output_dir, index_param=args.index)