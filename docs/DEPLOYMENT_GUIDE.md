# 🚀 Deployment Guide for Telegram Gemini Bot

This guide explains how to deploy your **Telegram Gemini Bot** across different platforms: **Local**, **Render**, **Docker**, and **Kubernetes with Helm**.



---

## 🏗️ Architecture Overview

![Architecture](telegram-gemini-architecture.png)

- **Telegram User** sends text/voice → **Bot** (Python, Webhook/Polling)
- **Bot** forwards prompts → **Google Gemini API**
- **Gemini API** returns response → **Bot**
- **Bot** replies back to **Telegram User**

---

## 1️⃣ Local Development

### Prerequisites
- Python 3.9+
- FFmpeg installed (`sudo apt install ffmpeg`)

### Steps
1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/telegram-gemini-bot.git
   cd telegram-gemini-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in:
   ```env
   TELEGRAM_TOKEN=your-telegram-token
   GEMINI_API_KEY=your-gemini-api-key
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

👉 Runs in **polling mode** locally.

---

## 2️⃣ Deploy on Render

### Environment Variables (set in Render Dashboard)
```env
TELEGRAM_TOKEN=your-telegram-token
GEMINI_API_KEY=your-gemini-api-key
PORT=8443   # Render sets automatically
RENDER_EXTERNAL_HOSTNAME=your-service.onrender.com   # Render sets automatically
```

👉 Bot runs in **webhook mode** on Render.

---

## 3️⃣ Deploy with Docker

### `.env` file (used by Docker & Docker Compose)
```env
TELEGRAM_TOKEN=your-telegram-token
GEMINI_API_KEY=your-gemini-api-key
```

### Build & Run
```bash
docker build -t telegram-gemini-bot .
docker run -d --name bot --env-file .env -p 8443:8443 telegram-gemini-bot
```

### With Docker Compose
```bash
docker-compose up -d
```

---

## 4️⃣ Kubernetes Deployment

### Secrets (`k8s/secrets.yaml`)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: telegram-gemini-secrets
type: Opaque
stringData:
  TELEGRAM_TOKEN: "your-telegram-token"
  GEMINI_API_KEY: "your-gemini-api-key"
```

Apply:
```bash
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
```

---

## 5️⃣ Helm Chart Deployment

### values.yaml (env section)
```yaml
env:
  TELEGRAM_TOKEN: "your-telegram-token"
  GEMINI_API_KEY: "your-gemini-api-key"
```

### Configure Ingress + HTTPS
```yaml
ingress:
  enabled: true
  host: "your-domain.com"
  tls: true
  tlsSecret: "telegram-gemini-bot-tls"
  clusterIssuer: "letsencrypt-prod"
```

Deploy:
```bash
helm install mybot ./helm/telegram-gemini-bot
```

Upgrade after editing values:
```bash
helm upgrade mybot ./helm/telegram-gemini-bot
```

---

## 6️⃣ GitHub Actions CI/CD

### Render Deploy
Workflow: `.github/workflows/deploy.yml`  
Secrets required in GitHub repo:
```env
RENDER_SERVICE_ID=your-render-service-id
RENDER_API_KEY=your-render-api-key
```

### Docker Hub Deploy
Workflow: `.github/workflows/dockerhub.yml`  
Secrets required in GitHub repo:
```env
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password-or-token
```

---

## ✅ Summary
- **Local** → `.env` file for TELEGRAM_TOKEN + GEMINI_API_KEY
- **Render** → Add variables in dashboard (PORT + HOSTNAME auto-set)
- **Docker** → `.env` file used in container
- **Kubernetes** → Secrets manifest
- **Helm** → Values.yaml manages env + ingress
- **GitHub Actions** → Repo secrets for Render & Docker Hub



[🔝 Back to top](#)
