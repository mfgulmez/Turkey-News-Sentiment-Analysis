from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
options.add_argument("--headless")  
options.add_argument("--disable-gpu") 
driver = webdriver.Chrome(options=options)

driver.get("https://www.aljazeera.com/where/turkey/")

# Track the index of the last scraped news
last_scraped_index = 0 

# Specify the CSV file name
csv_file = "news.csv"

# Define the fieldnames of news parameters
fieldnames = ["source", "article_url", "title", "full_text", "date"]

# Set to keep track of seen article hashes
seen_hashes = set()

# Get the number of articles to scrape from command-line arguments
max_articles = int(sys.argv[1]) if len(sys.argv) > 1 else 10
scraped_count = 0
while scraped_count < max_articles:
    #Wait for page to be loaded
    time.sleep(2)
    # Parse the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Parse article elements 
    articles = soup.find_all('article', {'class': 'u-clickable-card'})

    # Iterate through articles with counting scrappings 
    # Track which article to continue when page loads more
    for i, article in enumerate(articles):

        if i < last_scraped_index:
            continue  # Skip already processed articles

        # Getting the head with decomposition of title and link
        head = article.find('a', {'class': 'u-clickable-card__link'})  
        link = head['href']
        title = head.text.strip()
        full_url = f"https://www.aljazeera.com/where/turkey{link}"

        # Load the full page of article in a new window
        # Prevent loading of the same page over and over again
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)

        # Parse the article page defining all sentences to be filtered
        all_sentences = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Getting date time
        date = soup.find('span', {'aria-hidden': 'true'}).text.strip()

        # Splitting the sentences from text with appropriate regex while containing to array
        for paragraph in soup.find_all('p'):
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph.text.strip())
            all_sentences.extend(sentences)
        
        # Filter sentences containing the keyword
        filtered_sentences = [sentence for sentence in all_sentences if re.search(r'\b\w*turk\w*\b|\bistanbul\b|\bankara\b', sentence, re.IGNORECASE)]

        # Combine filtered sentences into a single text
        full_text = " ".join(filtered_sentences)
        
        # Append data as a single row
        row = (
            "AlJazeera",
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

        print(f"Scraping article {i + 1}")
        print(f"Link: {link}")
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    # Update the last scraped index
    last_scraped_index = len(articles)

    # Find and click "Show more" button to load new articles with handling exceptions
    try:
        show_more_button = driver.find_element(By.XPATH, '//button[@data-testid="show-more-button"]')
        driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
        time.sleep(1)  # Allow some time for scrolling
        scraped_count += 1
        show_more_button.click()

    except Exception as e:
        print("Error clicking 'Show more':", e)
        break
driver.quit()
