import streamlit as st

from utils.ai_analyst import (
    analyze_data_with_ai
)

from utils.report_generator import (
    generate_executive_report
)

from utils.qa_engine import answer_question
from utils.chart_engine import generate_chart

from utils.styles import load_css
load_css()

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)
st.title("🤖 AI Business Assistant")

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset from Home page first."
    )

    st.stop()

df = st.session_state["df"]
st.subheader("Ask Questions About Your Data")

question = st.text_input(
            "Ask a business question"
            )
if st.button("Get Answer"):
        
        if question.strip():

            ai_answer = analyze_data_with_ai(
                question,
                df
            )

            st.success(ai_answer)

        else:

            st.warning(
                "Please enter a question."
            )

            chart = generate_chart(
                    question,
                    df
                )

            if chart:

                    st.plotly_chart(
                        chart,
                        width="stretch"
                    )
else:
        st.warning(
             "Please enter a question.")
        

st.subheader(
        "AI Executive Report" )

if st.button(
        "Generate Executive Report" ):

        with st.spinner(
            "Generating Report..." ):

            report = (
                generate_executive_report(df)  )

            st.success(
                "Executive Report Generated"
            )

            st.markdown(report)


            st.download_button(
                label="📥 Download Executive Report",
                data=report,
                file_name="executive_report.txt",
                mime="text/plain"
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