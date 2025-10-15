# 🚀 Quick Start Guide

Get started with Google Maps Business Data Scraper in 5 minutes!

## ⚡ Fast Setup

### Step 1: Install Dependencies (2 minutes)

```powershell
pip install -r requirements.txt
```

### Step 2: Test Installation (1 minute)

```powershell
python test_setup.py
```

If all checks pass ✓, you're ready!

### Step 3: Run Your First Scrape (2 minutes)

```powershell
python maps_scraper.py
```

That's it! Check the `output/` folder for your results.

---

## 📝 Customize Your Scrape

### Edit Keywords

1. Open `keywords.csv`
2. Add your search terms (one per line):
   ```
   keyword
   restaurant in New York
   coffee shop in Seattle
   hotel in Miami
   ```

### Use Your Keywords

Edit `maps_scraper.py` (around line 421):

```python
# Replace these lines:
keywords = [
    "restaurant in Jakarta",
    "coffee shop in Bali",
    "hotel in Bandung"
]

# With:
keywords = load_keywords_from_csv('keywords.csv')
```

Then run:
```powershell
python maps_scraper.py
```

---

## 🎯 Common Use Cases

### Scrape One Keyword Quickly

```powershell
python examples.py
```

Select option 4, enter your keyword, done!

### Scrape in Background (Headless)

```powershell
python examples.py
```

Select option 3 for headless mode.

### Merge All Results

After scraping:

```powershell
python utils.py
```

Select option 1 to merge all Excel files into one.

---

## 📊 View Results

### Option 1: Open Excel Files

Navigate to `output/` folder and open any `.xlsx` file.

### Option 2: View in PowerShell

```powershell
python -c "import pandas as pd; df = pd.read_excel('output/restaurant_in_Jakarta.xlsx'); print(df)"
```

### Option 3: Generate Analytics

```powershell
python utils.py
```

Select option 2 for detailed statistics.

---

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
HEADLESS_MODE = False          # True = run in background
DELAY_BETWEEN_ACTIONS = 3      # Seconds between actions
MAX_RESULTS_PER_KEYWORD = 50   # Max businesses per keyword
```

---

## 🆘 Troubleshooting

### "Module not found" error?
```powershell
pip install -r requirements.txt
```

### Chrome issues?
Install Chrome from: https://www.google.com/chrome/

### Need more help?
Check `scraper_log.txt` for detailed error messages.

---

## 📚 Learn More

- **Full Documentation:** See [README.md](README.md)
- **Setup Guide:** See [docs/SETUP.md](docs/SETUP.md)
- **Project Requirements:** See [docs/prd.md](docs/prd.md)

---

## ✨ Pro Tips

1. **Start small:** Test with 3-5 keywords first
2. **Check logs:** Monitor `scraper_log.txt` during execution
3. **Use delays:** Keep 3-5 second delays to avoid detection
4. **Backup data:** Save your `output/` folder regularly

---

## 🎉 You're Ready!

Happy scraping! 🗺️

Questions? Check the full documentation or logs for details.
