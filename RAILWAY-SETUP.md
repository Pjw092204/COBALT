# Fix Railway: Scraper + API Key

Your app at **https://cobalt-production-d8d4.up.railway.app** needs two things configured so the scraper and AI chat work.

---

## 1. Add your OpenRouter API key (fixes chat / “API key not working”)

The app does **not** use a `.env` file on Railway. You must set the key in Railway.

1. Go to **https://railway.app** and open your **COBALT** project.
2. Click your **service** (the app box).
3. Open the **Variables** tab.
4. Click **+ New Variable** (or **Add Variable**).
5. Set:
   - **Name:** `OPENROUTER_API_KEY`
   - **Value:** your OpenRouter key (starts with `sk-or-v1-...` from https://openrouter.ai/keys)
6. Save. Railway will **redeploy** automatically.

After redeploy, check the **Deployments** log. You should see:

```text
OPENROUTER_API_KEY: SET
```

If you see `OPENROUTER_API_KEY: NOT SET`, the variable was not added correctly.

---

## 2. Use the Dockerfile (fixes scraper / “nothing loading”)

The scraper needs Playwright and Chromium. That only works if Railway builds with the **Dockerfile**, not the default Nixpacks build.

**Check your GitHub repo:**

1. Open your repo (e.g. `github.com/yourusername/cobalt-app`).
2. In the **root** of the repo, confirm you have a file named **`Dockerfile`** (no extension).
3. If it’s missing, add it (see below) and commit. Railway will redeploy from the new commit.

**Dockerfile contents** (paste into a new file named `Dockerfile` in the repo root):

```dockerfile
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

4. Commit and push. Wait for Railway to finish redeploying (build can take 3–5 minutes).

---

## 3. Confirm everything works

1. Open **https://cobalt-production-d8d4.up.railway.app/app**
2. Enter **588459** → click **Analyze Site**
   - You should see full site info (Status, Address, County, etc.) and a risk summary.
3. Click **Fetch Documents**
   - You should see a list of documents (e.g. 25).
4. Select at least one document, then ask a question and click **Ask AI**
   - You should get an AI reply (and have OpenRouter credits).

---

## Summary

| Issue              | Fix |
|--------------------|-----|
| API key not working | Add **OPENROUTER_API_KEY** in Railway → your service → **Variables**. |
| Scraper not working | Ensure **Dockerfile** exists in the **root** of your GitHub repo and Railway has redeployed. |

After both are done, the site and scraper should work and the chat should use your API key.
