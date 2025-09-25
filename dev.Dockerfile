FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y ffmpeg git curl && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install dev tools
RUN pip install pytest pytest-cov flake8 bandit pre-commit

# Copy project
COPY . .

CMD [ "bash" ]
