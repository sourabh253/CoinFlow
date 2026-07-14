import joblib
import pandas as pd

# Load trained model
model = joblib.load("ml/models/random_forest.pkl")

feature_names = [
    "Current Price",
    "Previous Price",
    "Price Difference",
    "Price Return",
    "Moving Average",
    "Volatility",
    "Volume Change"
]

importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance)