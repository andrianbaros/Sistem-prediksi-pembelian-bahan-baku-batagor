import streamlit as st
from auth import AuthManager
from ui import UI

UI.load_style()

# ===============================
# PROTEKSI LOGIN
# ===============================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.stop()

auth = AuthManager()

# ===============================
# IMPORT
# ===============================
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import io

st.title("📦 Sistem Prediksi Pembelian Bahan Baku (Harian)")
st.caption("Prediksi penjualan harian dengan musiman mingguan (7 hari)")

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
    "Upload Data Penjualan Harian (.xlsx)",
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
            st.error("Kolom bahan baku tidak ditemukan")
            st.stop()

        # ===============================
        # TIME SERIES HARIAN
        # ===============================
        df = df.set_index("Tanggal")
        ts = df["Penjualan_kg"].asfreq("D")

        # isi tanggal kosong kalau ada
        ts = ts.fillna(method="ffill")

        st.subheader("📅 Data Historis Harian")
        st.dataframe(ts.reset_index())

        # ===============================
        # MODEL SARIMA HARIAN (MUSIMAN 7)
        # ===============================
        model = SARIMAX(
            ts,
            order=(1,0,1),
            seasonal_order=(1,0,1,7),  # MUSIMAN MINGGUAN
            enforce_stationarity=True,
            enforce_invertibility=True
        )

        model_fit = model.fit(disp=False)

        # ===============================
        # INPUT FORECAST
        # ===============================
        forecast_days = st.number_input(
            "Periode Prediksi (hari)",
            min_value=1,
            max_value=60,
            value=14
        )

        # ===============================
        # FITTED HISTORIS
        # ===============================
        pred = model_fit.get_prediction(start=0, end=len(ts)-1)
        fitted_values = pred.predicted_mean

        # ===============================
        # FORECAST FUTURE
        # ===============================
        forecast_obj = model_fit.get_forecast(steps=forecast_days)
        forecast = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()

        future_dates = pd.date_range(
            start=ts.index[-1] + pd.DateOffset(days=1),
            periods=forecast_days,
            freq="D"
        )

        forecast_series = pd.Series(forecast.values, index=future_dates)

        # ===============================
        # KONVERSI KE ADONAN
        # ===============================
        df["Total_Adonan_kg"] = df[bahan_tersedia].sum(axis=1)

        loss_factor = (
            df["Penjualan_kg"] /
            df["Total_Adonan_kg"]
        ).mean()

        df_forecast = pd.DataFrame({
            "Tanggal": future_dates,
            "Prediksi_Penjualan_kg": forecast.round(2)
        })

        df_forecast["Estimasi_Adonan_kg"] = (
            df_forecast["Prediksi_Penjualan_kg"] / loss_factor
        ).round(2)

        # ===============================
        # RASIO BAHAN
        # ===============================
        rasio_bahan = (
            df[bahan_tersedia]
            .div(df["Total_Adonan_kg"], axis=0)
            .mean()
        )

        for bahan in bahan_tersedia:
            df_forecast[bahan] = (
                df_forecast["Estimasi_Adonan_kg"] * rasio_bahan[bahan]
            ).round(2)

        # ===============================
        # OUTPUT
        # ===============================
        st.subheader("📦 Rekomendasi Pembelian Bahan Baku (Harian)")
        st.dataframe(df_forecast[["Tanggal"] + bahan_tersedia])

        # ===============================
        # METRIC
        # ===============================
        col1, col2 = st.columns(2)
        col1.metric(
            "Total Prediksi Penjualan (kg)",
            f"{df_forecast['Prediksi_Penjualan_kg'].sum():.2f}"
        )
        col2.metric(
            "Total Adonan Dibutuhkan (kg)",
            f"{df_forecast['Estimasi_Adonan_kg'].sum():.2f}"
        )

        # ===============================
        # VISUALISASI MENYAMBUNG
        # ===============================
        fig, ax = plt.subplots(figsize=(12,5))

        ax.plot(ts.index, ts.values, label="Aktual", color="blue")
        ax.plot(ts.index, fitted_values,
                linestyle="--", label="Model Historis")

        ax.plot(future_dates, forecast_series,
                linestyle="--", marker="o", label="Forecast")

        ax.fill_between(
            future_dates,
            conf_int.iloc[:,0],
            conf_int.iloc[:,1],
            alpha=0.3,
            color="gray",
            label="Confidence Interval"
        )

        ax.set_title("Prediksi Penjualan Harian (Musiman 7 Hari)")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Kg")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # ===============================
        # EXPORT EXCEL
        # ===============================
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_forecast.to_excel(writer, index=False, sheet_name='Rekomendasi')

        output.seek(0)

        st.download_button(
            label="Export Rekomendasi Harian (Excel)",
            data=output,
            file_name="rekomendasi_pembelian_harian.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# ===============================
# LOGOUT
# ===============================
if st.button("Logout"):
    auth.logout()
    st.switch_page("app.py")
