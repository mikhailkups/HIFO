import pandas as pd

# Define a function to calculate the capital gains using the HIFO method
def calculate_hifo_capital_gains(buy_transactions, sell_transactions):
    # Create a dataframe to store the buy and sell transactions
    df = pd.DataFrame(columns=["date", "type", "quantity", "price"])

    # Add the buy and sell transactions to the dataframe
    for tx in buy_transactions:
        df = df.append({"date": tx["date"], "type": "buy", "quantity": tx["quantity"], "price": tx["price"]}, ignore_index=True)

    for tx in sell_transactions:
        df = df.append({"date": tx["date"], "type": "sell", "quantity": tx["quantity"], "price": tx["price"]}, ignore_index=True)

    # Sort the transactions by date
    df = df.sort_values(by="date")

    # Initialize the capital gains and the quantity of the asset owned
    capital_gains = 0
    quantity_owned = 0

    # Iterate through the transactions
    for index, row in df.iterrows():
        if row["type"] == "buy":
            # If it's a buy transaction, add the quantity to the quantity owned
            quantity_owned += row["quantity"]
        else:
            # If it's a sell transaction, calculate the capital gains using the HIFO method
            quantity_sold = row["quantity"]
            remaining_quantity = quantity_sold
            cost_basis = 0

            # Iterate through the buy transactions in reverse order
            for i, r in df.loc[:index].sort_values(by="date", ascending=False).iterrows():
                if r["type"] == "buy":
                    # Calculate the quantity to use for this transaction
                    quantity_to_use = min(r["quantity"], remaining_quantity)
                    remaining_quantity -= quantity_to_use

                    # Calculate the cost basis for this quantity
                    cost_basis += quantity_to_use * r["price"]

                    # If we've used all the quantity sold, we can stop iterating
                    if remaining_quantity == 0:
                        break

            # Calculate the capital gains for this sell transaction
            proceeds = quantity_sold * row["price"]
            basis = cost_basis / quantity_sold
            gain = proceeds - basis
            capital_gains += gain

            # Reduce the quantity owned by the quantity sold
            quantity_owned -= quantity_sold

    # Return the total capital gains
    return capital_gains
