import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics: Audit & Risk")

# 1. Load Data
uploaded_file = st.file_uploader("Upload CSV Audit", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip() # Bersihkan nama kolom
    st.session_state["df"] = df
    st.success("Data berhasil dimuat!")

if "df" in st.session_state:
    df = st.session_state["df"]
    
    # Fungsi untuk mengubah kolom menjadi angka murni (menghapus simbol non-angka)
    def bersihkan_angka(col):
        if col in df.columns:
            return pd.to_numeric(df[col].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        return pd.Series([0]*len(df))

    # Sidebar Navigasi
    menu = st.sidebar.radio("Pilih Analisis:", ["Jumlah Temuan per Dept", "ISO & Finansial", "Pentagon Analysis", "Risk Maturity"])

    if menu == "Jumlah Temuan per Dept":
        st.subheader("Distribusi Temuan per Departemen")
        fig = px.bar(df.groupby('Departemen Divisi/Area').size().reset_index(name='Jumlah'), 
                     x='Departemen Divisi/Area', y='Jumlah', color='Jumlah')
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "ISO & Finansial":
        st.subheader("Standar ISO vs Dampak Finansial")
        df['Finansial'] = bersihkan_angka('Estimasi Kerugian Perusahaan akibat audit Ini')
        fig = px.scatter(df, x='Standar ISO yang Terdampak', y='Finansial', color='Departemen Divisi/Area', size='Finansial')
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Pentagon Analysis":
        st.subheader("Fraud Pentagon & Risk Treatment")
        # Asumsi kolom pentagon ada, jika tidak, kita tampilkan tabel saja
        st.write("Analisis Fraud Pentagon per Departemen:")
        fig = px.sunburst(df, path=['Departemen Divisi/Area', 'Risk Treatment'], values='Finansial')
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Risk Maturity":
        st.subheader("Pengendalian & Risk Maturity")
        fig = px.scatter(df, x='Risk Treatment', y='Implementation Risk Maturity', color='Departemen Divisi/Area')
        st.plotly_chart(fig, use_container_width=True)
