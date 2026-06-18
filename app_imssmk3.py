import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

# 1. UPLOAD FILE
uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Bersihkan nama kolom
        df.columns = df.columns.str.strip()
        st.success("File berhasil dimuat!")
        st.write("Jumlah data:", len(df))
    except Exception as e:
        st.error(f"Error membaca file: {e}")
        st.stop()

    # 2. TAB MENU
    tab1, tab2 = st.tabs(["Dashboard Ringkasan", "Analisis Finansial"])

    with tab1:
        st.write("### Distribusi Temuan")
        if 'Departemen Divisi/Area' in df.columns:
            # Menggunakan chart bawaan streamlit yang paling stabil
            chart_data = df.groupby('Departemen Divisi/Area').size()
            st.bar_chart(chart_data)
        else:
            st.warning("Kolom 'Departemen Divisi/Area' tidak ditemukan.")

    with tab2:
        st.write("### Estimasi Kerugian Finansial")
        
        # Nama kolom kerugian
        target_col = 'Estimasi Kerugian Finansial Atas Temuan Audit'
        
        if target_col in df.columns:
            # Pembersihan data paksa
            df[target_col] = pd.to_numeric(df[target_col].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
            
            # Plot
            fig = px.scatter(df, x='Departemen Divisi/Area', y=target_col, color='Departemen Divisi/Area', size=target_col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Kolom '{target_col}' tidak ditemukan. Cek ejaan di file Excel Anda.")
            st.write("Kolom yang tersedia di file Anda:", df.columns.tolist())

else:
    st.info("Silakan upload file untuk memulai.")
