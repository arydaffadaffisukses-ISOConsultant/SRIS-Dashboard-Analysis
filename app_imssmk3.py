import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. Konfigurasi Awal
st.set_page_config(layout="wide")
st.title("SRIS Dashboard Analysis")

# 2. Upload Data
uploaded_file = st.file_uploader("Upload file CSV/Excel:", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # 3. DEFINISI TAB HARUS DI SINI (Sebelum 'with tab2')
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

   tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.histogram(df, x='Departemen Divisi/Area', color='Estimasi Kerugian Finansial Atas Temuan Audit', 
                                title='Komposisi Kerugian per Departemen', barmode='group')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        # Radar Chart
        cols_pentagon = ['Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 'Skoring Pentagon Analisis [P4- Operasional]', 'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]']
        avg_scores = df[cols_pentagon].mean().values
        fig_radar = go.Figure(data=go.Scatterpolar(r=avg_scores, theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'], fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Rata-rata Pentagon Analysis")
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Risk & Maturity
        fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', title='Tingkat Kematangan Risiko', color='Departemen Divisi/Area')
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', color='Departemen Divisi/Area', size='Implementation Risk Maturity', hover_data=['Detail Temuan Ketidaksesuaian'], title='Bubble Analysis: Risiko vs Kerugian')
        st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.subheader("AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        temuan_col = "Detail Temuan Ketidaksesuaian"
        if temuan_col in df.columns:
            selected = st.selectbox("Pilih Temuan:", df[temuan_col].dropna().unique())
            if st.button("Generate Analisis AI"):
                if user_api_key:
                    try:
                        genai.configure(api_key=user_api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(f"Analisis akar masalah dan rencana CAPA untuk: {selected}")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error AI: {e}")
                else:
                    st.warning("Mohon masukkan API Key.")
else:
    st.info("Silakan upload file untuk memulai.")
