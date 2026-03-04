# TrendScope

A comprehensive platform for processing, summarizing, and generating structured reports from conference content using AI. This project combines automated transcript processing, web scraping, data management, and report generation capabilities.

## 🎯 Project Overview

TrendScope is an automated tool that processes conference transcripts, presentations, and web-scraped content to generate structured reports. It includes:

- **AI-Powered Summarization**: Uses Google Gemini API to generate structured summaries
- **Web Scraping**: Automated scrapers for various conference websites
- **Data Management**: BigQuery integration for storing and querying conference data
- **Report Generation**: Automated generation of HTML/Markdown reports
- **RESTful API**: FastAPI-based backend for frontend integration

## ✨ Key Features

### Core Functionality
- **Batch Processing**: Process large volumes of conference transcripts and presentations
- **AI Summary Generation**: Automated structured summaries using Gemini API
- **Topic Categorization**: Organize content by technical topics
- **Multi-threaded Processing**: Efficient parallel processing support
- **Error Handling**: Comprehensive error handling with retry mechanisms

### API & Backend
- **RESTful API**: FastAPI-based backend with comprehensive endpoints
- **Web Scraping Management**: API endpoints for managing scrapers
- **PPT/PDF Processing**: Upload and process presentation files
- **BigQuery Integration**: Query and manage conference data
- **Batch Report Generation**: Generate reports from BigQuery data

### Infrastructure
- **Unified Configuration**: Centralized settings management with Pydantic
- **Structured Logging**: Comprehensive logging system
- **Error Handling**: Global exception handlers with unified error responses
- **CORS Support**: Configurable CORS settings per environment

## 📁 Project Structure

```
TrendScope/
├── base/                    # Backend API and core modules
│   ├── api/                # FastAPI application
│   │   ├── routes/        # API route handlers
│   │   ├── modules/       # Business logic modules
│   │   └── middleware/    # Middleware (error handlers, etc.)
│   ├── bigquery/          # BigQuery client and schemas
│   ├── scrapers/          # Web scraping modules
│   │   ├── parsers/       # Site-specific parsers
│   │   └── utils/         # Scraper utilities
│   ├── gcs/               # Google Cloud Storage client
│   └── utils/             # Shared utilities (logging, etc.)
├── config/                # Configuration management
│   ├── settings.py        # Centralized settings (Pydantic)
│   └── config.py          # Backward compatibility layer
├── scripts/               # Processing scripts
│   ├── 01_batch_summarize_process.py
│   ├── 02_category_page.py
│   └── ...
├── src/                   # Legacy core modules
├── frontend/              # React frontend application
├── data/                  # Input data directory
├── output/                # Generated reports
├── logs/                  # Application logs
└── pyproject.toml         # Project package configuration
```

## 🖼️ UI Overview

The following screenshots show the end-to-end workflow of TrendScope:

- **Home dashboard** – overall entry point and navigation.
  ![TrendScope Home](images/0-home.png)
- **BigQuery data & configuration** – manage conference data source and query.
  ![BigQuery & Data Setup](images/1-db.png)
- **PPT / PDF upload** – upload slide decks for AI-based processing.
  ![PPT Upload](images/2-ppt.png)
- **Batch report generation page** – configure and launch batch AI reports.
  ![Batch Report Generation](images/3-report.png)
- **Generated Markdown / HTML reports** – view and browse analysis results.
  ![Generated Reports](images/4-reportm.png)
- **Scraper management** – manage and run web scrapers for conference sources.
  ![Scraper Management](images/5-scraper.png)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+ (for frontend)
- Google Cloud account (for BigQuery and Gemini API)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TrendScope
   ```

2. **Install as a package (Recommended)**
   ```bash
   pip install -e .
   ```

   Or install dependencies directly:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Copy `.env_example` to `.env` and configure:
   ```bash
   cp .env_example .env
   ```

   Required environment variables:
   ```bash
   # Gemini API
   GEMINI_API_KEY=your_gemini_api_key
   
   # Google Cloud
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   GOOGLE_CLOUD_PROJECT=your-project-id
   
   # API Configuration (optional)
   API_ENVIRONMENT=development  # development, production, testing
   CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

### Running the Backend API

```bash
# Method 1: Using the main script
python base/main.py

# Method 2: Using uvicorn directly
uvicorn base.api.app:app --host 0.0.0.0 --port 8001 --reload
```

The API will be available at:
- **API Root**: http://localhost:8001/
- **API Docs**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

### Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📚 Usage

### 1. Conference Transcript Processing

```bash
python scripts/01_batch_summarize_process.py -i data/google_next_txt -o summaries/md
```

### 2. Generate Category Pages

```bash
python scripts/02_category_page.py
```

### 3. Generate Homepage Report

```bash
python scripts/03_generator_home.py -c google_next -i data/sheet/20250427_Qcon.csv -o output/google_next25_report
```

### 4. Generate Context Diagrams

```bash
python scripts/04_context_diagram.py
```

### 5. Using the API

