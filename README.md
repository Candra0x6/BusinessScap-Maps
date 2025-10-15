# 🗺️ Google Maps Business Data Scraper

An automated web scraping system built with **Python and Selenium** to collect business information from Google Maps for multiple search keywords.

## 📋 Features

- ✅ Automated data extraction from Google Maps
- ✅ Scrapes business name, description, website, phone number, and Google Maps link
- ✅ Supports up to 100 keywords per batch
- ✅ Exports each keyword's data to a separate Excel file
- ✅ Comprehensive error handling and logging
- ✅ Summary report generation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Chrome browser installed
- Internet connection

### Installation

1. **Clone or download this project**

2. **Install required packages:**

```powershell
pip install -r requirements.txt
```

3. **Verify Chrome is installed:**
   - The scraper uses Chrome WebDriver
   - Chrome will be automatically detected

### Usage

#### Option 1: Use Default Keywords

Run the scraper with example keywords:

```powershell
python maps_scraper.py
```

#### Option 2: Use Custom Keywords from CSV

1. Edit `keywords.csv` and add your search terms (one per line)
2. Modify `maps_scraper.py` to load from CSV:

```python
# In main() function, replace:
keywords = load_keywords_from_csv('keywords.csv')
```

3. Run the scraper:

```powershell
python maps_scraper.py
```

## 📂 Output

All results are saved in the `output/` folder:

- **Individual Excel files:** One `.xlsx` file per keyword (e.g., `restaurant_in_Jakarta.xlsx`)
- **Summary report:** `scraping_summary_[timestamp].xlsx` with overview of all scraped keywords
- **Log file:** `scraper_log.txt` with detailed execution logs

## 📊 Data Structure

Each Excel file contains the following columns:

| Column Name        | Description                                    |
|--------------------|------------------------------------------------|
| Business Name      | The name of the business                       |
| Description        | Short description or category of the business  |
| Website            | The official website URL (if available)        |
| Phone              | Contact number (if available)                  |
| Google Maps Link   | Direct URL to the business page on Google Maps |

## ⚙️ Configuration

### Adjust Scraping Behavior

In `maps_scraper.py`, you can modify:

```python
# Initialize with custom settings
scraper = GoogleMapsScraper(
    headless=False,  # Set True to run without opening browser window
    delay=3          # Delay between actions (seconds)
)
```

### Limit Results per Keyword

In the `extract_business_data()` method, adjust:

```python
for idx, listing in enumerate(listings[:50], 1):  # Change 50 to desired limit
```

## 📝 Logging

All activities are logged to `scraper_log.txt`:

- Timestamps for each action
- Success/failure status
- Error messages
- Summary statistics

## ⚠️ Important Notes

### Legal & Ethical Considerations

- **Terms of Service:** This scraper is for educational purposes. Always review and comply with Google's Terms of Service
- **Rate Limiting:** The scraper includes delays (3-5 seconds) to avoid overloading servers
- **Respectful Scraping:** Limit your scraping to reasonable amounts

### Known Limitations

- **CAPTCHA:** Google may present CAPTCHAs if too many requests are detected
- **Layout Changes:** Google Maps updates may require selector adjustments
- **Missing Data:** Not all businesses have complete information (website/phone)
- **IP Blocking:** Excessive scraping may result in temporary IP blocks

## 🛠️ Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver errors:

```powershell
pip install webdriver-manager --upgrade
```

The script will automatically download the correct ChromeDriver version.

### Element Not Found Errors

If selectors break due to Google Maps updates:

1. Check `scraper_log.txt` for error details
2. Update CSS selectors in `extract_details()` method
3. Use browser DevTools to find new selectors

### Timeout Errors

If pages load slowly:

1. Increase wait time in `setup_driver()`:
   ```python
   self.wait = WebDriverWait(self.driver, 20)  # Increase from 10 to 20
   ```
2. Increase delay between actions:
   ```python
   scraper = GoogleMapsScraper(delay=5)  # Increase from 3 to 5
   ```

## 📈 Performance

- **Average time per keyword:** 1-2 minutes (depends on result count)
- **Maximum results per keyword:** 50 (configurable)
- **Batch capacity:** Up to 100 keywords

## 🔧 Advanced Usage

### Run in Headless Mode

For server deployment or background execution:

```python
scraper = GoogleMapsScraper(headless=True, delay=3)
```

### Custom Keyword Processing

```python
# Load keywords from different sources
keywords = [
    "dentist in " + city 
    for city in ["Jakarta", "Bali", "Bandung"]
]

# Or read from text file
with open('keywords.txt', 'r') as f:
    keywords = [line.strip() for line in f.readlines()]
```

## 📦 Project Structure

```
business-scrap/
├── maps_scraper.py      # Main scraper script
├── keywords.csv         # Input keywords file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── docs/
│   └── prd.md          # Product Requirements Document
├── output/             # Generated Excel files (created automatically)
└── scraper_log.txt     # Execution logs (created automatically)
```

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share improvements

## 📄 License

This project is for educational purposes. Use responsibly and ethically.

## 👤 Author

**Version:** 1.0  
**Date:** October 15, 2025

---

## 🎯 Quick Command Reference

```powershell
# Install dependencies
pip install -r requirements.txt

# Run scraper with default keywords
python maps_scraper.py

# View logs
Get-Content scraper_log.txt -Tail 50

# Check output files
Get-ChildItem output/
```

---

**Happy Scraping! 🚀**

Remember to scrape responsibly and respect website terms of service.
