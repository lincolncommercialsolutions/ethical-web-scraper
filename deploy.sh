#!/bin/bash

# Deployment script for Ethical Web Scraper
# This script sets up the application as a systemd service

set -e

echo "🚀 Deploying Ethical Web Scraper..."

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)" 
   exit 1
fi

# Variables
APP_DIR="/home/linkl0n/web-scrape"
SERVICE_FILE="web-scraper.service"
VENV_PATH="/home/linkl0n/venv"
USER="linkl0n"

echo "📁 Application directory: $APP_DIR"
echo "👤 Running as user: $USER"

# Check if directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "❌ Application directory not found: $APP_DIR"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found: $VENV_PATH"
    echo "💡 Run setup.sh first to create the environment"
    exit 1
fi

# Copy service file
echo "📝 Installing systemd service..."
cp "$APP_DIR/$SERVICE_FILE" /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

# Enable service
echo "✅ Enabling web-scraper service..."
systemctl enable web-scraper

# Start service
echo "▶️  Starting web-scraper service..."
systemctl start web-scraper

# Wait a moment
sleep 2

# Check status
echo ""
echo "📊 Service Status:"
systemctl status web-scraper --no-pager

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📌 Useful commands:"
echo "  • View status:  sudo systemctl status web-scraper"
echo "  • View logs:    sudo journalctl -u web-scraper -f"
echo "  • Restart:      sudo systemctl restart web-scraper"
echo "  • Stop:         sudo systemctl stop web-scraper"
echo "  • Disable:      sudo systemctl disable web-scraper"
echo ""
echo "🌐 Access the app at: http://localhost:8501"
echo "   (or http://YOUR_SERVER_IP:8501 if on a VPS)"
