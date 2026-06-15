import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
from pypdf import PdfReader

st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("📊 SRIS Dashboard Analysis")

# Inisialisasi Session State untuk teks regulasi
if 'regulasi_text' not in st.session_state:
    st.session_state['regulasi_text'] = "Tidak ada regulasi khusus."

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
            fig2 = px.histogram(df, x='Departemen Divisi/Area', color='Estimasi Kerugian Finansial Atas Temuan Audit')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        # (Logika mapping tetap sama seperti sebelumnya)
        # ... [Potongan kode mapping Pentagon] ...
        st.write("Radar Chart akan menampilkan rata-rata performa berdasarkan data di atas.")

    with tab4:
        st.subheader("📜 Upload Peraturan K3/Lingkungan (PDF)")
        pdf_file = st.file_uploader("Upload PDF Regulasi:", type=["pdf"])
        if pdf_file:
            reader = PdfReader(pdf_file)
            text = "".join([page.extract_text() for page in reader.pages])
            st.session_state['regulasi_text'] = text
            st.success(f"Regulasi berhasil dimuat: {pdf_file.name}")
            with st.expander("Lihat ringkasan dokumen"):
                st.write(text[:1000] + "...")

    with tab3:
        st.subheader("🤖 AI Root Cause Analysis (Berbasis Regulasi)")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        
        if user_api_key and "Detail Temuan Ketidaksesuaian" in df.columns:
            model = genai.GenerativeModel('gemini-pro')
            selected = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].unique())
            
            if st.button("Generate Analisis Berbasis Regulasi"):
                reg_context = st.session_state['regulasi_text']
                prompt = f"""
                Analisis temuan audit berikut: {selected}.
                Gunakan konteks peraturan/regulasi K3/Lingkungan berikut sebagai acuan hukum:
                {reg_context[:4000]}
                
                Berikan rekomendasi perbaikan yang patuh pada regulasi tersebut.
                """
                with st.spinner('AI sedang mencocokkan temuan dengan regulasi...'):
                    response = model.generate_content(prompt)
                    st.markdown("### Hasil Analisis AI:")
                    st.write(response.text)
