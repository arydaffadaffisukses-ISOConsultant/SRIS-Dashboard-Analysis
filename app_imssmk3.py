import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("SRIS Dashboard Analysis")

uploaded_file = st.file_uploader("Upload file CSV/Excel:", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Perhatikan: Baris di bawah ini harus menjorok 4 spasi dari margin kiri
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
        
        # 1. Mapping Teks ke Angka (Penerjemah)
        # Sesuaikan isi 'mapping' ini dengan kata-kata yang ada di file Excel Bapak
        mapping = {'Rendah': 1, 'Cukup': 2, 'Sedang': 3, 'Baik': 4, 'Sangat Baik': 5}
        
        cols_pentagon = [
            'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 
            'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 
            'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 
            'Skoring Pentagon Analisis [P4- Operasional]', 
            'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
        ]
        
        # Mengonversi kolom teks menjadi angka
        for col in cols_pentagon:
            if col in df.columns:
                df[col] = df[col].map(mapping).fillna(0) # Jika teks tidak cocok, jadi 0

        # Radar Chart
        avg_scores = df[cols_pentagon].mean().values
        fig_radar = go.Figure(data=go.Scatterpolar(r=avg_scores, theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'], fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Rata-rata Pentagon Analysis")
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Risk & Maturity (Memastikan kolom ini juga angka)
        # Jika kolom ini juga berupa teks, ganti angka 4 di bawah dengan cara yang sama seperti di atas
        st.markdown("### Implementation Risk Maturity")
        fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', color='Departemen Divisi/Area')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Bubble Chart
        st.markdown("### Hubungan Risiko & Kerugian")
        fig4 = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', 
                          color='Departemen Divisi/Area', size='Implementation Risk Maturity', 
                          hover_data=['Detail Temuan Ketidaksesuaian'], template="plotly_white")
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
