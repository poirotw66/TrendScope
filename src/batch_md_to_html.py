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
        body {
            font-family: 'Roboto', 'Microsoft JhengHei', sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
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
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        """,
        "technical": """
        /* Technical Documentation Style */
        body {
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: #1e1e1e;
            color: #d4d4d4;
            margin: 0;
            padding: 0;
            line-height: 1.5;
        }
        header {
            text-align: left;
            padding: 20px;
            background: #252526;
            color: #cccccc;
            border-bottom: 2px solid #007acc;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        header h1 {
            font-size: 1.8rem;
            margin: 0;
            color: #569cd6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: #252526;
            border: 1px solid #3c3c3c;
            min-height: 100vh;
        }
        .content {
            padding: 20px;
        }
        h1, h2, h3 {
            color: #569cd6;
            border-left: 3px solid #007acc;
            padding-left: 10px;
        }
        h2 { color: #4ec9b0; }
        h3 { color: #dcdcaa; }
        p { margin: 10px 0; }
        code {
            background-color: #3c3c3c;
            padding: 2px 4px;
            border-radius: 3px;
            color: #ce9178;
        }
        pre {
            background-color: #1e1e1e;
            border: 1px solid #3c3c3c;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .meeting-item {
            background-color: #2d2d30;
            border: 1px solid #3c3c3c;
            margin: 15px 0;
            padding: 15px;
            border-radius: 5px;
        }
        .video-link {
            display: inline-block;
            margin: 10px 0;
            padding: 8px 15px;
            background-color: #007acc;
            color: #fff;
            text-decoration: none;
            border-radius: 3px;
            font-weight: 500;
        }
        .video-link:hover {
            background-color: #005a9e;
        }
        """,
        "concise": """
        body {
            font-family: 'Arial', sans-serif;
            background-color: #ffffff;
            color: #333;
            margin: 0;
            padding: 20px;
            line-height: 1.4;
        }
        header {
            text-align: center;
            padding: 15px;
            background: #f5f5f5;
            border-bottom: 3px solid #007acc;
            margin-bottom: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
        }
        h1 { font-size: 1.8em; margin-bottom: 10px; }
        h2 { font-size: 1.4em; margin: 15px 0 8px 0; }
        """,
        "presentation": """
        body {
            font-family: 'Segoe UI', 'Tahoma', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .container {
            max-width: 1000px;
            margin: 20px auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        h1 { font-size: 2.5em; color: #4a5568; }
        h2 { color: #667eea; border-left: 4px solid #667eea; padding-left: 15px; }
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