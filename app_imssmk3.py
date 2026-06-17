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
        # Membaca file dengan aman
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    # Tab 1: Ringkasan
    with tab1:
        st.subheader("Analisis Temuan")
        if 'Departemen Divisi/Area' in df.columns:
            df_temuan = df.groupby('Departemen Divisi/Area').size().reset_index(name='Jumlah')
            fig_bar = px.bar(df_temuan, x='Departemen Divisi/Area', y='Jumlah', color='Jumlah', color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        if "Detail Temuan Ketidaksesuaian" in df.columns:
            st.dataframe(df[['Departemen Divisi/Area', 'Detail Temuan Ketidaksesuaian']], use_container_width=True)

    # Tab 2: Pentagon
    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        # Logika pembersihan skor
        def clean_score(val):
            try: return int(float(str(val).split()[0])) # Mengambil angka pertama
            except: return 0

        # ... (Gunakan logika pembersihan yang sudah Anda buat sebelumnya)
        st.info("Pastikan data Pentagon sudah terisi angka 1-5 agar radar chart muncul.")

    # Tab 3: AI Analyst
    with tab3:
        api_key = st.text_input("Google API Key:", type="password")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                temuan_list = df["Detail Temuan Ketidaksesuaian"].dropna().unique() if "Detail Temuan Ketidaksesuaian" in df.columns else []
                selected = st.selectbox("Pilih Temuan:", temuan_list)
                
                if st.button("Generate Analisis AI"):
                    response = model.generate_content(f"Analisis temuan audit: {selected}")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error pada AI: {e}")
