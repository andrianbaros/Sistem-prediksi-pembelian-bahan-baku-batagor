import streamlit as st
from auth import AuthManager
from ui import UI

st.set_page_config(page_title="Sistem Prediksi", layout="centered")
UI.load_style()

# ===============================
# PROTEKSI LOGIN
# ===============================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

auth = AuthManager()

# ===============================
# IMPORT
# ===============================
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import io
import math
import warnings

warnings.filterwarnings("ignore")

st.title("Sistem Prediksi Pembelian Bahan Baku Batagor Mang Omeng (Bulanan)")
st.caption("Menampilkan prediksi penjualan dan rekomendasi pembelian bahan baku setiap bulan")

# ===============================
# KOLOM
# ===============================
REQUIRED_COLUMNS = {"Tanggal", "Penjualan_kg"}

BAHAN_COLUMNS = [
    "Tepung_Tapioka_kg",
    "Terigu_kg",
    "Ikan_kg",
    "Pangsit_kg",
    "Kacang_kg",
    "Tahu_kg"
]

# ===============================
# VALIDASI
# ===============================
def validate_dataframe(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Kolom wajib tidak ditemukan: {missing}"
    return True, None

# ===============================
# UPLOAD
# ===============================
uploaded_file = st.file_uploader(
    "Unggah Data Penjualan Harian (.xlsx)",
    type=["xlsx"]
)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        valid, msg = validate_dataframe(df)
        if not valid:
            st.error(msg)
            st.stop()

        df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
        df = df.dropna(subset=["Tanggal", "Penjualan_kg"])
        df = df.sort_values("Tanggal")

        bahan_tersedia = [c for c in BAHAN_COLUMNS if c in df.columns]
        if not bahan_tersedia:
            st.error("Kolom bahan baku tidak ditemukan dalam file.")
            st.stop()

        # ===============================
        # AGREGASI BULANAN
        # ===============================
        df_monthly = (
            df.set_index("Tanggal")
              .resample("MS")
              .sum()
              .reset_index()
        )

        st.subheader("📅 Data Historis Penjualan Bulanan")
        st.dataframe(df_monthly)

        df_monthly["Total_Adonan_kg"] = df_monthly[bahan_tersedia].sum(axis=1)

        ts = df_monthly.set_index("Tanggal")["Penjualan_kg"]

        # ===============================
        # MODEL SARIMAX
        # ===============================
        model = SARIMAX(
            ts,
            order=(2,0,1),
            seasonal_order=(1,0,1,7),
            enforce_stationarity=True,
            enforce_invertibility=True
        )

        model_fit = model.fit(disp=False)

        # ===============================
        # MODEL HISTORIS (FITTED VALUES)
        # ===============================
        pred_historis = model_fit.get_prediction(start=0, end=len(ts)-1)
        fitted_values = pred_historis.predicted_mean

        # ===============================
        # INPUT PERIODE PREDIKSI
        # ===============================
        forecast_months = st.number_input(
            "Masukkan periode prediksi (dalam bulan)",
            min_value=1,
            max_value=24,
            value=3
        )

        # ===============================
        # PREDIKSI MASA DEPAN
        # ===============================
        forecast_obj = model_fit.get_forecast(steps=forecast_months)
        forecast = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()

        future_dates = pd.date_range(
            start=ts.index[-1] + pd.DateOffset(months=1),
            periods=forecast_months,
            freq="MS"
        )

        forecast_series = pd.Series(forecast.values, index=future_dates)

        # ===============================
        # VISUALISASI GRAFIK
        # ===============================
        st.subheader("📊 Grafik Prediksi Bulanan")

        fig, ax = plt.subplots(figsize=(12, 5))

        # Data aktual
        ax.plot(ts.index, ts.values,
                marker="o",
                label="Data Aktual")

        # Model historis
        ax.plot(ts.index, fitted_values,
                linestyle="--",
                label="Model Historis")

        # Prediksi masa depan
        ax.plot(future_dates, forecast_series,
                linestyle="--",
                marker="o",
                label="Prediksi")

        # Interval kepercayaan
        ax.fill_between(
            future_dates,
            conf_int.iloc[:, 0],
            conf_int.iloc[:, 1],
            alpha=0.2,
            label="Interval Kepercayaan"
        )

        # Format per bulan
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45)

        ax.grid(True, linestyle="--", linewidth=0.5)
        ax.set_title("Grafik Prediksi Pembelian Bulanan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Kilogram (kg)")
        ax.legend()

        st.pyplot(fig)

        # ===============================
        # EXPORT
        # ===============================
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_monthly.to_excel(writer, index=False, sheet_name='Historis')

        output.seek(0)

        st.download_button(
            label="Unduh Data Historis",
            data=output,
            file_name="data_historis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# ===============================
# LOGOUT
# ===============================
if st.button("Keluar"):
    auth.logout()
    st.switch_page("app.py")
