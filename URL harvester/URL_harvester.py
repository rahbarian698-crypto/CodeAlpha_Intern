"""
Professional Webpage Scraper
============================

This script allows you to fetch the **title** and **meta description** of webpages
and save the results in **CSV** and **JSON** files.

How to Use:
1. Run the script in a Python environment.
2. Paste one or more webpage URLs when prompted.
   - You do NOT need to quote the URLs.
   - You can paste URLs with or without 'http://' or 'https://'.
3. Press Enter after each URL.
4. Type 'done' (or 'exit' in the immediate-fetch version) to finish.
5. The script will fetch the page data and save it to:
   - 'webpage_data.csv' (CSV format)
   - 'webpage_data.json' (JSON format)

Example:
----------
Enter webpage URL (or 'done' to finish): https://github.com
Enter webpage URL (or 'done' to finish): https://www.google.com
Enter webpage URL (or 'done' to finish): done
----------
"""
import os
import requests
from bs4 import BeautifulSoup
import csv
import json

# Output files
CSV_FILE = "webpage_data.csv"
JSON_FILE = "webpage_data.json"

def fetch_page_data(url):
    """Fetch title and meta description of a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[Error] Could not fetch URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("title")
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})

    title = title_tag.text.strip() if title_tag and title_tag.text.strip() else "No Title Found"
    meta_desc = meta_desc_tag.get("content").strip() if meta_desc_tag and meta_desc_tag.get("content") else "No Meta Description"

    return {"url": url, "title": title, "meta_description": meta_desc}

def save_to_csv(data_list, filename=CSV_FILE):
    """Save list of webpage data dictionaries to CSV."""
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["url", "title", "meta_description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for data in data_list:
            writer.writerow(data)
    print(f"Saved {len(data_list)} entries to {filename}")

def save_to_json(data_list, filename=JSON_FILE):
    """Save list of webpage data dictionaries to JSON."""
    existing_data = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

    existing_data.extend(data_list)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(data_list)} entries to {filename}")

def main():
    print("=== Professional Webpage Scraper ===")
    urls = []
    while True:
        url = input("Enter webpage URL (or 'done' to finish): ").strip()
        if not url:  # Ignore empty input
            continue
        if url.lower() == "done":
            break
        if not url.startswith("http"):
            url = "http://" + url
        urls.append(url)

    if not urls:
        print("No URLs entered. Exiting.")
        return

    results = []
    for url in urls:
        data = fetch_page_data(url)
        if data:
            results.append(data)
            print(f"Fetched: {data['title']}")

    if results:
        save_to_csv(results)
        save_to_json(results)
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()