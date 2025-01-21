import argparse
import subprocess

def scrape_news(source, count):
    """
    Scrape news from a specific source using a subprocess to run the respective scraper.
    
    Args:
    - source (str): The name of the source ("nyt", "bbc", "alj" and "gua").
    - count (int): Number of articles to scrape.
    """
    if source == "nyt":
        script = "sources/new_york_times.py"

    elif source == "sources/bbc.py":
        script = "bbc.py"

    elif source == "alj":
        script = "sources/aljazeera.py"

    elif source == "gua":
        script = "sources/guardian.py"
    else:
        print(f"Unknown source: {source}")
        return
    
    print(f"Scraping {count} articles from {source}...")
    subprocess.run(["python", script, str(count)])

def main():
    parser = argparse.ArgumentParser(description="News Scraper")
    parser.add_argument(
        "--nyt", type=int, default=100,
        help="Number of news articles to scrape from The New York Times"
    )
    parser.add_argument(
        "--bbc", type=int, default=100,
        help="Number of news articles to scrape from BBC"
    )

    parser.add_argument(
        "--alj", type=int, default=100,
        help="Number of news articles to scrape from AlJazeera"
    )

    parser.add_argument(
        "--gua", type=int, default=100,
        help="Number of news articles to scrape from The Guardian"
    )

    args = parser.parse_args()
    
    if args.nyt > 0:
        scrape_news("nyt", args.nyt)

    if args.bbc > 0:
        scrape_news("bbc", args.bbc)

    if args.alj > 0:
        scrape_news("alj", args.alj)
    
    if args.gua > 0:
        scrape_news("gua", args.gua)
        
if __name__ == "__main__":
    main()
