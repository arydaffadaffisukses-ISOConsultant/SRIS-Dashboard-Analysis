import streamlit as st
import pandas as pd
import numpy as np
import os

# Paksa Matplotlib menggunakan backend non-interaktif
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA DASHBOARD
# ==========================================
st.set_page_config(page_title="SRIS Multi-Engine Dashboard", layout="wide", page_icon="🛡️")

# Desain Tema Premium Corporate Cyber Security & HSE
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); border-left: 6px solid #007A87; }
    .security-banner { background-color: #0f2027; color: white; padding: 20px; border-radius: 8px; margin-bottom: 25px; background: linear-gradient(to right, #134E5E, #71B280); }
    .chat-bubble-user { background-color: #007A87; color: white; padding: 12px; border-radius: 15px; margin-bottom: 10px; text-align: right; }
    .chat-bubble-bot { background-color: #e9ecef; color: #333; padding: 12px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='security-banner'>
        <h2>🛡️ SRIS Integrated Multi-Engine: ISO & SMK3 Dashboard</h2>
        <p>Sistem Informasi Risiko Strategis | Otomatisasi Multi-Standar ISO 27001, ISO 9001, ISO 14001, ISO 45001 & SMK3 PP 50/2012</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. DEFINISI NAMA KOLOM SECARA GLOBAL (ANTI-EROR)
# ==========================================
kolom_dept = 'Departemen Divisi/Area'
kolom_status = 'Posisi Status NC'
kolom_standar = 'STANDARD'
kolom_temuan = 'Detail Temuan Ketidaksesuaian'
kolom_auditor = 'Nama Auditor'

# Kolom Spesifik ISO 27001
kolom_cyber = 'Cybersecurity Consepts'  
kolom_pilar = 'Pillars Information Security'
kolom_ops = 'Operational Capabilities'
kolom_annex = 'Kategori Kontrol ( Annex A ) ISO 27001'
kolom_no_annex = 'No Annex dan No Control ( ISO 27001)'

# ==========================================
# 3. DETEKSI & PEMBACAAN DATA SECARA OTOMATIS (SMART LOADER)
# ==========================================
st.sidebar.header("📂 Sumber Data Audit")
uploaded_file = st.sidebar.file_uploader("Unggah File CSV/XLSX Hasil Audit:", type=["csv", "xlsx"])

df = None
status_pembacaan = ""

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        status_pembacaan = f"Berhasil memuat file unggahan: {uploaded_file.name}"
    except Exception as e:
        st.sidebar.error(f"Gagal membaca file unggahan: {e}")

if df is None:
    for file in os.listdir('.'):
        if (file.endswith('.csv') or file.endswith('.xlsx')) and file != 'app.py' and "Simulasi" not in file:
            if any(kunci in file for kunci in ["Formulir", "Responses", "Jawaban", "kompilasi", "smk3", "iso"]):
                try:
                    if file.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file)
                    status_pembacaan = f"Otomatis mendeteksi file workspace: {file}"
                    break
                except:
                    pass

# ==========================================
# 4. CORE PROCESSING ENGINE & ENGINE DETECTOR
# ==========================================
df_filtered = None
sris_mode = "ISO-IMS" # Default fallback mode

if df is not None:
    df.columns = [col.strip() for col in df.columns]
    
    # Standardisasi Data Departemen
    if kolom_dept in df.columns:
        df[kolom_dept] = df[kolom_dept].astype(str).str.strip()
        mapping_mr = {
            'Management Representatif /MR': 'Management Representative (MR)',
            'MR Management Representatif': 'Management Representative (MR)',
            'MR': 'Management Representative (MR)'
        }
        df[kolom_dept] = df[kolom_dept].replace(mapping_mr)
    
    # SMART STANDAR DETECTOR (Mendeteksi otomatis isi file)
    if kolom_standar in df.columns:
        sample_standar = "".join(df[kolom_standar].dropna().astype(str).unique()).upper()
        if "SMK3" in sample_standar or "PP 50" in sample_standar or "K3" in sample_standar:
            sris_mode = "SMK3"
        elif "27001" in sample_standar:
            sris_mode = "ISO-27001"
        else:
            sris_mode = "ISO-IMS"
    else:
        if kolom_cyber in df.columns:
            sris_mode = "ISO-27001"
        else:
            sris_mode = "ISO-IMS"

    # PROSES EKSTRAKSI SKOR PENTAGON RISK MAP
    pilar_skor = {
        'P1_Regulasi': 'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
        'P2_Finansial': 'Skoring Pentagon Analisis [P2- Finansial & Kerugian]',
        'P3_Integritas': 'Skoring Pentagon Analisis [P3- Integritas data & System]',
        'P4_Operasional': 'Skoring Pentagon Analisis [P4- Operational]',
        'P5_Reputasi': 'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
    }
    for key, nama_kolom in pilar_skor.items():
        if nama_kolom in df.columns:
            df[key] = df[nama_kolom].astype(str).str.extract(r'(\d+)')[0].astype(float)
            df[key] = df[key].fillna(0.0)
        else:
            df[key] = 0.0

    st.sidebar.success(f"🔌 Status Data: Terhubung ({sris_mode} Mode)")
    st.sidebar.info(f"ℹ️ {status_pembacaan}")
    
    # PANEL KONTROL FILTER DEPARTEMEN
    if kolom_dept in df.columns:
        list_dept = ["Semua Departemen"] + sorted(list(df[kolom_dept].dropna().unique()))
        selected_dept = st.sidebar.selectbox("Pilih Departemen/Divisi:", list_dept)
        if selected_dept != "Semua Departemen":
            df_filtered = df[df[kolom_dept] == selected_dept].copy()
        else:
            df_filtered = df.copy()
    else:
        df_filtered = df.copy()

    st.session_state['df_filtered_saved'] = df_filtered
    st.session_state['df'] = df
    st.
