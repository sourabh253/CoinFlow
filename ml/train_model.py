import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("ml/crypto_features.csv")

# -----------------------------------
# ONLY BITCOIN
# -----------------------------------

df = df[df["coin_id"] == "bitcoin"].copy()

# -----------------------------------
# REMOVE NaN VALUES
# -----------------------------------

df.dropna(inplace=True)

# -----------------------------------
# CREATE TARGET
# -----------------------------------

df["target"] = df["current_price"].shift(-1)

df.dropna(inplace=True)

# -----------------------------------
# FEATURES
# -----------------------------------

X = df[
    [
        "current_price",
        "previous_price",
        "price_difference",
        "price_return",
        "moving_average",
        "volatility",
        "volume_change"
    ]
]

y = df["target"]

# -----------------------------------
# TIME SERIES SPLIT
# -----------------------------------

tscv = TimeSeriesSplit(n_splits=5)

for train_index, test_index in tscv.split(X):

    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]

    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]

# -----------------------------------
# MODEL
# -----------------------------------

model = LinearRegression()

model.fit(X_train, y_train)

# -----------------------------------
# PREDICTIONS
# -----------------------------------

predictions = model.predict(X_test)

# -----------------------------------
# METRICS
# -----------------------------------

mae = mean_absolute_error(y_test, predictions)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print("="*50)

print("MODEL PERFORMANCE")

print("="*50)

print(f"MAE  : {mae:.4f}")

print(f"RMSE : {rmse:.4f}")

print(f"R²   : {r2:.4f}")

print("="*50)

# -----------------------------------
# SAVE MODEL
# -----------------------------------

joblib.dump(
    model,
    "ml/models/bitcoin_model.pkl"
)

print("\nModel Saved Successfully!")