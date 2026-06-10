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
# 2. DEFINISI NAMA KOLOM SECARA GLOBAL
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
# 3. DETEKSI & PEMBACAAN DATA SECARA OTOMATIS
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
sris_mode = "ISO-IMS" 

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

    # PROSES EKSTRAKSI SKOR PENTAGON RISK MAP (DIBUAT RINGKAS / ANTI-TRUNCATE)
    pilar_skor = {
        'P1_Regulasi': 'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
        'P2_Finansial': 'Skoring Pentagon Analisis [P2- Finansial & Kerugian]',
        'P3_Integritas': 'Skoring Pentagon Analisis [P3- Integritas data & System]',
        'P4_Operasional': 'Skoring Pentagon Analisis [P4- Operational]',
        'P5_Reputasi': 'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
    }
    
    for key, nama_kolom in pilar_skor.items():
        if nama_kolom in df.columns:
            # Dipecah menjadi 3 baris pendek agar tidak terpotong di GitHub
            teks_kolom = df[nama_kolom].astype(str)
            angka_ekstrak = teks_kolom.str.extract(r'(\d+)')[0]
            df[key] = pd.to_numeric(angka_ekstrak, errors='coerce').fillna(0.0)
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
    st.session_state['sris_mode'] = sris_mode

# ==========================================
# 5. MENU NAVIGASI UTAMA
# ==========================================
menu = st.sidebar.radio("Pilih Navigasi Dashboard:", [
    "📊 Ringkasan Eksekutif & Status Temuan",
    "🕸️ Analisis Radar Pentagon (SRIS Model)",
    "🔍 Audit Deep Dive & Kepatuhan Klausul",
    "🤖 SRIS Chatbot AI (Tanya Jawab Audit)"
])

if 'df_filtered_saved' in st.session_state:
    df_filtered = st.session_state['df_filtered_saved']
    sris_mode = st.session_state['sris_mode']

# Eksekusi Tampilan Dashboard
if df_filtered is not None:

    if menu == "📊 Ringkasan Eksekutif & Status Temuan":
        st.subheader(f"Metrik Utama Hasil Audit - Mode: {sris_mode}")
        total_temuan = len(df_filtered)
        if kolom_status in df_filtered.columns:
            open_nc = len(df_filtered[df_filtered[kolom_status].astype(str).str.contains('Open|On Progress', case=False, na=False)])
            closed_nc = total_temuan - open_nc
        else:
            open_nc = total_temuan; closed_nc = 0
            
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Total Temuan Kasus", value=f"{total_temuan} Temuan")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Open / Process", value=f"{open_nc} Kasus", delta="Risk Exposure", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Closed (Selesai)", value=f"{closed_nc} Kasus", delta="Mitigated")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # LOGIKA DYNAMIC RENDERING (CEK KOLOM SIBER)
        has_cyber_cols = (kolom_cyber in df_filtered.columns and not df_filtered[kolom_cyber].isna().all()) and \
                         (kolom_pilar in df_filtered.columns and not df_filtered[kolom_pilar].isna().all()) and \
                         (kolom_ops in df_filtered.columns and not df_filtered[kolom_ops].isna().all())

        if has_cyber_cols:
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### Distribusi Temuan Berdasarkan Departemen")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#0a4b78', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1)
                plt.close(fig1)
            with col_g2:
                st.write("##### Profil Temuan Berdasarkan Cybersecurity Concepts")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_cyber].value_counts().plot(kind='bar', color='#00a8cc', edgecolor='black', ax=ax2)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)

            st.markdown("<br>", unsafe_allow_html=True)
            col_g3, col_g4 = st.columns(2)
            with col_g3:
                st.write("##### Distribusi Pillars Information Security (CIA)")
                fig3, ax3 = plt.subplots(figsize=(6, 3.5))
                pilar_series = df_filtered[kolom_pilar].dropna().astype(str).str.split(',\s*').explode()
                pilar_series.value_counts().plot(kind='bar', color='#4b86b4', edgecolor='black', ax=ax3)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig3)
                plt.close(fig3)
            with col_g4:
                st.write("##### Distribusi Berdasarkan Operational Capabilities")
                fig4, ax4 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_ops].value_counts().plot(kind='bar', color='#2a9d8f', edgecolor='black', ax=ax4)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig4)
                plt.close(fig4)
        else:
            # INTERFACE DINAMIS UNTUK SMK3 / STANDAR LAIN
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### Distribusi Temuan Pelanggaran per Departemen/Area")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                if kolom_dept in df_filtered.columns:
                    df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#1e5631', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1)
                plt.close(fig1)
            with col_g2:
                st.write("##### Breakdown Volume Berdasarkan Standar / Kriteria Regulasi")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                kolom_kriteria_aktif = 'Nomor Kriteria' if 'Nomor Kriteria' in df_filtered.columns else \
                                      ('Nomor Kriteria ' if 'Nomor Kriteria ' in df_filtered.columns else kolom_standar)
                if kolom_kriteria_aktif in df_filtered.columns:
                    df_filtered[kolom_kriteria_aktif].value_counts().head(10).plot(kind='bar', color='#4c9a2a', edgecolor='black', ax=ax2)
                    plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)

    elif menu == "🕸️ Analisis Radar Pentagon (SRIS Model)":
        st.subheader("Pemetaan Profil Risiko Organisasi (Pentagon Model)")
        
        p1 = df_filtered['P1_Regulasi'].mean() if 'P1_Regulasi' in df_filtered.columns else 0
        p2 = df_filtered['P2_Finansial'].mean() if 'P2_Finansial' in df_filtered.columns else 0
        p3 = df_filtered['P3_Integritas'].mean() if 'P3_Integritas' in df_filtered.columns else 0
        p4 = df_filtered['P4_Operasional'].mean() if 'P4_Operasional'
