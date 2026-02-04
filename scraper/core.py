"""
Core web scraping functionality for static and dynamic content.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import List, Optional
from datetime import datetime
import ssl
import socket

from .models import SecurityReport
from .ethics import is_allowed_by_robots, ethical_delay, should_respect_rate_limit, exponential_backoff
from .utils import get_headers, logger, identify_security_headers, get_missing_headers


def scrape_static(
    url: str,
    contact_email: str = "security-research@lincolncommercial.com",
    respect_robots: bool = True,
    max_retries: int = 3,
    timeout: int = 15
) -> SecurityReport:
    """
    Scrape static web content using requests and BeautifulSoup.
    
    Args:
        url: Target URL to scrape
        contact_email: Contact email for ethical identification
        respect_robots: Whether to respect robots.txt
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds
    
    Returns:
        SecurityReport object containing extracted information
    """
    headers = get_headers(contact_email)
    
    # Check robots.txt compliance
    if respect_robots and not is_allowed_by_robots(url):
        logger.warning("scraping_blocked", url=url, reason="robots.txt")
        return SecurityReport(
            url=url,
            status_code=0,
            error="Disallowed by robots.txt"
        )
    
    # Ethical delay before request
    ethical_delay()
    
    # Retry logic with exponential backoff
    for attempt in range(max_retries):
        try:
            logger.info("fetching_url", url=url, attempt=attempt + 1)
            
            # Make the request
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
                verify=True,
                allow_redirects=True
            )
            
            # Check for rate limiting
            if should_respect_rate_limit(response.status_code):
                backoff_time = exponential_backoff(attempt)
                logger.warning(
                    "rate_limited",
                    url=url,
                    status_code=response.status_code,
                    backoff=backoff_time
                )
                if attempt < max_retries - 1:
                    import time
                    time.sleep(backoff_time)
                    continue
            
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract data
            report_data = _extract_static_data(url, response, soup)
            
            logger.info("scraping_successful", url=url, status_code=response.status_code)
            return SecurityReport(**report_data)
            
        except requests.exceptions.SSLError as e:
            logger.error("ssl_error", url=url, error=str(e))
            return SecurityReport(
                url=url,
                status_code=0,
                error=f"SSL verification failed: {str(e)}",
                ssl_verified=False
            )
            
        except requests.exceptions.Timeout:
            logger.warning("timeout", url=url, attempt=attempt + 1)
            if attempt < max_retries - 1:
                continue
            return SecurityReport(
                url=url,
                status_code=0,
                error=f"Request timeout after {max_retries} attempts"
            )
            
        except requests.exceptions.RequestException as e:
            logger.error("request_error", url=url, error=str(e), attempt=attempt + 1)
            if attempt < max_retries - 1:
                continue
            return SecurityReport(
                url=url,
                status_code=getattr(e.response, 'status_code', 0) if hasattr(e, 'response') else 0,
                error=str(e)
            )
    
    # Should not reach here
    return SecurityReport(
        url=url,
        status_code=0,
        error="Max retries exceeded"
    )


def _extract_static_data(url: str, response: requests.Response, soup: BeautifulSoup) -> dict:
    """
    Extract security-relevant data from static HTML.
    
    Args:
        url: Original URL
        response: requests Response object
        soup: BeautifulSoup parsed HTML
    
    Returns:
        Dictionary of extracted data
    """
    data = {
        "url": url,
        "status_code": response.status_code,
        "timestamp": datetime.now(),
    }
    
    # Extract page metadata
    title_tag = soup.find('title')
    data["title"] = title_tag.string.strip() if title_tag and title_tag.string else None
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        data["meta_description"] = meta_desc['content']
    
    # Extract security headers
    data["security_headers"] = identify_security_headers(dict(response.headers))
    data["missing_important_headers"] = get_missing_headers(dict(response.headers))
    
    # Server information
    data["server"] = response.headers.get('Server')
    data["powered_by"] = response.headers.get('X-Powered-By')
    
    # Check for generator meta tag (tech stack fingerprint)
    generator = soup.find('meta', attrs={'name': 'generator'})
    if generator and generator.get('content'):
        data["generator"] = generator['content']
    
    # Check for security.txt
    security_txt_present, security_txt_url = _check_security_txt(url)
    data["has_security_txt"] = security_txt_present
    data["security_txt_url"] = security_txt_url
    
    # Extract emails (use cautiously)
    data["extracted_emails"] = _extract_emails(soup)
    
    # Extract and categorize links
    links = soup.find_all('a', href=True)
    internal, external = _categorize_links(url, links)
    data["internal_links"] = list(set(internal))  # Remove duplicates
    data["external_links"] = list(set(external))  # Remove duplicates
    data["internal_links_count"] = len(data["internal_links"])
    data["external_links_count"] = len(data["external_links"])
    
    # Detect JavaScript frameworks
    data["js_framework_hints"] = _detect_js_frameworks(soup, response.text)
    
    # SSL/TLS information
    data["ssl_verified"] = True  # If we got here, SSL was verified
    try:
        ssl_info = _get_ssl_info(url)
        data["ssl_issuer"] = ssl_info.get("issuer")
    except Exception:
        pass
    
    return data


def _check_security_txt(base_url: str) -> tuple:
    """
    Check if security.txt exists.
    
    Args:
        base_url: Base URL of the site
    
    Returns:
        Tuple of (exists: bool, url: Optional[str])
    """
    security_txt_paths = [
        "/.well-known/security.txt",
        "/security.txt"
    ]
    
    for path in security_txt_paths:
        url = urljoin(base_url, path)
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                logger.info("security_txt_found", url=url)
                return True, url
        except Exception:
            continue
    
    return False, None


def _extract_emails(soup: BeautifulSoup) -> List[str]:
    """
    Extract email addresses from HTML (use responsibly).
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        List of email addresses
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    text = soup.get_text()
    emails = list(set(re.findall(email_pattern, text)))
    
    # Limit to avoid PII issues - only take first 5
    return emails[:5]


