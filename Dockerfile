# -------------------------------
# Dockerfile for Telegram Gemini Bot
# -------------------------------
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for webhook
EXPOSE 8443

# Start bot
CMD ["python", "bot.py"]
