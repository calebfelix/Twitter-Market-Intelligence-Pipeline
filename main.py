from scraper.twitter_scraper import scrape_tweets
from processing.cleaner import clean_text
from storage.parquet_writer import save_parquet
from analysis.signals import generate_signal
import pandas as pd

print("🚀 Starting Twitter Market Intelligence Pipeline...")

if __name__ == "__main__":
    print("🐦 Scraping tweets...")
    tweets = scrape_tweets(limit=2000)

    print(f"✅ Scraped {len(tweets)} tweets")

    print("🧼 Cleaning tweets...")
    for t in tweets:
        t["content"] = clean_text(t["content"])

    print("💾 Saving to parquet...")
    save_parquet(tweets, "data/processed/tweets.parquet")

    print("📊 Generating signals...")
    df = pd.DataFrame(tweets)
    df, ci = generate_signal(df)

    print("📈 Signal Mean & CI:", ci)
    print("✅ Pipeline finished.")
