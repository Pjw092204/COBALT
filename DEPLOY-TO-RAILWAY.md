# Deploy COBALT to Railway - Step-by-Step Guide

Follow these steps in order. Take your time—you can pause between steps.

---

## Part 1: Put Your Code on GitHub

### Step 1.1: Create a GitHub Account (if you don't have one)

1. Go to **https://github.com**
2. Click **Sign up**
3. Enter your email, create a password, choose a username
4. Verify your email if asked

---

### Step 1.2: Create a New Repository

1. Sign in to GitHub
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name:** `cobalt-app` (or any name you like)
   - **Description:** (optional) "Environmental risk analysis for Wisconsin BRRTS"
   - **Public** (selected)
   - **Do NOT** check "Add a README" (we're uploading existing code)
4. Click **Create repository**

---

### Step 1.3: Upload Your Project Files

1. You'll see a page that says "Quick setup" or "uploading an existing file"
2. Click **"uploading an existing file"** (or the link that lets you add files)
3. Open File Explorer on your PC and go to:
   ```
   C:\Users\1127wisniep\Desktop\Cobalt AI YEA\COBALT-main
   ```
4. Select **ALL** files and folders inside COBALT-main:
   - .env.example
   - .gitignore
   - Procfile
   - nixpacks.toml
   - main.py
   - requirements.txt
   - README.md
   - brrts_client.py
   - document_scraper.py
   - filedownload.py
   - pdf_extractor.py
   - playwright_scraper.py
   - risk_analysis.py
   - scraper1.py
   - pyproject.toml
   - uv.lock
   - generated-icon.png
   - **attached_assets** (folder)
   - **static** (folder)
   - **templates** (folder)

   **Important:** Do NOT upload your `.env` file (it contains your secret API key). It should not be in the list—if you see it, leave it unchecked.

5. Drag and drop all selected items into the GitHub upload area, OR click "choose your files" and select them
6. In the box at the bottom, type: `Initial upload`
7. Click **Commit changes**

---

## Part 2: Deploy on Railway

### Step 2.1: Create a Railway Account

1. Go to **https://railway.app**
2. Click **Login** or **Start a New Project**
3. Choose **Login with GitHub**
4. Authorize Railway to access your GitHub account (click **Authorize** if asked)

---

### Step 2.2: Create a New Project and Deploy

1. On Railway's dashboard, click **New Project**
2. Select **Deploy from GitHub repo**
3. If asked to install Railway's GitHub app, click **Configure** and select your account (or "All repositories" or just the `cobalt-app` repo)
4. In the list of repositories, find **cobalt-app** (or whatever you named it)
5. Click on it to select it
6. Railway will start building. Wait 2–5 minutes. You may see logs scrolling.

---

### Step 2.3: Add Your API Key

1. Once the project is created, click on your **service** (the box that represents your app)
2. Click the **Variables** tab (or **Settings** → **Variables**)
3. Click **+ New Variable** or **Add Variable**
4. Enter:
   - **Variable name:** `OPENROUTER_API_KEY`
   - **Value:** Your OpenRouter API key (the long string from your .env file, starting with `sk-or-v1-...`)
5. Click **Add** or **Save**
6. Railway will automatically **redeploy** with the new variable (wait 1–2 minutes)

---

### Step 2.4: Get Your Public URL

1. Click on your service again
2. Go to the **Settings** tab
3. Find the **Networking** or **Domains** section
4. Click **Generate Domain** (or **Add Domain**)
5. Railway will create a URL like: `https://cobalt-app-production-xxxx.up.railway.app`
6. **Copy this URL**—this is your permanent public link

---

### Step 2.5: Use Your App

- Your app's main page: `https://your-url.up.railway.app`
- The analysis page: `https://your-url.up.railway.app/app`

Share the first URL with others. The app will stay online 24/7.

---

## Troubleshooting

**Build fails?**
- Check that you uploaded all files, including `Procfile` and `nixpacks.toml`
- Make sure `requirements.txt` was uploaded

**"OPENROUTER_API_KEY not configured"?**
- Add the variable in Railway → Variables
- Wait for the app to redeploy after adding it

**Documents not loading?**
- Playwright may not work on Railway's free tier. The app will still run but with limited document fetching. Upgrading to a paid Railway plan can improve this.
