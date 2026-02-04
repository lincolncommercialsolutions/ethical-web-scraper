# ScrapyScrape

A professional web scraper for security research, OSINT analysis, and security auditing. Built for responsible security testing and analysis.

## Features

- **Ethical by Design**: Respects robots.txt, implements rate limiting, and uses clear identification
- **Security-Focused**: Extracts security headers, SSL/TLS info, tech stack fingerprints, and security.txt
- **Dual Mode**: Static scraping (fast) and dynamic scraping with Playwright (JavaScript support)
- **Structured Output**: Clean JSON reports with Pydantic validation
- **Audit Trail**: Comprehensive structured logging for compliance
- **CLI Interface**: Easy-to-use command-line tool with rich formatting
- **Web Interface**: Streamlit-based UI for interactive scraping

## What It Extracts

- HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
- Missing critical security headers
- SSL/TLS certificate information
- Server and technology stack details (Server, X-Powered-By, generator meta)
- JavaScript framework detection (React, Vue, Angular, etc.)
- Security.txt presence and location
- Page metadata (title, description)
- Link analysis (internal/external with full URLs)
- Contact information (emails - use responsibly)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Quick Setup

**Automated setup (recommended):**
```bash
./setup.sh
```

### Manual Setup

1. **Clone or download this project**:
   ```bash
   cd /path/to/web-scrape
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # OR on Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (for dynamic scraping):
   ```bash
   playwright install chromium
   ```

## Usage

### Web Interface (Recommended)

**Start the web UI**:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features**:
- Interactive URL input
- Real-time progress tracking
- Two-column results display
- Downloadable CSV files for links
- JSON export
- Quick test presets

### Command Line Interface

**Basic usage**:
```bash
python main.py https://example.com
```

**Static scraping (fast)**:
```bash
python main.py https://example.com --mode static
```

**Dynamic scraping (JavaScript-heavy sites)**:
```bash
python main.py https://example.com --mode dynamic
```

**Save to specific file**:
```bash
python main.py https://example.com --output my-report.json
```

**Override robots.txt** (use with permission):
```bash
python main.py https://example.com --no-respect-robots
```

**Adjust timeout and retries**:
```bash
python main.py https://example.com --timeout 30 --max-retries 5
```

**Get help**:
```bash
python main.py --help
```

## Output

Reports are saved as JSON files in the `output/` directory with timestamps.

**Example report structure**:
```json
{
  "url": "https://example.com",
  "status_code": 200,
  "timestamp": "2026-02-04T10:30:00",
  "title": "Example Domain",
  "security_headers": {
    "Content-Security-Policy": "default-src 'self'",
    "X-Frame-Options": "DENY"
  },
  "missing_important_headers": [
    "Strict-Transport-Security"
  ],
  "ssl_verified": true,
  "ssl_issuer": "DigiCert Inc",
  "server": "nginx/1.18.0",
  "internal_links": [
    "https://example.com/about",
    "https://example.com/contact"
  ],
  "external_links": [
    "https://www.iana.org/domains/example"
  ]
}
```

## Project Structure

```
web-scrape/
├── scraper/              # Core scraping package
│   ├── __init__.py
│   ├── core.py          # Main scraping logic
│   ├── models.py        # Pydantic data models
│   ├── ethics.py        # Ethical compliance layer
│   └── utils.py         # Helper functions
├── app.py               # Streamlit web interface
├── main.py              # CLI entry point
├── requirements.txt     # Python dependencies
├── setup.sh            # Automated setup script
├── run_ui.sh           # Quick UI launcher
├── test_scraper.py     # Installation verification
├── output/             # Generated reports
├── README.md           # This file
├── QUICKSTART.md       # Quick reference guide
├── WEB_UI_GUIDE.md     # Web UI documentation
└── DEPLOYMENT.md       # Deployment instructions
```

## Ethical Use

This tool is designed for legitimate security research and testing. Always ensure you have permission before scanning any website.

**Guidelines**:
- Only scan sites you own or have explicit permission to test
- Respect robots.txt unless you have permission to override
- Use appropriate delays to avoid overloading servers
- Identify yourself with a valid contact email
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## Security Headers Checked

- **Content-Security-Policy** (CSP): Prevents XSS attacks
- **Strict-Transport-Security** (HSTS): Enforces HTTPS
- **X-Frame-Options**: Prevents clickjacking
- **X-Content-Type-Options**: Prevents MIME sniffing
- **Referrer-Policy**: Controls referrer information
- **Permissions-Policy**: Controls browser features
- **X-XSS-Protection**: Legacy XSS protection

## Technology Detection

The scraper can detect:
- React
- Vue.js
- Angular
- jQuery
- Bootstrap
- Next.js
- Nuxt.js
- And more...

## Requirements

- Python 3.9+
- requests
- beautifulsoup4
- lxml
- pydantic
- structlog
- httpx
- playwright (optional, for dynamic scraping)
- streamlit (for web UI)

## Troubleshooting

### Playwright Installation Issues

If you encounter issues with Playwright:
```bash
playwright install chromium
playwright install-deps
```

### Permission Errors

Make sure scripts are executable:
```bash
chmod +x setup.sh run_ui.sh
```

### Import Errors

Ensure the virtual environment is activated:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Port Already in Use

If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

## Development

**Run tests**:
```bash
python test_scraper.py
```

**Check installed packages**:
```bash
pip list
```

**Update dependencies**:
```bash
pip install --upgrade -r requirements.txt
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Docker deployment
- Cloud VPS deployment
- Streamlit Cloud
- Railway deployment
- systemd service setup
- Nginx reverse proxy
- SSL/TLS configuration

**Quick deployment**:
```bash
sudo ./deploy.sh
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License with an ethical use clause. See [LICENSE](LICENSE) for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/lincolncommercialsolutions/ethical-web-scraper/issues
- Documentation: See guides in this repository

## Changelog

### Version 1.0.0
- Initial release
- Static and dynamic scraping modes
- Web UI with Streamlit
- CLI interface
- Link extraction and export
- Security header analysis
- SSL/TLS verification
- Technology detection

## Acknowledgments

Built with:
- Beautiful Soup for HTML parsing
- Playwright for browser automation
- Streamlit for web interface
- Pydantic for data validation
- structlog for structured logging

---

**Version**: 1.0.0  
**Last Updated**: February 4, 2026  
**Status**: Production Ready
