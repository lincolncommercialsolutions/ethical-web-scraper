#!/usr/bin/env python3
"""
Quick test script to verify the scraper installation and functionality.
"""

import sys
from scraper import scrape_static, SecurityReport
from scraper.utils import logger

def test_basic_functionality():
    """Test basic scraping functionality with a safe target."""
    print("=" * 70)
    print("ETHICAL WEB SCRAPER - QUICK TEST")
    print("=" * 70)
    print("\nTesting basic functionality with example.com...")
    print("This is a safe, public domain designed for testing.\n")
    
    try:
        # Test with a safe, public domain
        report = scrape_static(
            url="https://example.com",
            respect_robots=True,
            timeout=10
        )
        
        if report.error:
            print(f"❌ Test failed with error: {report.error}")
            return False
        
        print("✅ Successfully scraped example.com")
        print(f"   Status Code: {report.status_code}")
        print(f"   Title: {report.title}")
        print(f"   Security Headers Found: {len(report.security_headers)}")
        print(f"   Missing Headers: {len(report.missing_important_headers)}")
        
        if report.has_critical_missing_headers():
            print("\n⚠️  Note: Some critical security headers are missing (expected for example.com)")
        
        print("\n✅ All tests passed!")
        print("\nYou can now use the scraper with:")
        print("  python main.py <your-target-url>")
        print("\nFor help:")
        print("  python main.py --help")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
