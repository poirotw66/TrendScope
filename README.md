# Google Next 2025 Report Generator

This project is an automated tool for processing, summarizing, and generating structured reports about the content from Google Next 2025 and NVIDIA GTC 2025 conferences.

## Project Description

This tool can process original conference transcripts using generative AI to create summaries and organize them into structured report pages, including:
- Conference content summaries (categorized by topics)
- Topic page generation
- Homepage report generation
- Context relationship diagram generation

## Key Features

- **Batch Processing of Conference Transcripts**: Automatically process large volumes of meeting transcript files
- **AI Summary Generation**: Use Gemini API to automatically generate structured summaries of conference content
- **Topic Categorization**: Organize content by technical topics
- **HTML Report Output**: Output summaries and categorization results as web-based reports
- **Multi-threading Processing**: Support multi-threaded batch processing for improved efficiency
- **Error Retry Mechanism**: Automatically retry when API calls fail
- **Quota Management**: Manage API call frequency to comply with limitations

## Directory Structure

- **config/**: Configuration files
- **data/**: Original conference text data
  - **google_next_txt/**: Google Next 2025 conference transcripts
  - **GTC_all_transcript/**: NVIDIA GTC 2025 conference transcripts
  - **sheet/**: Conference spreadsheet data
- **scripts/**: Processing scripts
  - **01_batch_summarize_process.py**: Batch summary processing
  - **02_category_page.py**: Category page generation
  - **03_generator_home.py**: Homepage generation
  - **04_context_diagram.py**: Context diagram generation
- **src/**: Core source code
  - **api/**: API-related modules
  - **templates/**: HTML templates
  - **utils/**: Utility functions
- **summaries/**: Generated summaries
  - **html/**: HTML format summaries
  - **md/**: Markdown format summaries
  - **session/**: Session summaries
- **output/**: Final output reports

## Installation and Setup

### Requirements
- Python 3.10+
- Install dependencies according to requirements.txt

```bash
pip install -r requirements.txt
```

### Environment Variable Configuration
Create a `.env` file containing the following settings:
```
GEMINI_API_KEY=your_api_key
DEFAULT_INPUT_DIR=data/google_next_txt
DEFAULT_OUTPUT_DIR=summaries/md
```

## Usage Instructions

### 1. Conference Transcript Summary Processing

```bash
python scripts/01_batch_summarize_process.py -i data/google_next_txt -o summaries/md
```

### 2. Generate Category Pages

```bash
python scripts/02_category_page.py
```

### 3. Generate Homepage

```bash
python scripts/03_generator_home.py -c google_next -i data/sheet/20250427_Qcon.csv -o output/google_next25_report
```

### 4. Generate Context Diagrams

```bash
python scripts/04_context_diagram.py
```

## Output Results

After processing, you can find the generated report pages in the `output/google_next25_report` directory, including:
- Homepage overview
- Conference summaries categorized by topics
- Detailed content summaries for each session

## Dependencies

- google-generativeai: Python client for Google Gemini API
- pandas: Data processing and analysis
- markdown: Markdown processing
- python-dotenv: Environment variable management
- Jinja2: Template engine
- beautifulsoup4: HTML parsing