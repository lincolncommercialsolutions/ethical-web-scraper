#!/usr/bin/env python3
"""
Install Playwright browsers during Streamlit Cloud deployment
"""
import subprocess
import sys

try:
    print("Installing Playwright browsers...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install-deps", "chromium"])
    print("Playwright installation complete!")
except Exception as e:
    print(f"Warning: Playwright installation failed: {e}")
    print("Dynamic scraping will not be available.")