#### Upload PPT Files
```bash
curl -X POST "http://localhost:8001/ppt/upload" \
  -F "files=@presentation1.pdf" \
  -F "files=@presentation2.pdf" \
  -F "seminar=Google IO 2025"
```

#### Query BigQuery Data
```bash
curl "http://localhost:8001/data/sessions?seminar=Google%20IO%2025&limit=10"
```

#### Run Scraper
```bash
curl -X POST "http://localhost:8001/scrapers/run" \
  -H "Content-Type: application/json" \
  -d '{"scraper_type": "aws_london", "headless": true}'
```

## 🔧 Configuration

### Settings Management

All configuration is centralized in `config/settings.py` using Pydantic Settings:

```python
from config.settings import settings

# Access configuration
api_key = settings.gemini_api_key
input_dir = settings.default_input_dir
```

### Environment Variables

See `.env_example` for all available configuration options. Key settings:

- **API Configuration**: `API_ENVIRONMENT`, `API_HOST`, `API_PORT`
- **CORS**: `CORS_ALLOW_ORIGINS`, `CORS_ALLOW_METHODS`
- **Gemini**: `GEMINI_API_KEY`, `GEMINI_MODEL_NAME`
- **Paths**: `DATA_DIR`, `DEFAULT_INPUT_DIR`, `DEFAULT_OUTPUT_DIR`

## 🏗️ Architecture

### Module Organization

- **Standard Imports**: Project is installed as a package, use standard imports:
  ```python
  from config.settings import settings
  from base.bigquery.client import BigQueryClient
  from base.scrapers.parsers.aws_london import run_aws_london_scraper
  ```

- **Error Handling**: Unified error handling with custom exception classes
- **Logging**: Structured logging with module-specific loggers
- **Configuration**: Centralized Pydantic-based settings

### Key Improvements

1. **Package Structure**: Project can be installed as a Python package
2. **Unified Error Handling**: Global exception handlers with consistent error responses
3. **Structured Logging**: Comprehensive logging system with file rotation
4. **Configuration Management**: Centralized settings with environment variable support
5. **Code Organization**: Clear separation of concerns, no duplicate code

## 📖 API Documentation

Full API documentation is available at `/docs` when the server is running. Key endpoints:

### PPT Upload
- `POST /ppt/upload` - Upload and process PPT/PDF files
- `GET /ppt/status/{task_id}` - Get processing status

### Scrapers
- `POST /scrapers/run` - Run a scraper
- `GET /scrapers/list` - List available scrapers
- `GET /scrapers/status/{task_id}` - Get scraper status

### Data Query
- `GET /data/sessions` - Query sessions from BigQuery
- `GET /data/seminars` - Get seminar list
- `GET /data/stats` - Get data statistics

### Batch Reports
- `POST /reports/generate` - Generate batch reports
- `GET /reports/status/{task_id}` - Get report generation status

## 🛠️ Development

### Setup Development Environment

```bash
# Install in editable mode
pip install -e ".[dev]"

# Install development dependencies
pip install pytest black ruff mypy
```

### Code Style

- Follow PEP 8
- Use type hints
- Use standard imports (no `sys.path` manipulation)
- Use logging instead of `print()`

### Testing

```bash
# Run tests (when available)
pytest

# Type checking
mypy base/

# Linting
ruff check .
```

## 📝 Logging

Logs are automatically saved to `logs/` directory:

- `logs/api_YYYYMMDD.log` - API logs
- `logs/scraper_YYYYMMDD.log` - Scraper logs
- `logs/bigquery_YYYYMMDD.log` - BigQuery logs

Log levels are automatically adjusted based on `API_ENVIRONMENT`:
- `development`: DEBUG level
- `production`: INFO level

## 🔗 Related Documentation

- [Optimization Guide](OPTIMIZATION_GUIDE.md) - Detailed optimization documentation
- [API Optimization Summary](API_OPTIMIZATION_SUMMARY.md) - API improvements
- [Logging Optimization Summary](LOGGING_OPTIMIZATION_SUMMARY.md) - Logging system
- [Setup Guide](SETUP.md) - Quick setup reference
- [Base API README](base/README.md) - Backend API documentation

## 📦 Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management

### AI & Cloud
- `google-generativeai` - Gemini API client
- `google-cloud-bigquery` - BigQuery client
- `google-cloud-storage` - GCS client

### Processing
- `pandas` - Data processing
- `selenium` - Web scraping
- `opencc-python-reimplemented` - Traditional/Simplified Chinese conversion

### Utilities
- `python-dotenv` - Environment variable management
- `Jinja2` - Template engine
- `beautifulsoup4` - HTML parsing

## 🚧 Roadmap

- [ ] PostgreSQL integration
- [ ] Redis caching layer
- [ ] Improved retry mechanisms with exponential backoff
- [ ] Complete scraper logging migration
- [ ] Comprehensive test coverage

## 📄 License

MIT License

## 👥 Contributing

Contributions are welcome! Please ensure:
1. Code follows the project's style guidelines
2. All tests pass
3. Documentation is updated
4. Use standard imports (no `sys.path` manipulation)

## 📞 Support

For issues and questions, please open an issue on GitHub.
