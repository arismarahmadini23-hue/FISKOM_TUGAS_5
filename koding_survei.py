import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Analisis Tes", layout="wide")

st.title("📊 Dashboard Analisis Hasil Tes Siswa")

# =============================
# LOAD DATA
# =============================
try:
    df = pd.read_excel("data_simulasi_50_siswa_20_soal.xlsx")
except Exception as e:
    st.error("File tidak ditemukan atau gagal dibaca.")
    st.stop()

st.subheader("📄 Data Asli")
st.dataframe(df, use_container_width=True)

# =============================
# AMBIL KOLOM NUMERIK (SOAL)
# =============================
df_numerik = df.select_dtypes(include="number")

if df_numerik.empty:
    st.error("Tidak ditemukan kolom numerik (skor). Pastikan soal berupa angka.")
    st.stop()

# =============================
# HITUNG SKOR TOTAL
# =============================
df["Skor Total"] = df_numerik.sum(axis=1)

# =============================
# TAMPILKAN SKOR TOTAL
# =============================
st.subheader("🧮 Skor Total Siswa")

hasil = pd.DataFrame({
    "Siswa": df.index + 1,
    "Skor Total": df["Skor Total"]
})

st.dataframe(hasil, use_container_width=True)

# =============================
# STATISTIK
# =============================
st.subheader("📈 Statistik Skor")

col1, col2, col3 = st.columns(3)

col1.metric("Skor Tertinggi", int(df["Skor Total"].max()))
col2.metric("Skor Terendah", int(df["Skor Total"].min()))
col3.metric("Rata-rata", round(df["Skor Total"].mean(), 2))

# =============================
# GRAFIK SKOR TOTAL
# =============================
st.subheader("📊 Grafik Skor Total Siswa")

grafik_total = hasil.set_index("Siswa")
st.bar_chart(grafik_total)

# =============================
# RATA-RATA PER SOAL
# =============================
st.subheader("📘 Rata-rata Skor Tiap Soal")

mean_soal = df_numerik.mean().reset_index()
mean_soal.columns = ["Soal", "Rata-rata Skor"]

st.dataframe(mean_soal, use_container_width=True)

st.bar_chart(mean_soal.set_index("Soal"))

# =============================
# FILTER INTERAKTIF
# =============================
st.subheader("🎛️ Filter Berdasarkan Skor")

min_score = int(df["Skor Total"].min())
max_score = int(df["Skor Total"].max())

range_score = st.slider(
    "Pilih rentang skor",
    min_score,
    max_score,
    (min_score, max_score)
)

filtered = hasil[
    (hasil["Skor Total"] >= range_score[0]) &
    (hasil["Skor Total"] <= range_score[1])
]

st.dataframe(filtered, use_container_width=True)

st.success("Dashboard berhasil dijalankan ✅")