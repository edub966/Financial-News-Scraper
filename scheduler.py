import time
import scraper

INTERVAL_MINUTES = 15

def run():
    print(f"Scheduler started. Running every {INTERVAL_MINUTES} minutes.")
    while True:
        scraper.scrape_feeds()
        print(f"Waiting {INTERVAL_MINUTES} minutes...")
        time.sleep(INTERVAL_MINUTES*60)

if __name__ == "__main__":
    run()