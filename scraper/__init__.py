"""
Ethical Web Scraper for Cybersecurity Projects
Lincoln Commercial Solutions - 2026

This module provides ethical web scraping capabilities for security research,
OSINT analysis, and cybersecurity development projects.
"""

__version__ = "1.0.0"
__author__ = "Lincoln Commercial Solutions"

from .core import scrape_static, scrape_dynamic
from .models import SecurityReport
from .ethics import is_allowed_by_robots, ethical_delay
from .utils import get_headers, logger

__all__ = [
    "scrape_static",
    "scrape_dynamic",
    "SecurityReport",
    "is_allowed_by_robots",
    "ethical_delay",
    "get_headers",
    "logger",
]