def _categorize_links(base_url: str, links: List) -> tuple:
    """
    Categorize links as internal or external.
    
    Args:
        base_url: Base URL for comparison
        links: List of link elements
    
    Returns:
        Tuple of (internal_links, external_links)
    """
    base_domain = urlparse(base_url).netloc
    internal = []
    external = []
    
    for link in links:
        href = link.get('href', '')
        if not href or href.startswith(('#', 'javascript:', 'mailto:')):
            continue
        
        absolute_url = urljoin(base_url, href)
        link_domain = urlparse(absolute_url).netloc
        
        if link_domain == base_domain:
            internal.append(absolute_url)
        else:
            external.append(absolute_url)
    
    return internal, external


def _detect_js_frameworks(soup: BeautifulSoup, html: str) -> List[str]:
    """
    Detect JavaScript frameworks in use.
    
    Args:
        soup: BeautifulSoup object
        html: Raw HTML string
    
    Returns:
        List of detected framework names
    """
    frameworks = []
    
    # Check for common framework indicators
    indicators = {
        'React': ['react.js', 'react.min.js', 'react-dom', '__REACT_'],
        'Vue': ['vue.js', 'vue.min.js', '__vue__'],
        'Angular': ['angular.js', 'angular.min.js', 'ng-app', 'ng-controller'],
        'jQuery': ['jquery.js', 'jquery.min.js', 'jQuery'],
        'Bootstrap': ['bootstrap.js', 'bootstrap.min.js', 'bootstrap.css'],
        'Next.js': ['_next/', '__NEXT_DATA__'],
        'Nuxt': ['_nuxt/'],
    }
    
    html_lower = html.lower()
    
    for framework, patterns in indicators.items():
        if any(pattern.lower() in html_lower for pattern in patterns):
            frameworks.append(framework)
    
    return frameworks


def _get_ssl_info(url: str) -> dict:
    """
    Get SSL certificate information.
    
    Args:
        url: Target URL
    
    Returns:
        Dictionary with SSL info
    """
    parsed = urlparse(url)
    hostname = parsed.netloc
    port = 443
    
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                return {
                    "issuer": issuer.get('organizationName', 'Unknown')
                }
    except Exception:
        return {}


