# Fix Railway Deployment - Playwright Not Working

Your app is deployed but showing "Not available" and 0 documents because Playwright (the browser) doesn't work with the default Railway build. These changes fix that.

## What Was Changed

1. **Dockerfile** - Uses the official Playwright Docker image with Chromium pre-installed
2. **.dockerignore** - Keeps the image smaller
3. **playwright_scraper.py** - Added Chromium launch args for Docker

## How to Apply the Fix

You need to add these updated files to your GitHub repo so Railway can redeploy.

### Option A: Add Files via GitHub Website

1. Go to your GitHub repo (e.g. `github.com/yourusername/cobalt-app`)
2. **Add the Dockerfile:**
   - Click **Add file** → **Create new file**
   - Name it: `Dockerfile` (exactly, no extension)
   - Paste this content:

```
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
```

   - Click **Commit changes**

3. **Add .dockerignore:**
   - Click **Add file** → **Create new file**
   - Name it: `.dockerignore`
   - Paste:

```
.env
.env.local
.env.production
.git
__pycache__
*.pyc
venv
.venv
.vscode
.idea
*.log
downloads
*.pdf
```

   - Click **Commit changes**

4. **Update playwright_scraper.py:**
   - Open `playwright_scraper.py` in your repo
   - Click the pencil icon (Edit)
   - Find this line (around line 28):
     ```python
     browser = p.chromium.launch(headless=True)
     ```
   - Replace it with:

     ```python
     # Args needed for Chromium in Docker/Railway (no sandbox, avoid shm issues)
     browser = p.chromium.launch(
         headless=True,
         args=[
             "--no-sandbox",
             "--disable-dev-shm-usage",
             "--disable-gpu",
             "--disable-software-rasterizer",
         ]
     )
     ```
   - Click **Commit changes**

### Option B: Re-upload All Files

If you prefer, you can delete all files in your repo and re-upload the entire `COBALT-main` folder (with the new Dockerfile, .dockerignore, and updated playwright_scraper.py from your PC).

---

## Trigger Redeploy on Railway

1. Go to **railway.app** → Your project
2. Railway should **automatically redeploy** when it detects new commits on GitHub
3. If not, click your service → **Deployments** → **Redeploy** (or **Trigger Deploy**)
4. Wait 3–5 minutes for the build to complete (Docker builds take longer than Nixpacks)

---

## After Redeploy

- **Analyze Site** should show full site info (Status, Address, County, etc.)
- **Fetch Documents** should return documents (e.g. 25 for DSN 588459)
- **Ask AI** will work once documents are loaded (and you have OpenRouter credits)
