import streamlit as st
from utils.ai_analyst import analyze_data_with_ai
from utils.insights import generate_insights
from utils.qa_engine import answer_question
from utils.report_generator import generate_executive_report
from utils.chart_engine import generate_chart
from utils.styles import load_css

st.set_page_config(page_title="Universal AI BI | AI Assistant", page_icon="🤖", layout="wide")
load_css()
st.title("🤖 Dataset-aware AI Assistant")
if "df" not in st.session_state:
    st.warning("Upload a dataset on the Home page first.")
    st.stop()

df = st.session_state["df"]
insights = generate_insights(df)

with st.form("question_form"):
    question = st.text_input("Ask a question about the uploaded dataset", placeholder="Example: What is the average revenue? or Show revenue by channel")
    submitted = st.form_submit_button("Analyze question")

if submitted:
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Analyzing your dataset..."):
            answer = answer_question(question, df, insights)
            # Deterministic answer when supported; otherwise ask Gemini with dataset context.
            if answer is None:
                answer = analyze_data_with_ai(question, df)
            st.markdown(answer)
            chart = generate_chart(question, df)
            if chart is not None:
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.caption("No suitable chart could be created for that question and the available columns.")

st.divider()
st.subheader("Executive report")
if st.button("Generate executive report"):
    with st.spinner("Preparing a report from the uploaded data..."):
        report = generate_executive_report(df)
    st.markdown(report)
    st.download_button("Download report", data=report, file_name="executive_report.md", mime="text/markdown")
