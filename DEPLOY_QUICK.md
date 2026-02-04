# Quick Deployment Guide

## 🚀 Deployment Options

### 1. **Local Production (systemd service)**
```bash
sudo ./deploy.sh
```
Then access at `http://localhost:8501`

**Manage service:**
```bash
sudo systemctl status web-scraper    # Check status
sudo systemctl restart web-scraper   # Restart
sudo journalctl -u web-scraper -f    # View logs
```

---

### 2. **Docker (Recommended for isolation)**
```bash
docker-compose up -d
```
Access at `http://localhost:8501`

**Manage container:**
```bash
docker-compose logs -f        # View logs
docker-compose restart        # Restart
docker-compose down           # Stop
```

---

### 3. **Background Process (Current)**
Already running! Your current setup:
```bash
nohup streamlit run app.py --server.port 8501 --server.headless true > /dev/null 2>&1 &
```

**Manage:**
```bash
pkill -f streamlit                                    # Stop
nohup streamlit run app.py ... > /dev/null 2>&1 &   # Start
```

---

### 4. **Cloud VPS (DigitalOcean, AWS, Linode)**

**SSH into server:**
```bash
ssh root@YOUR_SERVER_IP
```

**Clone and setup:**
```bash
cd /opt
git clone https://github.com/lincolncommercialsolutions/ethical-web-scraper.git
cd ethical-web-scraper
./setup.sh
sudo ./deploy.sh
```

**Set up firewall:**
```bash
ufw allow 22/tcp
ufw allow 8501/tcp
ufw enable
```

Access at `http://YOUR_SERVER_IP:8501`

---

### 5. **Streamlit Cloud (Free, Easy)**

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select: `lincolncommercialsolutions/ethical-web-scraper`
5. Main file: `app.py`
6. Deploy!

**Note:** Playwright may not work on Streamlit Cloud. Use static mode only.

---

### 6. **Railway (Free $5/month credit)**

1. Go to https://railway.app
2. Deploy from GitHub repo
3. Set start command:
   ```
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
4. Deploy and access via Railway URL

---

## 🔒 Production Checklist

- [ ] Enable HTTPS/SSL
- [ ] Set up authentication
- [ ] Configure firewall
- [ ] Enable rate limiting
- [ ] Set up monitoring/logs
- [ ] Use environment variables for secrets
- [ ] Regular backups of output/

---

## 📖 Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

**Current Status:** ✅ Running locally at http://localhost:8501
