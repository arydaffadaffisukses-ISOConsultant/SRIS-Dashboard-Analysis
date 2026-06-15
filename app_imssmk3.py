import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("📊 SRIS Dashboard Analysis")

uploaded_file = st.file_uploader("Upload file CSV/Excel:", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.histogram(df, x='Departemen Divisi/Area', color='Estimasi Kerugian Finansial Atas Temuan Audit')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        
        cols_pentagon = [
            'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 
            'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 
            'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 
            'Skoring Pentagon Analisis [P4- Operasional]', 
            'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
        ]
        
        def clean_and_map(val):
            val_str = str(val).strip().lower()
            if any(x in val_str for x in ['rendah', 'low', '1']): return 1
            if any(x in val_str for x in ['cukup', 'medium', '2']): return 2
            if any(x in val_str for x in ['sedang', '3']): return 3
            if any(x in val_str for x in ['baik', 'high', '4']): return 4
            if any(x in val_str for x in ['sangat baik', 'excellent', '5']): return 5
            return 0

        for col in cols_pentagon:
            if col in df.columns:
                df[col] = df[col].apply(clean_and_map)
        
        # Tampilkan data agar Bapak bisa memastikan angka sudah benar
        st.write("Data yang terdeteksi (1-5):")
        st.write(df[cols_pentagon].head())
        
        avg_scores = df[cols_pentagon].mean().values
        categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_scores, theta=categories, fill='toself',
            fillcolor='rgba(99, 110, 250, 0.4)',
            line=dict(color='#636EFA', width=3),
            marker=dict(size=8)
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Rata-rata Skor Pentagon")
        st.plotly_chart(fig_radar, use_container_width=True)
        
        fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', color='Departemen Divisi/Area')
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        
        if user_api_key:
            try:
                genai.configure(api_key=user_api_key)
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_name = st.selectbox("Pilih Model AI:", models)
                
                if "Detail Temuan Ketidaksesuaian" in df.columns:
                    selected = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
                    if st.button("Generate Analisis AI"):
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(f"Analisis akar masalah: {selected}")
                        st.markdown(response.text)
            except Exception as e:
                st.error(f"Error AI: {e}")
