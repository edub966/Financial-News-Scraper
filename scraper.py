import feedparser
import database

FEEDS = {
    "MarketWatch": "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "WSJ Markets": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
    "Investing Commodities/Futures": "https://www.investing.com/rss/news_11.rss",
    "Investing Forex": "https://www.investing.com/rss/news_1.rss",
    "Investing Earnings": "https://www.investing.com/rss/news_1062.rss",
    "Investing SEC Filings": "https://www.investing.com/rss/news_1064.rss",
    "SEC Current Filings": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&owner=include&count=40&output=atom",
}

def scrape_feeds():
    total_saved = 0

    for source, url in FEEDS.items():
        print(f"Scraping {source}...")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", "")

            saved = database.insert_article(title, source, published, link)
            if saved:
                total_saved += 1

    print(f"Done. Saved {total_saved} articles.")


if __name__ == "__main__":
    database.init_db()
    scrape_feeds()