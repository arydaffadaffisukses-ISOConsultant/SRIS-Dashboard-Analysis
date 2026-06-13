import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Pro Dashboard", layout="wide")

# Sidebar - Unggah Data
st.sidebar.header("📁 Sumber Data Audit")
uploaded_file = st.sidebar.file_uploader("Unggah File (CSV/XLSX):", type=["csv", "xlsx"])
st.sidebar.caption("200MB per file • CSV, XLSX")

st.sidebar.markdown("---")
st.sidebar.header("Pilih Navigasi Dashboard:")
nav = st.sidebar.radio("", [
    "📊 Executive Summary & Status Temuan",
    "📈 Risk Maturity Analysis & Pentagon",
    "🤖 SRIS Management AI Consultant"
])

# Fungsi Radar Chart Pentagon
def plot_radar(df):
    categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
    # Pastikan kolom ini ada di CSV Bapak, jika tidak akan diisi 0
    vals = [df.get('P1_Regulasi', 0).mean(), df.get('P2_Finansial', 0).mean(), 
            df.get('P3_Integritas', 0).mean(), df.get('P4_Operasional', 0).mean(), 
            df.get('P5_Reputasi', 0).mean()]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals, theta=categories, fill='toself', name='Score'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    return fig

# Logika Utama
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    if nav == "📊 Executive Summary & Status Temuan":
        st.subheader("📊 Executive Summary & Status Temuan")
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Temuan per Departemen")
            fig, ax = plt.subplots()
            sns.countplot(data=df, y='Departemen', ax=ax)
            st.pyplot(fig)
        with col2:
            st.write("### Status Temuan")
            fig2, ax2 = plt.subplots()
            df['Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
            st.pyplot(fig2)
        st.dataframe(df, use_container_width=True)

    elif nav == "📈 Risk Maturity Analysis & Pentagon":
        st.subheader("📈 Risk Maturity Analysis")
        # Perhitungan Maturitas
        total_avg = df.filter(like='P').mean().mean() if 'P1_Regulasi' in df.columns else 0
        
        st.metric("Tingkat Maturitas Organisasi", f"{total_avg:.2f} / 5.0")
        
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.info(f"Analisis berdasarkan 5 Pilar Risiko. Skor rata-rata: {total_avg:.2f}")
        with col2:
            st.write("### Pentagon Risk Analysis")
            st.plotly_chart(plot_radar(df), use_container_width=True)

   elif nav == "🤖 SRIS Management AI Consultant":
        st.subheader("🤖 SRIS Management AI Consultant")
        
        # Pilih temuan mana yang ingin dianalisis
        temuan_list = df['Temuan'].unique()
        selected_temuan = st.selectbox("Pilih Temuan untuk dianalisis:", temuan_list)
        
        if st.button("Analisis Akar Masalah & CAPA"):
            import google.generativeai as genai
            
            # Konfigurasi API
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Anda adalah Auditor Ahli SMK3 dan ISO. Analisis temuan berikut: '{selected_temuan}'.
            Berikan:
            1. Analisis Akar Masalah (Root Cause Analysis - 5 Whys).
            2. Rekomendasi Tindakan Perbaikan (CAPA).
            3. Analisis Risiko jika tidak segera diperbaiki.
            """
            
            response = model.generate_content(prompt)
            st.write("### Hasil Analisis AI:")
            st.write(response.text)

else:
    st.warning("Silakan unggah file data audit di sidebar untuk memulai analisis.")
