import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(layout="wide")
st.title("SRIS Dashboard Analysis")

# 2. Upload Data
uploaded_file = st.file_uploader("Upload file CSV/Excel data temuan:", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Membersihkan spasi pada kolom
    df.columns = df.columns.str.strip()

    # 3. Membuat Tab
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.bar(df, x='Departemen Divisi/Area', y='Estimasi Kerugian Finansial Atas Temuan Audit', title='Estimasi Kerugian')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Risk & Maturity")
        fig3 = px.box(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', title='Tingkat Kematangan Risiko')
        st.plotly_chart(fig3, use_container_width=True)
        fig4 = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', color='Departemen Divisi/Area', title='Hubungan Risiko & Kerugian')
        st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.subheader("AI Root Cause Analysis & CAPA")
        user_api_key = st.text_input("Masukkan API Key:", type="password")
        temuan_col = "Detail Temuan Ketidaksesuaian"
        if temuan_col in df.columns:
            selected_temuan = st.selectbox("Pilih Temuan:", df[temuan_col].dropna().unique())
            if st.button("Generate Analisis AI"):
                if not user_api_key:
                    st.warning("Masukkan API Key terlebih dahulu!")
                else:
                    try:
                        genai.configure(api_key=user_api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(f"Analisis akar masalah dan rencana CAPA untuk: {selected_temuan}")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error AI: {e}")

else:
    st.info("Silakan upload file CSV atau Excel Bapak di atas untuk memulai.")
