import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("📊 SRIS Dashboard Analysis")

# Inisialisasi Session State
if 'regulasi_text' not in st.session_state:
    st.session_state['regulasi_text'] = ""

uploaded_file = st.file_uploader("Upload file CSV/Excel Data Audit:", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🕸️ Pentagon & Risk", "🤖 AI Analyst", "📜 Regulasi PDF"])

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.subheader("Trend Estimasi Kerugian")
            fig_line = px.line(df, x='Departemen Divisi/Area', y='Estimasi Kerugian Finansial Atas Temuan Audit', 
                               color='Departemen Divisi/Area', markers=True, template="plotly_white")
            st.plotly_chart(fig_line, use_container_width=True)

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
            if col in df.columns: df[col] = df[col].apply(clean_and_map)
        
        avg_scores = df[cols_pentagon].mean().values
        categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure(go.Scatterpolar(r=avg_scores, theta=categories, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 5])), title="Rata-rata Skor Pentagon")
        st.plotly_chart(fig_radar, use_container_width=True)

        st.subheader("📈 Hubungan Risiko vs Kerugian")
        fig_bubble = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', 
                                size='Implementation Risk Maturity', color='Departemen Divisi/Area', template="plotly_white")
        st.plotly_chart(fig_bubble, use_container_width=True)

    with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        if user_api_key and "Detail Temuan Ketidaksesuaian" in df.columns:
            genai.configure(api_key=user_api_key)
            model = genai.GenerativeModel('gemini-pro')
            selected = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
            if st.button("Generate Analisis"):
                prompt = f"Analisis akar masalah: {selected}. Regulasi acuan: {st.session_state['regulasi_text'][:2000]}"
                st.write(model.generate_content(prompt).text)

    with tab4:
        st.subheader("📜 Upload PDF Regulasi")
        if PdfReader:
            pdf_file = st.file_uploader("Upload PDF:", type=["pdf"])
            if pdf_file:
                reader = PdfReader(pdf_file)
                st.session_state['regulasi_text'] = "".join([p.extract_text() for p in reader.pages])
                st.success("Regulasi dimuat!")
        else:
            st.warning("Instalasi pypdf tidak ditemukan.")
