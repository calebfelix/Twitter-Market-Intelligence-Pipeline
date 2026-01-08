from logs.logger import setup_logger
from scraper.twitter_scraper import scrape_tweets
from processing.cleaner import clean_text
from storage.parquet_writer import save_parquet
from analysis.signals import generate_signal
import pandas as pd

logger = setup_logger("main")

if __name__ == "__main__":
    logger.info("Pipeline started")

    tweets = scrape_tweets(limit=5)
    logger.info(f"Scraped {len(tweets)} tweets")

    logger.info("Cleaning text")
    for t in tweets:
        t["content"] = clean_text(t["content"])

    logger.info("Saving data to Parquet")
    save_parquet(tweets, "data/processed/tweets.parquet")

    logger.info("Generating trading signals")
    df = pd.DataFrame(tweets)
    _, ci = generate_signal(df)

    logger.info(f"Signal Mean & CI: {ci}")
    logger.info("Pipeline finished successfully")
