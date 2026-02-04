# Quick Reference Guide - Ethical Web Scraper

## 🌐 Web UI (Easiest Way!)

### Launch the Web Interface
```bash
# Quick launch
./run_ui.sh

# Or manually
streamlit run app.py
```

**Then open:** http://localhost:8501 in your browser

### Features
- 🎨 Beautiful visual interface
- 📊 Real-time scanning progress
- 🔍 Interactive results
- ⬇️ One-click downloads
- ⚙️ Easy configuration

See [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) for full details.

---

## 🖥️ Command-Line Interface

## Installation

```bash
# 1. Navigate to project directory
cd /home/linkl0n/web-scrape

# 2. Create virtual environment (if not exists)
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test installation
python test_scraper.py
```

## Basic Commands

### Simple Scraping
```bash
# Scrape a single URL
python main.py https://example.com

# Scrape with custom contact email
python main.py https://example.com --email your-email@company.com
```

### Advanced Options
```bash
# Dynamic scraping (JavaScript support) - requires Playwright
python main.py https://example.com --dynamic

# Custom timeout and retries
python main.py https://example.com --timeout 30 --max-retries 5

# Debug mode
python main.py https://example.com --log-level DEBUG

# Save to specific file
python main.py https://example.com --output my_report.json

# JSON output only (no formatting)
python main.py https://example.com --json-only

# Ignore robots.txt (use responsibly!)
python main.py https://example.com --ignore-robots
```

### Installing Playwright (Optional)
```bash
pip install playwright
playwright install chromium
```

## What Gets Extracted

✅ **Security Headers**
- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options
- And more...

✅ **Page Information**
- Title
- Meta description
- Status code

✅ **Technology Stack**
- Server type
- JavaScript frameworks
- Generator/CMS information

✅ **Security.txt**
- Presence detection
- Location

✅ **SSL/TLS**
- Certificate validation
- Issuer information

✅ **Links**
- Internal/external link counts

## Output Files

Reports are saved in: `output/`
Logs are saved in: `logs/`

Report filename format: `report_<domain>_<timestamp>.json`

## Common Use Cases

### 1. Quick Security Audit
```bash
python main.py https://yoursite.com
```

### 2. Check Multiple Sites
```bash
for url in https://site1.com https://site2.com https://site3.com; do
    python main.py "$url"
    sleep 5
done
```

### 3. Scan with Custom Settings
```bash
python main.py https://target.com \
    --email security@yourcompany.com \
    --timeout 30 \
    --log-level INFO \
    --output security_audit.json
```

### 4. JavaScript-Heavy Site
```bash
python main.py https://react-app.com --dynamic
```

## Ethical Guidelines

⚠️ **Always Remember:**
- Only scrape sites you own or have permission to test
- Respect robots.txt (default behavior)
- Use appropriate delays (automatic)
- Include valid contact information
- Don't harvest personal data
- Comply with all applicable laws

## Troubleshooting

### SSL Errors
```bash
# Check with debug logging
python main.py https://site.com --log-level DEBUG
```

### Timeout Issues
```bash
# Increase timeout
python main.py https://slow-site.com --timeout 60
```

### Missing Dependencies
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

### Playwright Not Working
```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium
```

## File Structure

```
web-scrape/
├── scraper/              # Main package
│   ├── core.py          # Scraping logic
│   ├── models.py        # Data models
│   ├── ethics.py        # Robots.txt & delays
│   └── utils.py         # Helpers
├── output/              # JSON reports
├── logs/                # Log files
├── main.py              # CLI tool
├── test_scraper.py      # Quick test
└── requirements.txt     # Dependencies
```

## Help

```bash
# Get full help
python main.py --help

# Version info
python main.py --version
```

## Examples of Safe Test Targets

- https://example.com
- https://httpbin.org/html
- Your own websites only!

**Never test on production systems without authorization!**
