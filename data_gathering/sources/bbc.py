from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options
import hashlib
import csv
import os
import sys

#Adding options for optimizing scrapping speed with ignoring insecurity warnings
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--headless")  
options.add_argument("--disable-gpu") 
driver = webdriver.Chrome(options=options)

url = "https://www.bbc.com/news/topics/c207p54mdq3t"
driver.get(url)

#Define csv file
csv_file = "news.csv"

# Define the fieldnames of news parameters
fieldnames = ["source", "article_url", "title", "full_text", "date"]

# Set to keep track of seen article hashes
seen_hashes = set()

# Get the number of articles to scrape from command-line arguments
max_articles = int(sys.argv[1]) if len(sys.argv) > 1 else 10
scraped_count = 0

try:
    while scraped_count > max_articles:
        # Wait for the page to load
        time.sleep(2)

        # Parse the current page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find articles on the current page
        for card in soup.find_all('div', {'data-testid': 'liverpool-card'}):
            link_tag = card.find("a")
            if link_tag:
                relative_link = link_tag.get("href")
                if relative_link:
                    # Form the full URL, title and date
                    full_url = f"https://www.bbc.com{relative_link}"
                    title = card.find('h2').text.strip()
                    date = card.find('span', {'data-testid': 'card-metadata-lastupdated'}).text.strip()

                    # Load the full page of article in a new window
                    # Prevent loading of the same page over and over again
                    driver.execute_script("window.open(arguments[0]);", full_url)
                    driver.switch_to.window(driver.window_handles[1])
                    
                    # Parse the article page
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # Collect all sentences from the article
                    # Track sentences appropriately for the type of videos
                    all_sentences = []
                    if relative_link.startswith("/news/videos/"):
                        for section in soup.find_all('div', {'data-testid': 'video-page-video-section'}):
                            for paragraph in section.find_all('p'):
                                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.text.strip())
                                all_sentences.extend(sentences)
                    
                    elif relative_link.startswith("/sport/football/videos/"):
                        for wrapper in soup.find_all('div', {'data-testid': 'reveal-text-wrapper'}):
                            for paragraph in wrapper.find_all('p'):
                                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.text.strip())
                                all_sentences.extend(sentences)
                    else:
                        for text_block in soup.find_all('div', {'data-component': 'text-block'}):
                            for paragraph in text_block.find_all('p'):
                                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.text.strip())
                                all_sentences.extend(sentences)

                    # Filter sentences containing the keyword
                    filtered_sentences = [sentence for sentence in all_sentences if re.search(r'\b\w*turk\w*\b|\bistanbul\b|\bankara\b', sentence, re.IGNORECASE)]

                    # Combine filtered sentences into a single text
                    full_text = " ".join(filtered_sentences)
                    
                    # Append data as a single row
                    row = (
                        "BBC",
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
        
        # Find and click "Next Button" to load new articles with handling exceptions
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="pagination-next-button"]'))
            )
            scraped_count += 1
            next_button.click()
        except Exception as e:
            print(f"Error clicking next button: {e}")
            break
except Exception as e:
    print(f"Error during scraping: {e}")
finally:
    driver.quit()
