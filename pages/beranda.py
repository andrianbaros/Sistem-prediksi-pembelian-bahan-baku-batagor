import streamlit as st
from auth import AuthManager
from ui import UI

UI.load_style()


# st.set_page_config(page_title="Beranda", layout="wide")
# proteksi halaman
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.stop()

auth = AuthManager()


#SARIMA
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import io


st.title("📦 Sistem Prediksi Pembelian Bahan Baku (Bulanan)")
st.caption("Prediksi penjualan & rekomendasi pembelian bahan baku per bulan")

# =====================================================
# KOLOM
# =====================================================
REQUIRED_COLUMNS = {"Tanggal", "Penjualan_kg"}

BAHAN_COLUMNS = [
    "Tepung_Tapioka_kg",
    "Terigu_kg",
    "Ikan_kg",
    "Pangsit_kg",
    "Kacang_kg",
    "Tahu_kg"
]

# =====================================================
# VALIDASI
# =====================================================
def validate_dataframe(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Kolom wajib tidak ditemukan: {missing}"
    return True, None

# =====================================================
# UPLOAD
# =====================================================
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

        # =================================================
        # AGREGASI BULANAN
        # =================================================
        df_monthly = (
            df.set_index("Tanggal")
              .resample("MS")
              .sum()
              .reset_index()
        )

        st.subheader("📅 Data Historis Bulanan")
        st.dataframe(df_monthly)

        # =================================================
        # TOTAL ADONAN (BULANAN)
        # =================================================
        df_monthly["Total_Adonan_kg"] = df_monthly[bahan_tersedia].sum(axis=1)

        # =================================================
        # SARIMA BULANAN
        # =================================================
        ts = df_monthly.set_index("Tanggal")["Penjualan_kg"]

        model = SARIMAX(
            ts,
            order=(1, 0, 0),
            seasonal_order=(1, 0, 1, 7),  # MUSIMAN BULANAN
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        model_fit = model.fit(disp=False)

        # =================================================
        # PARAMETER
        # =================================================
        forecast_months = st.number_input(
            "Periode Prediksi (bulan)",
            min_value=1,
            max_value=24,
            value=1
        )

        forecast = model_fit.forecast(steps=forecast_months)

        last_date = ts.index[-1]

        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=forecast_months,
            freq="MS"
        )

        df_forecast = pd.DataFrame({
            "Tanggal": future_dates,
            "Prediksi_Penjualan_kg": forecast.round(2)
        })

        # =================================================
        # KONVERSI → ADONAN
        # =================================================
        loss_factor = (
            df_monthly["Penjualan_kg"] /
            df_monthly["Total_Adonan_kg"]
        ).mean()

        df_forecast["Estimasi_Adonan_kg"] = (
            df_forecast["Prediksi_Penjualan_kg"] / loss_factor
        ).round(2)

        # =================================================
        # RASIO BAHAN (BOM)
        # =================================================
        rasio_bahan = (
            df_monthly[bahan_tersedia]
            .div(df_monthly["Total_Adonan_kg"], axis=0)
            .mean()
        )

        for bahan in bahan_tersedia:
            df_forecast[bahan] = (
                df_forecast["Estimasi_Adonan_kg"] * rasio_bahan[bahan]
            ).round(2)

        # =================================================
        # OUTPUT BULANAN
        # =================================================
        st.subheader("📦 Rekomendasi Pembelian Bahan Baku BULANAN")
        st.dataframe(df_forecast[["Tanggal"] + bahan_tersedia])

        # =================================================
        # METRIC
        # =================================================
        col1, col2 = st.columns(2)
        col1.metric(
            "Total Prediksi Penjualan (kg)",
            f"{df_forecast['Prediksi_Penjualan_kg'].sum():.2f}"
        )
        col2.metric(
            "Total Adonan Dibutuhkan (kg)",
            f"{df_forecast['Estimasi_Adonan_kg'].sum():.2f}"
        )

        # =================================================
        # VISUALISASI (SAMA KONSEP, LEVEL BULANAN)
        # =================================================
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(ts.index, ts.values, label="Aktual Bulanan", marker="o")
        ax.plot(df_forecast["Tanggal"],
                df_forecast["Prediksi_Penjualan_kg"],
                linestyle="--", marker="o", label="Prediksi Bulanan")
        ax.set_title("Prediksi Penjualan Bulanan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Kg")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # # =================================================
        # # EXPORT
        # # =================================================
        # st.download_button(
        #     "Export Rekomendasi Bulanan (CSV)",
        #     data=df_forecast.to_csv(index=False),
        #     file_name="rekomendasi_pembelian_bulanan.csv",
        #     mime="text/csv"
        # )
        # =================================================
        # EXPORT EXCEL
        # =================================================
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_forecast.to_excel(writer, index=False, sheet_name='Rekomendasi')

        output.seek(0)

        st.download_button(
            label="Export Rekomendasi Bulanan (Excel)",
            data=output,
            file_name="rekomendasi_pembelian_bulanan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
# # INISIALISASI UI
# # HEADER
# st.title("Sistem Prediksi Pembelian Bahan Baku Batagor")
# st.caption("Sistem Prediksi Pembelian Bahan Baku Batagor")

# st.markdown("---")

# # KONTEN CONTOH
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric("Total Bahan Baku", "12 Item")

# with col2:
#     st.metric("Rata-rata Pembelian / Bulan", "1.250 Kg")

# with col3:
#     st.metric("Status Sistem", "Normal")

# st.markdown("### Ringkasan")
# st.write(
#     "Beranda ini akan menampilkan data pembelian, "
#     "prediksi kebutuhan bahan baku, dan laporan internal."
# )

# st.markdown("---")

if st.button("Logout"):
    auth.logout()
    st.switch_page("app.py")

