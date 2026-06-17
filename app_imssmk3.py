import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

st.set_page_config(page_title="SRIS AI Auditor", layout="wide")

# Sidebar untuk API Key (Simpan di sini agar tidak di kode)
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

st.title("🛡️ SRIS: Smart Risk & Audit System")

# Load Data
try:
    df = pd.read_excel("contoh soal.xlsx")
    df.columns = df.columns.str.strip()
except:
    st.error("File 'contoh soal.xlsx' tidak ditemukan! Pastikan file diunggah di folder yang sama.")
    st.stop()

# Tampilan Visual (Sunburst & Matrix)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Risiko")
    fig_sun = px.sunburst(df, path=['Risk Treatment (Strategis)', 'Pengendalian Resiko (Taktis)'], 
                          values='Estimasi Kerugian Finansial Atas Temuan Audit')
    st.plotly_chart(fig_sun, use_container_width=True)

with col2:
    st.subheader("Analisis AI")
    selected_issue = st.selectbox("Pilih Temuan untuk dianalisis AI:", df['Detail Temuan Ketidaksesuaian'].unique())
    
    if st.button("Analisis dengan AI"):
        if not api_key:
            st.warning("Masukkan API Key terlebih dahulu!")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Sebagai auditor profesional, analisis temuan berikut: {selected_issue}. Berikan akar masalah dan rekomendasi perbaikan."
            response = model.generate_content(prompt)
            st.success("Hasil Analisis AI:")
            st.write(response.text)
