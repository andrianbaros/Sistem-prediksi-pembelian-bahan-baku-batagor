import streamlit as st
from auth import AuthManager
from ui import UI

st.set_page_config(page_title="Login", layout="centered")

auth = AuthManager()

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

UI.load_style()

# jika sudah login
if st.session_state.logged_in:
    st.switch_page("pages/beranda.py")

# ======================
# LOGIN PAGE
# ======================
if st.session_state.page == "login":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Owner Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sistem Prediksi Pembelian</div>', unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.validate(user, pwd):
            auth.login()
            st.switch_page("pages/beranda.py")
        else:
            st.error("Username atau password salah")


    if st.button("Lupa Password"):
        st.session_state.page = "forgot"

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# LUPA PASSWORD PAGE
# ======================
elif st.session_state.page == "forgot":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Reset Password</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Masukkan kode owner</div>', unsafe_allow_html=True)

    code = st.text_input("Kode Owner", type="password")
    new_pwd = st.text_input("Password Baru", type="password")

    if st.button("Reset Password"):
        if auth.reset_password(code, new_pwd):
            st.success("Password berhasil direset (sementara)")
            st.session_state.page = "login"
        else:
            st.error("Kode owner salah")

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"

    st.markdown("</div>", unsafe_allow_html=True)
