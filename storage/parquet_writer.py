import pandas as pd

def save_parquet(data, path):
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df.to_parquet(
        path,
        engine="pyarrow",
        compression="snappy",
        index=False
    )
