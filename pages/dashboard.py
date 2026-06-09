import streamlit as st

from utils.load_data import load_file

from utils.insights import (
    generate_insights,
    generate_recommendations
)

from utils.eda import (
    dataset_info
)

import streamlit as st

from utils.insights import (
    generate_insights,
    generate_recommendations
)

from utils.eda import (
    dataset_info
)
from utils.styles import load_css
load_css()
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Dashboard")

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset from Home page."
    )

    st.stop()

df = st.session_state["df"]


info = dataset_info(df)

st.subheader("Dataset Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", info["rows"])

with col2:
    st.metric("Columns", info["columns"])

with col3:
    st.metric("Missing Values", info["missing_values"])

with col4:
    st.metric("Duplicate Rows", info["duplicate_rows"])

# DATASET PREVIEW

st.subheader("Dataset Preview")

st.dataframe(
    df.head(),
    width="stretch"
    )
# BUSINESS INSIGHTS

st.subheader("Business Insights")

insights = generate_insights(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        insights.get("total_sales", 0)
    )

with col2:
    st.metric(
        "Average Sales",
        insights.get("average_sales", 0)
    )

with col3:
    st.metric(
        "Average Profit",
        insights.get("average_profit", 0)
    )

with col4:
    st.metric(
        "Total Profit",
        insights.get("total_profit", 0)
    )

# KEY BUSINESS FINDINGS

st.subheader("Key Business Findings")

st.write(
    f"🏆 Best Selling Product: "
    f"{insights.get('top_product', 'N/A')}"
)

st.write(
    f"🌍 Highest Revenue Region: "
    f"{insights.get('top_region', 'N/A')}"
)

st.subheader("Executive Recommendations")

recommendations = generate_recommendations(
    insights )


for rec in recommendations:

    st.info(rec)


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