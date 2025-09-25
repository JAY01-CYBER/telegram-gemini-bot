# 🤝 Contributing to Telegram Gemini Bot

Thank you for considering contributing! 🚀

We welcome contributions of all kinds, including:
- 🐞 Bug reports
- ✨ New features
- 🛠️ Improvements to code or documentation

---

## 📋 Contribution Guidelines

### 1. Fork & Clone
```bash
git fork https://github.com/your-username/telegram-gemini-bot.git
git clone https://github.com/your-username/telegram-gemini-bot.git
cd telegram-gemini-bot
```

### 2. Create a Branch
```bash
git checkout -b feature/my-feature
```

### 3. Run Pre-commit Hooks
Make sure you have pre-commit installed:
```bash
pip install pre-commit
pre-commit install
```

Every commit will auto-run:
- **flake8** (lint)
- **bandit** (security)

### 4. Run Tests
```bash
pytest --cov
```

### 5. Commit & Push
```bash
git commit -m "Add my feature"
git push origin feature/my-feature
```

### 6. Open Pull Request
- Go to GitHub and open a PR against `main`
- Ensure CI checks (lint, tests, security) pass

---

## 💡 Tips
- Follow Python best practices (PEP8, max line length 120)
- Keep commits small & focused
- Update docs if needed (MkDocs site)

---

## 📜 Code of Conduct
By participating, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).
