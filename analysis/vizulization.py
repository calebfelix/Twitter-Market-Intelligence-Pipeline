import matplotlib.pyplot as plt

def plot_signal(df):
    sampled = df.sample(frac=0.1)
    plt.plot(sampled["signal"].rolling(20).mean())
    plt.title("Market Sentiment Signal")
    plt.xlabel("Samples")
    plt.ylabel("Signal Strength")
    plt.show()
