"""
Example usage script for Google Maps Scraper
Demonstrates different ways to use the scraper
"""

from maps_scraper import GoogleMapsScraper, load_keywords_from_csv


def example_1_simple_usage():
    """Example 1: Basic usage with a few keywords"""
    print("\n" + "="*60)
    print("Example 1: Simple Usage")
    print("="*60 + "\n")
    
    keywords = [
        "restaurant in Jakarta",
        "coffee shop in Bali",
    ]
    
    scraper = GoogleMapsScraper(headless=False, delay=3)
    
    try:
        scraper.scrape_multiple_keywords(keywords)
        print("\n✓ Scraping completed successfully!")
    finally:
        scraper.close()


def example_2_csv_usage():
    """Example 2: Load keywords from CSV file"""
    print("\n" + "="*60)
    print("Example 2: CSV Usage")
    print("="*60 + "\n")
    
    keywords = load_keywords_from_csv('keywords.csv')
    
    if not keywords:
        print("❌ No keywords found in CSV file")
        return
    
    print(f"Loaded {len(keywords)} keywords from CSV")
    
    scraper = GoogleMapsScraper(headless=False, delay=3)
    
    try:
        scraper.scrape_multiple_keywords(keywords)
        print("\n✓ Scraping completed successfully!")
    finally:
        scraper.close()


def example_3_headless_mode():
    """Example 3: Run in headless mode (background)"""
    print("\n" + "="*60)
    print("Example 3: Headless Mode")
    print("="*60 + "\n")
    
    keywords = ["gym in Surabaya"]
    
    scraper = GoogleMapsScraper(headless=True, delay=3)
    
    try:
        scraper.scrape_multiple_keywords(keywords)
        print("\n✓ Scraping completed successfully in headless mode!")
    finally:
        scraper.close()


def example_4_single_keyword():
    """Example 4: Scrape a single keyword"""
    print("\n" + "="*60)
    print("Example 4: Single Keyword")
    print("="*60 + "\n")
    
    keyword = "bookstore in Semarang"
    
    scraper = GoogleMapsScraper(headless=False, delay=3)
    
    try:
        count = scraper.scrape_keyword(keyword)
        print(f"\n✓ Successfully scraped {count} businesses for '{keyword}'")
    finally:
        scraper.close()


def example_5_custom_delay():
    """Example 5: Use custom delay for slower/careful scraping"""
    print("\n" + "="*60)
    print("Example 5: Custom Delay")
    print("="*60 + "\n")
    
    keywords = ["pharmacy in Medan"]
    
    # Slower scraping with 5 second delays
    scraper = GoogleMapsScraper(headless=False, delay=5)
    
    try:
        scraper.scrape_multiple_keywords(keywords)
        print("\n✓ Scraping completed with custom delay!")
    finally:
        scraper.close()


def main():
    """Run example demonstrations"""
    
    print("\n" + "🗺️ "*30)
    print("Google Maps Scraper - Example Usage")
    print("🗺️ "*30 + "\n")
    
    print("Available examples:")
    print("1. Simple usage with hardcoded keywords")
    print("2. Load keywords from CSV file")
    print("3. Run in headless mode")
    print("4. Scrape a single keyword")
    print("5. Use custom delay")
    print("0. Exit")
    
    while True:
        choice = input("\nSelect an example to run (0-5): ").strip()
        
        if choice == "0":
            print("\nGoodbye! 👋")
            break
        elif choice == "1":
            example_1_simple_usage()
        elif choice == "2":
            example_2_csv_usage()
        elif choice == "3":
            example_3_headless_mode()
        elif choice == "4":
            example_4_single_keyword()
        elif choice == "5":
            example_5_custom_delay()
        else:
            print("❌ Invalid choice. Please select 0-5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
