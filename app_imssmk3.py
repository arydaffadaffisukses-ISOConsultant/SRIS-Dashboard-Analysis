import streamlit as st
import google.generativeai as genai
import pandas as pd # Jika Bapak menggunakan pandas

# Pastikan tidak ada spasi di awal baris untuk definisi tab di bawah ini
tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

with tab1:
    st.write("Konten Tab 1")

with tab2:
    st.write("Konten Tab 2")

with tab3:
    st.subheader("AI Root Cause Analysis & CAPA")
    
    # Form input API Key
    user_api_key = st.text_input("Masukkan API Key:", type="password", help="Masukkan kunci yang diawali AIza atau kunci dari Google Cloud")
    
    temuan_col = "Detail Temuan Ketidaksesuaian"
    
    if temuan_col in df.columns:
        selected_temuan = st.selectbox("Pilih Temuan untuk dianalisis:", df[temuan_col].dropna().unique())
        
        if st.button("Generate Analisis AI"):
            if not user_api_key:
                st.warning("Mohon masukkan API Key terlebih dahulu!")
            else:
                try:
                    genai.configure(api_key=user_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Analisis akar masalah dan buatkan rencana CAPA untuk temuan: {selected_temuan}")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
