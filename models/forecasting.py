from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


def forecast_sales(df):

    if "Sales" not in df.columns:
        return None, None

    sales_data = (
        df.groupby(df.index)["Sales"]
        .sum()
        .reset_index(drop=True)
    )

    X = np.arange(len(sales_data)).reshape(-1, 1)

    y = sales_data.values

    model = LinearRegression()

    model.fit(X, y)

    next_period = np.array([[len(sales_data)]])

    prediction = model.predict(next_period)[0]

    future_x = np.append(
        X.flatten(),
        len(sales_data)
    )

    future_y = np.append(
        y,
        prediction
    )

    return prediction, (future_x, future_y)

