import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("📊 SRIS Dashboard Analysis")

# Upload File
uploaded_file = st.file_uploader("Upload file CSV/Excel Data Audit:", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    # Tab 1: Dashboard Ringkasan
    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        
        with col1:
            # Grafik Batang: Temuan Per Departemen (Terbanyak = Merah)
            st.subheader("Temuan Per Departemen")
            df_temuan = df.groupby('Departemen Divisi/Area').size().reset_index(name='Jumlah')
            df_temuan = df_temuan.sort_values(by='Jumlah', ascending=False)
            
            # Membuat list warna: merah untuk yang tertinggi, biru untuk lainnya
            colors = ['red' if i == 0 else 'royalblue' for i in range(len(df_temuan))]
            
            fig_bar = px.bar(df_temuan, x='Departemen Divisi/Area', y='Jumlah', 
                             title='Distribusi Jumlah Temuan per Departemen',
                             color_discrete_sequence=['royalblue'])
            fig_bar.update_traces(marker_color=colors)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            # Pie Chart: Estimasi Kerugian Per Departemen (Resiko Tinggi = Merah)
            st.subheader("Estimasi Kerugian Per Departemen")
            df_kerugian = df.groupby('Departemen Divisi/Area')['Estimasi Kerugian Finansial Atas Temuan Audit'].sum().reset_index()
            df_kerugian = df_kerugian.sort_values(by='Estimasi Kerugian Finansial Atas Temuan Audit', ascending=False)
            
            # Logika warna: Merah untuk nilai tertinggi (asumsi resiko tinggi di kerugian terbesar)
            colors_pie = ['red' if i == 0 else 'lightgrey' for i in range(len(df_kerugian))]
            
            fig_pie = px.pie(df_kerugian, names='Departemen Divisi/Area', 
                             values='Estimasi Kerugian Finansial Atas Temuan Audit',
                             title='Proporsi Estimasi Kerugian Finansial',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            
            # Memaksa warna merah untuk bagian terbesar
            fig_pie.update_traces(marker=dict(colors=colors_pie))
            st.plotly_chart(fig_pie, use_container_width=True)

    # Tab 2: Pentagon & Risk
    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        # ... (kode Pentagon Radar & Bubble Chart tetap sama) ...
        # (Kode di atas sudah Anda miliki, silakan pertahankan)

    # Tab 3: AI Analyst
    with tab3:
        # ... (kode AI tetap sama) ...
