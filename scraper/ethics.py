"""
Ethical scraping utilities: robots.txt compliance, rate limiting, and delays.
"""

import random
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)


def is_allowed_by_robots(url: str, user_agent: str = "EthicalCyberScraper/1.0") -> bool:
    """
    Check if a URL is allowed to be scraped according to robots.txt.
    
    Args:
        url: The target URL to check
        user_agent: The user agent string to check against
    
    Returns:
        True if scraping is allowed, False otherwise
    """
    rp = RobotFileParser()
    try:
        robots_url = urljoin(url, "/robots.txt")
        rp.set_url(robots_url)
        rp.read()
        allowed = rp.can_fetch(user_agent, url)
        
        if not allowed:
            logger.warning(f"Access to {url} disallowed by robots.txt")
        else:
            logger.info(f"Access to {url} permitted by robots.txt")
        
        return allowed
    except Exception as e:
        logger.warning(f"Could not fetch robots.txt for {url}: {e} — allowing conservatively")
        return True  # Default to allow if robots.txt is unreachable


def ethical_delay(min_sec: float = 2.5, max_sec: float = 7.0):
    """
    Introduce a randomized delay between requests to avoid overwhelming servers.
    
    Uses triangular distribution with peak in the middle for more natural behavior.
    
    Args:
        min_sec: Minimum delay in seconds
        max_sec: Maximum delay in seconds
    """
    delay = random.triangular(min_sec, (min_sec + max_sec) / 2, max_sec)
    logger.debug(f"Ethical delay: {delay:.2f} seconds")
    time.sleep(delay)


def get_crawl_delay(url: str, user_agent: str = "EthicalCyberScraper/1.0") -> float:
    """
    Get the crawl delay specified in robots.txt, if any.
    
    Args:
        url: The target URL
        user_agent: The user agent to check for
    
    Returns:
        Crawl delay in seconds, or 0 if not specified
    """
    rp = RobotFileParser()
    try:
        robots_url = urljoin(url, "/robots.txt")
        rp.set_url(robots_url)
        rp.read()
        delay = rp.crawl_delay(user_agent)
        return delay if delay else 0.0
    except Exception:
        return 0.0


def should_respect_rate_limit(response_status: int) -> bool:
    """
    Check if we should back off based on response status.
    
    Args:
        response_status: HTTP status code
    
    Returns:
        True if we should back off (429, 503, etc.)
    """
    rate_limit_codes = [429, 503, 509]  # Too Many Requests, Service Unavailable, Bandwidth Exceeded
    return response_status in rate_limit_codes


def exponential_backoff(attempt: int, base_delay: float = 2.0, max_delay: float = 60.0) -> float:
    """
    Calculate exponential backoff delay.
    
    Args:
        attempt: Current retry attempt (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay cap
    
    Returns:
        Delay in seconds
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    # Add jitter
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter
