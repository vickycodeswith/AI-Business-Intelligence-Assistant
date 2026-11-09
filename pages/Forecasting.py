import streamlit as st
from models.forecasting import forecast_series
from charts.forecast_chart import create_forecast_chart
from utils.profiling import profile_dataset
from utils.styles import load_css

st.set_page_config(page_title="Universal AI BI | Forecasting", page_icon="🔮", layout="wide")
load_css()
st.title("🔮 Universal Forecasting")
if "df" not in st.session_state:
    st.warning("Upload a dataset on the Home page first.")
    st.stop()

df = st.session_state["df"]
profile = profile_dataset(df)
metrics = profile["measure_columns"]
dates = profile["datetime_columns"]
if not metrics:
    st.warning("This dataset has no suitable numeric measure to forecast. Forecasting is unavailable for this file, but the other analytics pages can still work.")
    st.stop()

st.write("Choose the numerical measure to forecast. If a date/time column exists, choose it as the time axis. Otherwise, the app uses row order.")
with st.form("forecast_form"):
    metric = st.selectbox("Numerical measure", metrics, index=0)
    date_options = ["Use row order (no date column)"] + dates
    date_choice = st.selectbox("Date/time column", date_options, index=(date_options.index(profile["date_column"]) if profile["date_column"] else 0))
    date_col = None if date_choice.startswith("Use row order") else date_choice
    periods = st.slider("Forecast horizon (future periods)", min_value=1, max_value=30, value=7)
    aggregation = st.selectbox("Combine multiple rows on the same date", ["sum", "mean"], index=0)
    run = st.form_submit_button("Generate forecast")

if run:
    try:
        result = forecast_series(df, metric, date_col, periods=periods, aggregation=aggregation)
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Next predicted {metric}", f"{result['next_value']:,.2f}")
        c2.metric("Forecast periods", result["periods"])
        c3.metric("Training observations", len(result["history_y"]))
        st.caption(f"Method: {result['method']}. This is a simple trend baseline, not a guarantee of future results.")
        chart = create_forecast_chart(
            result["history_x"], result["history_y"],
            result["forecast_x"], result["forecast_y"],
            metric_name=metric,
            date_name=date_col or "Observation",
        )
        st.plotly_chart(chart, use_container_width=True)
        forecast_table = {date_col or "Observation": result["forecast_x"], f"Predicted {metric}": result["forecast_y"]}
        st.dataframe(__import__("pandas").DataFrame(forecast_table), use_container_width=True)
    except Exception as exc:
        st.error(f"Forecast could not be generated: {exc}")
