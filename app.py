#!/usr/bin/env python3
"""
ScrapyScrape - Web UI

A Streamlit-based web interface for web scraping.
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

from scraper import scrape_static, scrape_dynamic, SecurityReport
from scraper.utils import save_report, sanitize_url, logger

# Check if Playwright is available
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False


# Page configuration
st.set_page_config(
    page_title="ScrapyScrape",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">ScrapyScrape</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Web Scraping & Analysis Tool</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    st.markdown("---")
    
    # Scraping mode
    scraping_modes = ["Static (Fast)"]
    if PLAYWRIGHT_AVAILABLE:
        scraping_modes.append("Dynamic (JavaScript)")
    else:
        st.warning("Dynamic mode unavailable - Playwright not installed")
    
    mode = st.radio(
        "Scraping Mode",
        scraping_modes,
        help="Static mode is faster. Use Dynamic for JavaScript-heavy sites."
    )
    use_dynamic = mode == "Dynamic (JavaScript)" and PLAYWRIGHT_AVAILABLE
    
    st.markdown("---")
    
    # Ethics settings
    st.subheader("Ethics Settings")
    respect_robots = st.checkbox("Respect robots.txt", value=False, help="Uncheck to override robots.txt (use only with permission)")
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        timeout = st.slider("Timeout (seconds)", 5, 60, 15)
        max_retries = st.slider("Max Retries", 1, 10, 3)
        log_level = st.selectbox("Log Level", ["INFO", "DEBUG", "WARNING", "ERROR"])
    
    st.markdown("---")
    
    # Ethical reminder
    st.info("Only scan sites you own or have permission to test.")
    
    # Stats
    output_dir = Path("output")
    if output_dir.exists():
        report_count = len(list(output_dir.glob("*.json")))
        st.metric("Reports Generated", report_count)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Target Configuration")
    
    # URL input
    url = st.text_input(
        "Target URL",
        placeholder="https://example.com",
        help="Enter the URL you want to scan"
    )
    
    # Quick presets
    st.caption("Quick Test:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("Example.com"):
            url = "https://example.com"
            st.rerun()
    with col_b:
        if st.button("HTTPBin"):
            url = "https://httpbin.org/html"
            st.rerun()
    with col_c:
        if st.button("Mozilla"):
            url = "https://www.mozilla.org"
            st.rerun()

with col2:
    st.header("Actions")
    
    scan_button = st.button("Start Scan", type="primary", use_container_width=True)
    
    if st.button("Clear Results", use_container_width=True):
        if 'report' in st.session_state:
            del st.session_state.report
        st.rerun()

st.markdown("---")

# Scan execution
if scan_button:
    if not url:
        st.error("Please enter a URL to scan")
    else:
        # Sanitize URL
        url = sanitize_url(url)
        
        with st.spinner(f"Scanning {url}..."):
            try:
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Checking robots.txt...")
                progress_bar.progress(20)
                
                status_text.text("Fetching page...")
                progress_bar.progress(40)
                
                # Perform scraping
                if use_dynamic:
                    status_text.text("Launching browser...")
                    progress_bar.progress(60)
                    report = scrape_dynamic(
                        url=url,
                        contact_email="scraper@example.com",
                        respect_robots=respect_robots,
                        timeout=timeout * 1000
                    )
                else:
                    progress_bar.progress(60)
                    report = scrape_static(
                        url=url,
                        contact_email="scraper@example.com",
                        respect_robots=respect_robots,
                        max_retries=max_retries,
                        timeout=timeout
                    )
                
                status_text.text("Analyzing results...")
                progress_bar.progress(80)
                
                # Save report
                report_dict = report.to_dict()
                save_report(report_dict, output_dir="output")
                
                progress_bar.progress(100)
                status_text.text("Scan complete!")
                
                # Store in session state
                st.session_state.report = report
                st.session_state.report_dict = report_dict
                st.session_state.url = url
                
                st.success("Scan completed successfully!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error("ui_scan_error", error=str(e), url=url)

# Display results
if 'report' in st.session_state:
    report = st.session_state.report
    report_dict = st.session_state.report_dict
    
    st.header("Scan Results")
    
    # Error check
    if report.error:
        st.markdown(f'<div class="error-box"><strong>Error:</strong> {report.error}</div>', unsafe_allow_html=True)
    else:
        # Summary metrics - Expanded
        st.subheader("Quick Summary")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Status Code", report.status_code)
        with col2:
            st.metric("Security Headers", len(report.security_headers))
        with col3:
            st.metric("Missing Headers", len(report.missing_important_headers))
        with col4:
            st.metric("Internal Links", report.internal_links_count)
        with col5:
            st.metric("External Links", report.external_links_count)
        with col6:
            ssl_status = "Valid" if report.ssl_verified else "Invalid"
            st.metric("SSL/TLS", ssl_status)
        
        # Critical findings alert
        if report.has_critical_missing_headers():
            st.markdown('<div class="warning-box"><strong>Warning:</strong> Critical security headers are missing!</div>', unsafe_allow_html=True)
        
        # Complete Information Display
        st.markdown("---")
        
        # All Information in One View
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Page Information
            st.subheader("Page Information")
            st.write(f"**URL:** {report.url}")
            st.write(f"**Title:** {report.title or 'N/A'}")
            st.write(f"**Status Code:** {report.status_code}")
            if report.meta_description:
                st.write(f"**Description:** {report.meta_description}")
            st.write(f"**Scan Time:** {report.timestamp}")
            
            st.markdown("---")
            
            # Server & Technology
            st.subheader("Server & Technology")
            st.write(f"**Server:** {report.server or 'Not disclosed'}")
            st.write(f"**Powered By:** {report.powered_by or 'Not disclosed'}")
            st.write(f"**Generator:** {report.generator or 'Not detected'}")
            
            if report.js_framework_hints:
                st.write("**JavaScript Frameworks:**")
                for framework in report.js_framework_hints:
                    st.write(f"  • {framework}")
            else:
                st.write("**JavaScript Frameworks:** None detected")
            
            st.markdown("---")
            
            # SSL/TLS Information
            st.subheader("SSL/TLS Information")
            if report.ssl_verified:
                st.success("Certificate Valid")
                if report.ssl_issuer:
                    st.write(f"**Issuer:** {report.ssl_issuer}")
            else:
                st.error("Certificate Verification Failed")
            
            st.markdown("---")
            
            # Links & Content
            st.subheader("Links Analysis")
            st.write(f"**Internal Links:** {report.internal_links_count}")
            st.write(f"**External Links:** {report.external_links_count}")
            
            if report.extracted_emails:
                st.write("**Extracted Emails:**")
                for email in report.extracted_emails:
                    st.write(f"  • {email}")
            
            st.markdown("---")
            
            # Security.txt
            st.subheader("Security.txt")
            if report.has_security_txt:
                st.success(f"Found at: {report.security_txt_url}")
            else:
                st.warning("Not found")
        
        with col_right:
            # Security Headers - Complete List
            st.subheader("Security Headers")
            
            if report.security_headers:
                st.write("**Present Headers:**")
                for header, value in report.security_headers.items():
                    with st.expander(header, expanded=False):
                        st.code(value, language="text")
            else:
                st.warning("No security headers found")
            
            st.markdown("---")
            
            # Missing Headers
            st.write("**Missing Important Headers:**")
            if report.missing_important_headers:
                for header in report.missing_important_headers:
                    st.write(f"  - {header}")
            else:
                st.success("All important headers present!")
            
            st.markdown("---")
            
            # Security Recommendations
            st.subheader("Security Recommendations")
            if report.has_critical_missing_headers():
                st.error("CRITICAL: Important security headers are missing!")
                st.write("**Recommended Actions:**")
                if "Content-Security-Policy" in report.missing_important_headers:
                    st.write("- Implement Content-Security-Policy to prevent XSS attacks")
                if "Strict-Transport-Security" in report.missing_important_headers:
                    st.write("- Add Strict-Transport-Security (HSTS) to enforce HTTPS")
                if "X-Frame-Options" in report.missing_important_headers:
                    st.write("- Set X-Frame-Options to prevent clickjacking")
                if "X-Content-Type-Options" in report.missing_important_headers:
                    st.write("- Add X-Content-Type-Options to prevent MIME sniffing")
            else:
                st.success("Security posture looks good!")
            
            st.markdown("---")
            
            # Additional Findings
            st.subheader("Additional Findings")
            findings = []
            
            if not report.has_security_txt:
                findings.append("- No security.txt file - Consider adding one for vulnerability disclosure")
            
            if report.server:
                findings.append(f"- Server type disclosed: {report.server}")
            
            if report.generator:
                findings.append(f"- CMS/Generator disclosed: {report.generator}")
            
            if not report.js_framework_hints:
                findings.append("- No JavaScript frameworks detected (or static site)")
            
            if findings:
                for finding in findings:
                    st.write(finding)
            else:
                st.write("No additional findings")
        
        st.markdown("---")
        
        # Links Display Section
        st.header("All Links Found")
        
        tab_internal, tab_external = st.tabs([f"Internal Links ({report.internal_links_count})", f"External Links ({report.external_links_count})"])
        
        with tab_internal:
            if report.internal_links:
                st.write(f"Found **{report.internal_links_count}** internal links:")
                
                # Create DataFrame for better display
                df_internal = pd.DataFrame({"URL": sorted(report.internal_links)})
                df_internal.index = range(1, len(df_internal) + 1)
                
                # Display as table with clickable links
                st.dataframe(df_internal, use_container_width=True, height=400)
                
                # Download button
                csv_internal = df_internal.to_csv(index=False)
                st.download_button(
                    label="Download Internal Links CSV",
                    data=csv_internal,
                    file_name=f"internal_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No internal links found")
        
        with tab_external:
            if report.external_links:
                st.write(f"Found **{report.external_links_count}** external links:")
                
                # Create DataFrame for better display
                df_external = pd.DataFrame({"URL": sorted(report.external_links)})
                df_external.index = range(1, len(df_external) + 1)
                
                # Display as table
                st.dataframe(df_external, use_container_width=True, height=400)
                
                # Download button
                csv_external = df_external.to_csv(index=False)
                st.download_button(
                    label="Download External Links CSV",
                    data=csv_external,
                    file_name=f"external_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No external links found")
        
        st.markdown("---")
        
        # Tabs for downloads
        tab1, tab2 = st.tabs(["Raw JSON", "Downloads"])
        
        with tab1:
            st.subheader("Complete JSON Report")
            st.json(report_dict)
        
        with tab2:
            st.subheader("Download Reports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                json_str = json.dumps(report_dict, indent=2, default=str)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                st.info(f"Report also saved to:\n`output/report_*.json`")

# Footer
st.markdown("---")
st.caption("ScrapyScrape - Web Scraping Tool")
