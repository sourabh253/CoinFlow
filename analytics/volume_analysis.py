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
    total_volume
FROM crypto_prices
ORDER BY total_volume DESC
LIMIT 10;
"""

df = pd.read_sql(query, engine)

print("\nTOP VOLUME COINS\n")
print(df)