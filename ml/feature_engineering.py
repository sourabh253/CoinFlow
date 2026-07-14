import pandas as pd
from sqlalchemy import create_engine

from config.config import *

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------

query = """
SELECT *
FROM crypto_prices
ORDER BY coin_id, snapshot_time;
"""

df = pd.read_sql(query, engine)

# ---------------------------------
# FEATURE ENGINEERING
# ---------------------------------

# Previous Price
df["previous_price"] = (
    df.groupby("coin_id")["current_price"]
      .shift(1)
)

# Price Difference
df["price_difference"] = (
    df["current_price"] -
    df["previous_price"]
)

# Percentage Return
df["price_return"] = (
    df["price_difference"] /
    df["previous_price"]
) * 100

# Moving Average (3 snapshots)
df["moving_average"] = (
    df.groupby("coin_id")["current_price"]
      .transform(lambda x: x.rolling(3).mean())
)

# Rolling Volatility
df["volatility"] = (
    df.groupby("coin_id")["current_price"]
      .transform(lambda x: x.rolling(3).std())
)

# Volume Change
df["volume_change"] = (
    df.groupby("coin_id")["total_volume"]
      .diff()
)

print(df.head(15))

# Save dataset for ML
df.to_csv(
    "ml/crypto_features.csv",
    index=False
)

print("\nFeature Engineering Completed Successfully!")