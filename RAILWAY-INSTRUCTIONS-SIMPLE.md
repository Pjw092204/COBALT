# How to Fix Your COBALT Website on Railway (Super Simple Steps)

Your website lives on the internet at: **https://cobalt-production-d8d4.up.railway.app/app**

Right now two things are broken:
1. **The “chat” / “Ask AI”** – The AI needs a secret code (called an API key) to work. We have to type that code into Railway’s website.
2. **The scraper** – The part that loads site info and documents needs a special recipe file (called a Dockerfile) to be in your GitHub project. We’ll add that file.

You will do **two separate tasks**. Each one has small steps. Do them in order.

---

# PART 1: Add the Secret Code So the AI Chat Works

**What you’re doing:** Giving Railway your OpenRouter “password” (API key) so the “Ask AI” button can talk to the AI.

---

## Step 1: Open Railway in your browser

1. Open **Chrome** (or any browser).
2. Click the **address bar** at the top (where you type websites).
3. Type: **railway.app**
4. Press **Enter**.

---

## Step 2: Log in and find your project

1. If it asks you to log in, click **Login** and sign in (often with GitHub).
2. You should see a list of your projects. Find the one that has your COBALT app (it might be named something like **cobalt-app** or **COBALT**).
3. **Click once** on that project. The screen will change and you’ll see your “service” (a box that represents your app).

---

## Step 3: Open the place where you add the secret code

1. **Click once** on the box that represents your app (your “service”). It might say your app name or “Service.”
2. Look at the **top** of the screen. You should see tabs like **Deployments**, **Variables**, **Settings**, etc.
3. **Click** the tab that says **Variables**.

---

## Step 4: Add a new variable (the secret code)

1. On the Variables page, look for a button that says **+ New Variable** or **Add Variable** or **New**.
2. **Click** that button.
3. You’ll see **two empty boxes** (or two fields).

   **First box – the name (type this exactly):**
   - Click in the first box.
   - Type exactly: **OPENROUTER_API_KEY**
   - Do not add spaces. Do not add quotes. All capital letters.

   **Second box – the secret code (paste your key):**
   - You need your OpenRouter API key. It’s a long line of letters and numbers that starts with **sk-or-v1-**.
   - If you have it in a file on your computer:
     - Open the file **.env** in the folder: `C:\Users\1127wisniep\Desktop\Cobalt AI YEA` or in `COBALT-main`. The line looks like: `OPENROUTER_API_KEY=sk-or-v1-...`
     - Copy only the part **after** the `=` (the long code starting with sk-or-v1-).
   - If you don’t have it:
     - Go to **https://openrouter.ai/keys** in your browser.
     - Log in. Click to create or copy your API key.
     - Copy the whole key (it starts with sk-or-v1-).
   - Click in the **second box** on Railway (the “value” box).
   - **Paste** the key there (right‑click → Paste, or Ctrl+V).
   - Do not add spaces at the start or end.

4. Click **Add** or **Save** (whatever button appears to save the variable).

Railway will automatically restart your app. Wait about 1–2 minutes.

---

## Step 5: Check that it worked

1. Stay in Railway. Click the **Deployments** tab at the top.
2. Click the **newest** deployment (the one at the top of the list).
3. Click **View Logs** or open the logs.
4. Scroll until you see a line that says either:
   - **OPENROUTER_API_KEY: SET** ← Good. The secret code is in place.
   - **OPENROUTER_API_KEY: NOT SET** ← Bad. Go back to Step 4 and add the variable again; make sure the name is exactly **OPENROUTER_API_KEY**.

---

# PART 2: Add the Dockerfile So the Scraper Works

**What you’re doing:** Adding a special file (Dockerfile) to your GitHub project. That file tells Railway how to run your app with a “browser” so it can load site info and documents.

---

## Step 1: Open your project on GitHub

1. Open a new browser tab.
2. In the address bar, type: **github.com**
3. Press **Enter**.
4. Log in if you need to.
5. Find the **repository** (project) where you put your COBALT app. It might be named **cobalt-app** or something similar.
6. **Click** on that repository name to open it.

---

## Step 2: See if the Dockerfile is already there

1. You’re now on the main page of your repository. You’ll see a list of **files and folders** (like **main.py**, **templates**, **requirements.txt**, etc.).
2. Look for a file named **Dockerfile** (no .txt, no .py – just **Dockerfile**).
   - **If you see “Dockerfile”** – You’re done with Part 2. Skip to “When You’re All Done” below.
   - **If you do NOT see “Dockerfile”** – Continue to Step 3.

---

## Step 3: Create a new file named Dockerfile

1. On the GitHub repository page, click the green button that says **Add file**.
2. In the menu that drops down, click **Create new file**.
3. You’ll see a box that says “Name your file…” or has a path like `yourusername/cobalt-app/` and then an empty place for the filename.
4. In that **filename box**, type exactly: **Dockerfile**
   - Capital D, rest lowercase. No .txt, no .py. Just: **Dockerfile**

---

## Step 4: Put the recipe (code) into the Dockerfile

1. Below the filename, you’ll see a **big text area** (where you type the file contents).
2. **Click inside** that big text area so your cursor is there.
3. **Delete** any text that’s already there (if any).
4. **Copy** everything in the gray box below (from the first line to the last line), then **paste** it into that big text area.

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

5. Make sure you didn’t add any extra spaces at the very top or bottom. The first line should start with **#** and the last line should be **CMD ["python", "main.py"]**

---

## Step 5: Save the file on GitHub

1. Scroll down the page until you see a green button that says **Commit new file** or **Commit changes**.
2. You can leave the commit message as is (e.g. “Create Dockerfile”) or type something like “Add Dockerfile for Railway.”
3. **Click** the green **Commit new file** (or **Commit changes**) button.

GitHub will save the file. Railway will notice the change and start rebuilding your app. That can take **3–5 minutes**.

---

## Step 6: Wait for Railway to finish

1. Go back to your **Railway** tab (railway.app).
2. Click your project, then your service.
3. Click the **Deployments** tab.
4. You should see a **new** deployment (it might say “Building” or “Deploying”). Wait until it says **Success** or shows a green check. This can take 3–5 minutes.

---

# When You’re All Done – Test Your Website

1. Open a new tab and go to: **https://cobalt-production-d8d4.up.railway.app/app**
2. In the **Site Analysis** box, type: **588459**
3. Click the green **Analyze Site** button.
   - You should see real info (numbers, addresses, status) instead of “Not available” and dashes.
4. Click the **Fetch Documents** button.
   - You should see a list of documents (lots of rows), not “0 documents.”
5. Click one or two documents so they’re selected, then type a question in the **Ask a question** box and click **Ask AI**.
   - You should get an answer from the AI (and no “401” or “User not found” error).

If all of that works, you’re done.

---

# Quick Reminder

| What’s broken | Where to fix it | What to do |
|---------------|-----------------|------------|
| AI chat / “Ask AI” | **Railway** → your service → **Variables** | Add a variable named **OPENROUTER_API_KEY** and paste your OpenRouter key as the value. |
| Scraper / no site info or documents | **GitHub** → your repo | Add a new file named **Dockerfile** (no extension) and paste the recipe from Step 4 of Part 2. Then commit. |

If something doesn’t work, double‑check:
- The variable name on Railway is **exactly** **OPENROUTER_API_KEY** (no typos, no spaces).
- The file on GitHub is named **exactly** **Dockerfile** (capital D, no .txt).
- You waited a few minutes after saving so Railway could redeploy.
