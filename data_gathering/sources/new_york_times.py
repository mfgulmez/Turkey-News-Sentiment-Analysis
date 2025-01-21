from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import csv
import os
import sys

#Adding options for optimizing scrapping speed with ignoring insecurity warnings
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration
driver = webdriver.Chrome(options=options)

driver.get("https://www.nytimes.com/topic/destination/turkey")

# Track the index of the last scraped news
last_scraped_index = 0  # Initialize as 0 for the first run

# Specify the CSV file name
csv_file = "news.csv"

# Define the fieldnames (column headers)
fieldnames = ["source", "article_url", "title", "full_text", "date"]

# Set to keep track of seen article hashes
seen_hashes = set()

# Get the number of articles to scrape from command-line arguments
max_articles = int(sys.argv[1]) if len(sys.argv) > 1 else 10
scraped_count = 0

while scraped_count < max_articles:
    time.sleep(2)
    # Parse the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('li', {'class': 'css-18yolpw'})

    # Loop through articles starting from the last scraped index
    for i, article in enumerate(articles):
        if i < last_scraped_index:
            continue  # Skip already processed articles
        
        title = article.find('h3').text.strip()
        date = article.find('span', {'data-testid': 'todays-date'}).text.strip()

        head = article.find('a', {'class': 'css-8hzhxf'})  # Extract the link
        link = head['href']
        
        full_url = f"https://www.nytimes.com{link}"
        print(full_url)
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)

        # Collect all sentences from the article
        all_sentences = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        print(title)
        for paragraph in soup.find_all('p'):
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.text.strip())
            all_sentences.extend(sentences)
          
        # Filter sentences containing the keyword
        filtered_sentences = [sentence for sentence in all_sentences if re.search(r'\b\w*turk\w*\b|\bistanbul\b|\bankara\b', sentence, re.IGNORECASE)]

        # Combine filtered sentences into a single text
        full_text = " ".join(filtered_sentences)
        
        # Append data as a single row
        row = (
            "The New York Times",
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
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                
                # Create a DictWriter
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write the header only if the file does not exist
                if not file_exists:
                    writer.writeheader()
                if full_text != "":
                    # Write the row to the CSV
                    writer.writerow(row_dict)

        except Exception as e:
            print("Error appending csv 'Show more':", e)

        scraped_count += 1

        print(f"Scraping article {i + 1}")
        print(f"Link: {link}")
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    # Update the last scraped index
    last_scraped_index = len(articles)
    print(last_scraped_index)
    # Find and click "Show more" button to load new articles
    try:
        show_more_button = driver.find_element(By.XPATH, '//div[@data-testid="load-more-posts"]')
        driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
        time.sleep(1)  # Allow some time for scrolling
    except Exception as e:
        print("Error clicking 'Show more':", e)
        break
driver.quit()
