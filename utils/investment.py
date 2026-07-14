def simulate_investment(
    investment_amount,
    current_price,
    predicted_price
):
    """
    Simulate investment based on current and predicted price.
    """

    coins = investment_amount / current_price

    future_value = coins * predicted_price

    profit = future_value - investment_amount

    roi = (profit / investment_amount) * 100

    if profit > 0:
        recommendation = "BUY"

    elif profit < 0:
        recommendation = "SELL"

    else:
        recommendation = "HOLD"

    return {
        "coins": coins,
        "future_value": future_value,
        "profit": profit,
        "roi": roi,
        "recommendation": recommendation
    }