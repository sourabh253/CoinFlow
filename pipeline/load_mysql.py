from sqlalchemy import create_engine
from config.config import *
from config.config import *

print("USER =", MYSQL_USER)
print("PASSWORD =", MYSQL_PASSWORD)
print("HOST =", MYSQL_HOST)
print("DB =", MYSQL_DB)
from pipeline.fetch_data import fetch_crypto_data
from pipeline.transform import transform_crypto_data

from urllib.parse import quote_plus

# Encode password safely
password = quote_plus(MYSQL_PASSWORD)

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

print("Fetching data...")

df = fetch_crypto_data()

print("Transforming data...")

df = transform_crypto_data(df)

print(df.head())

print("\nTesting Database Connection...")

try:
    with engine.connect() as conn:
        print("Database Connected Successfully!")
except Exception as e:
    print("Database Connection Failed!")
    print(e)
    exit()

print("\nLoading Data into MySQL...")

try:
    df.to_sql(
        "crypto_prices",
        con=engine,
        if_exists="append",
        index=False
    )

    print("Data inserted successfully!")

except Exception as e:
    print("Data Insert Failed!")
    print(e)