def scrape_dynamic(
    url: str,
    contact_email: str = "security-research@lincolncommercial.com",
    respect_robots: bool = True,
    headless: bool = True,
    timeout: int = 30000
) -> SecurityReport:
    """
    Scrape dynamic web content using Playwright (for JS-heavy sites).
    
    Note: Requires playwright to be installed: pip install playwright && playwright install
    
    Args:
        url: Target URL to scrape
        contact_email: Contact email for ethical identification
        respect_robots: Whether to respect robots.txt
        headless: Run browser in headless mode
        timeout: Page load timeout in milliseconds
    
    Returns:
        SecurityReport object containing extracted information
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("playwright_not_installed")
        return SecurityReport(
            url=url,
            status_code=0,
            error="Playwright not installed. Run: pip install playwright && playwright install"
        )
    
    # Check robots.txt compliance
    if respect_robots and not is_allowed_by_robots(url):
        logger.warning("scraping_blocked", url=url, reason="robots.txt")
        return SecurityReport(
            url=url,
            status_code=0,
            error="Disallowed by robots.txt"
        )
    
    # Ethical delay before request
    ethical_delay()
    
    try:
        with sync_playwright() as p:
            logger.info("launching_browser", url=url, headless=headless)
            
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                user_agent=f"EthicalCyberScraper/1.0 (Lincoln Commercial Solutions; {contact_email})",
                viewport={"width": 1280, "height": 800},
                locale="en-US",
            )
            
            page = context.new_page()
            
            # Navigate to page
            response = page.goto(url, wait_until="networkidle", timeout=timeout)
            
            if not response:
                browser.close()
                return SecurityReport(
                    url=url,
                    status_code=0,
                    error="Failed to load page"
                )
            
            # Get rendered content
            content = page.content()
            soup = BeautifulSoup(content, 'lxml')
            
            # Extract basic data (similar to static scraping)
            data = {
                "url": url,
                "status_code": response.status,
                "timestamp": datetime.now(),
                "title": page.title(),
            }
            
            # Get security headers from response
            headers = response.headers
            data["security_headers"] = identify_security_headers(headers)
            data["missing_important_headers"] = get_missing_headers(headers)
            
            # Extract metadata
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                data["meta_description"] = meta_desc['content']
            
            # Detect JS frameworks using page evaluation
            js_frameworks = []
            
            # Check for React
            if page.evaluate("() => !!window.React || !!window.__REACT_"):
                js_frameworks.append("React")
            
            # Check for Vue
            if page.evaluate("() => !!window.Vue || !!window.__VUE__"):
                js_frameworks.append("Vue")
            
            # Check for Angular
            if page.evaluate("() => !!window.angular || !!window.getAllAngularRootElements"):
                js_frameworks.append("Angular")
            
            # Check for jQuery
            if page.evaluate("() => !!window.jQuery || !!window.$"):
                js_frameworks.append("jQuery")
            
            data["js_framework_hints"] = js_frameworks
            
            # Other extractions
            generator = soup.find('meta', attrs={'name': 'generator'})
            if generator and generator.get('content'):
                data["generator"] = generator['content']
            
            data["extracted_emails"] = _extract_emails(soup)
            
            # Extract and categorize links
            links = soup.find_all('a', href=True)
            internal, external = _categorize_links(url, links)
            data["internal_links"] = list(set(internal))  # Remove duplicates
            data["external_links"] = list(set(external))  # Remove duplicates
            data["internal_links_count"] = len(data["internal_links"])
            data["external_links_count"] = len(data["external_links"])
            
            # Check security.txt
            security_txt_present, security_txt_url = _check_security_txt(url)
            data["has_security_txt"] = security_txt_present
            data["security_txt_url"] = security_txt_url
            
            data["ssl_verified"] = True
            
            browser.close()
            
            logger.info("dynamic_scraping_successful", url=url)
            return SecurityReport(**data)
            
    except Exception as e:
        logger.error("dynamic_scraping_error", url=url, error=str(e))
        return SecurityReport(
            url=url,
            status_code=0,
            error=f"Playwright error: {str(e)}"
        )
