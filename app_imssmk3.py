import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("SRIS Dashboard Analysis")

uploaded_file = st.file_uploader("Upload file CSV/Excel:", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.histogram(df, x='Departemen Divisi/Area', color='Estimasi Kerugian Finansial Atas Temuan Audit', barmode='group')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        
        # Pembersihan Data agar Mapping Berhasil
        cols_pentagon = [
            'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 
            'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 
            'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 
            'Skoring Pentagon Analisis [P4- Operasional]', 
            'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
        ]
        
        for col in cols_pentagon:
            if col in df.columns:
                # Membersihkan string dan mengubah jadi huruf kapital awal saja
                df[col] = df[col].astype(str).str.strip().str.capitalize()
        
        # Mapping Angka
        mapping = {'Rendah': 1, 'Cukup': 2, 'Sedang': 3, 'Baik': 4, 'Sangat baik': 5}
        for col in cols_pentagon:
            if col in df.columns:
                df[col] = df[col].map(mapping).fillna(0)

        # Debugging (untuk melihat apakah data sudah jadi angka)
        st.write("Cek Data Pentagon (Pastikan kolom berisi angka):")
        st.write(df[cols_pentagon].head()) 
        
        # Hitung Rata-rata
        avg_scores = df[cols_pentagon].mean().values
        categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']

        # Radar Chart
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_scores, theta=categories, fill='toself', 
            fillcolor='rgba(99, 110, 250, 0.5)', line=dict(color='#636EFA', width=3)
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Rata-rata Skor Pentagon")
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Risk & Maturity
        fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', color='Departemen Divisi/Area')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Hubungan Risiko & Kerugian
        fig4 = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', 
                          color='Departemen Divisi/Area', size='Implementation Risk Maturity', 
                          hover_data=['Detail Temuan Ketidaksesuaian'], template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.subheader("AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        if "Detail Temuan Ketidaksesuaian" in df.columns:
            selected = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
            if st.button("Generate Analisis AI") and user_api_key:
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Analisis akar masalah: {selected}")
                st.markdown(response.text)
