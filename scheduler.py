import time
import scraper

INTERVAL_MINUTES = 15

def run():
    print(f"Scheduler started. Running every {INTERVAL_MINUTES} minutes.")

    running_count = 0
    cycles = 0

    while True:
        saved_this_cycle = scraper.scrape_feeds()

        running_count += saved_this_cycle
        cycles += 1

        print(f"{running_count} articles saved total in {cycles} cycle(s).")
        print(f"Waiting {INTERVAL_MINUTES} minutes...")

        time.sleep(INTERVAL_MINUTES * 60)
if __name__ == "__main__":
    run()