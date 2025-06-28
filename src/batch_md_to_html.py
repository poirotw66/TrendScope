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
        /* Professional Business Style - Modern Corporate Design */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #2d3748;
            margin: 0;
            padding: 24px;
            line-height: 1.7;
            font-size: 18px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 64px 48px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }

        header h1 {
            font-size: 2.75rem;
            font-weight: 700;
            margin: 0 0 20px 0;
            letter-spacing: -0.025em;
            position: relative;
            z-index: 1;
        }

        .content {
            padding: 56px 48px;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #1a202c;
            font-weight: 600;
            line-height: 1.3;
            margin-top: 2.4em;
            margin-bottom: 1.2em;
        }

        h1 { font-size: 2.75rem; }
        h2 {
            font-size: 2rem;
            color: #667eea;
            border-left: 4px solid #667eea;
            padding-left: 24px;
            margin-top: 3.2em;
        }
        h3 {
            font-size: 1.625rem;
            color: #4a5568;
        }

        p {
            margin: 1.6em 0;
            color: #4a5568;
            font-size: 1.125rem;
        }

        .meeting-item {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 32px;
            margin: 32px 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .meeting-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
        }

        .video-link {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 24px 0;
            padding: 14px 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .video-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }

        code {
            background: #edf2f7;
            color: #e53e3e;
            padding: 4px 8px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9em;
        }

        pre {
            background: #1a202c;
            color: #e2e8f0;
            padding: 24px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 2em 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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
        /* Technical Documentation Style - Modern Dark Theme */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
            background: #0d1117;
            color: #e6edf3;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
            font-size: 16px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            box-shadow: 0 16px 32px rgba(1, 4, 9, 0.85);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: #f9fafb;
            padding: 48px;
            border-bottom: 1px solid #30363d;
            position: relative;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #58a6ff 0%, #1f6feb 50%, #388bfd 100%);
        }

        header h1 {
            font-size: 2rem;
            font-weight: 600;
            margin: 0;
            color: #58a6ff;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .content {
            padding: 48px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 600;
            line-height: 1.3;
            margin-top: 2.8em;
            margin-bottom: 1.2em;
        }

        h1 {
            font-size: 2.75rem;
            color: #58a6ff;
        }
        h2 {
            font-size: 2rem;
            color: #7dd3fc;
            border-left: 4px solid #58a6ff;
            padding-left: 20px;
            background: rgba(88, 166, 255, 0.1);
            padding: 16px 20px;
            border-radius: 6px;
            margin: 2.4em 0 1.2em 0;
        }
        h3 {
            font-size: 1.5rem;
            color: #a5f3fc;
        }

        p {
            margin: 1.6em 0;
            color: #c9d1d9;
            line-height: 1.7;
            font-size: 1rem;
        }

        .meeting-item {
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 28px;
            margin: 28px 0;
            transition: all 0.2s ease;
            position: relative;
        }

        .meeting-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #58a6ff 0%, #1f6feb 100%);
            border-radius: 2px 0 0 2px;
        }

        .meeting-item:hover {
            background: #262c36;
            border-color: #58a6ff;
            transform: translateY(-1px);
        }

        .video-link {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 20px 0;
            padding: 12px 20px;
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            font-size: 15px;
            transition: all 0.2s ease;
            border: 1px solid #2ea043;
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
        /* Concise Summary Style - Modern Minimalist */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            background: #fafafa;
            color: #1f2937;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
            font-size: 18px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        header {
            background: #ffffff;
            color: #1f2937;
            padding: 48px 36px 36px;
            text-align: center;
            border-bottom: 1px solid #e5e7eb;
            position: relative;
        }

        header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: #3b82f6;
            border-radius: 2px;
        }

        header h1 {
            font-size: 2.25rem;
            font-weight: 700;
            margin: 0;
            color: #111827;
            letter-spacing: -0.025em;
        }

        .content {
            padding: 48px 36px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            line-height: 1.3;
            margin-top: 2.4em;
            margin-bottom: 1em;
            color: #111827;
        }

        h1 { font-size: 2.75rem; }
        h2 {
            font-size: 2rem;
            color: #3b82f6;
            margin-top: 2.8em;
            padding-bottom: 0.6em;
            border-bottom: 2px solid #e5e7eb;
        }
        h3 {
            font-size: 1.5rem;
            color: #4b5563;
        }

        p {
            margin: 1.4em 0;
            color: #374151;
            font-size: 1.125rem;
        }

        .meeting-item {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 24px;
            margin: 24px 0;
            transition: all 0.2s ease;
        }

        .meeting-item:hover {
            background: #f3f4f6;
            border-color: #d1d5db;
        }

        .video-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 20px 0;
            padding: 10px 20px;
            background: #3b82f6;
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            font-size: 15px;
            transition: all 0.2s ease;
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
        /* Presentation Style - Modern Visual Design */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: #1a202c;
            margin: 0;
            padding: 24px;
            line-height: 1.7;
            font-size: 18px;
            min-height: 100vh;
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
            z-index: -1;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        header {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
            color: white;
            padding: 72px 48px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        header h1 {
            font-size: 3.25rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.025em;
            position: relative;
            z-index: 1;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .content {
            padding: 56px 48px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-weight: 700;
            line-height: 1.2;
            margin-top: 2.8em;
            margin-bottom: 1.2em;
        }

        h1 {
            font-size: 2.75rem;
            color: #667eea;
            text-align: center;
            margin-bottom: 1.6em;
        }

        h2 {
            font-size: 2.25rem;
            color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 24px 36px;
            border-radius: 16px;
            border-left: 6px solid #667eea;
            margin: 2.4em 0 1.6em 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }

        h2::before {
            content: '🎯';
            position: absolute;
            right: 24px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2em;
            opacity: 0.6;
        }

        h3 {
            font-size: 1.75rem;
            color: #764ba2;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.6em;
        }

        p {
            margin: 1.6em 0;
            color: #4a5568;
            font-size: 1.125rem;
            text-align: justify;
        }

        .meeting-item {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 36px;
            margin: 36px 0;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .meeting-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }

        .meeting-item:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15);
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