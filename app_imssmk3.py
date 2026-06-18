import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 1. BACA DATA
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    # 2. PEMBERSIHAN DATA KERUGIAN
    def get_num(text):
        text = str(text)
        nums = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
        return float(nums[0]) if nums else 0

    df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_num)

    # 3. TAB DASHBOARD
    tab1, tab2, tab3 = st.tabs(["Dashboard Ringkasan", "Analisis Finansial", "AI Analyst"])

    with tab1:
        st.subheader("Jumlah Temuan per Departemen")
        dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
        dept_counts.columns = ['Departemen', 'Jumlah']
        fig = px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Analisis Kerugian Finansial")
        fig_scat = px.scatter(
            df, x='Departemen Divisi/Area', y='Kerugian_Val', size='Kerugian_Val',
            color='Departemen Divisi/Area', hover_name='Detail Temuan Ketidaksesuaian'
        )
        st.plotly_chart(fig_scat, use_container_width=True)

    with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        
        if user_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=user_api_key)
                
                # Gunakan model yang stabil
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if "Detail Temuan Ketidaksesuaian" in df.columns:
                    options = df["Detail Temuan Ketidaksesuaian"].dropna().unique()
                    selected = st.selectbox("Pilih Temuan:", options)
                    
                    if st.button("Generate Analisis AI"):
                        with st.spinner("Menganalisis..."):
                            response = model.generate_content(f"Analisis akar masalah untuk: {selected}")
                            st.write(response.text)
            except Exception as e:
                st.error(f"Error AI: {e}")
else:
    st.info("Silakan upload file untuk memulai.")
