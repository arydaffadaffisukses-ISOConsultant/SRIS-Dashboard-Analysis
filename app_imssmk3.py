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

def extract_score(text):
    nums = re.findall(r'\d+', str(text))
    return float(nums[0]) if nums else 0

# 1. Upload File
uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Load Data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # Pembersihan Data Utama
        df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_num)
        df['Maturity_Val'] = df['Implementation Risk Maturity'].apply(get_num)
        
        # 2. Layout Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Analisis Finansial", "AI Analyst", "Pentagon Analysis"])

        with tab1:
            st.subheader("📊 Statistik Temuan")
            col1, col2 = st.columns(2)
            with col1:
                dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
                dept_counts.columns = ['Departemen', 'Jumlah']
                fig = px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah')
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Daftar Lengkap Temuan")
            st.dataframe(df, hide_index=True, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", data=csv, file_name='data_audit.csv', mime='text/csv')

        with tab2:
            st.subheader("📈 Analisis Korelasi Finansial")
            fig_scat = px.scatter(df, x='Maturity_Val', y='Kerugian_Val', color='Departemen Divisi/Area', 
                                  size='Kerugian_Val', hover_name='Detail Temuan Ketidaksesuaian')
            st.plotly_chart(fig_scat, use_container_width=True)

        with tab3:
            st.subheader("🤖 AI Root Cause Analysis")
            api_key = st.text_input("Masukkan Google API Key:", type="password")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    selected_temuan = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].unique())
                    if st.button("Generate Analisis"):
                        with st.spinner("AI sedang berpikir..."):
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            response = model.generate_content(f"Analisis akar masalah untuk: {selected_temuan}")
                            st.markdown("### Hasil Analisis:")
                            st.write(response.text)
                except Exception as e:
                    st.error(f"Error AI: {e}")

        with tab4:
            st.subheader("📊 Pentagon Analysis: Risk Factors")
            
            cols_pentagon = [
                'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
                'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]',
                'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]',
                'Skoring Pentagon Analisis [P4- Operasional]',
                'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
            ]
            
            # Hitung rata-rata dengan penanganan data kosong
            radar_means = [df[col].apply(extract_score).mean() for col in cols_pentagon]
            
            labels = ['P1- Regulasi', 'P2- Finansial', 'P3- Integritas', 'P4- Operasional', 'P5- Reputasi']
            pentagon_data = pd.DataFrame({'r': radar_means, 'theta': labels})
            
            # Plot Radar
            fig_radar = px.line_polar(pentagon_data, r='r', theta='theta', line_close=True)
            fig_radar.update_traces(fill='toself')
            fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 5])))
            st.plotly_chart(fig_radar, use_container_width=True)
            st.info("Visualisasi radar chart di atas berdasarkan rata-rata skoring yang diinput pada form audit.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
else:
    st.info("Silakan upload file untuk memulai.")
