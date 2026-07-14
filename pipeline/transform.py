import pandas as pd

def transform_crypto_data(df):

    selected_columns = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "total_volume",
        "high_24h",
        "low_24h",
        "price_change_24h",
        "price_change_percentage_24h",
        "circulating_supply",
        "total_supply",
        "ath",
        "atl",
        "last_updated"
    ]

    df = df[selected_columns].copy()

    df.rename(columns={
        "id": "coin_id",
        "name": "coin_name",
        "last_updated": "snapshot_time"
    }, inplace=True)

    # Convert timestamp to MySQL DATETIME format
    df["snapshot_time"] = pd.to_datetime(
        df["snapshot_time"],
        utc=True
    ).dt.strftime("%Y-%m-%d %H:%M:%S")

    return df