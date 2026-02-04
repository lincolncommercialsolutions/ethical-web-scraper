ScrapyScrape
A focused, security-oriented web scraper built for security researchers, OSINT practitioners, penetration testers, and compliance auditors.
Designed from the ground up with responsible and ethical use in mind, supporting legitimate security testing, vulnerability discovery, and site analysis.

Key Features

Ethical defaults: respects robots.txt, enforces configurable rate limiting, uses identifiable user-agent strings
Security-first focus: collects security headers, SSL/TLS details, technology fingerprints, security.txt files
Two scraping modes: fast static (requests + BeautifulSoup) and JavaScript-capable dynamic (Playwright)
Clean, validated JSON output using Pydantic models
Structured, audit-friendly logging
Simple, well-documented CLI
Interactive web interface built with Streamlit


What It Collects

Important HTTP security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy, etc.)
Missing critical security headers
SSL/TLS certificate information (issuer, validity, protocol)
Server and tech stack fingerprints (Server, X-Powered-By, meta generator tags)
Detection of common JavaScript frameworks/libraries (React, Vue, Angular, jQuery, Bootstrap, Next.js, Nuxt.js, etc.)
Presence and location of security.txt
Page metadata (title, description)
Internal and external links (fully resolved URLs)
Contact details like email addresses (use responsibly and only when appropriate)


Installation
Requirements

Python 3.9+
pip

Quick Setup (Recommended)
Bash./setup.sh
Manual Setup

Go to the project folderBashcd /path/to/scrapyscrape
Create and activate a virtual environmentBashpython3 -m venv venv
source venv/bin/activate          # Linux/macOS
# Windows:
venv\Scripts\activate
Install dependenciesBashpip install -r requirements.txt
Install Playwright browsers (needed for dynamic mode)Bashplaywright install chromium


Usage
Web Interface (Most People Prefer This)
Bashstreamlit run app.py
Then open http://localhost:8501
Includes: URL input, live progress, side-by-side results, link CSV export, JSON download, quick presets.
Command Line
Basic scan (static mode default):
Bashpython main.py https://example.com
Static mode:
Bashpython main.py https://example.com --mode static
Dynamic mode (JavaScript rendered):
Bashpython main.py https://example.com --mode dynamic
Custom output file:
Bashpython main.py https://example.com --output reports/example.json
Ignore robots.txt (only with permission):
Bashpython main.py https://example.com --no-respect-robots
Tune timeout/retries:
Bashpython main.py https://example.com --timeout 30 --max-retries 5
Show all options:
Bashpython main.py --help

Output Example
Reports are saved as timestamped JSON files in the output/ folder.
JSON{
  "url": "https://example.com",
  "status_code": 200,
  "timestamp": "2026-02-04T14:22:18",
  "title": "Example Domain",
  "security_headers": {
    "Content-Security-Policy": "default-src 'self'",
    "X-Frame-Options": "DENY"
  },
  "missing_important_headers": [
    "Strict-Transport-Security",
    "Permissions-Policy"
  ],
  "ssl": {
    "verified": true,
    "issuer": "DigiCert Inc",
    "protocol": "TLSv1.3"
  },
  "server": "nginx/1.18.0",
  "internal_links": [
    "https://example.com/about",
    "https://example.com/contact"
  ],
  "external_links": [
    "https://www.iana.org/domains/example"
  ],
  "technologies": ["jquery", "bootstrap"]
}
