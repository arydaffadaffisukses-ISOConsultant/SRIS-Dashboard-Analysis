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

        # 2. Layout Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Analisis Finansial", "AI Analyst", "Pentagon Analysis"])

        with tab1:
            st.subheader("Jumlah Temuan per Departemen")
            dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
            dept_counts.columns = ['Departemen', 'Jumlah']
            fig = px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah')
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Daftar Lengkap Temuan Ketidaksesuaian")
            st.dataframe(df, hide_index=True, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Daftar Temuan (CSV)", data=csv, file_name='daftar_temuan.csv', mime='text/csv')

        with tab2:
            st.subheader("Analisis Korelasi Finansial")
            fig_scat = px.scatter(
                df, x='Maturity_Val', y='Kerugian_Val', size='Kerugian_Val',
                color='Departemen Divisi/Area', hover_name='Detail Temuan Ketidaksesuaian',
                template="plotly_white"
            )
            st.plotly_chart(fig_scat, use_container_width=True)

        with tab3:
            st.subheader("🤖 AI Root Cause Analysis")
            api_key = st.text_input("Masukkan Google API Key:", type="password")
            
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    model_names = [m.name for m in models]
                    
                    if model_names:
                        selected_model = st.selectbox("Pilih Model AI:", model_names)
                        options = df["Detail Temuan Ketidaksesuaian"].dropna().unique()
                        selected_temuan = st.selectbox("Pilih Temuan:", options)
                        
                        if st.button("Generate Analisis"):
                            with st.spinner("AI sedang berpikir..."):
                                model = genai.GenerativeModel(selected_model)
                                response = model.generate_content(f"Analisis akar masalah untuk: {selected_temuan}")
                                st.markdown("### Hasil Analisis AI:")
                                st.write(response.text)
                    else:
                        st.warning("Tidak ditemukan model yang tersedia.")
                except Exception as e:
                    st.error(f"Error AI: {e}")

        with tab4:
    st.subheader("📊 Pentagon Analysis: Risk Factors")
    
    # 1. Pastikan kita punya cara untuk mengelompokkan data ke P1-P5
    # Karena data Anda mungkin belum memiliki kolom P1-P5, 
    # kita bisa menggunakan rata-rata berdasarkan kolom 'Maturity_Val'
    # sebagai contoh untuk setiap dimensi (Anda bisa menyesuaikan logikanya):
    
    # Contoh kalkulasi sederhana berdasarkan data yang ada:
    # Anda bisa mengganti angka-angka ini dengan logika per-departemen atau per-klausul
    val_p1 = df[df['Implementation Risk Maturity'] == 'Low']['Kerugian_Val'].mean() if 'Low' in df['Implementation Risk Maturity'].values else 3
    val_p2 = df['Kerugian_Val'].mean() / 1000000 # Contoh normalisasi data finansial
    val_p3 = 4 # Dummy value, silakan ganti dengan kolom relevan
    val_p4 = 3.5 
    val_p5 = 4
    
    pentagon_data = pd.DataFrame(dict(
        r=[val_p1, val_p2, val_p3, val_p4, val_p5], 
        theta=['P1- Regulasi & Kepatuhan', 
               'P2- Finansial', 
               'P3- Integritas data', 
               'P4- Operasional', 
               'P5- Reputasi']
    ))
    
    fig_radar = px.line_polar(pentagon_data, r='r', theta='theta', line_close=True)
    fig_radar.update_traces(fill='toself')
    st.plotly_chart(fig_radar, use_container_width=True)
    except Exception as e:
        st.error(f"Terjadi kesalahan pada data: {e}")
else:
    st.info("Silakan upload file untuk memulai.")
