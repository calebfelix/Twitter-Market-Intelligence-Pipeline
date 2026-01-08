import numpy as np

KEYWORDS = {
    "bullish": ["breakout", "buy", "support", "long"],
    "bearish": ["sell", "resistance", "crash", "short"]
}

def keyword_score(text):
    score = 0
    for k in KEYWORDS["bullish"]:
        if k in text.lower():
            score += 1
    for k in KEYWORDS["bearish"]:
        if k in text.lower():
            score -= 1
    return score

def generate_signal(df):
    df["engagement"] = df["likes"].fillna(0)
    df["keyword_bias"] = df["content"].apply(keyword_score)

    df["signal"] = (
        0.5 * df["keyword_bias"] +
        0.5 * (df["engagement"] / (df["engagement"].max() + 1))
    )

    mean = df["signal"].mean()
    std = df["signal"].std()

    return df, (mean, mean - std, mean + std)
