import streamlit as st

class UI:

    @staticmethod
    def theme_toggle():
        if "theme" not in st.session_state:
            st.session_state.theme = "light"

        # toggle kecil di kanan atas halaman
        col1, col2 = st.columns([8, 1])
        with col2:
            toggle = st.toggle(
                "🌙",
                value=(st.session_state.theme == "dark"),
                help="Light / Dark Mode"
            )

        st.session_state.theme = "dark" if toggle else "light"

    @staticmethod
    def load_style():
        theme = st.session_state.get("theme", "light")

        if theme == "dark":
            bg = "#0e1117"
            card = "#161b22"
            text = "#e5e7eb"
            subtext = "#9ca3af"
            button = "#2563eb"
            button_hover = "#1d4ed8"
            shadow = "0 10px 30px rgba(0,0,0,0.6)"
        else:
            bg = "#f4f6f8"
            card = "#ffffff"
            text = "#1f2937"
            subtext = "#6b7280"
            button = "#1f4fd8"
            button_hover = "#173bb5"
            shadow = "0 10px 30px rgba(0,0,0,0.12)"

        st.markdown(f"""
        <style>
        /* ===== HILANGKAN HEADER & FOOTER STREAMLIT ===== */
        header[data-testid="stHeader"] {{
            display: none;
        }}
        footer {{
            display: none;
        }}

        /* ===== HILANGKAN PADDING ATAS ===== */
        .block-container {{
            padding-top: 2rem;
        }}

        /* ===== BACKGROUND ===== */
        .main {{
            background-color: {bg};
        }}

        /* ===== LOGIN CARD ===== */
        .card {{
            background: {card};
            padding: 42px 38px;
            border-radius: 14px;
            box-shadow: {shadow};
            width: 380px;
            margin: 6rem auto;
        }}

        .title {{
            font-size: 26px;
            font-weight: 600;
            text-align: center;
            color: {text};
            margin-bottom: 6px;
        }}

        .subtitle {{
            text-align: center;
            font-size: 13px;
            color: {subtext};
            margin-bottom: 28px;
        }}

        label, p {{
            color: {text} !important;
        }}

        input {{
            border-radius: 8px !important;
        }}

        /* ===== BUTTON ===== */
        div.stButton > button {{
            width: 100%;
            background-color: {button};
            color: white;
            padding: 11px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
        }}

        div.stButton > button:hover {{
            background-color: {button_hover};
        }}
        </style>
        """, unsafe_allow_html=True)
