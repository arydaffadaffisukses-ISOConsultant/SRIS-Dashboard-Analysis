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
st.set_page_config(page_title="SRIS Engine - Dashboard Audit ISO 27001", layout="wide", page_icon="🔒")

# Desain Tema Premium Corporate Cyber Security
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); border-left: 6px solid #0a4b78; }
    .security-banner { background-color: #0f2027; color: white; padding: 20px; border-radius: 8px; margin-bottom: 25px; background: linear-gradient(to right, #203a43, #0f2027); }
    .chat-bubble-user { background-color: #0a4b78; color: white; padding: 12px; border-radius: 15px; margin-bottom: 10px; text-align: right; }
    .chat-bubble-bot { background-color: #e9ecef; color: #333; padding: 12px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='security-banner'>
        <h2>🔒 SRIS Engine: Dashboard Temuan & Risiko Audit ISO 27001:2022</h2>
        <p>Sistem Informasi Risiko Strategis (SRIS) | Integrasi Otomatis Kontrol Annex A & Chatbot AI Consultant</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. DETEKSI & PEMBACAAN DATA SECARA OTOMATIS (SMART LOADER)
# ==========================================
st.sidebar.header("📂 Sumber Data Audit")
uploaded_file = st.sidebar.file_uploader("Unggah File CSV Hasil Audit Terbaru:", type=["csv", "xlsx"])

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
            if any(kunci in file for kunci in ["Formulir", "Responses", "Jawaban", "kompilasi"]):
                try:
                    if file.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file)
                    status_pembacaan = f"Otomatis mendeteksi file workspace: {file}"
                    break
                except:
                    pass

if df is None:
    for file in os.listdir('.'):
        if (file.endswith('.csv') or file.endswith('.xlsx')) and file != 'app.py':
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                status_pembacaan = f"Memuat file yang tersedia: {file}"
                break
            except:
                pass

# KONDISI AWAL VARIABEL SEBELUM PROSES FILTERING
df_filtered = None

# ==========================================
# 3. CORE PROCESSING ENGINE & DATA CLEANING
# ==========================================
if df is not None:
    df.columns = [col.strip() for col in df.columns]
    
    kolom_dept = 'Departemen Divisi/Area'
    kolom_status = 'Posisi Status NC'
    kolom_cyber = 'Cybersecurity Concepts'
    kolom_annex = 'Kategori Kontrol ( Annex A ) ISO 27001'
    kolom_auditor = 'Nama Auditor'
    kolom_standar = 'STANDARD'
    kolom_temuan = 'Detail Temuan Ketidaksesuaian'
    kolom_no_annex = 'No Annex dan No Control ( ISO 27001)'
    
    if kolom_dept in df.columns:
        df[kolom_dept] = df[kolom_dept].astype(str).str.strip()
        mapping_mr = {
            'Management Representatif /MR': 'Management Representative (MR)',
            'MR Management Representatif': 'Management Representative (MR)',
            'MR': 'Management Representative (MR)'
        }
        df[kolom_dept] = df[kolom_dept].replace(mapping_mr)
    
    # PROSES EKSTRAKSI SKOR SKORING PENTAGON (WAJIB DI SINI AGAR MASUK KE DF UTAMA)
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

    st.sidebar.success("🔌 Status Data: Terhubung")
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

    # Kunci hasil akhir ke Session State agar aman saat navigasi dipindah
    st.session_state['df_filtered_saved'] = df_filtered
    st.session_state['df'] = df

# ==========================================
# 4. MENU NAVIGASI UTAMA
# ==========================================
menu = st.sidebar.radio("Pilih Navigasi Dashboard:", [
    "📊 Ringkasan Executif & Status Temuan",
    "🕸️ Analisis Radar Pentagon (SRIS Model)",
    "🔍 Audit Deep Dive & Manajemen Annex A",
    "🤖 SRIS Chatbot AI (Tanya Jawab Audit)"
])

# Ambil data pengaman dari session state
if 'df_filtered_saved' in st.session_state:
    df_filtered = st.session_state['df_filtered_saved']

# Eksekusi Menu Hanya Jika Data Berhasil Dimuat
if df_filtered is not None:
    
    kolom_dept = 'Departemen Divisi/Area'
    kolom_status = 'Posisi Status NC'
    kolom_cyber = 'Cybersecurity Concepts'
    kolom_annex = 'Kategori Kontrol ( Annex A ) ISO 27001'
    kolom_auditor = 'Nama Auditor'
    kolom_standar = 'STANDARD'
    kolom_temuan = 'Detail Temuan Ketidaksesuaian'
    kolom_no_annex = 'No Annex dan No Control ( ISO 27001)'

    if menu == "📊 Ringkasan Executif & Status Temuan":
        st.subheader("📊 Metrik Utama Hasil Audit Sistem Manajemen")
        total_temuan = len(df_filtered)
        if kolom_status in df_filtered.columns:
            open_nc = len(df_filtered[df_filtered[kolom_status].astype(str).str.contains('Open|On Progress', case=False, na=False)])
            closed_nc = total_temuan - open_nc
        else:
            open_nc = total_temuan; closed_nc = 0
            
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Total Kasus Temuan Audit", value=f"{total_temuan} Temuan")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Open / On Progress", value=f"{open_nc} Kasus", delta="Risk Exposure", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Closed (Selesai Perbaikan)", value=f"{closed_nc} Kasus", delta="Mitigated")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("##### 🏢 Distribusi Temuan Berdasarkan Departemen")
            fig, ax = plt.subplots(figsize=(6, 4))
            if kolom_dept in df_filtered.columns and not df_filtered[kolom_dept].isna().all():
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#0a4b78', ax=ax)
            st.pyplot(fig); plt.close(fig)
        with col_g2:
            st.write("##### 🛡️ Profil Temuan Berdasarkan Cybersecurity Concepts")
            fig, ax = plt.subplots(figsize=(
