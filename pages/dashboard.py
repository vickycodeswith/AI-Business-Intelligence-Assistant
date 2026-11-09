import streamlit as st
import plotly.express as px
from utils.eda import dataset_info
from utils.insights import generate_insights, generate_recommendations
from utils.profiling import profile_dataset
from utils.styles import load_css

st.set_page_config(page_title="Universal AI BI | Dashboard", page_icon="📊", layout="wide")
load_css()
st.title("📊 Universal Business Dashboard")
if "df" not in st.session_state:
    st.warning("Upload a dataset on the Home page first.")
    st.stop()

df = st.session_state["df"]
profile = profile_dataset(df)
insights = generate_insights(df)
info = dataset_info(df)

st.subheader("Dataset health")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{info['rows']:,}")
c2.metric("Columns", f"{info['columns']:,}")
c3.metric("Missing cells", f"{info['missing_values']:,}")
c4.metric("Duplicate rows", f"{info['duplicate_rows']:,}")

st.subheader("Available numerical metrics")
if insights["metrics"]:
    metric_items = list(insights["metrics"].items())
    for start in range(0, len(metric_items), 4):
        cols = st.columns(min(4, len(metric_items) - start))
        for col_ui, (name, values) in zip(cols, metric_items[start:start + 4]):
            col_ui.metric(f"Total {name}", f"{values['sum']:,.2f}")
            col_ui.caption(f"Average: {values['mean']:,.2f} · n={values['count']:,}")
else:
    st.info("No numeric measures were detected. This dataset can still be explored through its categorical columns and records.")

st.subheader("Dataset preview")
st.dataframe(df.head(20), use_container_width=True)

if profile["measure_columns"]:
    metric = profile["default_metric"]
    if profile["datetime_columns"]:
        st.subheader("Trend preview")
        date_col = profile["date_column"]
        chart_df = df[[date_col, metric]].copy()
        chart_df[date_col] = __import__("pandas").to_datetime(chart_df[date_col], errors="coerce", format="mixed")
        chart_df[metric] = __import__("pandas").to_numeric(chart_df[metric], errors="coerce")
        chart_df = chart_df.dropna().groupby(date_col, as_index=False)[metric].sum().sort_values(date_col)
        if not chart_df.empty:
            st.plotly_chart(px.line(chart_df, x=date_col, y=metric, markers=True, title=f"{metric} over time"), use_container_width=True)
    elif profile["dimension_columns"]:
        st.subheader("Category breakdown")
        dimension = profile["dimension_columns"][0]
        chart_df = df[[dimension, metric]].copy()
        chart_df[metric] = __import__("pandas").to_numeric(chart_df[metric], errors="coerce")
        chart_df = chart_df.dropna().groupby(dimension, as_index=False)[metric].sum().sort_values(metric, ascending=False).head(20)
        if not chart_df.empty:
            st.plotly_chart(px.bar(chart_df, x=dimension, y=metric, title=f"{metric} by {dimension}"), use_container_width=True)

st.subheader("Automatic findings")
recommendations = generate_recommendations(insights)
for item in recommendations:
    st.info(item)
