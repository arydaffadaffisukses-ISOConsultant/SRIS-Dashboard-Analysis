import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google import genai

st.set_page_config(page_title="SRIS Data Hub", layout="wide")

st.title("📊 Security Risk Intelligence System (SRIS)")
st.subheader("Pusat Analisis & Database Multi-Klien Terintegrasi")
st.markdown("---")

# --- SIDEBAR CONFIG ---
st.sidebar.markdown("### 🔑 KONFIGURASI AI")
api_key_input = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
uploaded_file = st.sidebar.file_uploader("📂 Hubungkan Database Pusat (Excel/CSV):", type=["xlsx", "csv"])

if uploaded_file:
    df_pusat = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df_pusat.columns = [col.strip() for col in df_pusat.columns]

    # Deteksi kolom perusahaan
    kolom_perusahaan = next((col for col in ['nama_perusahaan', 'perusahaan', 'Nama Perusahaan', 'company', 'Nama instansi / perusahaan'] if col in df_pusat.columns), None)

    if kolom_perusahaan:
        daftar = df_pusat[kolom_perusahaan].dropna().unique().tolist()
        perusahaan_terpilih = st.sidebar.selectbox("Pilih Klien Aktif:", daftar)
        df_aktif = df_pusat[df_pusat[kolom_perusahaan] == perusahaan_terpilih].copy()
        st.sidebar.success(f"🔐 Data Terkunci: {perusahaan_terpilih}")
    else:
        df_aktif = df_pusat.copy()
        perusahaan_terpilih = "Semua Klien"
        st.sidebar.warning("⚠️ Kolom 'nama_perusahaan' tidak ditemukan.")

    # --- MAIN DASHBOARD ---
    st.header(f"🏢 Executive Dashboard: {perusahaan_terpilih}")
    col1, col2 = st.columns(2)
    col1.metric("Total Temuan/Log Kasus", len(df_aktif))
    col2.metric("Standar Klausul", "HLS Universal (ISO & SMK3)")

    st.markdown("---")
    
    # --- AI CONSULTANT ---
    st.subheader(f"🤖 SRIS AI Consultant - Mode: {perusahaan_terpilih}")
    if api_key_input:
        client = genai.Client(api_key=api_key_input)
        if "messages" not in st.session_state: st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if user_prompt := st.chat_input(f"Tanyakan analisis untuk {perusahaan_terpilih}..."):
            with st.chat_message("user"): st.markdown(user_prompt)
            st.session_state.messages.append({"role": "user", "content": user_prompt})

            # Batasi konteks agar tidak melebihi token limit
            data_konteks = df_aktif.to_string(index=False)[:15000]
            
            prompt_final = f"""
            Anda adalah Konsultan Ahli Senior ISO dan SMK3. 
            Analisis data berikut untuk perusahaan '{perusahaan_terpilih}':
            {data_konteks}
            
            Pertanyaan: {user_prompt}
            """

            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=prompt_final
                )
                with st.chat_message("assistant"): st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error AI: {e}")
    else:
        st.info("Masukkan API Key di sidebar untuk mengaktifkan AI Consultant.")
else:
    st.info("Silakan upload file database untuk memulai.")
