"""
Utility functions for Google Maps Scraper
Helper functions for data processing and analysis
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict
import json


def merge_excel_files(output_dir: str = "output", output_file: str = "merged_results.xlsx"):
    """
    Merge all Excel files in output directory into a single file.
    
    Args:
        output_dir: Directory containing Excel files
        output_file: Name for merged output file
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"❌ Output directory '{output_dir}' not found")
        return
    
    excel_files = list(output_path.glob("*.xlsx"))
    
    # Filter out summary files
    excel_files = [f for f in excel_files if "summary" not in f.name.lower()]
    
    if not excel_files:
        print(f"❌ No Excel files found in '{output_dir}'")
        return
    
    print(f"Found {len(excel_files)} Excel files to merge")
    
    merged_data = []
    
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            df['Source_Keyword'] = file.stem  # Add source keyword column
            merged_data.append(df)
            print(f"✓ Loaded {len(df)} records from {file.name}")
        except Exception as e:
            print(f"❌ Error loading {file.name}: {e}")
    
    if merged_data:
        merged_df = pd.concat(merged_data, ignore_index=True)
        output_path_file = output_path / output_file
        merged_df.to_excel(output_path_file, index=False, engine='openpyxl')
        print(f"\n✓ Merged {len(merged_df)} total records into {output_path_file}")
    else:
        print("❌ No data to merge")


def analyze_results(output_dir: str = "output"):
    """
    Analyze scraping results and generate statistics.
    
    Args:
        output_dir: Directory containing Excel files
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"❌ Output directory '{output_dir}' not found")
        return
    
    excel_files = list(output_path.glob("*.xlsx"))
    excel_files = [f for f in excel_files if "summary" not in f.name.lower()]
    
    if not excel_files:
        print(f"❌ No Excel files found in '{output_dir}'")
        return
    
    print("\n" + "="*60)
    print("📊 Scraping Results Analysis")
    print("="*60 + "\n")
    
    total_businesses = 0
    keywords_with_data = 0
    websites_found = 0
    phones_found = 0
    
    stats = []
    
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            count = len(df)
            total_businesses += count
            
            if count > 0:
                keywords_with_data += 1
            
            websites = df['Website'].notna().sum() if 'Website' in df.columns else 0
            phones = df['Phone'].notna().sum() if 'Phone' in df.columns else 0
            
            websites_found += websites
            phones_found += phones
            
            stats.append({
                'Keyword': file.stem,
                'Businesses': count,
                'With_Website': websites,
                'With_Phone': phones,
                'Completeness': f"{((websites + phones) / (count * 2) * 100):.1f}%" if count > 0 else "0%"
            })
            
        except Exception as e:
            print(f"❌ Error analyzing {file.name}: {e}")
    
    # Print summary
    print(f"Total keywords processed: {len(excel_files)}")
    print(f"Keywords with data: {keywords_with_data}")
    print(f"Total businesses found: {total_businesses}")
    print(f"Businesses with website: {websites_found} ({websites_found/total_businesses*100:.1f}%)" if total_businesses > 0 else "N/A")
    print(f"Businesses with phone: {phones_found} ({phones_found/total_businesses*100:.1f}%)" if total_businesses > 0 else "N/A")
    
    # Print detailed stats
    print("\n" + "="*60)
    print("Detailed Statistics by Keyword")
    print("="*60 + "\n")
    
    stats_df = pd.DataFrame(stats)
    print(stats_df.to_string(index=False))
    
    # Save stats to file
    stats_file = output_path / "analysis_report.xlsx"
    stats_df.to_excel(stats_file, index=False, engine='openpyxl')
    print(f"\n✓ Analysis report saved to {stats_file}")


def export_to_json(output_dir: str = "output", json_file: str = "all_results.json"):
    """
    Export all Excel results to a single JSON file.
    
    Args:
        output_dir: Directory containing Excel files
        json_file: Name for JSON output file
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"❌ Output directory '{output_dir}' not found")
        return
    
    excel_files = list(output_path.glob("*.xlsx"))
    excel_files = [f for f in excel_files if "summary" not in f.name.lower()]
    
    if not excel_files:
        print(f"❌ No Excel files found in '{output_dir}'")
        return
    
    all_data = {}
    
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            keyword = file.stem
            all_data[keyword] = df.to_dict('records')
            print(f"✓ Exported {len(df)} records from {file.name}")
        except Exception as e:
            print(f"❌ Error exporting {file.name}: {e}")
    
    json_path = output_path / json_file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ All results exported to {json_path}")


def filter_businesses_with_websites(output_dir: str = "output"):
    """
    Create a filtered Excel file containing only businesses with websites.
    
    Args:
        output_dir: Directory containing Excel files
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"❌ Output directory '{output_dir}' not found")
        return
    
    excel_files = list(output_path.glob("*.xlsx"))
    excel_files = [f for f in excel_files if "summary" not in f.name.lower()]
    
    filtered_data = []
    
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            df['Source_Keyword'] = file.stem
            
            # Filter only businesses with websites
            df_with_websites = df[df['Website'].notna() & (df['Website'] != '')]
            
            if not df_with_websites.empty:
                filtered_data.append(df_with_websites)
                print(f"✓ Found {len(df_with_websites)} businesses with websites in {file.name}")
        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
    
    if filtered_data:
        merged_df = pd.concat(filtered_data, ignore_index=True)
        output_file = output_path / "businesses_with_websites.xlsx"
        merged_df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"\n✓ Saved {len(merged_df)} businesses with websites to {output_file}")
    else:
        print("❌ No businesses with websites found")


def main():
    """Main utility menu"""
    
    print("\n" + "🛠️ "*30)
    print("Google Maps Scraper - Utilities")
    print("🛠️ "*30 + "\n")
    
    while True:
        print("\nAvailable utilities:")
        print("1. Merge all Excel files")
        print("2. Analyze results")
        print("3. Export to JSON")
        print("4. Filter businesses with websites")
        print("0. Exit")
        
        choice = input("\nSelect a utility (0-4): ").strip()
        
        if choice == "0":
            print("\nGoodbye! 👋")
            break
        elif choice == "1":
            merge_excel_files()
        elif choice == "2":
            analyze_results()
        elif choice == "3":
            export_to_json()
        elif choice == "4":
            filter_businesses_with_websites()
        else:
            print("❌ Invalid choice. Please select 0-4.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
