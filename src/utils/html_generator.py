import logging
from pathlib import Path
import markdown
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).parent.parent / 'templates'

class HtmlGenerator:
    """Responsible for generating HTML content from Markdown summaries using Jinja2 templates."""

    def __init__(self):
        """Initializes the Jinja2 environment."""
        try:
            if not TEMPLATE_DIR.is_dir():
                raise FileNotFoundError(f"Template directory not found: {TEMPLATE_DIR}")

            self.env = Environment(
                loader=FileSystemLoader(TEMPLATE_DIR),
                autoescape=select_autoescape(['html', 'xml'])
            )
            self.template = self.env.get_template('summary_template.html')
            logger.info(f"Jinja2 environment initialized. Template 'summary_template.html' loaded from {TEMPLATE_DIR}")
        except FileNotFoundError as e:
             logger.error(f"Error initializing Jinja2 environment: {e}")
             raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during Jinja2 initialization: {e}")
            raise

    def _parse_summary_sections(self, summary_markdown):
        """
        Parses the markdown summary into sections based on H2 headers.

        Args:
            summary_markdown (str): The full summary in Markdown format.

        Returns:
            dict: A dictionary where keys are section identifiers (e.g., 'core', 'detail', 'conclusion')
                  and values are the Markdown content of each section.
        """
        sections = {'header': '', 'core': '', 'detail': '', 'conclusion': ''}
        current_section = 'header'
        lines = summary_markdown.strip().split('\n')

        header_lines = []
        content_start_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('## '):
                content_start_index = i
                break
            header_lines.append(line)
        sections['header'] = "\n".join(header_lines).strip()


        for line in lines[content_start_index:]:
            line_strip = line.strip()
            if line_strip.startswith('## 1. 核心觀點'):
                current_section = 'core'
            elif line_strip.startswith('## 2. 詳細內容'):
                current_section = 'detail'
            elif line_strip.startswith('## 3. 重要結論'):
                current_section = 'conclusion'
            elif line_strip.startswith('## '):
                 logger.warning(f"Unexpected H2 section found: {line_strip}")
                 current_section = 'other'
                 if 'other' not in sections: sections['other'] = ''
            elif current_section and line_strip != "---":
                 if current_section in sections:
                    sections[current_section] += line + '\n'

        for key in sections:
            sections[key] = sections[key].strip()

        return sections

    def _convert_markdown_to_html(self, md_text):
        """Converts a markdown string to HTML."""
        if not md_text:
            return ""
        try:
            return markdown.markdown(md_text, extensions=['extra', 'nl2br'])
        except ImportError:
            logger.error("The 'markdown' library is required. Please install it (`pip install markdown`).")
            return f"<p>Error: Markdown library not installed.</p><pre>{md_text}</pre>"
        except Exception as e:
            logger.error(f"Error converting markdown to HTML: {e}")
            return f"<p>Error converting markdown.</p><pre>{md_text}</pre>"


    def _generate_html_content(self, summary_markdown, meeting_title=None, url=None):
        """
        Generates HTML content by rendering the Jinja2 template with parsed summary sections.

        Args:
            summary_markdown (str): Markdown formatted summary text.
            meeting_title (str, optional): Meeting title. Defaults to None.
            url (str, optional): Meeting video link (used as fallback if not found in header). Defaults to None.

        Returns:
            str: Generated HTML content. Returns an error string if template loading failed.
        """
        if not hasattr(self, 'template'):
             logger.error("HTML template was not loaded successfully during initialization.")
             return "<html><body><h1>Error</h1><p>HTML template could not be loaded.</p></body></html>"

        try:
            sections_md = self._parse_summary_sections(summary_markdown)

            header_lines = sections_md.get('header', '').split('\n')
            en_title = meeting_title or "Meeting Summary"
            zh_title = ""
            extracted_url = None

            url_pattern = re.compile(r'\[.*?\]\((.*?)\)')

            processed_lines_for_titles = []
            for line in header_lines:
                match = url_pattern.search(line)
                if match:
                    extracted_url = match.group(1)
                else:
                    processed_lines_for_titles.append(line.strip())

            if processed_lines_for_titles:
                 en_title = processed_lines_for_titles[0].lstrip('# ').strip()
                 if len(processed_lines_for_titles) > 1:
                     zh_title = processed_lines_for_titles[1].strip()
                 elif len(processed_lines_for_titles) == 1 and en_title != zh_title:
                    pass

            final_url = extracted_url if extracted_url is not None else url

            context = {
                'en_title': en_title,
                'zh_title': zh_title,
                'video_url': final_url,
                'core_html': self._convert_markdown_to_html(sections_md.get('core', '')),
                'detail_html': self._convert_markdown_to_html(sections_md.get('detail', '')),
                'conclusion_html': self._convert_markdown_to_html(sections_md.get('conclusion', '')),
            }

            html_content = self.template.render(context)
            return html_content

        except ImportError:
             logger.error("Markdown library is required. Please install it (`pip install markdown`).")
             return "<html><body><h1>Error</h1><p>Markdown library not installed.</p></body></html>"
        except Exception as e:
            logger.error(f"Error generating HTML content using Jinja2 template: {e}", exc_info=True)
            return f"<html><body><h1>Error</h1><p>An error occurred while generating the HTML report: {e}</p></body></html>"


    def save_summary_html(self, summary_markdown, output_path, meeting_title=None, url=None):
        """
        Saves the meeting summary as an HTML file using the Jinja2 template.

        Args:
            summary_markdown (str): Markdown formatted summary text.
            output_path (str): Output file path.
            meeting_title (str, optional): Meeting title. Defaults to None.
            url (str, optional): Meeting video link. Defaults to None.

        Returns:
            bool: True if saving was successful, False otherwise.
        """
        try:
            html_content = self._generate_html_content(summary_markdown, meeting_title, url)

            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"Summary successfully saved as HTML: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save summary to HTML file '{output_path}': {e}", exc_info=True)
            return False