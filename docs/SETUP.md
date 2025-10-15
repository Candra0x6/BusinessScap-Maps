# 🚀 Setup and Installation Guide

Complete setup instructions for the Google Maps Business Data Scraper.

## 📋 Prerequisites

Before you begin, ensure you have:

### Required Software

1. **Python 3.10 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Google Chrome Browser**
   - Download from: https://www.google.com/chrome/
   - The scraper requires Chrome to be installed

3. **Internet Connection**
   - Required for scraping Google Maps

### System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** At least 500MB free

## 🔧 Installation Steps

### Step 1: Download the Project

Clone or download this repository to your local machine.

### Step 2: Open Terminal/PowerShell

Navigate to the project directory:

```powershell
cd d:\Vs_Code_Project\Building\Python\business-scrap
```

### Step 3: Create Virtual Environment (Recommended)

Create an isolated Python environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

Install all required Python packages:

```powershell
pip install -r requirements.txt
```

This will install:
- `selenium` - Web automation framework
- `pandas` - Data manipulation and Excel export
- `openpyxl` - Excel file handling
- `webdriver-manager` - Automatic ChromeDriver management

### Step 5: Verify Installation

Check if all packages are installed correctly:

```powershell
pip list
```

You should see all the required packages listed.

## ✅ Testing the Setup

### Quick Test

Run a quick test to ensure everything works:

```powershell
python -c "from maps_scraper import GoogleMapsScraper; print('✓ Installation successful!')"
```

If you see "✓ Installation successful!", you're ready to go!

### Test Run

Perform a test scraping with one keyword:

```powershell
python examples.py
```

Select option 4 (Single Keyword) to test with a single search term.

## 📁 Project Structure

After setup, your project should look like this:

```
business-scrap/
├── venv/                    # Virtual environment (if created)
├── __pycache__/            # Python cache (auto-generated)
├── docs/
│   ├── prd.md              # Product Requirements Document
│   ├── python.md           # Python documentation
│   └── SETUP.md            # This file
├── output/                 # Output folder (created on first run)
├── maps_scraper.py         # Main scraper script
├── config.py               # Configuration settings
├── examples.py             # Example usage scripts
├── utils.py                # Utility functions
├── keywords.csv            # Input keywords file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
└── scraper_log.txt        # Log file (created on first run)
```

## 🎯 First Run

### Option 1: Run with Default Keywords

The simplest way to start:

```powershell
python maps_scraper.py
```

This will scrape 3 example keywords and save results to the `output/` folder.

### Option 2: Run with Custom Keywords

1. Edit `keywords.csv` to add your search terms
2. Modify `maps_scraper.py` (line 421):
   ```python
   # Change from:
   keywords = [
       "restaurant in Jakarta",
       "coffee shop in Bali",
       "hotel in Bandung"
   ]
   
   # To:
   keywords = load_keywords_from_csv('keywords.csv')
   ```
3. Run the scraper:
   ```powershell
   python maps_scraper.py
   ```

### Option 3: Use Interactive Examples

Run the examples script for guided usage:

```powershell
python examples.py
```

## 🔍 Troubleshooting

### Issue: "Python is not recognized"

**Solution:** Python is not in your system PATH.
- Reinstall Python and check "Add Python to PATH" during installation
- Or manually add Python to PATH

### Issue: "pip is not recognized"

**Solution:** pip is not installed or not in PATH.
```powershell
python -m ensurepip --default-pip
```

### Issue: "Cannot activate virtual environment"

**Solution:** Execution policy issue on Windows.

Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Issue: "ChromeDriver not found"

**Solution:** The webdriver-manager should handle this automatically.

If it fails:
```powershell
pip install webdriver-manager --upgrade
```

### Issue: "selenium.common.exceptions.WebDriverException"

**Solution:** Chrome browser is not installed or not found.
- Install Google Chrome
- Ensure Chrome is up to date

### Issue: "Module not found" errors

**Solution:** Dependencies not installed correctly.
```powershell
pip install -r requirements.txt --force-reinstall
```

## 🔐 Configuration

### Adjust Scraping Settings

Edit `config.py` to customize:

```python
# Run in background
HEADLESS_MODE = True

# Slower scraping (more careful)
DELAY_BETWEEN_ACTIONS = 5

# More results per keyword
MAX_RESULTS_PER_KEYWORD = 100
```

### Use Configuration in Script

```python
from config import HEADLESS_MODE, DELAY_BETWEEN_ACTIONS

scraper = GoogleMapsScraper(
    headless=HEADLESS_MODE,
    delay=DELAY_BETWEEN_ACTIONS
)
```

## 📊 Viewing Results

After scraping completes:

1. **Navigate to output folder:**
   ```powershell
   cd output
   ```

2. **List all files:**
   ```powershell
   Get-ChildItem
   ```

3. **Open an Excel file:**
   - Double-click any `.xlsx` file
   - Or open with Excel/LibreOffice

## 🧰 Additional Tools

### Merge Results

Combine all Excel files into one:

```powershell
python utils.py
```

Select option 1 (Merge all Excel files)

### Analyze Results

Generate statistics report:

```powershell
python utils.py
```

Select option 2 (Analyze results)

### Export to JSON

Convert all results to JSON format:

```powershell
python utils.py
```

Select option 3 (Export to JSON)

## 🔄 Updating the Project

### Update Dependencies

```powershell
pip install -r requirements.txt --upgrade
```

### Update ChromeDriver

```powershell
pip install webdriver-manager --upgrade
```

## 🆘 Getting Help

If you encounter issues:

1. **Check the log file:**
   ```powershell
   Get-Content scraper_log.txt -Tail 50
   ```

2. **Enable verbose logging:**
   Edit `maps_scraper.py` and change:
   ```python
   logging.basicConfig(level=logging.DEBUG)  # Changed from INFO
   ```

3. **Test with a single keyword:**
   Use `examples.py` option 4 to test with one search term

4. **Run in visible mode:**
   Set `headless=False` to watch the browser

## ✨ Best Practices

1. **Start Small:** Test with 3-5 keywords before running large batches
2. **Use Delays:** Keep delays at 3-5 seconds to avoid detection
3. **Monitor Logs:** Check `scraper_log.txt` regularly
4. **Backup Data:** Save output files regularly
5. **Respectful Scraping:** Follow Google's Terms of Service

## 🎓 Next Steps

Once setup is complete:

1. ✅ Read the full [README.md](../README.md)
2. ✅ Review the [PRD](prd.md) for project details
3. ✅ Customize `keywords.csv` with your search terms
4. ✅ Run your first scraping session
5. ✅ Analyze results using `utils.py`

---

**Setup Complete! Happy Scraping! 🚀**

For questions or issues, refer to the README.md or check scraper_log.txt
