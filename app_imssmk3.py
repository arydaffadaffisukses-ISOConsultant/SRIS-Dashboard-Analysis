import streamlit as st
import pandas as pd
import plotly.express as px
import re
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

# Fungsi Pembersihan Angka
def get_num(text):
    text = str(text)
    nums = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
    return float(nums[0]) if nums else 0

# 1. Upload File
uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Load Data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # Pembersihan Data
        df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_num)
        df['Maturity_Val'] = df['Implementation Risk Maturity'].apply(get_num)
        
        # --- LOGIKA KATEGORISASI OTOMATIS ---
        # Kita membagi data ke 5 dimensi berdasarkan isi kolom 'Detail Temuan Ketidaksesuaian'
        def categorize_finding(text):
            text = str(text).lower()
            if any(x in text for x in ['regulasi', 'kepatuhan', 'legal', 'uu']): return 'P1- Regulasi & Kepatuhan'
            if any(x in text for x in ['budget', 'biaya', 'kerugian', 'finansial', 'anggaran']): return 'P2- Finansial'
            if any(x in text for x in ['data', 'sistem', 'it', 'input']): return 'P3- Integritas data'
            if any(x in text for x in ['prosedur', 'operasional', 'proses', 'kerja']): return 'P4- Operasional'
            return 'P5- Reputasi'

        df['Dimensi_Audit'] = df['Detail Temuan Ketidaksesuaian'].apply(categorize_finding)

        # 2. Layout Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Analisis Finansial", "AI Analyst", "Pentagon Analysis"])

        with tab1:
            st.subheader("Jumlah Temuan per Departemen")
            dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
            dept_counts.columns = ['Departemen', 'Jumlah']
            fig = px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, hide_index=True, use_container_width=True)

        with tab2:
            st.subheader("Analisis Korelasi Finansial")
            fig_scat = px.scatter(df, x='Maturity_Val', y='Kerugian_Val', color='Departemen Divisi/Area', size='Kerugian_Val')
            st.plotly_chart(fig_scat, use_container_width=True)

        with tab3:
            st.subheader("🤖 AI Root Cause Analysis")
            api_key = st.text_input("Masukkan Google API Key:", type="password")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    selected_temuan = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].unique())
                    if st.button("Generate Analisis"):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(f"Analisis akar masalah untuk: {selected_temuan}")
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error AI: {e}")

        with tab4:
            st.subheader("📊 Pentagon Analysis: Risk Factors")
            
            # Daftar kolom yang tepat sesuai header CSV Anda
            cols_pentagon = [
                'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
                'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]',
                'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]',
                'Skoring Pentagon Analisis [P4- Operasional]',
                'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
            ]
            
            # Fungsi untuk membersihkan angka (mengambil angka pertama yang muncul)
            def extract_score(text):
                nums = re.findall(r'\d+', str(text))
                return float(nums[0]) if nums else 0

            # Hitung rata-rata tiap kolom
            radar_means = []
            for col in cols_pentagon:
                # Membersihkan data terlebih dahulu lalu hitung rata-rata
                score = df[col].apply(extract_score).mean()
                radar_means.append(score)
            
            # Label untuk radar chart
            labels = ['P1- Regulasi', 'P2- Finansial', 'P3- Integritas', 'P4- Operasional', 'P5- Reputasi']
            
            pentagon_data = pd.DataFrame(dict(r=radar_means, theta=labels))
            
            # Plot
            fig_radar = px.line_polar(pentagon_data, r='r', theta='theta', line_close=True)
            fig_radar.update_traces(fill='toself')
            fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 5]))) # Asumsi skala 1-5
            st.plotly_chart(fig_radar, use_container_width=True)
            
            st.info("Perhitungan ini mengambil rata-rata langsung dari kolom 'Skoring Pentagon' yang ada di file Anda.")
