# Twitter Market Intelligence Pipeline

A Python-based data pipeline that scrapes recent market-related tweets from Twitter/X (without using the official API), processes the data, and prepares it for downstream analysis.

This project is designed as a **proof-of-concept** to demonstrate pipeline architecture, defensive scraping, and real-world failure handling.

---

## 📌 Features

- Scrapes recent tweets for market-related hashtags:
  - `#nifty50`
  - `#sensex`
  - `#banknifty`
  - `#intraday`
- Simulates human browsing behavior using Selenium
- Filters tweets from the last 24 hours
- Removes duplicates
- Extracts structured fields:
  - Username
  - Timestamp
  - Content
  - Likes
  - Hashtags
  - Mentions
- Detects Twitter/X login walls and exits gracefully
- Modular, readable project structure

---

## 🏗️ Project Structure

```
twitter-market-intel/
├── main.py
├── run.sh
├── scraper/
│   ├── browser.py
│   └── twitter_scraper.py
├── processing/
├── analysis/
├── storage/
├── logs/
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

- Python **3.11** (recommended)
- Google Chrome (installed locally)
- Linux environment

> ⚠️ Python 3.13 + Selenium may be unstable. Python 3.11 is recommended for reliability.

---

## 🚀 Setup & Run

### 1️⃣ Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the pipeline

```bash
python main.py 
```

Or using the helper script:

```bash
chmod +x run.sh
./run.sh
```

---

## ⚠️ Twitter/X Access Limitation

Twitter/X employs anti-bot protections that may present a **login wall**, especially in headless or unauthenticated sessions.

This pipeline:
- **Detects login walls**
- **Fails fast with a clear error**
- Avoids infinite waits or silent failures

> Authentication via session reuse or official APIs would be required for a production-grade system.  
> This was intentionally not implemented to stay within ethical and assignment constraints.

---

## 🧠 Design Decisions

- **No Twitter API usage** (as per assignment requirement)
- **No automated login or credential handling**
- Human-like scrolling with randomized delays
- Defensive error handling for unstable external dependencies
- Modular pipeline design for extensibility

---

## 📈 Future Improvements

- Authenticated scraping via session reuse (cookie-based)
- Concurrency across hashtags
- Retry and backoff strategies
- Persistent storage (Parquet / database)
- Sentiment scoring and signal aggregation


## 👤 Author

Caleb Felix
