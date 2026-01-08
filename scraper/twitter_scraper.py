import time
import random
import re
from datetime import datetime, timedelta
from collections import deque

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from scraper.browser import get_driver

HASHTAGS = ["nifty50", "sensex", "banknifty", "intraday"]
BASE_URL = "https://twitter.com/search?q={query}&src=typed_query&f=live"

def parse_tweet(tweet):
    try:
        text = tweet.find_element(By.XPATH, ".//div[2]//div[2]//div[1]").text
        username = tweet.find_element(By.XPATH, ".//span[contains(text(),'@')]").text
        timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")

        stats = tweet.find_elements(By.XPATH, ".//div[@data-testid='like']")
        likes = int(stats[0].text) if stats else 0

        hashtags = re.findall(r"#\w+", text)
        mentions = re.findall(r"@\w+", text)

        return {
            "username": username,
            "timestamp": timestamp,
            "content": text,
            "likes": likes,
            "hashtags": hashtags,
            "mentions": mentions,
        }
    except Exception:
        return None

def scrape_tweets(limit=2000):
    driver = get_driver()
    tweets_data = []
    seen = set()

    since_time = datetime.utcnow() - timedelta(hours=24)

    for tag in HASHTAGS:
        driver.get(BASE_URL.format(query=f"%23{tag}"))
        time.sleep(5)

        scrolls = 0
        while len(tweets_data) < limit and scrolls < 50:
            tweets = driver.find_elements(By.XPATH, "//article[@role='article']")

            for tweet in tweets:
                data = parse_tweet(tweet)
                if not data:
                    continue

                ts = datetime.fromisoformat(data["timestamp"].replace("Z", ""))
                if ts < since_time:
                    continue

                key = hash(data["content"] + data["username"])
                if key in seen:
                    continue

                seen.add(key)
                tweets_data.append(data)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scrolls += 1
            time.sleep(random.uniform(2, 5))

    driver.quit()
    return tweets_data
