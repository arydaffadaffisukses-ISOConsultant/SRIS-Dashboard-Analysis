import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Audit & Maturity Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload Data Audit (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Deteksi format
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # 1. Bersihkan Nama Kolom (Menghapus spasi di awal/akhir)
    df.columns = df.columns.str.strip()
    
    st.write("Data berhasil dimuat!")
    
    # 2. Ambil 5 kolom Pentagon secara otomatis (Indeks 6 sampai 10 sesuai screenshot Bapak)
    # Kita ambil kolom ke-6 hingga ke-10 (Indeks Python dimulai dari 0)
    cols_pentagon = df.columns[6:11]
    
    st.write("Kolom yang digunakan untuk Pentagon:", list(cols_pentagon))
    
    # Hitung rata-rata
    values = df[cols_pentagon].mean().tolist()
    
    # Radar Chart
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'],
        fill='toself'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
    
    st.subheader("🕸️ Pentagon Maturity Analysis")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Silakan unggah dokumen CSV atau Excel untuk memulai.")
