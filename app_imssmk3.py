import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="SRIS Pro Dashboard", layout="wide")

# --- 2. BANNER KUSTOM (CSS) ---
st.markdown("""
    <style>
    .banner {
        background: linear-gradient(90deg, #1a2a6c, #4a148c);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    <div class="banner">
        <h1>🛡️ Security Risk Intelligence System (SRIS)</h1>
        <p>Executive Audit & Risk Management Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LOAD & FILTER DATA ---
# (Pastikan data CSV Bapak sudah sesuai format)
csv_data = '''Timestamp,Auditor,Lokasi/Unit,Departemen,Temuan,Kategori,Tingkat Risiko,Rekomendasi Perbaikan,Status,Tenggat Waktu,Catatan Auditor
2026-06-01 09:00:00,Budi,Gudang A,Logistik,APAR kadaluarsa,Fasilitas,Medium,Ganti APAR,Open,2026-06-15,OK
2026-06-01 10:30:00,Siti,Produksi,Produksi,APD Kurang,K3,High,Sosialisasi,Closed,2026-06-03,OK
2026-06-01 13:15:00,Budi,Pusat,HRD,Data tidak enkripsi,Integritas Data,High,Enkripsi,Open,2026-06-30,Penting
2026-06-02 08:45:00,Andi,Workshop,Maintenance,Kabel terkelupas,Operasional,Critical,Perbaikan,Open,2026-06-05,Bahaya
'''
df = pd.read_csv(io.StringIO(csv_data))
bobot = {'Critical': 5, 'High': 3, 'Medium': 2, 'Low': 1}
df['Score'] = df['Tingkat Risiko'].map(bobot)

# Sidebar Filter
dept_list = ["Semua"] + list(df['Departemen'].unique())
pilihan_dept = st.sidebar.selectbox("Pilih Departemen:", dept_list)
df_filtered = df if pilihan_dept == "Semua" else df[df['Departemen'] == pilihan_dept]

# --- 4. TAMPILAN GRAFIK ---
col1, col2 = st.columns(2)
with col1:
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df_filtered, x='Departemen', hue='Departemen', palette='viridis', legend=False, ax=ax1)
    st.pyplot(fig1)

with col2:
    st.write("### Statistik Departemen")
    st.write(df_filtered)
