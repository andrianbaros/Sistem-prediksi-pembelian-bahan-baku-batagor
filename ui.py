import streamlit as st

class UI:

    @staticmethod
    def load_style():
        st.markdown("""
        <style>

        /* ===============================
           FIX CONTAINER
        =============================== */
        .block-container {
            padding-top: 2rem !important;
        }

        /* ===============================
           LIGHT MODE (DEFAULT)
        =============================== */
        :root {
            --bg: #f4f6f8;
            --text: #111827;      /* HITAM */
            --subtext: #4b5563;
            --button: #2563eb;
            --button-hover: #1d4ed8;
        }

        /* ===============================
           DARK MODE
        =============================== */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0e1117;
                --text: #e5e7eb;  /* PUTIH */
                --subtext: #9ca3af;
                --button: #2563eb;
                --button-hover: #1d4ed8;
            }
        }

        /* ===============================
           BACKGROUND
        =============================== */
        .stApp {
            background-color: var(--bg);
        }

        /* ===============================
           FORCE TEXT COLOR (STREAMLIT OVERRIDE)
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
            color: var(--text) !important;
        }

        /* Subtitle */
        .subtitle {
            color: var(--subtext) !important;
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
            background-color: var(--button) !important;
            color: white !important;
            border: none !important;
        }

        div.stButton > button:hover {
            background-color: var(--button-hover) !important;
        }

        </style>
        """, unsafe_allow_html=True)
