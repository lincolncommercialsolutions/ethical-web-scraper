#!/bin/bash
# Setup script for Ethical Web Scraper

echo "======================================================================"
echo "ETHICAL WEB SCRAPER - SETUP"
echo "Lincoln Commercial Solutions Cybersecurity Project"
echo "======================================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "======================================================================"
echo "SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "To activate the environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To test the installation:"
echo "  python test_scraper.py"
echo ""
echo "To use the scraper:"
echo "  python main.py https://example.com"
echo ""
echo "For dynamic scraping (optional), install Playwright:"
echo "  pip install playwright"
echo "  playwright install chromium"
echo ""
echo "For help:"
echo "  python main.py --help"
echo ""
