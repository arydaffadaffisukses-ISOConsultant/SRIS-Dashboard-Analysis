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
                except Exception as e:
                    st.error(f"Error AI: {e}")

        with tab4:
            st.subheader("📊 Pentagon Analysis: Risk Factors")
            
            # --- LOGIKA NORMALISASI DATA (Agar skala P1-P5 seragam 0-5) ---
            
            # 1. P1 (Regulasi) & P3 (Integritas) & P4 (Operasional) - Berdasarkan Maturity (Skala 1-5)
            val_p1 = df['Maturity_Val'].mean() if not df.empty else 0
            val_p3 = df['Maturity_Val'].median() if not df.empty else 0
            val_p4 = df['Maturity_Val'].std() + 1 if not df.empty else 1 # Menambahkan buffer agar tidak 0
            
            # 2. P2 (Finansial) - Normalisasi Kerugian ke Skala 0-5
            # Jika kerugian tinggi, maka risiko tinggi (bisa dibalik rumusnya jika perlu)
            max_loss = df['Kerugian_Val'].max() if df['Kerugian_Val'].max() > 0 else 1
            val_p2 = (df['Kerugian_Val'].mean() / max_loss) * 5
            
            # 3. P5 (Reputasi) - Normalisasi berdasarkan volume temuan per departemen
            val_p5 = min(5, (df.shape[0] / 10)) # Contoh: semakin banyak temuan, risiko reputasi naik
            
            # Pastikan semua nilai berada di rentang 0-5
            r_values = [min(5, max(0, val_p1)), min(5, max(0, val_p2)), 
                        min(5, max(0, val_p3)), min(5, max(0, val_p4)), 
                        min(5, max(0, val_p5))]
            
            pentagon_data = pd.DataFrame(dict(
                r=r_values, 
                theta=['P1- Regulasi & Kepatuhan', 'P2- Finansial', 
                       'P3- Integritas data', 'P4- Operasional', 'P5- Reputasi']
            ))
            
            # Plot
            fig_radar = px.line_polar(pentagon_data, r='r', theta='theta', line_close=True)
            fig_radar.update_traces(fill='toself')
            fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 5])))
            st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("Silakan upload file untuk memulai.")
