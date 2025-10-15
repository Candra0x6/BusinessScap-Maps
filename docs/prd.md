Here’s a **Product Requirements Document (PRD)** in English for your Selenium-based Google Maps data scraping project.
It describes the goals, workflow, data structure, and technical details precisely — suitable for guiding development or stakeholder review.

---

# 🧾 Product Requirements Document (PRD)

**Project Title:** Google Maps Business Data Scraper
**Version:** 1.0
**Date:** October 15, 2025
**Author:** [Your Name]

---

## 1. 📍 Overview

This project aims to build an **automated web scraping system** using **Python and Selenium** to collect business information from **Google Maps** for a list of up to **100 search keywords**.

For each keyword, the system will:

* Open Google Maps.
* Search for the keyword.
* Extract key business data (name, description, website, phone number, and direct Google Maps link).
* Save the results to an **individual Excel file** (one per keyword).

The goal is to enable fast, repeatable data collection from Google Maps without manual input.

---

## 2. 🎯 Objectives

* Automate data extraction from Google Maps search results.
* Collect core business information for each search term.
* Store each search term’s data in a **separate Excel file**.
* Ensure data quality, consistency, and easy scalability.

---

## 3. 🧩 Scope

### **In-Scope**

* Automation with **Selenium + Python**.
* Scraping data fields:

  * Business Name
  * Description (short description or category)
  * Website URL
  * Phone Number
  * Direct Google Maps Link
* Support for **up to 100 keywords** per run.
* Exporting data into **100 Excel (.xlsx)** files (one per keyword).

### **Out of Scope**

* Manual clicking or extension use (e.g., Instant Data Scraper).
* API-based or paid data sources (e.g., Google Maps API, SerpAPI).
* Handling CAPTCHA or rate-limiting beyond standard Selenium waits.

---

## 4. 📋 Functional Requirements

| ID    | Requirement       | Description                                                                                                                                                                                                |
| ----- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR-01 | Input Keywords    | System accepts a list of up to 100 search terms (can be from a CSV or Python list).                                                                                                                        |
| FR-02 | Automated Search  | For each keyword, the bot opens Google Maps, enters the keyword, and retrieves search results.                                                                                                             |
| FR-03 | Data Extraction   | For each business listing, the bot extracts: <ul><li>Business Name</li><li>Description / Category</li><li>Website URL (if available)</li><li>Phone Number (if available)</li><li>Google Maps URL</li></ul> |
| FR-04 | Detail Navigation | The bot clicks each listing to open its detail panel and scrapes website + phone number.                                                                                                                   |
| FR-05 | Excel Export      | Results for each keyword are saved as `{keyword}.xlsx` (e.g., `restaurant_in_jakarta.xlsx`).                                                                                                               |
| FR-06 | File Storage      | All Excel files are stored in a dedicated output folder (`/output`).                                                                                                                                       |
| FR-07 | Error Handling    | The bot skips unavailable data gracefully and logs errors to a text file.                                                                                                                                  |

---

## 5. 🧠 Non-Functional Requirements

| Category            | Requirement                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| **Performance**     | Each keyword search should complete in under 2 minutes (depending on result count). |
| **Scalability**     | System should handle up to 100 searches per batch.                                  |
| **Reliability**     | Must recover gracefully if a single search fails.                                   |
| **Maintainability** | Code should be modular and easy to update (separate scraping and export logic).     |
| **Compliance**      | Follow Google’s Terms of Service and limit scraping speed (e.g., 3–5 sec delays).   |

---

## 6. 🧰 Technical Design

### **Tech Stack**

* **Language:** Python 3.10+
* **Libraries:**

  * `selenium` — browser automation
  * `pandas` — data management and Excel export
  * `openpyxl` — Excel writer
* **Browser:** Google Chrome
* **Driver:** ChromeDriver (matching browser version)

### **System Flow**

1. Load list of search keywords.
2. Launch Chrome browser.
3. For each keyword:
   a. Go to Google Maps.
   b. Enter search keyword.
   c. Wait for results to load.
   d. Scroll results panel to load all listings.
   e. Click each listing → scrape details (name, desc, website, phone, link).
   f. Append data to a list.
   g. Export results to an Excel file named after the keyword.
4. Close browser when all keywords processed.

---

## 7. 📂 Data Structure

**Excel Columns (per keyword):**

| Column Name        | Description                                    |
| ------------------ | ---------------------------------------------- |
| `Business Name`    | The name of the business                       |
| `Description`      | Short description or category of the business  |
| `Website`          | The official website URL (if available)        |
| `Phone`            | Contact number (if available)                  |
| `Google Maps Link` | Direct URL to the business page on Google Maps |

**Example Output:**

| Business Name | Description  | Website                                         | Phone            | Google Maps Link                                         |
| ------------- | ------------ | ----------------------------------------------- | ---------------- | -------------------------------------------------------- |
| Café Aroma    | Coffee Shop  | [www.cafearoma.id](http://www.cafearoma.id)     | +62 812 3456 789 | [https://goo.gl/maps/abc123](https://goo.gl/maps/abc123) |
| Hotel Indah   | 3-Star Hotel | [www.hotelindah.com](http://www.hotelindah.com) | +62 21 5678 999  | [https://goo.gl/maps/xyz456](https://goo.gl/maps/xyz456) |

---

## 8. 🕐 Performance & Logging

* Delay between actions: 3–5 seconds (to mimic human behavior).
* Retry logic: 2 attempts for failed loads.
* Log file: `scraper_log.txt` records timestamp, keyword, and any errors.

---

## 9. 📦 Deliverables

1. **Python Script (`maps_scraper.py`)** – main automation logic.
2. **Config File (`keywords.csv`)** – list of search terms.
3. **Output Folder (`/output/`)** – contains up to 100 Excel files.
4. **Log File (`scraper_log.txt`)** – runtime logs and errors.
5. **README.md** – setup, installation, and usage instructions.

---

## 10. 🚧 Risks & Mitigations

| Risk                       | Description                                  | Mitigation                                           |
| -------------------------- | -------------------------------------------- | ---------------------------------------------------- |
| Google Maps layout changes | Page structure updates could break selectors | Use flexible XPaths and maintain selectors regularly |
| CAPTCHA or IP blocking     | Google may detect automation                 | Use delays, proxies, or headless mode                |
| Missing fields             | Some listings lack website or phone          | Record empty string (“”) instead of error            |
| Slow performance           | Too many listings per keyword                | Limit results per keyword (e.g., top 50)             |

---

## 11. 📈 Success Criteria

* ✅ 100 Excel files generated (one per keyword).
* ✅ Each file contains at least 20 valid records (if available).
* ✅ All columns populated for available data.
* ✅ No crashes during batch execution.

---

Would you like me to include the **Python code implementation** that fulfills this PRD (with working Selenium selectors for name, website, phone, etc.)?
I can generate a version that exactly matches these specifications.
