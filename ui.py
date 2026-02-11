import streamlit as st

class UI:

    @staticmethod
    def load_style():
        st.markdown("""
        <style>

        /* ===============================
           PERBAIKI CONTAINER STREAMLIT
        =============================== */

        /* Hilangkan blok kosong pertama */
        div.block-container > div:first-child:empty {
            display: none;
        }

        /* Kurangi padding atas default */
        .block-container {
            padding-top: 2rem !important;
        }

        /* ===============================
           WARNA DASAR
        =============================== */
        :root {
            --bg: #0e1117;
            --card: #161b22;
            --text: #e5e7eb;
            --subtext: #9ca3af;
            --button: #2563eb;
            --button-hover: #1d4ed8;
            --shadow: 0 10px 30px rgba(0,0,0,0.6);
        }

        .main {
            background-color: var(--bg);
        }

        /* ===============================
           CARD LOGIN (CENTER FIX)
        =============================== */
        .card {
            background: var(--card);
            padding: 42px 38px;
            border-radius: 14px;
            box-shadow: var(--shadow);
            width: 400px;
            margin: 4rem auto;
        }

        /* ===============================
           JUDUL
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

        label {
            color: var(--text) !important;
        }

        input {
            border-radius: 8px !important;
        }

        /* ===============================
           TOMBOL CENTER BENAR-BENAR
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
