import time
import random
import re
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By

from scraper.browser import get_driver

HASHTAGS = ["nifty50", "sensex", "banknifty", "intraday"]
BASE_URL = "https://twitter.com/search?q={query}&src=typed_query&f=live"


def is_login_wall(driver):
    """
    Detect Twitter/X login wall to avoid infinite scrolling.
    """
    url = driver.current_url.lower()

    if "login" in url or "i/flow/login" in url:
        return True

    page_text = driver.page_source.lower()
    indicators = [
        "sign in to x",
        "log in to x",
        "join x today",
        "create an account"
    ]

    return any(indicator in page_text for indicator in indicators)


def parse_tweet(tweet):
    try:
        text = tweet.find_element(
            By.XPATH, ".//div[2]//div[2]//div[1]"
        ).text

        username = tweet.find_element(
            By.XPATH, ".//span[contains(text(),'@')]"
        ).text

        timestamp = tweet.find_element(
            By.TAG_NAME, "time"
        ).get_attribute("datetime")

        likes_el = tweet.find_elements(
            By.XPATH, ".//div[@data-testid='like']"
        )
        likes = int(likes_el[0].text) if likes_el and likes_el[0].text.isdigit() else 0

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

    try:
        for tag in HASHTAGS:
            driver.get(BASE_URL.format(query=f"%23{tag}"))
            time.sleep(5)

            # 🚨 Login wall detection (FAIL FAST)
            if is_login_wall(driver):
                raise RuntimeError(
                    "Twitter/X login wall detected. "
                    "Disable headless mode or run with an authenticated session."
                )

            scrolls = 0
            empty_rounds = 0

            while scrolls < 50:
                tweets = driver.find_elements(
                    By.XPATH, "//article[@role='article']"
                )

                if not tweets:
                    empty_rounds += 1
                    if empty_rounds >= 3:
                        break
                else:
                    empty_rounds = 0

                for tweet in tweets:
                    if len(tweets_data) >= limit:
                        return tweets_data

                    data = parse_tweet(tweet)
                    if not data:
                        continue

                    ts = datetime.fromisoformat(
                        data["timestamp"].replace("Z", "")
                    )
                    if ts < since_time:
                        continue

                    key = hash(data["content"] + data["username"])
                    if key in seen:
                        continue

                    seen.add(key)
                    tweets_data.append(data)

                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                scrolls += 1
                time.sleep(random.uniform(2, 5))

    finally:
        driver.quit()

    return tweets_data
