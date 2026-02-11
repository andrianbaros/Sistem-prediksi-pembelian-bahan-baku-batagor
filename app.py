import streamlit as st
from auth import AuthManager
from ui import UI

st.set_page_config(page_title="Masuk Sistem", layout="centered")

UI.load_style()
auth = AuthManager()

# ======================
# INISIALISASI SESSION
# ======================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Jika sudah login → ke beranda
if st.session_state.logged_in:
    st.switch_page("pages/beranda.py")

# ======================
# HALAMAN LOGIN
# ======================
if st.session_state.page == "login":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Masuk ke Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sistem Prediksi Pembelian Bahan Baku</div>', unsafe_allow_html=True)

    username = st.text_input("Nama Pengguna")
    password = st.text_input("Kata Sandi", type="password")

    # Tombol Masuk (CENTER)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tombol_masuk = st.button("Masuk", use_container_width=True)

    if tombol_masuk:
        if auth.login(username, password):
            st.session_state.logged_in = True
            st.success("Berhasil masuk ke sistem.")
            st.switch_page("pages/beranda.py")
        else:
            st.error("Nama pengguna atau kata sandi tidak sesuai.")

    # Tombol Lupa Password (CENTER)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tombol_lupa = st.button("Lupa Kata Sandi?", use_container_width=True)

    if tombol_lupa:
        st.session_state.page = "forgot"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# HALAMAN RESET PASSWORD
# ======================
elif st.session_state.page == "forgot":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Atur Ulang Kata Sandi</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Kata sandi baru akan menggantikan yang lama secara permanen</div>', unsafe_allow_html=True)

    username = st.text_input("Nama Pengguna")
    new_password = st.text_input("Kata Sandi Baru", type="password")

    # Tombol Reset (CENTER)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tombol_reset = st.button("Atur Ulang Kata Sandi", use_container_width=True)

    if tombol_reset:
        success = auth.reset_password(username, new_password)
        if success:
            st.success("Kata sandi berhasil diperbarui secara permanen.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Nama pengguna tidak ditemukan.")

    # Tombol Kembali (CENTER)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tombol_kembali = st.button("Kembali ke Halaman Masuk", use_container_width=True)

    if tombol_kembali:
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
