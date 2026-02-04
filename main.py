#!/usr/bin/env python3
"""
Ethical Web Scraper CLI
Lincoln Commercial Solutions - Cybersecurity Project

A command-line interface for ethical web scraping focused on security analysis.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

from scraper import scrape_static, scrape_dynamic, SecurityReport
from scraper.utils import save_report, setup_file_logging, sanitize_url, logger


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ethical Web Scraper for Cybersecurity Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a single URL (static)
  python main.py https://example.com

  # Scrape with dynamic/JavaScript support
  python main.py https://example.com --dynamic

  # Scrape with custom contact email
  python main.py https://example.com --email your-email@example.com

  # Save to custom output file
  python main.py https://example.com --output my_report.json

  # Ignore robots.txt (use responsibly!)
  python main.py https://example.com --ignore-robots

  # Enable debug logging
  python main.py https://example.com --log-level DEBUG

For ethical use only. Respect robots.txt and rate limits.
        """
    )
    
    parser.add_argument(
        'url',
        help='Target URL to scrape'
    )
    
    parser.add_argument(
        '-d', '--dynamic',
        action='store_true',
        help='Use dynamic scraping with Playwright (for JavaScript-heavy sites)'
    )
    
    parser.add_argument(
        '-e', '--email',
        default='security-research@lincolncommercial.com',
        help='Contact email for ethical identification (default: security-research@lincolncommercial.com)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: auto-generated in output/ directory)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory (default: output/)'
    )
    
    parser.add_argument(
        '--ignore-robots',
        action='store_true',
        help='Ignore robots.txt restrictions (use responsibly!)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=15,
        help='Request timeout in seconds (default: 15)'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum retry attempts (default: 3)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--no-delay',
        action='store_true',
        help='Skip ethical delays (NOT recommended for production use)'
    )
    
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Output only JSON (no formatted display)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='EthicalCyberScraper 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_file_logging(log_level=args.log_level)
    
    # Sanitize URL
    url = sanitize_url(args.url)
    
    # Display header
    if not args.json_only:
        print("=" * 70)
        print("ETHICAL WEB SCRAPER - Lincoln Commercial Solutions")
        print("=" * 70)
        print(f"Target URL: {url}")
        print(f"Mode: {'Dynamic (Playwright)' if args.dynamic else 'Static (Requests)'}")
        print(f"Respecting robots.txt: {not args.ignore_robots}")
        print("=" * 70)
        print()
    
    # Perform scraping
    try:
        if args.dynamic:
            if not args.json_only:
                print("🚀 Launching browser for dynamic scraping...")
            
            report = scrape_dynamic(
                url=url,
                contact_email=args.email,
                respect_robots=not args.ignore_robots,
                timeout=args.timeout * 1000  # Convert to milliseconds
            )
        else:
            if not args.json_only:
                print("📡 Fetching static content...")
            
            report = scrape_static(
                url=url,
                contact_email=args.email,
                respect_robots=not args.ignore_robots,
                max_retries=args.max_retries,
                timeout=args.timeout
            )
        
        # Check for errors
        if report.error:
            if not args.json_only:
                print(f"\n❌ Error: {report.error}\n")
            logger.error("scraping_failed", url=url, error=report.error)
            sys.exit(1)
        
        # Save report
        report_dict = report.to_dict()
        output_file = save_report(
            report_dict,
            output_dir=args.output_dir,
            filename=args.output
        )
        
        # Display results
        if args.json_only:
            print(json.dumps(report_dict, indent=2, default=str))
        else:
            display_report(report)
            print(f"\n💾 Full report saved to: {output_file}")
        
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error("unexpected_error", error=str(e))
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def display_report(report: SecurityReport):
    """
    Display a formatted security report.
    
    Args:
        report: SecurityReport object to display
    """
    print("\n" + "=" * 70)
    print("SECURITY REPORT")
    print("=" * 70)
    
    # Basic info
    print(f"\n📋 Page Information:")
    print(f"   Status Code: {report.status_code}")
    print(f"   Title: {report.title or 'N/A'}")
    if report.meta_description:
        desc = report.meta_description[:100] + "..." if len(report.meta_description) > 100 else report.meta_description
        print(f"   Description: {desc}")
    
    # Server info
    if report.server or report.powered_by or report.generator:
        print(f"\n🖥️  Server & Technology:")
        if report.server:
            print(f"   Server: {report.server}")
        if report.powered_by:
            print(f"   Powered By: {report.powered_by}")
        if report.generator:
            print(f"   Generator: {report.generator}")
    
    # JavaScript frameworks
    if report.js_framework_hints:
        print(f"\n⚛️  Detected Frameworks:")
        for framework in report.js_framework_hints:
            print(f"   • {framework}")
    
    # Security headers
    print(f"\n🔒 Security Headers:")
    if report.security_headers:
        for header, value in report.security_headers.items():
            # Truncate long values
            display_value = value[:60] + "..." if len(value) > 60 else value
            print(f"   ✓ {header}: {display_value}")
    else:
        print("   ⚠️  No security headers found")
    
    # Missing headers
    if report.missing_important_headers:
        print(f"\n⚠️  Missing Important Headers:")
        for header in report.missing_important_headers:
            print(f"   ✗ {header}")
    
    # Security.txt
    print(f"\n📄 Security.txt:")
    if report.has_security_txt:
        print(f"   ✓ Found at: {report.security_txt_url}")
    else:
        print("   ✗ Not found")
    
    # SSL/TLS
    print(f"\n🔐 SSL/TLS:")
    if report.ssl_verified:
        print(f"   ✓ Certificate valid")
        if report.ssl_issuer:
            print(f"   Issuer: {report.ssl_issuer}")
    else:
        print("   ✗ Certificate verification failed")
    
    # Links
    print(f"\n🔗 Links:")
    print(f"   Internal: {report.internal_links_count}")
    print(f"   External: {report.external_links_count}")
    
    # Emails (if any)
    if report.extracted_emails:
        print(f"\n📧 Extracted Emails (use responsibly):")
        for email in report.extracted_emails[:3]:  # Limit display
            print(f"   • {email}")
        if len(report.extracted_emails) > 3:
            print(f"   ... and {len(report.extracted_emails) - 3} more")
    
    # Critical findings
    if report.has_critical_missing_headers():
        print(f"\n🚨 CRITICAL: Important security headers are missing!")
        print("   Consider implementing CSP, HSTS, or X-Frame-Options")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
