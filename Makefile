# 📦 Makefile for Telegram Gemini Bot

# Run locally
run:
	python bot.py

# Install dependencies
install:
	pip install -r requirements.txt

# Docker build & run
docker-build:
	docker build -t telegram-gemini-bot .

docker-run:
	docker run -d --name telegram-gemini-bot --env-file .env -p 8443:8443 telegram-gemini-bot

# Docker Compose
compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

# Kubernetes
k8s-apply:
	kubectl apply -f k8s/secrets.yaml
	kubectl apply -f k8s/deployment.yaml

k8s-delete:
	kubectl delete -f k8s/deployment.yaml
	kubectl delete -f k8s/secrets.yaml

# Helm
helm-install:
	helm install telegram-gemini ./helm/telegram-gemini-bot

helm-upgrade:
	helm upgrade telegram-gemini ./helm/telegram-gemini-bot

helm-uninstall:
	helm uninstall telegram-gemini
