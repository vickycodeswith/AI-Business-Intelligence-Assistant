import streamlit as st

from utils.eda import (
    column_information,
    column_categories,
    statistical_summary
)
from utils.styles import load_css
load_css()

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)
st.title("📈 Advanced Analytics")

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset from Home page first."
    )

    st.stop()

df = st.session_state["df"]
# COLUMN INFORMATION

st.subheader("Column Information")

column_info = column_information(df)

st.dataframe(

    column_info,
    width="stretch"
    )

# NUMERICAL & CATEGORICAL

numerical_cols, categorical_cols = column_categories(df)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Numerical Columns")

    st.write(numerical_cols)

with col2:

    st.subheader("Categorical Columns")

    st.write(categorical_cols)

# STATISTICAL SUMMARY

st.subheader("Statistical Summary")

summary = statistical_summary(df)

st.dataframe(
    summary,
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