import joblib
import pandas as pd
from sqlalchemy import create_engine

from config.config import *

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# -----------------------------------
# LOAD TRAINED MODEL
# -----------------------------------

model = joblib.load("ml/models/random_forest.pkl")


# -----------------------------------
# PREDICT NEXT PRICE
# -----------------------------------

def predict_next_price(coin_id):

    # -----------------------------------
    # LOAD LATEST 3 RECORDS
    # -----------------------------------

    query = f"""
    SELECT *
    FROM crypto_prices
    WHERE coin_id = '{coin_id}'
    ORDER BY snapshot_time DESC
    LIMIT 3
    """

    df = pd.read_sql(query, engine)

    # -----------------------------------
    # CHECK DATA
    # -----------------------------------

    if len(df) < 3:
        raise ValueError(
            f"Not enough historical data for {coin_id}"
        )

    # Oldest -> Newest

    df = df.sort_values("snapshot_time")

    # -----------------------------------
    # FEATURE ENGINEERING
    # -----------------------------------

    previous_price = df.iloc[-2]["current_price"]

    current_price = df.iloc[-1]["current_price"]

    price_difference = current_price - previous_price

    price_return = (
        price_difference / previous_price
    ) * 100

    moving_average = df["current_price"].mean()

    volatility = df["current_price"].std()

    volume_change = (
        df.iloc[-1]["total_volume"]
        - df.iloc[-2]["total_volume"]
    )

    # -----------------------------------
    # MODEL INPUT
    # -----------------------------------

    X = pd.DataFrame({

        "current_price": [current_price],

        "previous_price": [previous_price],

        "price_difference": [price_difference],

        "price_return": [price_return],

        "moving_average": [moving_average],

        "volatility": [volatility],

        "volume_change": [volume_change]

    })

    # -----------------------------------
    # PREDICTION
    # -----------------------------------

    prediction = model.predict(X)[0]

    change = prediction - current_price

    percentage = (change / current_price) * 100

    # -----------------------------------
    # RECOMMENDATION
    # -----------------------------------

    if percentage > 0.5:

        action = "BUY"

    elif percentage < -0.5:

        action = "SELL"

    else:

        action = "HOLD"

    # -----------------------------------
    # CONFIDENCE
    # -----------------------------------

    abs_change = abs(percentage)

    if abs_change > 2:

        confidence = 95

    elif abs_change > 1:

        confidence = 90

    elif abs_change > 0.5:

        confidence = 85

    elif abs_change > 0.2:

        confidence = 80

    else:

        confidence = 75

    return (
        current_price,
        prediction,
        percentage,
        action,
        confidence
    )