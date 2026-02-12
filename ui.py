import streamlit as st

class UI:

    @staticmethod
    def load_style():
        st.markdown("""
        <style>

        /* ===============================
           PERBAIKI CONTAINER STREAMLIT
        =============================== */

        div.block-container > div:first-child:empty {
            display: none;
        }

        .block-container {
            padding-top: 2rem !important;
        }

        /* ===============================
           LIGHT MODE (DEFAULT)
        =============================== */
        :root {
                --bg: #0e1117;
                --card: #161b22;
                --text: #e5e7eb;    /* PUTIH */
                --subtext: #9ca3af;
                --button: #2563eb;
                --button-hover: #1d4ed8;
                --shadow: 0 10px 30px rgba(0,0,0,0.6);
        }

        /* ===============================
           DARK MODE (AUTO DETECT)
        =============================== */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0e1117;
                --card: #161b22;
                --text: #e5e7eb;    /* PUTIH */
                --subtext: #9ca3af;
                --button: #2563eb;
                --button-hover: #1d4ed8;
                --shadow: 0 10px 30px rgba(0,0,0,0.6);
            }
        }

        /* ===============================
           BACKGROUND
        =============================== */
        .main {
            background-color: var(--bg);
            transition: 0.3s ease;
        }

        /* ===============================
           TEKS GLOBAL
        =============================== */
        body, p, span, label, h1, h2, h3, h4, h5, h6 {
            color: var(--text) !important;
        }

        /* ===============================
           JUDUL LOGIN
        =============================== */
        .title {
            font-size: 24px;
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

        /* ===============================
           INPUT
        =============================== */
        input {
            border-radius: 8px !important;
        }

        /* ===============================
           TOMBOL CENTER
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
            background-color: var(--button) !important;
            color: white !important;
            border: none !important;
            transition: 0.2s ease-in-out;
        }

        div.stButton > button:hover {
            background-color: var(--button-hover) !important;
            transform: translateY(-2px);
        }

        </style>
        """, unsafe_allow_html=True)
