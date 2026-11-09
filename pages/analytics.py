import streamlit as st
import plotly.express as px
from utils.profiling import profile_dataset
from utils.styles import load_css

st.set_page_config(page_title="Universal AI BI | Analytics", page_icon="📈", layout="wide")
load_css()
st.title("📈 Dataset Analytics")
if "df" not in st.session_state:
    st.warning("Upload a dataset on the Home page first.")
    st.stop()

df = st.session_state["df"]
profile = profile_dataset(df)
st.subheader("Column intelligence")
st.dataframe(profile["column_details"], use_container_width=True)

left, right = st.columns(2)
with left:
    st.markdown("**Numerical measures**")
    st.write(profile["measure_columns"] or "None detected")
    st.markdown("**Date/time columns**")
    st.write(profile["datetime_columns"] or "None detected")
with right:
    st.markdown("**Categorical dimensions**")
    st.write(profile["dimension_columns"] or "None detected")
    st.markdown("**Identifier columns**")
    st.write(profile["identifier_columns"] or "None detected")

numeric = df.select_dtypes(include="number")
st.subheader("Statistical summary")
if not numeric.empty:
    st.dataframe(numeric.describe().T, use_container_width=True)
else:
    st.info("No numeric columns are available for statistical summaries.")

if len(profile["measure_columns"]) >= 2:
    st.subheader("Correlation analysis")
    corr = df[profile["measure_columns"]].corr(numeric_only=True)
    st.plotly_chart(px.imshow(corr, text_auto=True, aspect="auto", title="Correlation between numeric measures"), use_container_width=True)

st.subheader("Missing values by column")
missing = df.isna().sum().sort_values(ascending=False)
missing = missing[missing > 0]
if not missing.empty:
    missing_df = missing.rename("Missing cells").reset_index(names="Column")
    st.plotly_chart(px.bar(missing_df, x="Column", y="Missing cells", title="Missing values by column"), use_container_width=True)
else:
    st.success("No missing cells detected.")
