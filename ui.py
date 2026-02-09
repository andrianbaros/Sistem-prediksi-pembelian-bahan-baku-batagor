import streamlit as st

class UI:

    @staticmethod
    def load_style():
        st.markdown("""
        <style>

        /* ===============================
           BACKGROUND
        =============================== */
        .main {
            background-color: var(--bg);
        }

        /* ===============================
           CARD
        =============================== */
        .card {
            background: var(--card);
            padding: 42px 38px;
            border-radius: 14px;
            box-shadow: var(--shadow);
            width: 380px;
            margin: 6rem auto;
        }

        .title {
            font-size: 26px;
            font-weight: 600;
            text-align: center;
            color: var(--text);
            margin-bottom: 6px;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: var(--subtext);
            margin-bottom: 28px;
        }

        label, p, h1, h2, h3 {
            color: var(--text) !important;
        }

        input {
            border-radius: 8px !important;
        }

        /* ===============================
           BUTTON
        =============================== */
        div.stButton > button {
            width: 100%;
            background-color: var(--button);
            color: white;
            padding: 11px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
        }

        div.stButton > button:hover {
            background-color: var(--button-hover);
        }
        </style>
        """, unsafe_allow_html=True)
