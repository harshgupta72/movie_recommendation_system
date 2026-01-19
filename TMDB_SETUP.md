# 🎬 TMDb API Setup Guide - Get Real Movie Posters!

## Quick Setup (5 minutes)

### Step 1: Get Your FREE TMDb API Key

1. **Sign Up**: Go to https://www.themoviedb.org/signup
   - Use your email
   - Create a password
   - Verify your email

2. **Request API Key**: Visit https://www.themoviedb.org/settings/api
   - Click **"Create"** under "Request an API Key"
   - Choose **"Developer"**
   - Fill in the form:
     - **Type of Use**: Personal/Education
     - **Application Name**: BollywoodFlix
     - **Application URL**: http://localhost:5000
     - **Application Summary**: Movie recommendation website
   - Accept terms and submit

3. **Copy Your API Key**
   - You'll see **"API Key (v3 auth)"**
   - Copy this key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### Step 2: Add API Key to the Script

1. Open `fetch_tmdb_posters.py` in your editor

2. Find this line (around line 22):
   ```python
   TMDB_API_KEY = "YOUR_API_KEY_HERE"
   ```

3. Replace with your actual key:
   ```python
   TMDB_API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
   ```

4. Save the file

### Step 3: Download All Real Posters

Run the script:

```bash
python fetch_tmdb_posters.py
```

**What happens:**
- ✅ Searches TMDb for each of your 100 movies
- ✅ Downloads official high-quality posters
- ✅ Saves them to `static/posters/` folder
- ✅ Shows progress for each movie
- ✅ Takes about 1-2 minutes

### Step 4: Refresh Your Browser

Open http://127.0.0.1:5000 and see **REAL movie posters**! 🎉

---

## Example Output

When you run the script, you'll see:

```
============================================================
TMDb Movie Poster Downloader
Downloading Real, Official Movie Posters
============================================================

Starting download...

  [OK] Movie 1: Kalki 2898 AD (2024)
  [OK] Movie 2: Stree 2 (2024)
  [OK] Movie 3: Fighter (2024)
  [OK] Movie 4: Laapataa Ladies (2024)
  ...
  [OK] Movie 100: Mr. & Mrs. Mahi (2024)

============================================================
Download Complete!
  Success: 95/100
  Failed:  5/100
  Skipped: 0/100
============================================================

✅ Great! Most posters downloaded successfully!
Refresh your browser to see real movie posters!
```

---

## Troubleshooting

### "ERROR: Please add your TMDb API key!"
- You forgot to replace `YOUR_API_KEY_HERE` with your actual key
- Open `fetch_tmdb_posters.py` and add your key

### "Invalid API key"
- Double-check you copied the full key
- Make sure there are no extra spaces
- Use the **v3 auth** key, not v4

### Some movies show "[SKIP] Not found"
- The movie name might be different on TMDb
- Don't worry! The generated poster will show as fallback
- You can manually download those specific posters later

### "Rate limit exceeded"
- TMDb has a limit of 40 requests per 10 seconds
- The script already has delays built-in
- If you see this, just wait 10 seconds and run again

---

## Benefits of TMDb Posters

✅ **Legal & Official** - Authorized by movie studios
✅ **High Quality** - Professional 500px wide posters
✅ **Always Updated** - New movies added regularly
✅ **Free Forever** - No cost for personal/educational use
✅ **Reliable** - 99.9% uptime
✅ **No Copyright Issues** - Safe for your project

---

## What's Your API Key Limit?

**FREE TMDb Account:**
- ✅ 50 requests per second
- ✅ Unlimited total requests
- ✅ No credit card required
- ✅ Never expires

Perfect for your project!

---

## Ready to Download?

1. ✅ Got your API key from TMDb
2. ✅ Added it to `fetch_tmdb_posters.py`
3. ✅ Run: `python fetch_tmdb_posters.py`
4. ✅ Wait 1-2 minutes
5. ✅ Refresh browser
6. ✅ Enjoy REAL movie posters! 🎉

---

**Questions?** Let me know and I'll help!
