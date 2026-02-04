# Deployment Guide

This guide covers multiple deployment options for the Ethical Web Scraper.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Cloud VPS Deployment](#cloud-vps-deployment)
3. [Streamlit Cloud (Free)](#streamlit-cloud-deployment)
4. [Railway Deployment](#railway-deployment)
5. [Security Considerations](#security-considerations)

---

## Docker Deployment

### 1. Create Dockerfile

The project includes a Dockerfile for containerized deployment.

**Build the image:**
```bash
docker build -t ethical-web-scraper .
```

**Run the container:**
```bash
docker run -d -p 8501:8501 --name web-scraper ethical-web-scraper
```

**Access the app:**
```
http://localhost:8501
```

**Stop the container:**
```bash
docker stop web-scraper
docker rm web-scraper
```

### 2. Docker Compose (Recommended)

**docker-compose.yml** is included for easier management.

**Start:**
```bash
docker-compose up -d
```

**Stop:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

---

## Cloud VPS Deployment

Deploy on DigitalOcean, AWS EC2, Linode, or any Linux VPS.

### Step 1: Set Up Server

**SSH into your server:**
```bash
ssh root@your-server-ip
```

**Update system:**
```bash
apt update && apt upgrade -y
```

**Install Python and dependencies:**
```bash
apt install -y python3 python3-pip python3-venv git
```

### Step 2: Clone Project

```bash
cd /opt
git clone https://github.com/lincolncommercialsolutions/ethical-web-scraper.git
cd ethical-web-scraper
```

### Step 3: Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### Step 4: Run with systemd (Production)

**Create service file:**
```bash
nano /etc/systemd/system/web-scraper.service
```

**Add this content:**
```ini
[Unit]
Description=Ethical Web Scraper - Streamlit App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ethical-web-scraper
Environment="PATH=/opt/ethical-web-scraper/venv/bin"
ExecStart=/opt/ethical-web-scraper/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
systemctl daemon-reload
systemctl enable web-scraper
systemctl start web-scraper
systemctl status web-scraper
```

**View logs:**
```bash
journalctl -u web-scraper -f
```

### Step 5: Set Up Nginx Reverse Proxy (Optional)

**Install Nginx:**
```bash
apt install -y nginx
```

**Create config:**
```bash
nano /etc/nginx/sites-available/web-scraper
```

**Add this:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**
```bash
ln -s /etc/nginx/sites-available/web-scraper /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 6: SSL with Let's Encrypt (Optional)

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

---

## Streamlit Cloud Deployment

**Easiest option** - Free hosting for Streamlit apps.

### Requirements:
- GitHub account
- Public GitHub repository

### Steps:

1. **Push your code to GitHub** (already done):
   ```
   https://github.com/lincolncommercialsolutions/ethical-web-scraper
   ```

2. **Go to Streamlit Cloud:**
   ```
   https://streamlit.io/cloud
   ```

3. **Sign in with GitHub**

4. **Deploy new app:**
   - Click "New app"
   - Select your repository: `lincolncommercialsolutions/ethical-web-scraper`
   - Main file: `app.py`
   - Click "Deploy"

5. **Wait 2-3 minutes** for deployment

6. **Access your app:**
   ```
   https://your-app-name.streamlit.app
   ```

### Note:
Streamlit Cloud may have issues with Playwright. For dynamic scraping, use Docker or VPS deployment.

---

## Railway Deployment

Railway offers free tier with $5 monthly credit.

### Steps:

1. **Go to Railway:**
   ```
   https://railway.app
   ```

2. **Sign in with GitHub**

3. **New Project > Deploy from GitHub repo**

4. **Select:** `lincolncommercialsolutions/ethical-web-scraper`

5. **Add start command in settings:**
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

6. **Set environment variables (if needed):**
   ```
   PYTHONUNBUFFERED=1
   ```

7. **Deploy and wait**

8. **Access your app** via Railway's generated URL

---

## Security Considerations

### For Public Deployment:

1. **Add Authentication:**
   ```bash
   pip install streamlit-authenticator
   ```

2. **Rate Limiting:**
   - Use Nginx rate limiting
   - Add Python-based throttling

3. **Firewall Rules:**
   ```bash
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

4. **Environment Variables:**
   - Store sensitive config in `.env` files
   - Never commit API keys to Git

5. **HTTPS Only:**
   - Always use SSL/TLS in production
   - Redirect HTTP to HTTPS

6. **Monitoring:**
   - Set up log monitoring
   - Configure alerts for errors

### For Private Use:

1. **VPN Access Only:**
   - Deploy on private network
   - Use VPN or SSH tunnel

2. **SSH Tunnel:**
   ```bash
   ssh -L 8501:localhost:8501 user@server-ip
   ```
   Then access: `http://localhost:8501`

---

## Quick Deployment Commands

### Local Production (using systemd)
```bash
# Create service file
sudo cp deployment/web-scraper.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable web-scraper
sudo systemctl start web-scraper
```

### Docker Quick Start
```bash
docker build -t ethical-web-scraper .
docker run -d -p 8501:8501 --name scraper ethical-web-scraper
```

### Simple Background Process (Current Method)
```bash
nohup streamlit run app.py --server.port 8501 --server.headless true > app.log 2>&1 &
```

---

## Updating Deployed App

### VPS with systemd:
```bash
cd /opt/ethical-web-scraper
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart web-scraper
```

### Docker:
```bash
docker-compose down
git pull
docker-compose build
docker-compose up -d
```

### Streamlit Cloud:
- Push changes to GitHub
- Streamlit Cloud auto-deploys

---

## Troubleshooting

### Port Already in Use:
```bash
# Find process
sudo lsof -i :8501

# Kill process
sudo kill -9 <PID>
```

### Playwright Not Working:
```bash
playwright install chromium
playwright install-deps
```

### Permission Denied:
```bash
chmod +x setup.sh run_ui.sh
```

### Service Won't Start:
```bash
# Check logs
journalctl -u web-scraper -n 50

# Check status
systemctl status web-scraper
```

---

## Recommended Deployment Path

**For Testing:** Local with nohup (current setup)
**For Development:** Docker Compose
**For Production (Public):** VPS with systemd + Nginx + SSL
**For Quick Demo:** Streamlit Cloud (static mode only)
**For Scalability:** Docker + Kubernetes or AWS ECS

---

## Support

For deployment issues, check:
- GitHub Issues: https://github.com/lincolncommercialsolutions/ethical-web-scraper/issues
- Project README: [README.md](README.md)

---

**Last Updated:** February 4, 2026
**Maintained by:** Lincoln Commercial Solutions
