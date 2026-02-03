import streamlit as st
from auth import AuthManager
from ui import CorporateUI

st.set_page_config(page_title="Corporate Login", layout="centered")

# session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

auth = AuthManager()
CorporateUI.load_style()

if st.session_state.logged_in:
    st.switch_page("pages/beranda.py")

# LOGIN UI
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="title">Owner Login</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistem Prediksi Pembelian Bahan Baku</div>', unsafe_allow_html=True)

user = st.text_input("Username")
pwd = st.text_input("Password", type="password")

if st.button("Login"):
    if auth.validate(user, pwd):
        auth.login()
        st.switch_page("pages/beranda.py")
    else:
        st.error("Username atau password salah")

st.markdown('</div>', unsafe_allow_html=True)
