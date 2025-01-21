from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options
import os
import csv
import sys

#Adding options for optimizing scrapping speed with ignoring insecurity warnings
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration

driver = webdriver.Chrome(options=options)

url = "https://www.theguardian.com/world/turkey"
driver.get(url)

csv_file = 'news.csv'
page_count = 1

# Define the fieldnames (column headers)
fieldnames = ["source", "article_url", "title", "full_text", "date"]

# Set to keep track of seen article hashes
seen_hashes = set()

# Get the number of articles to scrape from command-line arguments
max_articles = int(sys.argv[1]) if len(sys.argv) > 1 else 10
scraped_count = 0

try:
    while scraped_count < max_articles:
        # Wait for the page to load
        time.sleep(2)

        # Parse the current page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sections = soup.find_all('section', {'class': 'dcr-pslr00'})

        for section in sections:
            # Find articles on the current page
            for card in section.find_all('li'):
                link_tag = card.find("a")
                if link_tag:
                    relative_link = link_tag.get("href")
                    if relative_link:
                        # Form the full URL
                        full_url = f"https://www.theguardian.com{relative_link}"
                        title = card.find('h3').text.strip()
       
                        
                        date = card.find('footer').text.strip()
                        driver.execute_script("window.open(arguments[0]);", full_url)
                        driver.switch_to.window(driver.window_handles[1])
                        
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                       
                        # Collect all sentences from the article
                        all_sentences = []
                        for paragraph in soup.find_all('p'):
                            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.text.strip())
                            all_sentences.extend(sentences)

                        # Filter sentences containing the keyword
                        filtered_sentences = [sentence for sentence in all_sentences if re.search(r'\b\w*turk\w*\b|\bistanbul\b|\bankara\b', sentence, re.IGNORECASE)]

                        # Combine filtered sentences into a single text
                        full_text = " ".join(filtered_sentences)

                        # Append data as a single row
                        row = (
                            "The Guardian",
                            full_url,
                            title,
                            full_text,
                            date  # Add logic to extract the publication date if available
                        )

                        # Convert the tuple to a dictionary
                        row_dict = dict(zip(fieldnames, row))

                        # Check if the file exists to decide whether to write headers
                        file_exists = os.path.exists(csv_file)
                        # Open the CSV file in append mode
                        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                            
                            # Create a DictWriter
                            writer = csv.DictWriter(file, fieldnames=fieldnames)

                            # Write the header only if the file does not exist
                            if not file_exists:
                                writer.writeheader()
                            
                            # Write the row to the CSV
                            writer.writerow(row_dict)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

        try:
            scraped_count += 1
            next_link = f"https://www.theguardian.com/world/turkey?page={page_count}"
            driver.get(next_link)
        except Exception as e:
            print(f"Error clicking next button: {e}")
            break
except Exception as e:
    print(f"Error during scraping: {e}")
finally:
    driver.quit()

