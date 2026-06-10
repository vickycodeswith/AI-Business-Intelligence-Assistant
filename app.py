import streamlit as st

from utils.load_data import load_file

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)
from utils.styles import load_css
load_css()

st.markdown("""
<div class="glass-card">

<h1>
🚀 AI Business Intelligence Assistant
</h1>

<p>
Upload data, Analyze trends,
Generate AI insights,
Forecast sales,
and Create executive reports.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("### Upload Your Dataset")


uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file:
    try:
        df = load_file(uploaded_file)
        st.session_state["df"] = df
        st.success(
        f"Dataset Loaded Successfully ({len(df)} rows)")
        
    except Exception as e:

        st.error(
            f"Could not read file: {e}"
        )

        st.stop()

st.markdown("""
Upload your dataset and unlock:

✅ Automated EDA

✅ Business Insights

✅ AI Data Analyst

✅ Executive Reports

✅ Sales Forecasting

✅ Interactive Dashboards
""")


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