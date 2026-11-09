import streamlit as st

from utils.load_data import load_file
from utils.profiling import profile_dataset
from utils.styles import load_css

st.set_page_config(
    page_title="Universal AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide",
)
load_css()

st.markdown(
    """
    <div class="glass-card">
      <h1>🚀 AI Business Intelligence Assistant</h1>
      <p>Upload one CSV or Excel dataset. The application detects its structure
      and adapts its analytics, dashboard, charts, AI analysis and forecasting
      to the columns that are actually present.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Upload your dataset")
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="No fixed template is required. Use any tabular dataset with meaningful columns.",
)

if uploaded_file is not None:
    signature = (uploaded_file.name, uploaded_file.size)
    if st.session_state.get("upload_signature") != signature:
        try:
            df = load_file(uploaded_file)
            st.session_state["df"] = df
            st.session_state["upload_signature"] = signature
            st.session_state["dataset_name"] = uploaded_file.name
            st.success(f"Loaded {uploaded_file.name}: {len(df):,} rows × {len(df.columns):,} columns")
        except Exception as exc:
            st.error(f"Could not load this file: {exc}")
            st.stop()

if "df" in st.session_state:
    df = st.session_state["df"]
    profile = profile_dataset(df)
    st.divider()
    st.subheader(f"Dataset overview: {st.session_state.get('dataset_name', 'Uploaded dataset')}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{profile['rows']:,}")
    c2.metric("Columns", f"{profile['columns']:,}")
    c3.metric("Missing values", f"{profile['missing_values']:,}")
    c4.metric("Duplicate rows", f"{profile['duplicate_rows']:,}")

    st.subheader("Detected dataset structure")
    left, right = st.columns(2)
    with left:
        st.write("**Date/time columns**")
        st.write(profile["datetime_columns"] or "No date/time column detected")
        st.write("**Numerical measure candidates**")
        st.write(profile["measure_columns"] or "No suitable numerical measures detected")
    with right:
        st.write("**Categorical dimensions**")
        st.write(profile["dimension_columns"] or "No categorical dimensions detected")
        st.write("**Possible identifier columns**")
        st.write(profile["identifier_columns"] or "None detected")

    with st.expander("Preview uploaded data"):
        st.dataframe(df.head(20), use_container_width=True)

    st.info("Use the pages in the sidebar to explore the same uploaded dataset. You do not need to upload it again on each page.")
else:
    st.info("Upload a dataset to activate the dashboard, analytics, AI assistant and forecasting pages.")

st.markdown("### What adapts automatically?")
st.markdown(
    "- **Dashboard:** dataset statistics and relevant numerical metrics.\n"
    "- **Analytics:** data types, missing values, distributions and correlations.\n"
    "- **AI Assistant:** questions grounded in the uploaded dataset.\n"
    "- **Forecasting:** select a detected date column and a numerical measure, or forecast by row order.\n"
    "- **Charts and reports:** use available fields rather than assuming fixed names such as `Sales`, `Profit`, `Product` or `Region`."
)

st.sidebar.markdown("## 🚀 Universal AI BI Assistant")
st.sidebar.caption("Upload once on Home, then use the pages below.")
st.sidebar.markdown("Built with Streamlit, pandas, Plotly, scikit-learn and Gemini.")
st.caption("Built by Vicky Yadav | Universal AI Business Intelligence Assistant")
