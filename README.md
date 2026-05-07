# Financial News Scraper & Data Pipeline

**Stack:** Python · feedparser · SQLite · collections

---

## What This Is

A lightweight, automated financial news pipeline that scrapes headlines from eight live RSS feeds across equities, crypto, commodities, forex, earnings, and SEC filings — and stores them in a structured SQLite database for downstream analysis and ML model training.

This is not a one-off script. It's a continuously running data collection system designed to feed future projects in sentiment analysis (#5), anomaly detection (#7), and end-to-end ML pipelines (#8).

---

## Why It Exists

Most ML trading models fail not because of bad algorithms — they fail because of bad or insufficient data. This pipeline was built to solve that problem from day one by collecting diverse, timestamped financial headlines at scale before any modeling begins.

The core idea: by the time sentiment analysis and anomaly detection projects start, there will already be weeks of labeled, structured news data ready to train on. The scraper is the shovel. The models are what you dig with it.

---

## Features

- Scrapes 8 RSS feeds across 6 distinct financial categories
- Deduplicates articles automatically via URL uniqueness constraint
- Stores title, source, publish date, and scrape timestamp per article
- Runs on a configurable schedule (default: every 15 minutes)
- Analyzes collected data by source volume, recency, hourly velocity, and keyword frequency
- Keyword groups mapped to ML-relevant categories: macro, markets, earnings, filings, crypto, commodities, international, banks

---

## Data Sources

| Source | Category |
|---|---|
| Yahoo Finance | General markets |
| WSJ Markets | US equities & trading |
| MarketWatch | Real-time market headlines |
| CoinDesk | Crypto |
| Investing.com Commodities | Oil, gold, futures |
| Investing.com Forex | Currency & international markets |
| Investing.com Earnings | Earnings reports & guidance |
| SEC EDGAR | Official filings (10-K, 10-Q, 8-K, S-1) |

---

## Project Structure

```
financial-news-scraper/
├── scraper.py        # Pulls and parses RSS feeds, calls database inserts
├── database.py       # SQLite schema definition and insert logic
├── scheduler.py      # Runs scraper on a timed loop
├── analyze.py        # Query and summarize collected data
└── news.db           # SQLite database (auto-generated, not committed)
```

---

## Setup & Installation

**Prerequisites:** Python 3.8+

```bash
# Clone the repo
git clone https://github.com/erikwoods/financial-news-scraper.git
cd financial-news-scraper

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install feedparser requests
```

---

## Usage

**Initialize the database:**
```bash
python database.py
```

**Run a single scrape:**
```bash
python scraper.py
```

**Start the scheduler (runs every 15 minutes indefinitely):**
```bash
python scheduler.py
```
Stop with `Ctrl+C`.

**Analyze what's been collected:**
```bash
python analyze.py
```

---

## Database Schema

```sql
CREATE TABLE articles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    source      TEXT,
    published   TEXT,
    url         TEXT UNIQUE,
    scraped_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

`url` is unique — duplicate articles across feeds are silently dropped on insert. Both `published` (outlet timestamp) and `scraped_at` (pipeline timestamp) are stored because ML models that correlate news with price movements need to know when news actually hit the market, not just when it was collected.

---

## Sample Output

```
=== Articles by Source ===
Yahoo Finance: 210 articles
WSJ Markets: 45 articles
MarketWatch: 38 articles
CoinDesk: 25 articles
...

=== Recent Headlines ===
Yahoo Finance: Fed holds rates steady, signals two cuts in 2025
MarketWatch: Powell says labor market not a source of significant inflation pressure
WSJ Markets: Heard on the Street's Stock-Picking Series
...

=== Articles in Last Hour ===
34 articles in the last hour

=== Coverage by Topic ===
markets: 87 articles
macro: 64 articles
international: 41 articles
crypto: 28 articles
earnings: 22 articles
commodities: 19 articles
banks: 14 articles
filings: 8 articles
```

---

## Future Development

This pipeline is intentionally designed as infrastructure for future projects:

- **Project #5 — Sentiment Tracker:** Plug a HuggingFace or VADER sentiment model into `analyze.py` to score each headline. The `TODO: sentiment scoring` hook is already in the codebase.
- **Project #7 — Stock Anomaly Detection:** Use collected headlines as feature input alongside price data. Correlate keyword spikes in the `macro` and `markets` groups with price movement anomalies.
- **Project #8 — End-to-End ML Pipeline:** Wrap this scraper as the ingestion layer of a full training pipeline with MLflow experiment tracking.

The `published` timestamp stored per article is specifically preserved for this reason — it enables time-aligned correlation between news events and market data.

---

## Notes

- RSS feeds vary in update frequency. Yahoo Finance updates in near real-time. WSJ and MarketWatch rotate on a slower cycle. Investing.com feeds update roughly hourly.
- Some feeds append tracking parameters to URLs, which can cause near-duplicate articles to slip past the uniqueness constraint. Title-based deduplication is a planned improvement.
- SEC EDGAR feed returns Atom XML rather than standard RSS — `feedparser` handles both formats transparently.

---

## License

MIT
