# Use official Playwright Python image - includes Chromium + all system deps
FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

WORKDIR /app

# Install deps - pin Playwright to match Docker image's pre-installed browsers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -U "playwright==1.48.0"

# Browsers are pre-installed in base image - no need for playwright install

# Copy application code
COPY . .

# Railway sets PORT env var - main.py reads it
ENV PORT=5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
