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
           TEXT PUTIH SEMUA
        =============================== */

        .stApp,
        .stMarkdown,
        .stText,
        .stTextInput label,
        .stTextInput div,
        label,
        p,
        span,
        h1, h2, h3, h4, h5, h6 {
            color: #e5e7eb !important;
        }

        /* Subtitle lebih soft */
        .subtitle {
            color: #9ca3af !important;
        }

        /* ===============================
           INPUT DARK
        =============================== */

        div[data-baseweb="input"] {
            background-color: #1f2937 !important;
            border-radius: 8px !important;
        }

        input {
            background-color: #1f2937 !important;
            color: #e5e7eb !important;
        }

        /* ===============================
           BUTTON CENTER FIX
        =============================== */

        div.stButton {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }

        div.stButton > button {
            width: 240px !important;
            height: 44px !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            background-color: #2563eb !important;
            color: white !important;
            border: none !important;
            transition: 0.2s ease-in-out;
        }

        div.stButton > button:hover {
            background-color: #1d4ed8 !important;
            transform: translateY(-2px);
        }

        </style>
        """, unsafe_allow_html=True)
