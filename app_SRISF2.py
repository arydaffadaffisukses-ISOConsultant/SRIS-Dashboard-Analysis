import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul Aplikasi
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("🛡️ Security Risk Intelligence System (SRIS)")
st.markdown("---")

# Data Simulasi (Sama dengan yang kita gunakan)
csv_data = '''Timestamp,Auditor,Lokasi/Unit,Departemen,Temuan,Kategori,Tingkat Risiko,Rekomendasi Perbaikan,Status,Tenggat Waktu,Catatan Auditor
2026-06-01 09:00:00,Budi Santoso,Gudang A,Logistik,APAR kadaluarsa,Fasilitas,Medium,Ganti APAR baru,Open,2026-06-15,Segera dilakukan penggantian
2026-06-01 10:30:00,Siti Aminah,Area Produksi,Produksi,Operator tanpa sarung tangan,K3,High,Sosialisasi APD,Closed,2026-06-03,Sudah ditindaklanjuti
2026-06-01 13:15:00,Budi Santoso,Kantor Pusat,HRD,Data karyawan tidak terenkripsi,Sistem,High,Implementasi enkripsi data,Open,2026-06-30,Perlu koordinasi dengan IT
2026-06-02 08:45:00,Andi Wijaya,Workshop,Maintenance,Kabel terkelupas,K3,Critical,Perbaikan instalasi listrik,Open,2026-06-05,Bahaya tinggi
''' # (Tambahkan data lengkap lainnya di sini)

df = pd.read_csv(io.StringIO(csv_data))

# Logika Perhitungan
bobot = {'Critical': 5, 'High': 3, 'Medium': 2, 'Low': 1}
maturity_map = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
df['Score'] = df['Tingkat Risiko'].map(bobot)
df['Est_Kerugian_Jt'] = df['Tingkat Risiko'].map({'Critical': 100, 'High': 50, 'Medium': 20, 'Low': 5})
df['Maturity_Score'] = df['Tingkat Risiko'].map(maturity_map)

# Layout Dasbor
col1, col2 = st.columns(2)

st.subheader("Analisis Operasional & Finansial")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1) # Grafik Temuan
with col2:
    st.pyplot(fig2) # Grafik Kerugian

with col2:
    st.subheader("Analisis Maturitas & Pentagon")
col3, col4 = st.columns(2)
with col3:
    st.pyplot(fig3) # Grafik Maturitas
with col4:
    st.pyplot(fig4) # Grafik Pentagon (Radar Chart)

# Tambahkan elemen lain sesuai kebutuhan
st.success("Dasbor SRIS Siap Digunakan!")
