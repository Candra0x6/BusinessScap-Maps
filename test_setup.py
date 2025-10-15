"""
Test script to verify installation and basic functionality
Run this to ensure everything is set up correctly
"""

import sys
import importlib
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.10 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} detected")
        print("   Required: Python 3.10 or higher")
        return False


def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        importlib.import_module(package_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False


def check_required_packages():
    """Check all required packages"""
    print("\nChecking required packages...")
    
    packages = {
        'selenium': 'Selenium',
        'pandas': 'Pandas',
        'openpyxl': 'OpenPyXL',
    }
    
    all_installed = True
    
    for module_name, display_name in packages.items():
        if not check_package(module_name):
            all_installed = False
    
    return all_installed


def check_chrome():
    """Check if Chrome browser is available"""
    print("\nChecking Chrome browser...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        
        print("✓ Chrome browser and ChromeDriver are working")
        return True
        
    except Exception as e:
        print(f"❌ Chrome browser or ChromeDriver issue: {e}")
        print("   Make sure Chrome is installed")
        return False


def check_project_structure():
    """Check if all required files exist"""
    print("\nChecking project structure...")
    
    required_files = [
        'maps_scraper.py',
        'config.py',
        'examples.py',
        'utils.py',
        'keywords.csv',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"❌ {filename} is missing")
            all_exist = False
    
    return all_exist


def check_output_directory():
    """Check if output directory can be created"""
    print("\nChecking output directory...")
    
    try:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Try to create a test file
        test_file = output_dir / "test.txt"
        test_file.write_text("test")
        test_file.unlink()
        
        print(f"✓ Output directory is accessible: {output_dir.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Cannot create output directory: {e}")
        return False


def check_scraper_import():
    """Check if main scraper module can be imported"""
    print("\nChecking scraper module...")
    
    try:
        from maps_scraper import GoogleMapsScraper, load_keywords_from_csv
        print("✓ Scraper module imported successfully")
        print("✓ GoogleMapsScraper class is available")
        print("✓ load_keywords_from_csv function is available")
        return True
        
    except Exception as e:
        print(f"❌ Cannot import scraper module: {e}")
        return False


def check_keywords_file():
    """Check if keywords.csv is readable"""
    print("\nChecking keywords file...")
    
    try:
        from maps_scraper import load_keywords_from_csv
        
        keywords = load_keywords_from_csv('keywords.csv')
        
        if keywords:
            print(f"✓ keywords.csv is readable")
            print(f"✓ Found {len(keywords)} keywords")
            print(f"  Example keywords: {keywords[:3]}")
            return True
        else:
            print("⚠️  keywords.csv is empty or has no valid keywords")
            return True
            
    except Exception as e:
        print(f"❌ Cannot read keywords.csv: {e}")
        return False


def run_all_checks():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("🔍 Google Maps Scraper - Installation Verification")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Project Structure", check_project_structure),
        ("Output Directory", check_output_directory),
        ("Scraper Module", check_scraper_import),
        ("Keywords File", check_keywords_file),
        ("Chrome Browser", check_chrome),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Error during {check_name} check: {e}")
            results[check_name] = False
        print()
    
    # Summary
    print("="*60)
    print("📊 Verification Summary")
    print("="*60 + "\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {check_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} checks passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 All checks passed! You're ready to start scraping!")
        print("\nNext steps:")
        print("1. Run 'python maps_scraper.py' to start scraping")
        print("2. Or run 'python examples.py' for guided examples")
        print("3. Check 'output/' folder for results")
        return True
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Install Chrome browser from: https://www.google.com/chrome/")
        print("3. Check that all project files are present")
        return False


def main():
    """Main test execution"""
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Critical error during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
