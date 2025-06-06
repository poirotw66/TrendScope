import pandas as pd
import random
import markdown
import os
import re
import argparse
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.logging_utils import logger
from bs4 import BeautifulSoup
import sys
from src.utils.string_utils import normalize_string

CONFERENCE_CONFIG = {
    "google_next": {
        "title": "Google Cloud Next 2025",
        "date_info": "2025 年 4 月 9 日 ─ 4 月 11 日",
        "intro_text": "Next 是我們的全球性展覽，展現靈感、創新和教育。決策者、開發者以及任何熱衷於普及、可擴展、具社會責任感的雲端人士，都將齊聚一堂，分享挑戰、解決方案、突破性的構想（10 倍速的創意）和改變遊戲規則的技術。",
        "title_regex": r'\s*<h1[^>]*>\s*Google Cloud Next 2025\s*</h1>\s*',
        "date_regex": r'\s*<p[^>]*>\s*2025\s*年\s*4\s*月\s*9\s*日\s*[─—–-]\s*4\s*月\s*11\s*日\s*</p>\s*',
        "intro_regex_list": [
            r'\s*(Next\s*是我們的全球性展覽.*?改變遊戲規則的技術(?:。|\.))\s*'
        ],
        "category_links": {
            "Google Cloud Next 2025": "https://cloud.withgoogle.com/next/25",
            "Data_Analytics": "./topic/Data_Analytics.html",
            "Applied_AI": "./topic/Applied_AI.html",
            "AI": "./topic/AI.html",
            "Databases": "./topic/Databases.html",
            "Security": "./topic/Security.html",
            "Migration": "./topic/Migration.html",
            "Vertex_AI": "./topic/Vertex_AI.html",
            "Gemini": "./topic/Gemini.html",
            "Workspace": "./topic/Workspace.html",
            "App_Dev": "./topic/App_Dev.html",
            "Compute": "./topic/Compute.html",
            "Serverless": "./topic/Serverless.html",
        },
        "category_link_formatter": lambda cat: cat.replace(" ", "_"),
        "meeting_link_prefix": "./topic/session/",
        "topic_link_prefix": "./topic/",
    },
    "gtc": {
        "title": "開發人員人工智慧大會|NVIDIA GTC 2025",
        "date_info": "2025 年 3 月 17 日 ─ 3 月 21 日",
        "intro_text": """今年規模比以往更盛大、內容更精彩。數千名開發人員、創新領袖與企業領導者將齊聚一堂，體驗人工智慧和加速運算如何協助人類解決最複雜的挑戰。\nNVIDIA 執行長黃仁勳不容錯過的主題演講，還有超過 1000 場精彩演講、400 多場現場展示、技術實作訓練，以及無數的交流活動，都將讓您探索人工智慧及其優勢的實際案例。""",
        "title_regex": r'\s*<h1[^>]*>\s*開發人員人工智慧大會\|NVIDIA GTC 2025\s*</h1>\s*',
        "date_regex": r'\s*<p[^>]*>\s*2025\s*年\s*3\s*月\s*17\s*日\s*[─—–-]\s*3\s*月\s*21\s*日\s*</p>\s*',
        "intro_regex_list": [
            r'\s*(今年規模比以往更盛大.*?實際案例(?:。|\.))\s*'
        ],
        "category_links": {
            "開發人員人工智慧大會|NVIDIA GTC 2025": "https://www.nvidia.com/zh-tw/gtc/",
            "Quantum Computing": "./topic/Simulation  Modeling  Design - Quantum Computing.html",
            "Generative AI - Code  Software Generation": "./topic/Generative AI - Code  Software Generation.html",
            "Generative AI - Retrieval-Augmented Generation (RAG)": "./topic/Generative AI - Retrieval-Augmented Generation (RAG).html",
            "Simulation  Modeling  Design - Industrial Digitalization  Digital Twin": "./topic/Simulation  Modeling  Design - Industrial Digitalization  Digital Twin.html",
            "Simulation  Modeling  Design - Climate  Weather  Ocean Modeling": "./topic/Simulation  Modeling  Design - Climate  Weather  Ocean Modeling.html",
            "Data Center  Cloud - Data Storage": "./topic/Data Center  Cloud - Data Storage.html",
            "Conversational AI - Natural Language Processing (NLP)": "./topic/Conversational AI - Natural Language Processing (NLP).html",
            "Data Center  Cloud - Infrastructure": "./topic/Data Center  Cloud - Infrastructure.html",
            "Edge Computing - Autonomous Machines": "./topic/Edge Computing - Autonomous Machines.html",
            "Simulation  Modeling  Design - Supercomputing": "./topic/Simulation  Modeling  Design - Supercomputing.html",
            "Data Center  Cloud - Sustainable Computing": "./topic/Data Center  Cloud - Sustainable Computing.html",
            "Computer Vision  Video Analytics - Computation Imaging": "./topic/Computer Vision  Video Analytics - Computation Imaging.html",
        },
        "category_link_formatter": lambda cat: cat,
        "meeting_link_prefix": "./topic/session/",
        "topic_link_prefix": "./topic/",
    },
    "consensus": {
        "title": "Consensus HONG KONG 2025",
        "date_info": "2025 年 2 月 18 日 ─ 2 月 20 日",
        "intro_text": """
        自2015年以來，「共識峰會」(Consensus) 不僅僅是一個活動，更是各方人士的年度盛會。它是區塊鏈、數位資產和Web3領域中最具影響力的公司齊聚一堂，共同推動產業發展的平台。
        2025年，「共識峰會」將拓展至香港，連繫東西方，展開關鍵對話並促成交易，共同定義未來的發展方向。
        由屢獲殊榮的媒體機構CoinDesk主辦，「共識峰會」以獨立、客觀的新聞報導為基礎，推動變革性理念和坦誠的對話。
        """,
        "title_regex": r'\s*<h1[^>]*>\s*Consensus HONG KONG 2025\s*</h1>\s*',
        "date_regex": r'\s*<p[^>]*>\s*2025\s*年\s*2\s*月\s*18\s*日\s*[─—–-]\s*2\s*月\s*20s*日\s*</p>\s*',
        "intro_regex_list": [
            r'\s*(自2015年以來.*?坦誠的對話(?:。|\.))\s*'
        ],
        "category_links": {
            "Consensus HONG KONG 2025": "https://consensus-hongkong2025.coindesk.com/",
            "AI": "./topic/AI.html",
            "Blockchain": "./topic/Blockchain.html",
            "Community": "./topic/Community.html",
            "Crypto / Web3 Software": "./topic/Crypto  Web3 Software.html",
            "DeFi": "./topic/DeFi.html",
            "Gaming": "./topic/Gaming.html",
            "Policy": "./topic/Policy.html",
            "Smart Contracts": "./topic/Smart Contracts.html",
            "Web3 Software": "./topic/Web3 Software.html",
        },
        "category_link_formatter": lambda cat: cat,
        "meeting_link_prefix": "./topic/session/",
        "topic_link_prefix": "./topic/",
    }
}
TEMPLATE_DIR = Path(__file__).parent.parent / 'src' / 'templates'
try:
    if not TEMPLATE_DIR.is_dir():
        raise FileNotFoundError(f"Template directory not found: {TEMPLATE_DIR}")
    jinja_env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(['html', 'xml'])
    )
    homepage_template = jinja_env.get_template('homepage_template.html')
