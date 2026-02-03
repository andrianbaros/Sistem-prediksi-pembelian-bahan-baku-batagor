import streamlit as st

class CorporateUI:
    @staticmethod
    def load_style():
        st.markdown("""
        <style>
        .main { background-color: #f5f6f8; }

        .card {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 6px 25px rgba(0,0,0,0.08);
            width: 380px;
            margin: auto;
        }

        .title {
            font-size: 26px;
            font-weight: 600;
            text-align: center;
            color: #1f2937;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 25px;
        }

        div.stButton > button {
            width: 100%;
            background-color: #1f4fd8;
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #173bb5;
        }
        </style>
        """, unsafe_allow_html=True)
