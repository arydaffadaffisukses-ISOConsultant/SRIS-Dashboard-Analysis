import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Pro Dashboard", layout="wide")

# Sidebar - Unggah Data
st.sidebar.header("📁 Sumber Data Audit")
uploaded_file = st.sidebar.file_uploader("Unggah File (CSV/XLSX):", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    st.sidebar.markdown("---")
    st.sidebar.header("Pilih Navigasi:")
    nav = st.sidebar.radio("", [
        "📊 Executive Summary", 
        "📈 Risk Maturity & Pentagon", 
        "🤖 SRIS AI Consultant"
    ])

    # Logika Navigasi
    if nav == "📊 Executive Summary":
        st.subheader("Executive Summary")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            sns.countplot(data=df, y='Departemen', ax=ax)
            st.pyplot(fig)
        with col2:
            st.write("Status Temuan")
            fig2, ax2 = plt.subplots()
            df['Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
            st.pyplot(fig2)

    elif nav == "📈 Risk Maturity & Pentagon":
        st.subheader("Risk Maturity Analysis")
        # Radar Chart Logic
        categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        vals = [df.get('P1_Regulasi', 0).mean(), df.get('P2_Finansial', 0).mean(), 
                df.get('P3_Integritas', 0).mean(), df.get('P4_Operasional', 0).mean(), 
                df.get('P5_Reputasi', 0).mean()]
        fig = go.Figure(data=go.Scatterpolar(r=vals, theta=categories, fill='toself'))
        st.plotly_chart(fig)

    elif nav == "🤖 SRIS AI Consultant":
        st.subheader("SRIS AI Consultant")
        query = st.text_input("Masukkan pertanyaan audit Anda:")
        if st.button("Analisis"):
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(query)
                st.write(response.text)
            except Exception as e:
                st.error("Pastikan API Key sudah diset di menu Secrets!")

else:
    st.warning("Silakan unggah file audit di sidebar.")
