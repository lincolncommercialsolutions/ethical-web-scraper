# Ethical Web Scraper for Cybersecurity

A professional, ethical web scraper designed for cybersecurity research, OSINT analysis, and security auditing. Built by Lincoln Commercial Solutions for responsible security testing and analysis.

## 🎯 Features

- **Ethical by Design**: Respects robots.txt, implements rate limiting, and uses clear identification
- **Security-Focused**: Extracts security headers, SSL/TLS info, tech stack fingerprints, and security.txt
- **Dual Mode**: Static scraping (fast) and dynamic scraping with Playwright (JavaScript support)
- **Structured Output**: Clean JSON reports with Pydantic validation
- **Audit Trail**: Comprehensive structured logging for compliance
- **CLI Interface**: Easy-to-use command-line tool with rich formatting

## 📋 What It Extracts

- HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
- Missing critical security headers
- SSL/TLS certificate information
- Server and technology stack details (Server, X-Powered-By, generator meta)
- JavaScript framework detection (React, Vue, Angular, etc.)
- Security.txt presence and location
- Page metadata (title, description)
- Link analysis (internal/external counts)
- Contact information (emails - use responsibly)

## 🚀 Installation

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
   cd /home/linkl0n/web-scrape
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: Install Playwright for dynamic scraping**:
   ```bash
   pip install playwright
   playwright install chromium
   ```

## 💻 Usage

### 🌐 Web UI (Recommended for Easy Use)

**Launch the web interface:**
```bash
./run_ui.sh
```

Or manually:
```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

**Features:**
- 🎨 Beautiful, intuitive interface
- 📊 Real-time progress tracking
- 📈 Visual metrics and charts
- 🔍 Interactive results explorer
- ⬇️ One-click report downloads
- ⚙️ Easy configuration

See [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) for detailed instructions.

### 🖥️ Command-Line Interface

### Basic Static Scraping

```bash
# Scrape a single URL
python main.py https://example.com

# With custom contact email
python main.py https://example.com --email your-email@example.com
```

### Dynamic Scraping (JavaScript-heavy sites)

```bash
# Use Playwright for JavaScript rendering
python main.py https://example.com --dynamic
```

### Advanced Options

```bash
# Save to custom output file
python main.py https://example.com --output my_report.json

# Ignore robots.txt (use responsibly!)
python main.py https://example.com --ignore-robots

# Custom timeout and retries
python main.py https://example.com --timeout 30 --max-retries 5

# Debug logging
python main.py https://example.com --log-level DEBUG

# JSON-only output (no formatting)
python main.py https://example.com --json-only
```

### Command-Line Help

```bash
python main.py --help
```

## 📊 Output

### Console Output

The scraper provides a formatted security report in the terminal:

```
======================================================================
SECURITY REPORT
======================================================================

📋 Page Information:
   Status Code: 200
   Title: Example Domain
   Description: Example domain for use in illustrative examples...

🔒 Security Headers:
   ✓ Content-Security-Policy: default-src 'self'
   ✓ X-Frame-Options: DENY

⚠️  Missing Important Headers:
   ✗ Strict-Transport-Security
   ✗ X-Content-Type-Options

📄 Security.txt:
   ✓ Found at: https://example.com/.well-known/security.txt

🔐 SSL/TLS:
   ✓ Certificate valid
   Issuer: Let's Encrypt
```

### JSON Reports

All reports are saved as JSON files in the `output/` directory:

```json
{
  "url": "https://example.com",
  "status_code": 200,
  "timestamp": "2026-02-03T10:30:00",
  "title": "Example Domain",
  "security_headers": {
    "Content-Security-Policy": "default-src 'self'",
    "X-Frame-Options": "DENY"
  },
  "missing_important_headers": [
    "Strict-Transport-Security",
    "X-Content-Type-Options"
  ],
  "has_security_txt": true,
  "ssl_verified": true
}
```

## 🛡️ Ethical Guidelines

This tool is designed for **ethical and legal use only**:

1. ✅ **Only scrape public data** - No unauthorized access
2. ✅ **Respect robots.txt** - Always use `--respect-robots` (default)
3. ✅ **Rate limiting** - Built-in delays (2.5-7 seconds) prevent server overload
4. ✅ **Clear identification** - User-Agent includes contact email
5. ✅ **Authorized testing** - Only use on systems you own or have permission to test
6. ✅ **Data privacy** - Don't harvest personal information
7. ✅ **Audit trails** - All actions are logged for accountability

### ⚠️ Legal Disclaimer

Users are responsible for ensuring their use complies with:
- Website Terms of Service
- GDPR/CCPA and data protection laws
- Computer Fraud and Abuse Act (CFAA) and similar laws
- Applicable cybersecurity regulations

**This tool is for authorized security research and testing only.**

## 📁 Project Structure

```
web-scrape/
├── scraper/
│   ├── __init__.py       # Package initialization
│   ├── core.py           # Main scraping logic (static & dynamic)
│   ├── models.py         # Pydantic data models
│   ├── ethics.py         # Robots.txt compliance & rate limiting
│   └── utils.py          # Logging, headers, helpers
├── output/               # JSON reports saved here
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── details.txt           # Technical specifications
├── info.txt              # Technology stack info
├── instructions.txt      # Implementation guide
└── plan.txt              # Development plan
```

## 🔧 Configuration

### Custom Headers

Edit `scraper/utils.py` to customize HTTP headers:

```python
def get_headers(contact_email: str = "your-email@example.com"):
    return {
        "User-Agent": f"YourBot/1.0 ({contact_email})",
        # ... other headers
    }
```

### Delay Settings

Modify `scraper/ethics.py` to adjust delays:

```python
def ethical_delay(min_sec: float = 2.5, max_sec: float = 7.0):
    # Adjust min_sec and max_sec as needed
    ...
```

## 🧪 Testing

Test on safe, public domains:

```bash
# Safe test targets
python main.py https://example.com
python main.py https://httpbin.org/html
```

**Never test on production systems without authorization!**

## 🐛 Troubleshooting

### SSL Errors

```bash
# Check if site has valid SSL
python main.py https://example.com --log-level DEBUG
```

### Timeout Issues

```bash
# Increase timeout for slow sites
python main.py https://example.com --timeout 30
```

### Playwright Issues

```bash
# Reinstall browser binaries
playwright install chromium

# Check if Playwright is installed
python -c "import playwright; print('OK')"
```

### Import Errors

```bash
# Verify all dependencies are installed
pip install -r requirements.txt --upgrade
```

## 📚 Dependencies

- **requests** - HTTP requests
- **beautifulsoup4** - HTML parsing
- **lxml** - Fast XML/HTML parser
- **pydantic** - Data validation
- **structlog** - Structured logging
- **playwright** - Browser automation (optional)

## 🤝 Contributing

This is a private cybersecurity project. For issues or improvements, contact the Lincoln Commercial Solutions team.

## 📄 License

Copyright © 2026 Lincoln Commercial Solutions. All rights reserved.

For authorized use in cybersecurity research and development only.

## 📞 Contact

- **Organization**: Lincoln Commercial Solutions
- **Project**: Cybersecurity Development
- **Email**: security-research@lincolncommercial.com

---

**Remember**: With great scraping power comes great responsibility. Always act ethically and legally.
