#!/usr/bin/env bash

set -e

echo "🚀 Twitter Market Intelligence Pipeline"
echo "--------------------------------------"

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "❌ python3 not found. Please install Python 3."
  exit 1
fi

# Check virtual environment
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found."
  echo "👉 Run: python3 -m venv venv"
  exit 1
fi

echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo "🐦 Running pipeline..."
python main.py

echo "✅ Done."