except Exception as e:
    logger.error(f"Error loading Jinja2 template: {e}")
    homepage_template = None

def load_meetings(file_path):
    """
    Loads meeting data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame or None: A DataFrame containing the meeting data,
                              or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded meetings from {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Error: Input file not found at {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {e}")
        return None

def select_random_meetings(df, categories):
    """
    Selects one random meeting for each specified category.

    Args:
        df (pd.DataFrame): DataFrame containing all meetings.
        categories (list): A list of category names (topics) to select meetings from.

    Returns:
        dict: A dictionary where keys are categories and values are
              dictionaries representing the selected meeting's data.
    """
    selected_meetings = {}
    for category in categories:
        filtered = df[df["Topic"] == category]
        if not filtered.empty:
            selected_meetings[category] = filtered.sample(n=1).iloc[0].to_dict()
    return selected_meetings

def generate_markdown(selected_meetings, config):
    """
    Generates Markdown content based on selected meetings and configuration.

    Args:
        selected_meetings (dict): A dictionary of selected meetings,
                                  keyed by category.
        config (dict): The conference-specific configuration.

    Returns:
        str: The generated Markdown content.
    """
    # 過濾掉 Key 為空的會議
    filtered_meetings = {}
    for category, meeting in selected_meetings.items():
        key_value = meeting.get('Key')
        # 檢查各種可能的空值情況
        if key_value and key_value != 'nan' and key_value != 'N/A' and str(key_value).strip() != '':
            # 額外檢查是否為 pandas 的 NaN 值
            try:
                if pd.isna(key_value):
                    continue
            except:
                pass
            filtered_meetings[category] = meeting
    
    # 如果過濾後沒有會議，則返回基本內容
    if not filtered_meetings:
        return f"# {config['title']}\n{config['date_info']}\n\n{config['intro_text']}\n\n"
    
    df = pd.DataFrame(filtered_meetings.values())
    md_content = f"# {config['title']}\n{config['date_info']}\n\n{config['intro_text']}\n\n"

    for _, row in df.iterrows():
        topic = row.get('Topic', 'N/A')
        meeting = row.get('Meeting', 'N/A')
        key = row.get('Key', 'N/A')
        md_content += f"# {topic}\n"
        md_content += f"## {meeting}\n"
        md_content += f"### {key}\n"
    return md_content

def markdown_to_email_html(md_content, config):
    """
    Converts Markdown to HTML for the homepage, processing it according to the config.
    Uses BeautifulSoup for initial cleaning and regex for subsequent structuring.

    Args:
        md_content (str): The Markdown content to convert.
        config (dict): The conference-specific configuration.

    Returns:
        str: The processed HTML content.
    """
    if not homepage_template:
        logger.error("Homepage template could not be loaded.")
        return "<html><body><h1>Error</h1><p>Homepage template could not be loaded.</p></body></html>"

    html_from_markdown = markdown.markdown(md_content)
    soup = BeautifulSoup(html_from_markdown, 'html.parser')

    h1_to_remove = soup.find('h1', string=re.compile(config['title'].replace("|", r"\|")))
    if h1_to_remove:
        h1_to_remove.decompose()

    date_p_to_remove = soup.find('p', string=re.compile(config['date_info'].split('─')[0].strip()))
    if date_p_to_remove:
        date_p_to_remove.decompose()

    for intro_pattern_str in config['intro_regex_list']:
        intro_p_to_remove = soup.find('p', string=re.compile(intro_pattern_str.strip().lstrip(r'\s*<p[^>]*>\s*').rstrip(r'\s*</p>\s*'), flags=re.DOTALL))
        if intro_p_to_remove:
            logger.info(f"Found intro paragraph to remove with pattern: {intro_pattern_str[:50]}...")
            intro_p_to_remove.decompose()
        else:
            logger.warning(f"Could not find intro paragraph to remove with pattern: {intro_pattern_str[:50]}...")

    html_content = str(soup)
    html_content = html_content.strip()

    category_links_html = ""
    category_links = config['category_links']
    link_formatter = config['category_link_formatter']
    topic_prefix = config['topic_link_prefix']
    for cat, link in category_links.items():
        if not link.startswith(('http://', 'https://')):
            safe_cat_link = link_formatter(cat)
            link_target = category_links.get(cat, f"{topic_prefix}{safe_cat_link}.html")
        else:
            link_target = link
        category_links_html += f'<a href="{link_target}" class="category-link">{cat}</a>\n'

    def normalize_filename(title):
        """Normalizes the filename by removing illegal characters."""
        return normalize_string(title)

    def add_category_link(match):
        category = match.group(1).strip()
        safe_cat_link = normalize_filename(link_formatter(category))
        link = category_links.get(category, f"{topic_prefix}{safe_cat_link}.html")
        return f'<div class="category-section"><h1><a href="{link}" class="category-title-link">{category}</a></h1>'
    html_content = re.sub(r'<h1>(.*?)</h1>', add_category_link, html_content)

    def add_meeting_link(match):
        meeting_title = match.group(1).strip()
        meeting_title_link = re.sub(r'[\\/:*?"<>|]', '', meeting_title).strip()
        session_prefix = config['meeting_link_prefix']
        link = f"{session_prefix}{meeting_title_link}.html"
        return f'<div class="meeting-item"><h2><a href="{link}" class="meeting-title-link">{meeting_title}</a></h2>'
    html_content = re.sub(r'<h2>(.*?)</h2>', add_meeting_link, html_content)

    html_content = re.sub(r'<h3>(.*?)</h3>', r'<h3>\1</h3><div class="key-content">', html_content)
    html_content = re.sub(r'(<ul>.*?</ul>)', r'\1</div><div class="key-content">', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<div class="key-content">\s*</div>', '', html_content)
    html_content = re.sub(r'</div>\s*<div class="key-content">', '', html_content)

    meeting_items_split = re.split(r'(<div class="meeting-item">)', html_content)
    processed_html_content = meeting_items_split[0]
    for i in range(1, len(meeting_items_split), 2):
        item_start_tag = meeting_items_split[i]
        item_content = meeting_items_split[i + 1] if (i + 1) < len(meeting_items_split) else ""
        next_item_match = re.search(r'<div class="(?:meeting-item|category-section)">', item_content)
        if next_item_match:
            current_item_content = item_content[:next_item_match.start()]
            remaining_content = item_content[next_item_match.start():]
        else:
            current_item_content = item_content
            remaining_content = ""
        key_content_count = current_item_content.count('<div class="key-content">')
        end_div_count = current_item_content.count('</div>')
        needed_end_divs = key_content_count + 1 - end_div_count
        processed_html_content += item_start_tag + current_item_content
        if needed_end_divs > 0:
            processed_html_content += '</div>' * needed_end_divs
        processed_html_content += remaining_content
    html_content = processed_html_content

    category_sections_split = re.split(r'(<div class="category-section">)', html_content)
    processed_html_content_cat = category_sections_split[0]
    for i in range(1, len(category_sections_split), 2):
        section_start_tag = category_sections_split[i]
        section_content = category_sections_split[i + 1] if (i + 1) < len(category_sections_split) else ""
        next_section_match = re.search(r'<div class="category-section">', section_content)
        if next_section_match:
            current_section_content = section_content[:next_section_match.start()]
            remaining_content_cat = section_content[next_section_match.start():]
        else:
            current_section_content = section_content
            remaining_content_cat = ""
        start_tags = current_section_content.count('<div')
        end_tags = current_section_content.count('</div>')
        needed_tags = start_tags + 1 - end_tags
        processed_html_content_cat += section_start_tag + current_section_content
        if needed_tags > 0:
            processed_html_content_cat += '</div>' * needed_tags
        processed_html_content_cat += remaining_content_cat
    html_content = processed_html_content_cat

    context = {
        'title': config['title'],
        'date_info': config['date_info'],
        'intro_text': config['intro_text'],
        'category_links_html': category_links_html,
        'html_content': html_content
    }
    email_html = homepage_template.render(context)
    return email_html

def ensure_directories(output_dir):
    """
    Ensures that the necessary output directories exist.

    Args:
        output_dir (str or Path): The base output directory.
    """
    output_path = Path(output_dir)
    (output_path / "topic" / "md").mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

def main():
    """
    Main function to generate the conference homepage.
    Parses command-line arguments, loads data, processes it, and saves the output.
    """
    parser = argparse.ArgumentParser(description="Generate conference homepage from CSV data.")
    parser.add_argument(
        "-c", "--conference",
        required=True,
        choices=CONFERENCE_CONFIG.keys(),
        help="Type of conference to process (e.g., google_next, gtc)."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input CSV file."
    )
    parser.add_argument(
        "-o", "--output",
        default="./report",
        help="Path to the output directory."
    )
    args = parser.parse_args()

    config = CONFERENCE_CONFIG.get(args.conference)
    if not config:
        logger.error(f"Error: Invalid conference type '{args.conference}'.")
        return

    logger.info(f"Processing conference: {args.conference}")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Output directory: {args.output}")

    df = load_meetings(args.input)
    if df is None:
        return

    categories = df["Topic"].dropna().unique().tolist()
    if not categories:
        logger.warning("No topics found in the input file.")
        return

    ensure_directories(args.output)
    logger.info(f"Ensured output directories exist at {args.output}")

    selected_meetings = select_random_meetings(df, categories)
    logger.info(f"Number of selected meetings: {len(selected_meetings)}")

    markdown_output = generate_markdown(selected_meetings, config)
    html_output = markdown_to_email_html(markdown_output, config)
    logger.info("Generated Markdown and HTML content.")

    output_path = Path(args.output)

    md_path = output_path / "topic" / "md" / "homepage.md"
    try:
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_output)
        logger.info(f"Homepage Markdown saved to: {md_path}")
    except Exception as e:
        logger.error(f"Error writing Markdown file {md_path}: {e}")

    html_path = output_path / "homepage.html"
    try:
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_output)
        logger.info(f"Homepage HTML saved to: {html_path}")
    except Exception as e:
        logger.error(f"Error writing HTML file {html_path}: {e}")

if __name__ == "__main__":
    main()