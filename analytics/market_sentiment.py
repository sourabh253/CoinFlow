import pandas as pd
from sqlalchemy import create_engine
from config.config import *

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

query = """
SELECT
    coin_name,
    price_change_percentage_24h
FROM crypto_prices;
"""

df = pd.read_sql(query, engine)

bullish = len(df[df["price_change_percentage_24h"] > 5])
bearish = len(df[df["price_change_percentage_24h"] < -5])
neutral = len(df) - bullish - bearish

print("\nMARKET SENTIMENT\n")
print(f"Bullish Coins : {bullish}")
print(f"Neutral Coins : {neutral}")
print(f"Bearish Coins : {bearish}")