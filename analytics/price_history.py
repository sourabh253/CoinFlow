import pandas as pd
from sqlalchemy import create_engine
from config.config import *

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

query = """
SELECT
    coin_id,
    coin_name,
    current_price,
    snapshot_time
FROM crypto_prices
WHERE coin_id = 'bitcoin'
ORDER BY snapshot_time;
"""

df = pd.read_sql(query, engine)

print("\nBITCOIN PRICE HISTORY\n")
print(df)