# Twitter Market Intelligence System

A real-time data collection and analysis pipeline for Indian stock market sentiment using Twitter/X data.

## Features
- Selenium-based Twitter/X scraping (no paid APIs)
- Indian market hashtag focus (#nifty50, #sensex, #banknifty, #intraday)
- Unicode-safe text cleaning (Hindi/Hinglish supported)
- Deduplication and Parquet storage
- Text-to-signal conversion for algorithmic trading
- Memory-efficient analysis and visualization

## Setup (Linux)

```bash
python3 -m venv venv
chmod +x run.sh
./run.sh
