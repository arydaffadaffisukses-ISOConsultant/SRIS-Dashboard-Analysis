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
# 2. DETEKSI & PEMBACAAN DATA SECARA OTOMATIS (SMART LOADER)
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

# DEFINISI NAMA KOLOM SECARA GLOBAL
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

# Kolom Spesifik SMK3 / K3 Umum
kolom_kriteria_smk3 = 'Kriteria SMK3' # Tambahan kolom kriteria elemen jika ada

# ==========================================
# 3. CORE PROCESSING ENGINE & ENGINE DETECTOR
# ==========================================
df_filtered = None
sris_mode = "ISO-27001" # Default mode

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
            sris_mode = "ISO-IMS" # Integrated Management System (9001, 14001, 45001)
    else:
        # Fallback jika kolom STANDARD tidak ada, cek keberadaan kolom spesifik cyber
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
    st.session_state['sris_mode'] = sris_mode

# ==========================================
# 4. MENU NAVIGASI UTAMA
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
        st.subheader(f"📊 Metrik Utama Hasil Audit - Mode: {sris_mode}")
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
        
        # GRAFIK DINAMIS BERDASARKAN MODE STANDAR YANG TERDETEKSI
        if sris_mode == "ISO-27001":
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### 🏢 Distribusi Temuan Berdasarkan Departemen")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#0a4b78', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1); plt.close(fig1)
            with col_g2:
                st.write("##### 🛡️ Profil Temuan Berdasarkan Cybersecurity Concepts")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                if kolom_cyber in df_filtered.columns and not df_filtered[kolom_cyber].isna().all():
                    df_filtered[kolom_cyber].value_counts().plot(kind='bar', color='#00a8cc', edgecolor='black', ax=ax2)
                    plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig2); plt.close(fig2)

            st.markdown("<br>", unsafe_allow_html=True)
            col_g3, col_g4 = st.columns(2)
            with col_g3:
                st.write("##### 🔑 Distribusi Pillars Information Security (CIA)")
                fig3, ax3 = plt.subplots(figsize=(6, 3.5))
                if kolom_pilar in df_filtered.columns and not df_filtered[kolom_pilar].isna().all():
                    pilar_series = df_filtered[kolom_pilar].dropna().astype(str).str.split(',\s*').explode()
                    pilar_series.value_counts().plot(kind='bar', color='#4b86b4', edgecolor='black', ax=ax3)
                    plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig3); plt.close(fig3)
            with col_g4:
                st.write("##### ⚙️ Distribusi Berdasarkan Operational Capabilities")
                fig4, ax4 = plt.subplots(figsize=(6, 3.5))
                if kolom_ops in df_filtered.columns and not df_filtered[kolom_ops].isna().all():
                    df_filtered[kolom_ops].value_counts().plot(kind='bar', color='#2a9d8f', edgecolor='black', ax=ax4)
                    plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig4); plt.close(fig4)

        elif sris_mode == "SMK3":
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### 🏢 Distribusi Temuan Pelanggaran per Departemen/Area")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#1e5631', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1); plt.close(fig1)
            with col_g2:
                st.write("##### ⚠️ Breakdown Temuan Berdasarkan Jenis Regulasi K3")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                if kolom_standar in df_filtered.columns:
                    df_filtered[kolom_standar].value_counts().plot(kind='bar', color='#4c9a2a', edgecolor='black', ax=ax2)
                    plt.xticks(rotation=30, ha='right')
                plt.tight_layout()
                st.pyplot(fig2); plt.close(fig2)

        else: # ISO-IMS (9001, 14001, 45001 Terintegrasi)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### 🏢 Distribusi Temuan Per-Divisi (IMS)")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#d95d39', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1); plt.close(fig1)
            with col_g2:
                st.write("##### 📜 Komparasi Volume Temuan Lintas Standar ISO")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                if kolom_standar in df_filtered.columns:
                    df_filtered[kolom_standar].value_counts().plot(kind='bar', color='#f0a150', edgecolor='black', ax=ax2)
                    plt.xticks(rotation=0)
                plt.tight_layout()
                st.pyplot(fig2); plt.close(fig2)

    elif menu == "🕸️ Analisis Radar Pentagon (SRIS Model)":
        st.subheader("🕸️ Pemetaan Profil Risiko Organisasi (Pentagon Model)")
        
        p1 = df_filtered['P1_Regulasi'].mean() if 'P1_Regulasi' in df_filtered.columns else 0
        p2 = df_filtered['P2_Finansial'].mean() if 'P2_Finansial' in df_filtered.columns else 0
        p3 = df_filtered['P3_Integritas'].mean() if 'P3_Integritas' in df_filtered.columns else 0
        p4 = df_filtered['P4_Operasional'].mean() if 'P4_Operasional' in df_filtered.columns else 0
        p5 = df_filtered['P5_Reputasi'].mean() if 'P5_Reputasi' in df_filtered.columns else 0
        
        scores = [p1, p2, p3, p4, p5]
        categories = ['P1: Regulasi', 'P2: Finansial', 'P3: Integritas Data', 'P4: Operasional', 'P5: Reputasi']
        categories_loop = categories + [categories[0]]; scores_loop = scores + [scores[0]]
        angles = np.linspace(start=0, stop=2*np.pi, num=len(categories_loop))
        
        c_chart, c_narrative = st.columns([1.2, 1])
        with c_chart:
            fig_radar, ax_radar = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
            ax_radar.plot(angles, scores_loop, color='#007A87', linewidth=2.5, marker='o')
            ax_radar.fill(angles, scores_loop, color='#007A87', alpha=0.3)
            ax_radar.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=9, fontweight='bold')
            ax_radar.set_ylim(0, 5); st.pyplot(fig_radar); plt.close(fig_radar)
        with c_narrative:
            st.write("##### 💡 Analisis Risiko Strategis Management")
            if sum(scores) > 0:
                max_idx = np.argmax(scores)
                st.error(f"**Pilar Kerentanan Utama:** Area **{categories[max_idx]}** menunjukkan nilai eksposur risiko tertinggi ({scores[max_idx]:.2f}/5.0).")
            else:
                st.info("Belum ada data nilai skor untuk pemetaan pentagon.")

    elif menu == "🔍 Audit Deep Dive & Kepatuhan Klausul":
        if sris_mode == "ISO-27001":
            st.subheader("🛠️ Analisis Kontrol Keamanan Annex A ISO 27001")
            fig_annex, ax_annex = plt.subplots(figsize=(10, 4))
            if kolom_annex in df_filtered.columns and not df_filtered[kolom_annex].isna().all():
                df_filtered[kolom_annex].value_counts().plot(kind='bar', color='#ff7e67', edgecolor='black', ax=ax_annex)
            st.pyplot(fig_annex); plt.close(fig_annex)
        else:
            st.subheader("📋 Pemetaan Temuan Berdasarkan Klausul / Kriteria Pemenuhan Standar")
            fig_klausul, ax_klausul = plt.subplots(figsize=(10, 4))
            # Fallback untuk SMK3 / ISO IMS menggunakan klaster kolom kriteria/nomor pasal jika ada
            kolom_kriteria_umum = 'Nomor Kriteria' if 'Nomor Kriteria' in df_filtered.columns else ( 'Nomor Kriteria ' if 'Nomor Kriteria ' in df_filtered.columns else kolom_standar)
            if kolom_kriteria_umum in df_filtered.columns:
                df_filtered[kolom_kriteria_umum].value_counts().head(15).plot(kind='bar', color='#4b86b4', edgecolor='black', ax=ax_klausul)
            st.pyplot(fig_klausul); plt.close(fig_klausul)
        
        st.write("##### 🗂️ Master Data Inventori Temuan Audit")
        kolom_tampilan = [kolom_auditor, kolom_dept, kolom_standar, kolom_temuan, kolom_status]
        if sris_mode == "ISO-27001" and kolom_no_annex in df_filtered.columns:
            kolom_tampilan.append(kolom_no_annex)
        st.dataframe(df_filtered[[c for c in kolom_tampilan if c in df_filtered.columns]], use_container_width=True)

    elif menu == "🤖 SRIS Chatbot AI (Tanya Jawab Audit)":
        st.subheader("🤖 SRIS Executive AI Consultant (Multi-Standar)")
        st.info("Asisten AI siap menganalisis kepatuhan organisasi terhadap regulasi ISO maupun SMK3 secara simultan.")
        
        if "GEMINI_API_KEY" in st.secrets:
            api_key_input = st.secrets["GEMINI_API_KEY"]
        else:
            api_key_input = st.text_input("🔑 Masukkan Google Gemini API Key Anda:", type="password")
        
        if api_key_input:
            try:
                from google import genai
                client = genai.Client(api_key=api_key_input)
                
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                for chat in st.session_state.chat_history:
                    if chat["role"] == "user":
                        st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {chat['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b> {chat['text']}</div>", unsafe_allow_html=True)
                
                user_query = st.chat_input("Ketik pertanyaan atau minta rekomendasi tindakan perbaikan (CAPA)...")
                
                if user_query:
                    st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {user_query}</div>", unsafe_allow_html=True)
                    
                    kolom_ks = [kolom_dept, kolom_temuan, kolom_status, kolom_standar]
                    kolom_tersedia = [c for c in kolom_ks if c in df_filtered.columns]
                    ringkasan_data = df_filtered[kolom_tersedia].to_string(index=False) if kolom_tersedia else "Data kosong."
                    
                    system_instruction = f"""
                    Anda adalah SRIS Executive AI Consultant, Konsultan Manajemen Senior ahli ISO (9001, 14001, 45001, 27001) dan Auditor Senior SMK3 PP 50/2012.
                    Anda bertugas membantu menganalisis temuan dan memberikan rekomendasi perbaikan (CAPA) komprehensif bagi Top Management.
                    
                    --- MODE OPERASI SAAT INI ---
                    {sris_mode}
                    
                    --- DATA AUDIT AKTIF ---
                    {ringkasan_data[:25000]}
                    --- AKHIR DATA ---
                    
                    Berikan respon dengan Bahasa Indonesia profesional tingkat tinggi (Executive Level), solutif, dan mengacu pada standar regulasi yang tepat.
                    """
                    
                    with st.spinner("Menganalisis matriks kepatuhan..."):
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_query,
                            config={'system_instruction': system_instruction}
                        )
                        bot_response = response.text
                    
                    st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b><br><br>{bot_response}</div>", unsafe_allow_html=True)
                    st.session_state.chat_history.append({"role": "user", "text": user_query})
                    st.session_state.chat_history.append({"role": "bot", "text": bot_response})
                    
            except Exception as error_ai:
                st.error(f"Gagal menghubungkan ke AI Engine: {error_ai}")
        else:
            st.sidebar.warning("⚠️ Silakan masukkan Gemini API Key.")
else:
    st.error("🚨 File data audit belum dimuat atau tidak ditemukan di direktori!")
