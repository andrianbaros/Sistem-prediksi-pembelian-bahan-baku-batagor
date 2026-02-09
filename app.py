import streamlit as st
from auth import AuthManager
from ui import UI

st.set_page_config(page_title="Login", layout="centered")

UI.load_style()
auth = AuthManager()

# session init
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# jika sudah login → ke beranda
if st.session_state.logged_in:
    st.switch_page("pages/beranda.py")

# ======================
# LOGIN PAGE
# ======================
if st.session_state.page == "login":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Owner Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sistem Prediksi Pembelian</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.login(username, password):
            st.session_state.logged_in = True
            st.success("Login berhasil")
            st.switch_page("pages/beranda.py")
        else:
            st.error("Username atau password salah")

    if st.button("Lupa Password"):
        st.session_state.page = "forgot"
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# RESET PASSWORD (PERMANEN)
# ======================
elif st.session_state.page == "forgot":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Reset Password</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Password akan diubah permanen</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    new_password = st.text_input("Password Baru", type="password")

    if st.button("Reset Password"):
        success = auth.reset_password(username, new_password)
        if success:
            st.success("Password berhasil direset (PERMANEN)")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error("User tidak ditemukan")

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)
