import streamlit as st

from charts.bar_chart import (
    sales_by_product_chart,
    sales_by_region_chart,
    profit_by_product_chart
)

from models.forecasting import (
    forecast_sales
)

from charts.forecast_chart import (
    create_forecast_chart
)
from utils.styles import load_css
load_css()

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

df = st.session_state["df"]

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset first."
    )

    st.stop()

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset from Home page first."
    )

    st.stop()

df = st.session_state["df"]

st.title("📈 Sales Forecasting")

prediction, forecast_data = (
    forecast_sales(df)
)

if prediction:

    st.metric(
        "Predicted Next Period Sales",
        f"{prediction:,.2f}"
    )
    st.info(
    "Forecast generated using Linear Regression.")

    future_x, future_y = forecast_data

    forecast_chart = (
        create_forecast_chart(
            future_x,
            future_y
        )
    )

    st.plotly_chart(
        forecast_chart,
        width="stretch"
    )

st.sidebar.markdown("""
# 🚀 AI BI Assistant

### Navigation

📊 Dashboard

📈 Analytics

🤖 AI Assistant

🔮 Forecasting

---
Built with Gemini AI
""")


st.divider()

st.caption(
    "Built by Vicky Yadav | AI Business Intelligence Assistant"
)