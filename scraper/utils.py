"""
Utility functions for headers, logging, and helper operations.
"""

import logging
import structlog
from typing import Dict
import json
from pathlib import Path
from datetime import datetime


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def get_headers(contact_email: str = "security-research@lincolncommercial.com") -> Dict[str, str]:
    """
    Generate ethical scraper headers with clear identification.
    
    Args:
        contact_email: Contact email for the scraper operator
    
    Returns:
        Dictionary of HTTP headers
    """
    return {
        "User-Agent": f"EthicalCyberScraper/1.0 (Lincoln Commercial Solutions Cybersecurity Project; {contact_email})",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",  # Do Not Track
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def setup_file_logging(log_dir: str = "logs", log_level: str = "INFO"):
    """
    Setup file-based logging for audit trails.
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"scraper_{timestamp}.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger.info("file_logging_setup", log_file=str(log_file), level=log_level)


def save_report(report: dict, output_dir: str = "output", filename: str = None):
    """
    Save a security report to a JSON file.
    
    Args:
        report: Report dictionary to save
        output_dir: Output directory
        filename: Optional custom filename (auto-generated if not provided)
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize URL for filename
        url = report.get('url', 'unknown')
        sanitized = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        filename = f"report_{sanitized}_{timestamp}.json"
    
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    logger.info("report_saved", filepath=str(filepath), url=report.get('url'))
    return str(filepath)


def identify_security_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Extract security-relevant headers from response headers.
    
    Args:
        headers: Response headers dictionary
    
    Returns:
        Dictionary of security headers
    """
    important_headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
        "Referrer-Policy",
        "Permissions-Policy",
        "Cross-Origin-Embedder-Policy",
        "Cross-Origin-Opener-Policy",
        "Cross-Origin-Resource-Policy",
    ]
    
    security_headers = {}
    for header in important_headers:
        # Case-insensitive search
        for key, value in headers.items():
            if key.lower() == header.lower():
                security_headers[header] = value
                break
    
    return security_headers


def get_missing_headers(headers: Dict[str, str]) -> list:
    """
    Identify important security headers that are missing.
    
    Args:
        headers: Response headers dictionary
    
    Returns:
        List of missing header names
    """
    important = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
    ]
    
    present = {k.lower() for k in headers.keys()}
    missing = [h for h in important if h.lower() not in present]
    
    return missing


def sanitize_url(url: str) -> str:
    """
    Sanitize and validate URL input.
    
    Args:
        url: URL to sanitize
    
    Returns:
        Sanitized URL
    """
    url = url.strip()
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url
