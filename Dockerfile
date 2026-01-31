# Use official Playwright image
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Environment
ENV PYTHONUNBUFFERED=1

# Use shell script to start
CMD ["bash", "start.sh"]
