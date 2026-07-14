# test_engine.py

from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:root123@localhost:3306/cryptopulse"
)

try:
    with engine.connect() as conn:
        print("SQLAlchemy Connected!")
except Exception as e:
    print("ERROR:", e)