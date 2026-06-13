import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Paksa backend agar stabil di Cloud
matplotlib.use('Agg')

# ==========================================
# 1. KONFIGURASI HALAMAN (HANYA SEKALI)
# ==========================================
st.set_page_config(page_title="SRIS Engine Dashboard", layout="wide", page_icon="🛡️")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .metric-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); border-left: 6px solid #1E5631; }
    .security-banner { background: linear-gradient(to right, #1e5631, #4c9a2a); color: white; padding: 20px; border-radius: 8px; margin-bottom: 25px; }
    .chat-bubble-user { background-color: #1E5631; color: white; padding: 12px; border-radius: 15px; margin-bottom: 10px; text-align: right; }
    .chat-bubble-bot { background-color: #e9ecef; color: #333; padding: 12px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='security-banner'>
        <h2>🛡️ SRIS Integrated Engine: ISO-IMS & SMK3 Dashboard</h2>
        <p>Strategic Risk Intelligence System | Otomatisasi Matriks Kepatuhan ISO & SMK3 PP 50/2012</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA & STATE
# ==========================================
if 'df_ims' not in st.session_state:
    st.session_state['df_ims'] = None

st.sidebar.header("📂 Sumber Data Audit")
uploaded_file = st.sidebar.file_uploader("Unggah File (CSV/XLSX):", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.session_state['df_ims'] = df
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# ==========================================
# 3. LOGIKA ENGINE & FILTER
# ==========================================
if st.session_state['df_ims'] is not None:
    df = st.session_state['df_ims'].copy()
    df.columns = [col.strip() for col in df.columns]
    
    # Filter Departemen
    kolom_dept = 'Departemen Divisi/Area'
    if kolom_dept in df.columns:
        dept_list = ["Semua"] + sorted(list(df[kolom_dept].dropna().unique()))
        pilihan_dept = st.sidebar.selectbox("Pilih Departemen:", dept_list)
        df_filtered = df if pilihan_dept == "Semua" else df[df[kolom_dept] == pilihan_dept]
    else:
        df_filtered = df
        pilihan_dept = "Semua"

    # ==========================================
    # 4. NAVIGASI
    # ==========================================
    menu = st.sidebar.radio("Navigasi:", ["📊 Executive Summary", "🕸️ Pentagon Risk", "🤖 SRIS AI Consultant"])

    if menu == "📊 Executive Summary":
        st.subheader(f"Analisis Departemen: {pilihan_dept}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Temuan", len(df_filtered))
        c2.metric("Status Open", len(df_filtered)) # Sesuaikan dengan kolom status Bapak
        c3.metric("Status Closed", 0)
        
    elif menu == "🤖 SRIS AI Consultant":
        st.subheader("🤖 SRIS Executive AI Consultant")
        
        # INSTRUKSI AI (DIBUNGKUS AGAR TIDAK ERROR)
        system_instruction = """
        Anda adalah Senior Management Consultant & Auditor Utama bersertifikasi ISO 9001, 14001, 45001, dan SMK3 PP 50/2012.
        Tugas Anda membantu merumuskan akar masalah dan menyusun Rekomendasi Tindakan Perbaikan (CAPA) untuk Level Operasional.
        """
        
        api_key = st.text_input("🔑 Masukkan Gemini API Key:", type="password")
        if api_key:
            user_query = st.chat_input("Tanyakan solusi CAPA...")
            if user_query:
                st.write(f"🧑‍💼 Anda: {user_query}")
                st.info("AI sedang menganalisis data...")
                # Panggil API Gemini di sini...
        else:
            st.warning("Masukkan API Key untuk memulai sesi.")

else:
    st.info("Silakan unggah data audit di sidebar untuk memulai.")
