"""
Google Maps Business Data Scraper
A Selenium-based web scraper to collect business information from Google Maps.

Author: [Your Name]
Date: October 15, 2025
Version: 1.0
"""

import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
import re
try:
    import phonenumbers
    _HAS_PHONENUMBERS = True
except Exception:
    phonenumbers = None
    _HAS_PHONENUMBERS = False
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class GoogleMapsScraper:
    """Main scraper class for Google Maps business data extraction."""
    
    def __init__(self, headless: bool = False, delay: int = 3):
        """
        Initialize the scraper.
        
        Args:
            headless: Run browser in headless mode
            delay: Delay between actions in seconds (default: 3)
        """
        self.delay = delay
        self.driver = None
        self.wait = None
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Setup Chrome driver
        self.setup_driver(headless)
        
    def setup_logging(self):
        """Configure logging to file and console."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper_log.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self, headless: bool):
        """
        Setup Chrome WebDriver with appropriate options.
        
        Args:
            headless: Run browser in headless mode
        """
        try:
            chrome_options = Options()
            
            if headless:
                chrome_options.add_argument("--headless")
            
            # Additional options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Set user agent to mimic real browser
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            self.logger.info("Chrome WebDriver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
            
    def search_keyword(self, keyword: str) -> bool:
        """
        Search for a keyword on Google Maps.
        
        Args:
            keyword: Search term to look up
            
        Returns:
            True if search successful, False otherwise
        """
        try:
            self.logger.info(f"Searching for: {keyword}")
            
            # Navigate to Google Maps
            self.driver.get("https://www.google.com/maps")
            time.sleep(self.delay)
            
            # Find and click search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(self.delay)
            
            # Wait for results to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
            )
            
            self.logger.info(f"Search results loaded for: {keyword}")
            return True
            
        except TimeoutException:
            self.logger.error(f"Timeout while searching for: {keyword}")
            return False
        except Exception as e:
            self.logger.error(f"Error searching for {keyword}: {e}")
            return False
            
    def scroll_results(self, max_scrolls: int = 10):
        """
        Scroll through the results panel to load more listings.
        
        Args:
            max_scrolls: Maximum number of scroll attempts
        """
        try:
            results_panel = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            
            previous_height = 0
            for i in range(max_scrolls):
                # Get current scroll height
                current_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight;",
                    results_panel
                )
                
                # Scroll to bottom of results panel
                self.driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
                    results_panel
                )
                time.sleep(2)
                
                # Check if we've reached the end (no new content loaded)
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight;",
                    results_panel
                )
                
                if new_height == previous_height:
                    # Check for end marker
                    try:
                        end_marker = self.driver.find_element(
                            By.XPATH,
                            "//span[contains(text(), \"You've reached the end of the list\")]"
                        )
                        if end_marker:
                            self.logger.info("Reached end of results")
                            break
                    except NoSuchElementException:
                        pass
                    
                    # No new content and no end marker, might be at the end
                    self.logger.info(f"No new content after scroll {i+1}, stopping")
                    break
                
                previous_height = new_height
                self.logger.info(f"Scroll {i+1}/{max_scrolls} - Loaded more results")
                    
        except Exception as e:
            self.logger.warning(f"Error while scrolling: {e}")
            
    def extract_business_data(self) -> List[Dict[str, str]]:
        """
        Extract business data from current search results.
        
        Returns:
            List of dictionaries containing business information
        """
        businesses = []
        max_results = 50
        
        try:
            # Scroll to load more results
            self.scroll_results()
            
            # Get initial count of listings
            initial_listings = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div[role='feed'] > div > div > a"
            )
            total_available = len(initial_listings)
            self.logger.info(f"Found {total_available} listings")
            
            # Process listings one by one, re-querying each time to avoid stale elements
            idx = 0
            attempts = 0
            max_attempts = max_results * 2  # Safety limit
            
            while idx < min(max_results, total_available) and attempts < max_attempts:
                attempts += 1
                
                try:
                    # Re-query listings to get fresh elements
                    listings = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        "div[role='feed'] > div > div > a"
                    )
                    
                    if idx >= len(listings):
                        self.logger.warning(f"No more listings available at index {idx}")
                        break
                    
                    self.logger.info(f"Processing listing {idx + 1}/{min(max_results, total_available)}")
                    
                    # Get the current listing
                    listing = listings[idx]
                    
                    # Scroll the listing into view first
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", listing)
                    time.sleep(0.5)
                    
                    # Click on the listing to open details
                    self.driver.execute_script("arguments[0].click();", listing)
                    time.sleep(self.delay)
                    
                    # Extract business data
                    business_data = self.extract_details()
                    
                    if business_data:
                        businesses.append(business_data)
                        self.logger.info(f"Extracted: {business_data['Business Name']}")
                    else:
                        self.logger.warning(f"No data extracted for listing {idx + 1}")
                    
                    # Successfully processed, move to next
                    idx += 1
                    
                except StaleElementReferenceException:
                    self.logger.warning(f"Stale element at index {idx}, retrying...")
                    time.sleep(1)
                    # Don't increment idx, try again
                    continue
                    
                except Exception as e:
                    self.logger.error(f"Error processing listing {idx + 1}: {e}")
                    # Skip this listing and move to next
                    idx += 1
                    continue
            
            self.logger.info(f"Successfully extracted {len(businesses)} businesses")
                    
        except Exception as e:
            self.logger.error(f"Error extracting business data: {e}")
            
        return businesses
        
    def extract_details(self, max_retries: int = 2) -> Optional[Dict[str, str]]:
        """
        Extract detailed information from an open business listing.
        
        Args:
            max_retries: Number of times to retry if extraction fails
            
        Returns:
            Dictionary with business details or None if extraction fails
        """
        for attempt in range(max_retries):
            try:
                # Wait for details panel to load
                time.sleep(2)
                
                business_data = {
                    'Business Name': '',
                    'Description': '',
                    'Website': '',
                    'Phone': '',
                    'Google Maps Link': ''
                }
                
                # Extract business name
                try:
                    name_element = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "h1.DUwDvf.lfPIob"
                    )
                    business_data['Business Name'] = name_element.text
                except NoSuchElementException:
                    try:
                        name_element = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "h1"
                        )
                        business_data['Business Name'] = name_element.text
                    except:
                        self.logger.warning("Could not find business name")
                
                # If no business name on first attempt, wait and retry
                if not business_data['Business Name'] and attempt < max_retries - 1:
                    self.logger.info(f"No business name found, retrying... (attempt {attempt + 1})")
                    time.sleep(2)
                    continue
                
                # Extract description/category
                try:
                    desc_element = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "button[jsaction*='pane.rating.category']"
                    )
                    business_data['Description'] = desc_element.text
                except NoSuchElementException:
                    try:
                        desc_element = self.driver.find_element(
                            By.XPATH,
                            "//button[contains(@class, 'DkEaL')]"
                        )
                        business_data['Description'] = desc_element.text
                    except:
                        pass
                
                # Extract website
                try:
                    website_element = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "a[data-item-id='authority']"
                    )
                    business_data['Website'] = website_element.get_attribute('href')
                except NoSuchElementException:
                    try:
                        website_element = self.driver.find_element(
                            By.XPATH,
                            "//a[contains(@aria-label, 'Website')]"
                        )
                        business_data['Website'] = website_element.get_attribute('href')
                    except:
                        pass
                
                # Extract phone number
                try:
                    phone_element = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "button[data-item-id*='phone']"
                    )
                    raw_phone = phone_element.get_attribute('aria-label')
                    business_data['Phone'] = self._normalize_phone(raw_phone)
                except NoSuchElementException:
                    try:
                        phone_element = self.driver.find_element(
                            By.XPATH,
                            "//button[contains(@aria-label, 'Phone')]"
                        )
                        phone_data = phone_element.get_attribute('aria-label')
                        business_data['Phone'] = self._normalize_phone(phone_data) if phone_data else ''
                    except:
                        pass
                
                # Get Google Maps link
                business_data['Google Maps Link'] = self.driver.current_url
                
                # Return None if no business name found after all retries
                if not business_data['Business Name']:
                    if attempt == max_retries - 1:
                        return None
                    continue
                    
                return business_data
                
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"Error extracting details after {max_retries} attempts: {e}")
                    return None
                else:
                    self.logger.warning(f"Error extracting details (attempt {attempt + 1}), retrying: {e}")
                    time.sleep(1)
                    continue
        
        return None
            
    def save_to_excel(self, data: List[Dict[str, str]], keyword: str):
        """
        Save scraped data to Excel file.
        
        Args:
            data: List of business data dictionaries
            keyword: Search keyword (used for filename)
        """
        try:
            if not data:
                self.logger.warning(f"No data to save for keyword: {keyword}")
                return
                
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Clean filename
            safe_keyword = "".join(
                c if c.isalnum() or c in (' ', '_', '-') else '_' 
                for c in keyword
            ).strip()
            
            # Save to Excel
            filename = self.output_dir / f"{safe_keyword}.xlsx"
            df.to_excel(filename, index=False, engine='openpyxl')
            
            self.logger.info(f"Saved {len(data)} records to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving to Excel for {keyword}: {e}")

    def _normalize_phone(self, raw: Optional[str]) -> str:
        """Normalize phone strings by removing common prefixes and non-number noise.

        Examples of inputs handled:
        - "Phone: +1 661-335-6060"
        - "Telepon: +62 812-3456-789"
        - "P: +1 (555) 123-4567"

        Returns only the phone number with plus and digits, spaces, dashes and parentheses preserved.
        """
        if not raw:
            return ""

        # Remove common localized prefixes (case-insensitive)
        raw = raw.strip()
        # Patterns like 'Phone:', 'Phone', 'Telepon:', 'Telepon', 'P:' etc.
        raw = re.sub(r'^(phone|telepon|p|tel)\s*[:\-]?\s*', '', raw, flags=re.IGNORECASE)

        # Sometimes aria-label contains text like 'Phone: +1 555-123-4567' or 'Call: ...'
        raw = re.sub(r'^(call|hubungi)\s*[:\-]?\s*', '', raw, flags=re.IGNORECASE)

        # Trim again
        raw = raw.strip()

        # If there is any leading word like 'Mobile' remove it
        raw = re.sub(r'^[A-Za-z\s]+[:\-]?\s*', lambda m: '' if re.search(r'[0-9\+]', m.group(0)) else raw, raw)

        # Finally, try to extract a phone-like substring
        match = re.search(r'[\+\d][\d\s\-\(\)\.\/\+]+', raw)
        if match:
            phone = match.group(0).strip()

            # If phonenumbers is available, try to parse and format to E.164
            if _HAS_PHONENUMBERS:
                try:
                    # If phone contains a leading +, parse without region
                    if phone.startswith('+'):
                        pn = phonenumbers.parse(phone, None)
                    else:
                        # Fallback region: try to detect from raw text (not implemented) -> default to 'US'
                        pn = phonenumbers.parse(phone, 'US')

                    if phonenumbers.is_valid_number(pn):
                        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
                except Exception:
                    # parsing failed, fall back to raw phone
                    pass

            return phone

        # Fallback: return raw cleaned of excessive whitespace
        return ' '.join(raw.split())
            
    def scrape_keyword(self, keyword: str) -> int:
        """
        Complete scraping workflow for a single keyword.
        
        Args:
            keyword: Search term to scrape
            
        Returns:
            Number of businesses scraped
        """
        try:
            # Search for keyword
            if not self.search_keyword(keyword):
                return 0
                
            # Extract business data
            businesses = self.extract_business_data()
            
            # Save to Excel
            self.save_to_excel(businesses, keyword)
            
            return len(businesses)
            
        except Exception as e:
            self.logger.error(f"Error scraping keyword '{keyword}': {e}")
            return 0
            
    def scrape_multiple_keywords(self, keywords: List[str]):
        """
        Scrape data for multiple keywords.
        
        Args:
            keywords: List of search terms
        """
        total_keywords = len(keywords)
        self.logger.info(f"Starting scraping for {total_keywords} keywords")
        
        results_summary = []
        
        for idx, keyword in enumerate(keywords, 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Processing keyword {idx}/{total_keywords}: {keyword}")
            self.logger.info(f"{'='*60}\n")
            
            try:
                count = self.scrape_keyword(keyword)
                results_summary.append({
                    'Keyword': keyword,
                    'Records': count,
                    'Status': 'Success' if count > 0 else 'No Data'
                })
                
            except Exception as e:
                self.logger.error(f"Failed to process '{keyword}': {e}")
                results_summary.append({
                    'Keyword': keyword,
                    'Records': 0,
                    'Status': 'Failed'
                })
                
            # Add delay between keywords
            time.sleep(self.delay)
            
        # Save summary report
        self.save_summary_report(results_summary)
        
    def save_summary_report(self, results: List[Dict]):
        """
        Save a summary report of the scraping session.
        
        Args:
            results: List of result dictionaries
        """
        try:
            df = pd.DataFrame(results)
            summary_file = self.output_dir / f"scraping_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(summary_file, index=False, engine='openpyxl')
            
            self.logger.info(f"\nSummary report saved to {summary_file}")
            self.logger.info(f"Total keywords processed: {len(results)}")
            self.logger.info(f"Successful: {sum(1 for r in results if r['Status'] == 'Success')}")
            self.logger.info(f"Total records: {sum(r['Records'] for r in results)}")
            
        except Exception as e:
            self.logger.error(f"Error saving summary report: {e}")
            
    def close(self):
        """Close the browser and clean up resources."""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")


def load_keywords_from_csv(csv_file: str) -> List[str]:
    """
    Load keywords from a CSV file.
    
    Args:
        csv_file: Path to CSV file
        
    Returns:
        List of keywords
    """
    try:
        df = pd.read_csv(csv_file)
        # Assume first column contains keywords
        keywords = df.iloc[:, 0].tolist()
        return [str(k).strip() for k in keywords if str(k).strip()]
    except Exception as e:
        logging.error(f"Error loading keywords from CSV: {e}")
        return []


def main():
    """Main execution function."""
    
    # Example keywords - replace with load_keywords_from_csv('keywords.csv')
    keywords = [
        "Cafe near Bakersfield, CA"
        
    ]
    
    # Or load from CSV:
    # keywords = load_keywords_from_csv('keywords.csv')
    
    scraper = None
    
    try:
        # Initialize scraper
        scraper = GoogleMapsScraper(headless=False, delay=3)
        
        # Scrape all keywords
        scraper.scrape_multiple_keywords(keywords)
        
        print("\n" + "="*60)
        print("Scraping completed! Check the 'output' folder for results.")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        
    except Exception as e:
        logging.error(f"Critical error in main execution: {e}")
        
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
