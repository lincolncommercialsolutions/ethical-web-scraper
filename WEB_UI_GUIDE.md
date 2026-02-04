# 🌐 Web UI Quick Start Guide

## 🚀 Launch the Web Interface

### Option 1: Using the Launch Script (Easiest)
```bash
./run_ui.sh
```

### Option 2: Manual Launch
```bash
# Make sure you're in the project directory
cd /home/linkl0n/web-scrape

# Activate virtual environment (if not already active)
source venv/bin/activate

# Run Streamlit
streamlit run app.py
```

## 🌐 Access the Application

Once launched, the web UI will be available at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.1.143:8501

The application will automatically open in your default browser.

## 🎯 Using the Web UI

### 1. **Configure Settings (Left Sidebar)**
   - Choose scraping mode (Static or Dynamic)
   - Enter your contact email
   - Toggle robots.txt compliance
   - Adjust timeout and retry settings

### 2. **Enter Target URL**
   - Type or paste the URL you want to scan
   - Use quick test buttons for safe examples:
     - 🧪 Example.com
     - 🔧 HTTPBin
     - 🌐 Mozilla

### 3. **Start Scan**
   - Click "🔍 Start Scan" button
   - Watch the progress bar
   - Results appear automatically

### 4. **View Results**
   Navigate through tabs:
   - **📋 Overview** - Basic page information
   - **🔒 Security** - Security headers and analysis
   - **🖥️ Technology** - Tech stack detection
   - **🔗 Links** - Link analysis
   - **📄 Raw JSON** - Full report with download option

### 5. **Download Reports**
   - Go to the "Raw JSON" tab
   - Click "⬇️ Download JSON Report"
   - File saves with timestamp

## 🎨 Features

### Dashboard Highlights
✅ **Real-time scanning** with progress indicators  
✅ **Interactive results** with expandable sections  
✅ **Visual metrics** for quick insights  
✅ **Color-coded warnings** for missing security headers  
✅ **One-click report downloads**  
✅ **Dark/Light mode** support  

### Configuration Options
- **Scraping Mode**: Static (fast) or Dynamic (JavaScript support)
- **Ethics Settings**: robots.txt compliance toggle
- **Advanced Settings**: Timeout, retries, log level
- **Quick Presets**: Pre-configured safe test targets

## 📊 Understanding the Results

### Status Indicators
- **✅ Green** - Present and valid
- **❌ Red** - Missing or invalid
- **⚠️ Yellow** - Warning or caution

### Key Metrics
1. **Status Code** - HTTP response code
2. **Security Headers** - Count of security headers found
3. **Missing Headers** - Count of important missing headers
4. **External Links** - Number of outbound links
5. **SSL/TLS** - Certificate validation status

### Critical Alerts
- **🚨 Red Alert**: Critical security headers missing
- **⚠️ Warning**: Important headers missing
- **✅ Success**: All security measures in place

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where Streamlit is running.

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Can't Access from Browser
1. Check if the server is running
2. Try `http://localhost:8501` directly
3. Check firewall settings
4. Ensure virtual environment is activated

### UI Not Loading
```bash
# Restart Streamlit
# Press Ctrl+C to stop
# Then run again
streamlit run app.py
```

### Missing Dependencies
```bash
pip install streamlit pandas
```

## 📱 Browser Compatibility

The web UI works best with:
- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## 💡 Tips

1. **Use Static Mode** for most sites (faster)
2. **Enable Dynamic Mode** only for JavaScript-heavy sites
3. **Keep robots.txt enabled** for ethical scanning
4. **Download reports** for later analysis
5. **Test with Example.com** first to verify setup

## 🎯 Example Workflow

1. Launch UI: `./run_ui.sh`
2. Click "🧪 Example.com" for quick test
3. Click "🔍 Start Scan"
4. Wait 5-10 seconds
5. Explore results in tabs
6. Download JSON report if needed
7. Try your own URLs!

## ⚠️ Ethical Reminder

**Only scan websites you own or have permission to test!**

The UI makes scanning easy, but you're still responsible for:
- Respecting robots.txt
- Following site Terms of Service
- Complying with all applicable laws
- Using delays to avoid server overload

## 🆘 Need Help?

**CLI Alternative**: If the UI has issues, use the command-line tool:
```bash
python main.py https://example.com
```

**Check Logs**: Look in the `logs/` directory for detailed execution logs

**Test Installation**: Run the test script:
```bash
python test_scraper.py
```

---

**Enjoy your ethical web scraping! 🔒**
