import pandas as pd
from sqlalchemy import create_engine
from config.config import *

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

query = """
SELECT
    coin_name,
    symbol,
    current_price,
    price_change_percentage_24h
FROM crypto_prices
ORDER BY price_change_percentage_24h ASC
LIMIT 10;
"""

df = pd.read_sql(query, engine)

print("\nTOP 10 LOSERS\n")
print(df)