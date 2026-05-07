import sqlite3
import database
from collections import Counter
import re

KEYWORD_GROUPS = {
    "macro": [
        "fed", "rate", "rates", "inflation", "recession", "gdp",
        "jobs", "payrolls", "unemployment", "cpi", "ppi"
    ],

    "markets": [
        "market", "stock", "stocks", "bond", "bonds", "yield",
        "treasury", "nasdaq", "dow", "s&p", "vix", "rally", "selloff"
    ],

    "earnings": [
        "earnings", "revenue", "profit", "sales", "eps",
        "guidance", "forecast", "quarter", "results"
    ],

    "filings": [
        "sec", "filing", "10-k", "10-q", "8-k", "s-1",
        "ipo", "disclosure"
    ],

    "crypto": [
        "crypto", "bitcoin", "btc", "ethereum", "eth",
        "blockchain", "stablecoin", "defi", "token", "coinbase"
    ],

    "commodities": [
        "oil", "crude", "brent", "wti", "gold", "silver",
        "natural gas", "futures", "commodities", "opec"
    ],

    "international": [
        "asia", "china", "japan", "europe", "uk", "germany",
        "yen", "euro", "dollar", "forex", "currency", "ecb", "boj"
    ],

    "banks": [
        "bank", "banks", "jpmorgan", "goldman", "morgan stanley",
        "citigroup", "wells fargo", "regional banks"
    ]
}

def source_article_count():
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source, COUNT(*) as count
        FROM articles
        GROUP BY source
        ORDER BY count DESC
    """)

    results = cursor.fetchall()
    conn.close()

    for source, count in results:
        print(f"{source}: {count} articles")

def recent_headlines():
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, source
        FROM articles
        ORDER BY scraped_at DESC
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()

    for title, source in results:
        print(f"{source}: {title}")

def articles_perHour():
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as count
        FROM articles
        WHERE scraped_at >= datetime('now', '-1 hour')
    """)

    results = cursor.fetchall()
    conn.close()

    count = results[0][0]
    print(f"{count} articles per hour")

def keywords():
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title
        FROM articles
    """)

    results = cursor.fetchall()
    conn.close()

    group_counts = Counter()

    for (title,) in results:
        title_lower = title.lower()
        for group, words in KEYWORD_GROUPS.items():
            for word in words:
                if word in title_lower:
                    group_counts[group] += 1
                    break

    print("\n=== Coverage by Topic ===")
    for group, count in group_counts.most_common():
        print(f"{group}: {count} articles")


if __name__ == "__main__":
    database.init_db()

    print("=== Articles by Source ===")
    source_article_count()

    print("\n=== Recent Headlines ===")
    recent_headlines()

    print("\n=== Articles in Last Hour ===")
    articles_perHour()

    keywords()





