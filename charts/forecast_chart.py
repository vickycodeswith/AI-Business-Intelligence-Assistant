import pandas as pd
import plotly.express as px


def create_forecast_chart(history_x, history_y, forecast_x=None, forecast_y=None, metric_name="Value", date_name="Period"):
    history = pd.DataFrame({date_name: history_x, metric_name: history_y})
    history["Series"] = "Historical"
    frames = [history]
    if forecast_x is not None and forecast_y is not None:
        future = pd.DataFrame({date_name: forecast_x, metric_name: forecast_y})
        future["Series"] = "Forecast"
        frames.append(future)
    chart_df = pd.concat(frames, ignore_index=True)
    return px.line(chart_df, x=date_name, y=metric_name, color="Series", markers=True,
                   title=f"{metric_name}: historical data and forecast")
