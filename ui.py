import streamlit as st

class UI:

    @staticmethod
    def load_style():
        st.markdown("""
        <style>

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
           HILANGKAN BLOK STREAMLIT KOSONG ATAS
        =============================== */
        .block-container {
            padding-top: 2rem !important;
        }

        /* ===============================
           CARD LOGIN
        =============================== */
        .card {
            background: var(--card);
            padding: 42px 38px;
            border-radius: 14px;
            box-shadow: var(--shadow);
            width: 380px;
            margin: 3rem auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* ===============================
           JUDUL
        =============================== */
        .title {
            font-size: 24px;
            font-weight: 600;
            text-align: center;
            color: var(--text);
            margin-bottom: 4px;
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
           FIX TOMBOL BENAR-BENAR TENGAH
        =============================== */

        div.stButton {
            width: 100%;
            display: flex;
            justify-content: center;
        }

        div.stButton > button {
            width: 220px !important;
            height: 42px !important;
            border-radius: 8px !important;
            font-weight: 600;
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
