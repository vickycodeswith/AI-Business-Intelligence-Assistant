import plotly.express as px
import pandas as pd


def create_forecast_chart(
    future_x,
    future_y
):

    chart_df = pd.DataFrame({

        "Period": future_x,
        "Sales": future_y

    })

    fig = px.line(
        chart_df,
        x="Period",
        y="Sales",
        markers=True,
        title="Sales Forecast"
    )

    return fig