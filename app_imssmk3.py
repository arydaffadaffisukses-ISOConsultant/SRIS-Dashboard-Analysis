import streamlit as st
import pandas as pd
import plotly.express as px
import re
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

# Fungsi Pembersihan Data
def extract_score(text):
    nums = re.findall(r'\d+', str(text))
    return float(nums[0]) if nums else 0

# 1. Upload File
uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # Pembersihan Data Utama
        df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(extract_score)
        df['Maturity_Val'] = df['Implementation Risk Maturity'].apply(extract_score)
        
        # 2. Layout Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Analisis Finansial", "AI Analyst", "Pentagon Analysis"])

        with tab1:
            st.subheader("📊 Statistik Temuan")
            dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
            dept_counts.columns = ['Departemen', 'Jumlah']
            st.plotly_chart(px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah'), use_container_width=True)
            st.dataframe(df, hide_index=True, use_container_width=True)

        with tab2:
            st.subheader("📈 Analisis Korelasi Finansial")
            st.plotly_chart(px.scatter(df, x='Maturity_Val', y='Kerugian_Val', color='Departemen Divisi/Area', 
                                       size='Kerugian_Val', hover_name='Detail Temuan Ketidaksesuaian'), use_container_width=True)

        with tab3:
            st.subheader("🤖 AI Root Cause Analysis")
            api_key = st.text_input("Masukkan Google API Key:", type="password")
            if api_key:
                genai.configure(api_key=api_key)
                selected_temuan = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].unique())
                if st.button("Generate Analisis"):
                    with st.spinner("AI sedang berpikir..."):
                        response = genai.GenerativeModel('gemini-1.5-flash').generate_content(f"Analisis akar masalah untuk: {selected_temuan}")
                        st.markdown("### Hasil Analisis:")
                        st.write(response.text)

        with tab4:
            st.subheader("📊 Pentagon Analysis: Risk Profile")
            cols_p = [
                'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
                'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]',
                'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]',
                'Skoring Pentagon Analisis [P4- Operasional]',
                'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
            ]
            labels = ['P1-Regulasi', 'P2-Finansial', 'P3-Integritas', 'P4-Operasional', 'P5-Reputasi']
            
            data_plot = pd.DataFrame({
                'r': [df[c].apply(extract_score).mean() for c in cols_p] + [df[c].apply(extract_score).max() for c in cols_p],
                'theta': labels + labels,
                'Tipe': ['Rata-rata'] * 5 + ['Skor Tertinggi'] * 5
            })
            
            fig = px.line_polar(data_plot, r='r', theta='theta', color='Tipe', line_close=True, markers=True, 
                                color_discrete_map={'Rata-rata': 'blue', 'Skor Tertinggi': 'red'})
            fig.update_traces(fill='toself')
            fig.update_layout(polar=dict(radialaxis=dict(range=[0, 5])))
            st.plotly_chart(fig, use_container_width=True)
            st.warning("**Analisis:** Jika Garis Merah jauh melampaui Garis Biru, terdapat temuan kritis yang perlu segera dimitigasi.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Silakan upload file untuk memulai.")
