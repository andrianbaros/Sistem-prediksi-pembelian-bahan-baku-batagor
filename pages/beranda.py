import streamlit as st
from auth import AuthManager
from ui import UI

UI.load_style()


st.set_page_config(page_title="Beranda", layout="wide")

# proteksi halaman
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.stop()

auth = AuthManager()

# HEADER
st.title("Sistem Prediksi Pembelian Bahan Baku Batagor")
st.caption("Sistem Prediksi Pembelian Bahan Baku Batagor")

st.markdown("---")

# KONTEN CONTOH
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Bahan Baku", "12 Item")

with col2:
    st.metric("Rata-rata Pembelian / Bulan", "1.250 Kg")

with col3:
    st.metric("Status Sistem", "Normal")

st.markdown("### Ringkasan")
st.write(
    "Beranda ini akan menampilkan data pembelian, "
    "prediksi kebutuhan bahan baku, dan laporan internal."
)

st.markdown("---")

if st.button("Logout"):
    auth.logout()
    st.switch_page("app.py")

