# ScrapyScrape

A focused web scraper designed for security researchers, OSINT practitioners, and security auditors.  
It is built with responsible use in mind and aims to support legitimate security testing and analysis.

## Key Features

- Ethical defaults: respects robots.txt, enforces rate limiting, provides clear user-agent identification
- Security-oriented: collects security headers, SSL/TLS details, technology fingerprints, and security.txt files
- Two scraping modes: fast static scraping (requests-based) and dynamic JavaScript-capable scraping (Playwright)
- Structured, validated output using Pydantic models
- Detailed audit-friendly logging
- Simple CLI with helpful formatting
- Interactive web interface built with Streamlit

## What It Collects

- Important HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
- Missing critical security headers
- SSL/TLS certificate details
- Server and technology stack indicators (Server, X-Powered-By, meta generator tags)
- Common JavaScript framework/library detection (React, Vue, Angular, jQuery, etc.)
- Presence and location of security.txt
- Basic page metadata (title, description)
- Internal and external links with full URLs
- Contact information such as email addresses (use with extreme care and only when appropriate)

## Installation

### Requirements
- Python 3.9 or newer
- pip package manager

### Recommended: Automated Setup
```bash
./setup.sh
Manual Installation

Clone or download the repository and navigate to the project folder:Bashcd /path/to/scrapyscrape
Create and activate a virtual environment (strongly recommended):Bashpython3 -m venv venv
source venv/bin/activate      # Linux / macOS
# or on Windows:
venv\Scripts\activate
Install Python dependencies:Bashpip install -r requirements.txt
Install Playwright browsers (needed for dynamic mode):Bashplaywright install chromium

Usage
Web Interface (Recommended for most users)
Start the interactive UI:
Bashstreamlit run app.py
Then visit http://localhost:8501 in your browser.
The web UI offers:

Simple URL input
Live progress updates
Side-by-side result views
CSV export for links
JSON report download
Quick preset configurations

Command Line Interface
Basic scan (default: static mode):
Bashpython main.py https://example.com
Static mode (faster, no JavaScript rendering):
Bashpython main.py https://example.com --mode static
Dynamic mode (handles JavaScript-heavy sites):
Bashpython main.py https://example.com --mode dynamic
Save report to custom location:
Bashpython main.py https://example.com --output reports/example-scan.json
Override robots.txt (only with explicit permission):
Bashpython main.py https://example.com --no-respect-robots
Adjust timeout and retry behavior:
Bashpython main.py https://example.com --timeout 30 --max-retries 5
See all options:
Bashpython main.py --help
Output
Reports are saved as timestamped JSON files in the output/ directory.
Example report structure:
JSON{
  "url": "https://example.com",
  "status_code": 200,
  "timestamp": "2026-02-04T13:45:22",
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
Project Layout
textscrapyscrape/
├── scraper/              # Core scraping logic
│   ├── __init__.py
│   ├── core.py
│   ├── models.py         # Pydantic schemas
│   ├── ethics.py         # Compliance and rate-limiting
│   └── utils.py
├── app.py                # Streamlit web interface
├── main.py               # CLI entry point
├── requirements.txt
├── setup.sh              # Automated setup
├── run_ui.sh             # Quick UI launcher
├── test_scraper.py       # Basic verification test
├── output/               # Generated reports (git-ignored)
├── README.md
├── QUICKSTART.md
├── WEB_UI_GUIDE.md
└── DEPLOYMENT.md
Responsible & Ethical Use
This tool is intended only for legitimate security research, authorized testing, and OSINT activities.
Always obtain explicit permission before scanning any website you do not own.
Recommended practices:

Scan only domains you control or have written authorization to test
Honor robots.txt unless you have permission to ignore it
Apply reasonable delays between requests
Use a descriptive user-agent with contact information
Follow responsible disclosure guidelines
Comply with all relevant laws and terms of service

Security Headers Analyzed

Content-Security-Policy (CSP)
Strict-Transport-Security (HSTS)
X-Frame-Options
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
X-XSS-Protection (legacy)

Technology Detection
Detects common front-end frameworks and libraries including:

React
Vue.js
Angular
jQuery
Bootstrap
Next.js
Nuxt.js
…and several others

Troubleshooting
Playwright browser issues
Run:
Bashplaywright install chromium
playwright install-deps
Permission problems
Make scripts executable:
Bashchmod +x setup.sh run_ui.sh
Module not found errors
Ensure the virtual environment is active.
Port 8501 already in use
Try a different port:
Bashstreamlit run app.py --server.port 8502
Development & Maintenance
Run basic verification:
Bashpython test_scraper.py
Update dependencies:
Bashpip install --upgrade -r requirements.txt
Deployment
See DEPLOYMENT.md for instructions covering:

Docker
Cloud VPS
Streamlit Community Cloud
Railway
systemd service
Nginx reverse proxy with SSL

Quick start (if script is provided):
Bashsudo ./deploy.sh
Contributing
Contributions are welcome. Please read CONTRIBUTING.md first.
License
MIT License with an explicit ethical use restriction.
See the LICENSE file for full details.
Support & Contact

Report issues: https://github.com/lincolncommercialsolutions/ethical-web-scraper/issues
Documentation: check the various .md files in this repository


Version: 1.0.0
Last Updated: February 2026
Status: Production ready
