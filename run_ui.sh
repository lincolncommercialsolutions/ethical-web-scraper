#!/bin/bash
# Run the Ethical Web Scraper Web UI

echo "======================================================================"
echo "🔒 ETHICAL WEB SCRAPER - WEB UI"
echo "Lincoln Commercial Solutions - Cybersecurity Project"
echo "======================================================================"
echo ""
echo "Starting web interface..."
echo ""
echo "The application will open in your browser automatically."
echo "If not, navigate to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "======================================================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Streamlit
streamlit run app.py --server.port 8501 --server.address localhost
