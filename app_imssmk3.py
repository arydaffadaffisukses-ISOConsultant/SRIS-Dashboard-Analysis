import streamlit as st
import pandas as pd
import numpy as np
import os

# Paksa Matplotlib menggunakan backend non-interaktif agar aman di server Cloud
import matplotlib
matplotlib.use('Agg')
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA DASHBOARD
# ==========================================
st.set_page_config(page_title="SRIS Engine Dashboard", layout="wide", page_icon="🛡️")
# --- SETTING LAYOUT ---
st.set_page_config(page_title="SRIS Pro Dashboard", layout="wide")

# Desain Tema Premium Corporate Executive (HSE Green & Deep Slate)
# --- BANNER PROFESIONAL (Custom CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); border-left: 6px solid #1E5631; }
    .security-banner { background-color: #0f2027; color: white; padding: 20px; border-radius: 8px; margin-bottom: 25px; background: linear-gradient(to right, #1e5631, #4c9a2a); }
    .chat-bubble-user { background-color: #1E5631; color: white; padding: 12px; border-radius: 15px; margin-bottom: 10px; text-align: right; }
    .chat-bubble-bot { background-color: #e9ecef; color: #333; padding: 12px; border-radius: 15px; margin-bottom: 10px; }
    .banner {
        background: linear-gradient(90deg, #1a2a6c, #b21f1f, #fdbb2d);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='security-banner'>
        <h2>🛡️ SRIS Integrated Engine: ISO-IMS & SMK3 Dashboard</h2>
        <p>Strategic Risk Intelligence System | Otomatisasi Matriks Kepatuhan ISO 9001, ISO 14001, ISO 45001 & SMK3 PP 50/2012</p>
    <div class="banner">
        <h1>🛡️ Security Risk Intelligence System (SRIS)</h1>
        <p>Executive Dashboard - Internal Audit & Risk Management</p>
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

# ==========================================
# 3. DETEKSI & PEMBACAAN DATA SECARA OTOMATIS
# ==========================================
st.sidebar.header("📂 Sumber Data Audit")
uploaded_file = st.sidebar.file_uploader("Unggah File Hasil Audit (IMS/SMK3):", type=["csv", "xlsx"])

if 'df_ims' not in st.session_state:
    st.session_state['df_ims'] = None
    """, unsafe_allow_html=True)

df_input = None
status_pembacaan = ""
# --- LOAD DATA ---
# (Pastikan data dimuat seperti kode sebelumnya)
csv_data = '''...''' # Isi data Bapak
df = pd.read_csv(io.StringIO(csv_data))

if uploaded_file is not None:
    try:
        df_input = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        status_pembacaan = f"Berhasil memuat file: {uploaded_file.name}"
    except Exception as e:
        st.sidebar.error(f"Gagal membaca file: {e}")
# --- SIDEBAR PER DEPARTEMEN ---
st.sidebar.header("🔍 Filter Dashboard")
dept_list = ["Semua"] + list(df['Departemen'].unique())
pilihan_dept = st.sidebar.selectbox("Pilih Departemen:", dept_list)

if df_input is None:
    for file in os.listdir('.'):
        if (file.endswith('.csv') or file.endswith('.xlsx')) and file not in ['app.py', 'app_iso27001.py'] and "Simulasi" not in file:
            if any(kunci in file.lower() for kunci in ["formulir", "responses", "jawaban", "kompilasi", "smk3", "iso", "ims"]):
                try:
                    df_input = pd.read_csv(file) if file.endswith('.csv') else pd.read_excel(file)
                    status_pembacaan = f"Otomatis mendeteksi file workspace: {file}"
                    break
                except:
                    pass

if df_input is not None:
    st.session_state['df_ims'] = df_input

# Pemrosesan Data Utama
if st.session_state['df_ims'] is not None:
    df = st.session_state['df_ims'].copy()
    df.columns = [col.strip() for col in df.columns]
    
    # Standardisasi Data Departemen / MR
    if kolom_dept in df.columns:
        df[kolom_dept] = df[kolom_dept].astype(str).str.strip()
        mapping_mr = {
            'Management Representatif /MR': 'Management Representative (MR)',
            'MR Management Representatif': 'Management Representative (MR)',
            'MR': 'Management Representative (MR)'
        }
        df[kolom_dept] = df[kolom_dept].replace(mapping_mr)
    
    # Deteksi Mode Operasi (SMK3 vs ISO IMS)
    sris_mode = "ISO-IMS"
    if kolom_standar in df.columns:
        sample_txt = "".join(df[kolom_standar].dropna().astype(str).unique()).upper()
        if any(k in sample_txt for k in ["SMK3", "PP 50", "PP50", "K3"]):
            sris_mode = "SMK3"

    # Ekstraksi Skor Pentagon Risiko
    pilar_skor = {
        'P1_Regulasi': 'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
        'P2_Finansial': 'Skoring Pentagon Analisis [P2- Finansial & Kerugian]',
        'P3_Integritas': 'Skoring Pentagon Analisis [P3- Integritas data & System]',
        'P4_Operasional': 'Skoring Pentagon Analisis [P4- Operational]',
        'P5_Reputasi': 'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
    }
    for key, nama_kolom in pilar_skor.items():
        if nama_kolom in df.columns:
            df[key] = pd.to_numeric(df[nama_kolom].astype(str).str.extract(r'(\d+)')[0], errors='coerce').fillna(0.0)
        else:
            df[key] = 0.0

    st.sidebar.success(f"🔌 Engine {sris_mode} Aktif")
    st.sidebar.info(f"ℹ️ {status_pembacaan}")
    
    # Filter Departemen
    if kolom_dept in df.columns:
        list_dept = ["Semua Departemen"] + sorted(list(df[kolom_dept].dropna().unique()))
        selected_dept = st.sidebar.selectbox("Pilih Departemen/Divisi:", list_dept)
        df_filtered = df[df[kolom_dept] == selected_dept].copy() if selected_dept != "Semua Departemen" else df.copy()
    else:
        df_filtered = df.copy()
# Logika Filter
if pilihan_dept != "Semua":
    df_filtered = df[df['Departemen'] == pilihan_dept]
else:
    df_filtered = None
    sris_mode = "ISO-IMS"
    df_filtered = df

# ==========================================
# 4. KONTROL MENU NAVIGASI (KEY-BASED STABIL)
# ==========================================
menu_options = {
    "Overview": "📊 Executive Summary & Status Temuan",
    "Pentagon": "🕸️ Analisis Radar Pentagon (SRIS Model)",
    "DeepDive": "🔍 Deep Dive Klausul Kepatuhan",
    "Chatbot": "🤖 SRIS Management AI Consultant"
}
selected_menu_label = st.sidebar.radio("Pilih Navigasi Dashboard:", list(menu_options.values()))
current_menu = [k for k, v in menu_options.items() if v == selected_menu_label][0]
# --- TAMPILAN DASHBOARD ---
# Gunakan df_filtered untuk semua grafik agar dasbor mengikuti filter
col1, col2 = st.columns(2)

# ==========================================
# 5. EKSEKUSI TAMPILAN DASHBOARD
# ==========================================
if df_filtered is not None:
with col1:
    st.subheader(f"Analisis Departemen: {pilihan_dept}")
    # ... (masukkan kode grafik st.pyplot di sini menggunakan df_filtered)

    if current_menu == "Overview":
        st.subheader(f"Metrik Utama Hasil Audit - Mode: {sris_mode}")
        total_temuan = len(df_filtered)
        open_nc = len(df_filtered[df_filtered[kolom_status].astype(str).str.contains('Open|On Progress', case=False, na=False)]) if kolom_status in df_filtered.columns else total_temuan
        closed_nc = total_temuan - open_nc
            
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Total Temuan Ketidaksesuaian", value=f"{total_temuan} Temuan")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Open / On Progress", value=f"{open_nc} Kasus", delta="Risk Exposure", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Closed (Selesai)", value=f"{closed_nc} Kasus", delta="Mitigated")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("##### Temuan Ketidaksesuaian per Departemen/Area")
            fig1, ax1 = plt.subplots(figsize=(6, 3.5))
            if kolom_dept in df_filtered.columns:
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#1e5631', ax=fig1.gca())
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close(fig1)
        with col_g2:
            st.write("##### Jumlah Temuan berdasarkan Kriteria Standard")
            fig2, ax2 = plt.subplots(figsize=(6, 3.5))
            kolom_kriteria_aktif = 'Nomor Kriteria' if 'Nomor Kriteria' in df_filtered.columns else \
                                  ('Nomor Kriteria ' if 'Nomor Kriteria ' in df_filtered.columns else kolom_standar)
            if kolom_kriteria_aktif in df_filtered.columns:
                df_filtered[kolom_kriteria_aktif].value_counts().head(10).plot(kind='bar', color='#4c9a2a', edgecolor='black', ax=fig2.gca())
                plt.xticks(rotation=45, ha='right', fontsize=8)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

    elif current_menu == "Pentagon":
        st.subheader("Pemetaan Profil Risiko Organisasi (Pentagon Model)")
        p1 = df_filtered['P1_Regulasi'].mean() if 'P1_Regulasi' in df_filtered.columns else 0.0
        p2 = df_filtered['P2_Finansial'].mean() if 'P2_Finansial' in df_filtered.columns else 0.0
        p3 = df_filtered['P3_Integritas'].mean() if 'P3_Integritas' in df_filtered.columns else 0.0
        p4 = df_filtered['P4_Operasional'].mean() if 'P4_Operasional' in df_filtered.columns else 0.0
        p5 = df_filtered['P5_Reputasi'].mean() if 'P5_Reputasi' in df_filtered.columns else 0.0
        
        scores = [p1, p2, p3, p4, p5]
        categories = ['P1: Regulasi', 'P2: Finansial', 'P3: Integritas Data', 'P4: Operasional', 'P5: Reputasi']
        categories_loop = categories + [categories[0]]
        scores_loop = scores + [scores[0]]
        angles = np.linspace(start=0, stop=2*np.pi, num=len(categories_loop))
        
        c_chart, c_narrative = st.columns([1.2, 1])
        with c_chart:
            fig_radar, ax_radar = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
            ax_radar.plot(angles, scores_loop, color='#1e5631', linewidth=2.5, marker='o')
            ax_radar.fill(angles, scores_loop, color='#1e5631', alpha=0.3)
            ax_radar.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=9, fontweight='bold')
            ax_radar.set_ylim(0, 5)
            st.pyplot(fig_radar)
            plt.close(fig_radar)
        with c_narrative:
            st.write("##### Analisis Risiko Strategis Management")
            if sum(scores) > 0:
                max_idx = np.argmax(scores)
                st.error(f"Area **{categories[max_idx]}** memiliki nilai eksposur risiko tertinggi ({scores[max_idx]:.2f}/5.0).")
            else:
                st.info("Belum ada data nilai skor untuk pemetaan pentagon.")

    elif current_menu == "DeepDive":
        st.subheader("🔍 Penelaahan Mendalam Klausul Kepatuhan Standard/Regulasi")
        kolom_kriteria_umum = 'Nomor Kriteria' if 'Nomor Kriteria' in df_filtered.columns else \
                              ('Nomor Kriteria ' if 'Nomor Kriteria ' in df_filtered.columns else kolom_standar)
        
        st.write("##### Pemetaan Jumlah Ketidaksesuaian Berdasarkan Klausul / Kriteria")
        fig_klausul, ax_klausul = plt.subplots(figsize=(10, 3.8))
        if kolom_kriteria_umum in df_filtered.columns:
            df_filtered[kolom_kriteria_umum].value_counts().head(15).plot(kind='bar', color='#4b86b4', edgecolor='black', ax=fig_klausul.gca())
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig_klausul)
        plt.close(fig_klausul)
        
        st.write("##### Master Data Inventori Temuan Audit")
        kolom_tampilan = [kolom_auditor, kolom_dept, kolom_standar, kolom_temuan, kolom_status]
        st.dataframe(df_filtered[[c for c in kolom_tampilan if c in df_filtered.columns]], use_container_width=True)

    elif current_menu == "Chatbot":
        st.subheader("🤖 SRIS Executive AI Consultant (IMS & SMK3)")
        st.info("Asisten AI siap menganalisis kepatuhan organisasi terhadap regulasi ISO Management System maupun SMK3 PP 50/2012.")
        
        api_key_input = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else st.text_input("🔑 Masukkan Google Gemini API Key Anda:", type="password")
        
        if api_key_input:
            try:
                from google import genai
                client = genai.Client(api_key=api_key_input)
                
                if "ims_chat_history" not in st.session_state:
                    st.session_state.ims_chat_history = []
                
                for chat in st.session_state.ims_chat_history:
                    if chat["role"] == "user":
                        st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {chat['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b> {chat['text']}</div>", unsafe_allow_html=True)
                
                user_query = st.chat_input("Ketik pertanyaan atau minta tindakan perbaikan (CAPA) Klausul...")
                
                if user_query:
                    st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {user_query}</div>", unsafe_allow_html=True)
                    
                    kolom_ks = [kolom_dept, kolom_temuan, kolom_status, kolom_standar]
                    ringkasan_data = df_filtered[[c for c in kolom_ks if c in df_filtered.columns]].to_string(index=False)
                    
                    system_instruction = f"""
                    Anda adalah Senior Management Consultant & Auditor Utama bersertifikasi ISO 9001, 14001, 45001, dan SMK3 PP 50/2012.
                    Tugas Anda membantu merumuskan akar masalah dan menyusun Rekomendasi Tindakan Perbaikan (CAPA) untuk Level Operasional dan level Eksekutif.
                    
                    --- MODE OPERASI SAAT INI ---
                    {sris_mode}
                    
                    --- DATA AUDIT AKTIF ---
                    {ringkasan_data[:20000]}
                    --- AKHIR DATA ---
                    
                    Jawab menggunakan Bahasa Indonesia profesional tingkat tinggi, berikan rekomendasi taktis operasional (tindakan korektif) yang patuh regulasi nasional/internasional.
                    """
                    
                    with st.spinner("Menganalisis klausul kepatuhan..."):
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_query,
                            config={'system_instruction': system_instruction}
                        )
                        bot_response = response.text
                    
                    st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b><br><br>{bot_response}</div>", unsafe_allow_html=True)
                    st.session_state.ims_chat_history.append({"role": "user", "text": user_query})
                    st.session_state.ims_chat_history.append({"role": "bot", "text": bot_response})
                    
            except Exception as error_ai:
                st.error(f"Gagal menghubungkan ke AI Engine: {error_ai}")
        else:
            st.warning("⚠️ Silakan masukkan Gemini API Key.")
else:
    st.error("🚨 File data audit belum dimuat atau tidak ditemukan di direktori!")
st.success("Dasbor siap. Silakan gunakan menu di sidebar untuk memfilter data.
