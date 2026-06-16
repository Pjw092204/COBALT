# COBALT on Railway — Playwright base image (Chromium + system libs pre-installed)
# https://playwright.dev/python/docs/docker

FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Dependencies; pin Playwright to match image browsers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -U "playwright==1.48.0"

COPY . .

RUN chmod +x start.sh

# Railway injects PORT at runtime; default for local docker run
ENV PORT=5000
EXPOSE 5000

# Gunicorn WSGI (production) — not Flask dev server
CMD ["sh", "start.sh"]
