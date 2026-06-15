import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("SRIS Dashboard Analysis")

uploaded_file = st.file_uploader("Upload file CSV/Excel:", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 1. Load & Bersihkan Data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # 2. PENGOLAHAN DATA: Mengubah Teks ke Angka agar Grafik Hidup
    # Sesuaikan 'mapping' ini dengan kata-kata yang ada di file Excel Bapak
    mapping = {'Rendah': 1, 'Cukup': 2, 'Sedang': 3, 'Baik': 4, 'Sangat Baik': 5}
    cols_pentagon = [
        'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 
        'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 
        'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 
        'Skoring Pentagon Analisis [P4- Operasional]', 
        'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
    ]
    
    for col in cols_pentagon:
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(0)
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
        st.subheader("Analisis Temuan")
        fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        
        # Radar Chart yang berwarna dan menarik
        avg_scores = df[cols_pentagon].mean().values
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
              r=avg_scores, theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'], 
              fill='toself', fillcolor='rgba(99, 110, 250, 0.5)', line=dict(color='#636EFA', width=3)
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Rata-rata Skor Pentagon")
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Risk & Maturity
        fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', color='Departemen Divisi/Area', title='Kematangan Risiko')
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("AI Root Cause Analysis")
        key = st.text_input("Masukkan Google API Key:", type="password")
        if st.button("Generate Analisis AI") and key:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Mengambil data pertama sebagai sampel untuk analisis
            sample_data = df.iloc[0].to_string()
            response = model.generate_content(f"Analisis data berikut: {sample_data}")
            st.markdown(response.text)
