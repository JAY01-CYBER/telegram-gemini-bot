<p align="center">
  <img src="https://raw.githubusercontent.com/JAY01-CYBER/telegram-gemini-bot/main/assets/logo.png" alt="Telegram Gemini Bot Logo" width="200"/>
</p>


# 🤖 Telegram Gemini Bot

[![CI](https://github.com/JAY01-CYBER/telegram-gemini-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/JAY01-CYBER/telegram-gemini-bot/actions/workflows/ci.yml)
[![Roadmap](https://img.shields.io/badge/docs-roadmap-blue?style=flat&logo=github)](ROADMAP.md)
[![Security Scan](https://github.com/JAY01-CYBER/telegram-gemini-bot/actions/workflows/security.yml/badge.svg)](https://github.com/JAY01-CYBER/telegram-gemini-bot/actions/workflows/security.yml)
[![Docs](https://github.com/JAY01-CYBER/telegram-gemini-bot/actions/workflows/docs.yml/badge.svg)](https://JAY01-CYBER.github.io/telegram-gemini-bot/)
[![codecov](https://codecov.io/gh/JAY01-CYBER/telegram-gemini-bot/branch/main/graph/badge.svg)](https://codecov.io/gh/JAY01-CYBER/telegram-gemini-bot)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/JAY01-CYBER/telegram-gemini-bot/network/updates)

[![Docker Pulls](https://img.shields.io/docker/pulls/JAY01-CYBER/telegram-gemini-bot)](https://hub.docker.com/r/JAY01-CYBER/telegram-gemini-bot)
![GitHub Repo stars](https://img.shields.io/github/stars/JAY01-CYBER/telegram-gemini-bot)
![GitHub forks](https://img.shields.io/github/forks/JAY01-CYBER/telegram-gemini-bot)
![GitHub issues](https://img.shields.io/github/issues/JAY01-CYBER/telegram-gemini-bot)
![GitHub last commit](https://img.shields.io/github/last-commit/JAY01-CYBER/telegram-gemini-bot)

[![License](https://img.shields.io/github/license/JAY01-CYBER/telegram-gemini-bot)](LICENSE)


[![codecov](https://codecov.io/gh/JAY01-CYBER/telegram-gemini-bot/branch/main/graph/badge.svg)](https://codecov.io/gh/JAY01-CYBER/telegram-gemini-bot)

# 🤖 Telegram Gemini AI Bot

A Telegram bot powered by **python-telegram-bot v20** and **Google Gemini (gemini-pro)**, deployable on **Render**.

---

## 🚀 Features
- **Gemini integration** (`gemini-pro` model)
- **Streaming-like responses** (edits message while typing)
- **Voice message transcription** → AI reply
- **Typing indicator** while generating
- **Short-term memory** (last 10 messages per user)
- **/reset command** to clear conversation
- **Rate limiting** (5s cooldown per user, prevents spam)
- **Auto-switch**:
  - **Polling** when run locally
  - **Webhook** when deployed on Render

---

## 📦 Requirements

- Python 3.9+
- Dependencies in `requirements.txt`

---

## 🖥️ Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export TELEGRAM_TOKEN=your-telegram-bot-token
   export GEMINI_API_KEY=your-gemini-api-key
   ```

3. Start the bot:
   ```bash
   python bot.py
   ```

👉 Locally the bot runs in **polling mode**.

---

## 🌐 Deploy on Render

1. Push repo to GitHub.
2. In Render, create a **New Web Service**:
   - Runtime: **Python**
   - Start command: handled by `Procfile`
3. Add environment variables in Render dashboard:
   - `TELEGRAM_TOKEN`
   - `GEMINI_API_KEY`
4. Render automatically sets:
   - `PORT`
   - `RENDER_EXTERNAL_HOSTNAME`

5. Deploy.  
👉 On Render the bot runs in **webhook mode**.

---

## 📄 Procfile

```txt
web: python bot.py
```

---

## 🛠️ Commands
- `/start` → Greet the user
- `/reset` → Clear memory for the current user

---

## 📌 Notes
- **Gemini free tier**: 60 requests/minute and a daily quota.  
- Memory is stored **in RAM** (per user). It resets when the bot restarts.  
  For persistent memory, connect a database (e.g., Redis, Postgres).

---

## 🔍 Developer Setup (Pre-commit Hooks)

This project uses [pre-commit](https://pre-commit.com/) to catch issues before committing.

### Install hooks
```bash
pip install pre-commit
pre-commit install
```

Now every `git commit` will automatically run:
- **flake8** (linting)
- **bandit** (security scan)

---

## 🐳 Dockerized Development Environment

This project ships with a **developer container** so you don’t need Python locally.

### Build & Run Dev Container
```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml run --rm bot-dev
```

### Inside container you can run:
```bash
pytest --cov   # run tests with coverage
flake8 .       # lint
bandit -r .    # security scan
```

---

## 💻 VS Code Dev Container

This project includes a **VS Code Dev Container** for one-click setup.

### Usage
1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in VS Code.
2. Open the repo in VS Code.
3. Run `Dev Containers: Reopen in Container` from the command palette.
4. VS Code will build and start the development container defined in `.devcontainer/devcontainer.json`.

This container has:
- Python + dependencies
- Flake8, Bandit, Pytest
- Docker extension integration

---

## ☁️ GitHub Codespaces

This project supports **GitHub Codespaces**, allowing you to develop in the cloud without local setup.

### Usage
1. Open your repo on GitHub.
2. Click **Code → Codespaces → Create Codespace on Main**.
3. GitHub will launch a dev container with Python, linting, testing, and security tools pre-installed.
4. Run inside Codespaces terminal:
```bash
pytest --cov   # run tests with coverage
flake8 .       # lint
bandit -r .    # security scan
make run       # run bot
```


## 📊 Project Roadmap

<p align="center">
  <a href="ROADMAP.md">
    <img src="https://raw.githubusercontent.com/JAY01-CYBER/telegram-gemini-bot/main/docs/assets/roadmap.png" alt="Project Roadmap" width="80%"/>
  </a>
</p>

👉 See the full [ROADMAP.md](ROADMAP.md) for details.

📖 See full [Changelog](CHANGELOG.md) for release history.
