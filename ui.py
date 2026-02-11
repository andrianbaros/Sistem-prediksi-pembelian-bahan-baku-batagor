import streamlit as st

class UI:

    @staticmethod
    def load_style():
        st.markdown("""
        <style>

        /* ===============================
           FORCE DARK MODE TOTAL
        =============================== */

        .stApp {
            background-color: #0e1117 !important;
        }

        .block-container {
            padding-top: 2rem !important;
        }

        /* ===============================
           TEXT COLOR (PUTIH SEMUA)
        =============================== */

        .stApp,
        .stMarkdown,
        .stText,
        .stTextInput label,
        label,
        p,
        span,
        h1, h2, h3, h4, h5, h6 {
            color: #e5e7eb !important;
        }

        /* Subtitle */
        .subtitle {
            color: #9ca3af !important;
        }

        /* ===============================
           INPUT
        =============================== */

        input {
            background-color: #1f2937 !important;
            color: #e5e7eb !important;
            border-radius: 8px !important;
        }

        /* ===============================
           BUTTON CENTER
        =============================== */

        div.stButton {
            display: flex !important;
            justify-content: center !important;
        }

        div.stButton > button {
            width: 240px !important;
            height: 44px !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            background-color: #2563eb !important;
            color: white !important;
            border: none !important;
        }

        div.stButton > button:hover {
            background-color: #1d4ed8 !important;
        }

        </style>
        """, unsafe_allow_html=True)
