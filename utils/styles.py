import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0F172A, #111827);
        }
        h1, h2, h3 {
            color: white !important;
            font-weight: 700;
        }
        section[data-testid="stSidebar"] {
            background: rgba(15,23,42,0.85);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        .glass-card {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border-radius: 18px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }
        .stButton button {
            width: 100%;
            border-radius: 14px;
            border: none;
            color: white;
            font-weight: 600;
            background: linear-gradient(135deg, #6366F1, #8B5CF6);
            transition: 0.3s;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(99,102,241,0.5);
        }
        .stDataFrame {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .stTextInput input { border-radius: 12px; }
        .stSuccess { border-radius: 15px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
