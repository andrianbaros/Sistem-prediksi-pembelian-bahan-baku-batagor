import streamlit as st

class CorporateUI:

    @staticmethod
    def theme_toggle():
        if "theme" not in st.session_state:
            st.session_state.theme = "light"

        col1, col2 = st.columns([6, 1])
        with col2:
            toggle = st.toggle(
                "🌙",
                value=(st.session_state.theme == "dark"),
                help="Mode Gelap / Terang"
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
            shadow = "0 6px 25px rgba(0,0,0,0.6)"
        else:
            bg = "#f5f6f8"
            card = "#ffffff"
            text = "#1f2937"
            subtext = "#6b7280"
            button = "#1f4fd8"
            button_hover = "#173bb5"
            shadow = "0 6px 25px rgba(0,0,0,0.08)"

        st.markdown(f"""
        <style>
        .main {{
            background-color: {bg};
        }}

        .card {{
            background: {card};
            padding: 40px;
            border-radius: 12px;
            box-shadow: {shadow};
            width: 380px;
            margin: auto;
        }}

        .title {{
            font-size: 26px;
            font-weight: 600;
            text-align: center;
            color: {text};
        }}

        .subtitle {{
            text-align: center;
            font-size: 13px;
            color: {subtext};
            margin-bottom: 25px;
        }}

        label, p, h1, h2, h3 {{
            color: {text} !important;
        }}

        div.stButton > button {{
            width: 100%;
            background-color: {button};
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
        }}

        div.stButton > button:hover {{
            background-color: {button_hover};
        }}
        </style>
        """, unsafe_allow_html=True)
