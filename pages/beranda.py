import streamlit as st
from auth import AuthManager
from ui import UI

UI.load_style()

# ===============================
# PROTEKSI LOGIN
# ===============================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()


autentikasi = AuthManager()

# ===============================
# IMPORT LIBRARY
# ===============================
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import io

st.title("📦 Sistem Prediksi Pembelian Bahan Baku (Bulanan)")
st.caption("Prediksi penjualan dan rekomendasi pembelian bahan baku per bulan")

# ===============================
# KOLOM WAJIB
# ===============================
KOLOM_WAJIB = {"Tanggal", "Penjualan_kg"}

KOLOM_BAHAN = [
    "Tepung_Tapioka_kg",
    "Terigu_kg",
    "Ikan_kg",
    "Pangsit_kg",
    "Kacang_kg",
    "Tahu_kg"
]

# ===============================
# VALIDASI DATA
# ===============================
def validasi_data(data):
    kolom_hilang = KOLOM_WAJIB - set(data.columns)
    if kolom_hilang:
        return False, f"Kolom wajib tidak ditemukan: {kolom_hilang}"
    return True, None

# ===============================
# UPLOAD FILE
# ===============================
file_unggah = st.file_uploader(
    "Unggah Data Penjualan Harian (.xlsx)",
    type=["xlsx"]
)

if file_unggah:
    try:
        data = pd.read_excel(file_unggah)

        valid, pesan = validasi_data(data)
        if not valid:
            st.error(pesan)
            st.stop()

        data["Tanggal"] = pd.to_datetime(data["Tanggal"], errors="coerce")
        data = data.dropna(subset=["Tanggal", "Penjualan_kg"])
        data = data.sort_values("Tanggal")

        bahan_tersedia = [k for k in KOLOM_BAHAN if k in data.columns]
        if not bahan_tersedia:
            st.error("Kolom bahan baku tidak ditemukan")
            st.stop()

        # ===============================
        # AGREGASI BULANAN
        # ===============================
        data_bulanan = (
            data.set_index("Tanggal")
                .resample("MS")
                .sum()
                .reset_index()
        )

        st.subheader("📅 Data Historis Bulanan")
        st.dataframe(data_bulanan)

        # ===============================
        # HITUNG TOTAL ADONAN
        # ===============================
        data_bulanan["Total_Adonan_kg"] = data_bulanan[bahan_tersedia].sum(axis=1)

        # ===============================
        # DERET WAKTU
        # ===============================
        deret_waktu = data_bulanan.set_index("Tanggal")["Penjualan_kg"]

        # ===============================
        # MODEL SARIMA
        # ===============================
        model = SARIMAX(
            deret_waktu,
            order=(2, 0, 1),
            seasonal_order=(1, 0, 1, 7),
            enforce_stationarity=True,
            enforce_invertibility=True
        )

        hasil_model = model.fit(disp=False)

        # ===============================
        # INPUT PERIODE PREDIKSI
        # ===============================
        periode_prediksi = st.number_input(
            "Periode Prediksi (bulan)",
            min_value=1,
            max_value=24,
            value=3
        )

        # ===============================
        # PREDIKSI HISTORIS
        # ===============================
        prediksi_historis = hasil_model.get_prediction(
            start=0,
            end=len(deret_waktu) - 1
        )

        nilai_model_historis = prediksi_historis.predicted_mean

        # ===============================
        # PREDIKSI MASA DEPAN
        # ===============================
        objek_forecast = hasil_model.get_forecast(steps=periode_prediksi)
        nilai_forecast = objek_forecast.predicted_mean
        interval_kepercayaan = objek_forecast.conf_int()

        tanggal_masa_depan = pd.date_range(
            start=deret_waktu.index[-1] + pd.DateOffset(months=1),
            periods=periode_prediksi,
            freq="MS"
        )

        seri_forecast = pd.Series(nilai_forecast.values, index=tanggal_masa_depan)

        # ===============================
        # KONVERSI KE ADONAN
        # ===============================
        faktor_kehilangan = (
            data_bulanan["Penjualan_kg"] /
            data_bulanan["Total_Adonan_kg"]
        ).mean()

        data_forecast = pd.DataFrame({
            "Tanggal": tanggal_masa_depan,
            "Prediksi_Penjualan_kg": nilai_forecast.round(2)
        })

        data_forecast["Estimasi_Adonan_kg"] = (
            data_forecast["Prediksi_Penjualan_kg"] / faktor_kehilangan
        ).round(2)

        # ===============================
        # RASIO BAHAN
        # ===============================
        rasio_bahan = (
            data_bulanan[bahan_tersedia]
            .div(data_bulanan["Total_Adonan_kg"], axis=0)
            .mean()
        )

        for bahan in bahan_tersedia:
            data_forecast[bahan] = (
                data_forecast["Estimasi_Adonan_kg"] * rasio_bahan[bahan]
            ).round(2)

        # ===============================
        # TAMPILKAN REKOMENDASI
        # ===============================
        st.subheader("📦 Rekomendasi Pembelian Bahan Baku Bulanan")
        st.dataframe(data_forecast[["Tanggal"] + bahan_tersedia])

        # ===============================
        # RINGKASAN METRIK
        # ===============================
        kolom1, kolom2 = st.columns(2)

        kolom1.metric(
            "Total Prediksi Penjualan (kg)",
            f"{data_forecast['Prediksi_Penjualan_kg'].sum():.2f}"
        )

        kolom2.metric(
            "Total Adonan Dibutuhkan (kg)",
            f"{data_forecast['Estimasi_Adonan_kg'].sum():.2f}"
        )

        # ===============================
        # VISUALISASI
        # ===============================
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(deret_waktu.index, deret_waktu.values,
                label="Data Aktual", marker="o")

        ax.plot(deret_waktu.index, nilai_model_historis,
                linestyle="--", label="Hasil Model Historis")

        ax.plot(tanggal_masa_depan, seri_forecast,
                linestyle="--", marker="o", label="Prediksi Masa Depan")

        ax.fill_between(
            tanggal_masa_depan,
            interval_kepercayaan.iloc[:, 0],
            interval_kepercayaan.iloc[:, 1],
            color='gray',
            alpha=0.3,
            label="Interval Kepercayaan"
        )

        ax.set_title("Prediksi Penjualan Bulanan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Kilogram (kg)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # ===============================
        # EKSPOR EXCEL
        # ===============================
        buffer_output = io.BytesIO()

        with pd.ExcelWriter(buffer_output, engine='openpyxl') as penulis:
            data_forecast.to_excel(
                penulis,
                index=False,
                sheet_name='Rekomendasi'
            )

        buffer_output.seek(0)

        st.download_button(
            label="Unduh Rekomendasi Bulanan (Excel)",
            data=buffer_output,
            file_name="rekomendasi_pembelian_bulanan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# ===============================
# LOGOUT
# ===============================
if st.button("Keluar"):
    autentikasi.logout()
    st.switch_page("app.py")
