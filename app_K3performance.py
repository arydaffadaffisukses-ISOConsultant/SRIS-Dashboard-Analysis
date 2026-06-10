import streamlit as st
import pandas as pd
import numpy as np
import os

# Paksa Matplotlib menggunakan backend non-interaktif agar aman di server Streamlit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA DASHBOARD
# ==========================================
st.set_page_config(page_title="SRIS SMK3 Simulation Engine", layout="wide", page_icon="🦺")

# Desain Tema Premium Executive (HSE Green & Industrial Grey)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); border-left: 6px solid #1E5631; }
    .security-banner { background-color: #0f2027; color: white; padding: 20px; border-radius: 8px; margin-bottom: 25px; background: linear-gradient(to right, #11998e, #38ef7d); }
    .chat-bubble-user { background-color: #1E5631; color: white; padding: 12px; border-radius: 15px; margin-bottom: 10px; text-align: right; }
    .chat-bubble-bot { background-color: #e9ecef; color: #333; padding: 12px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='security-banner'>
        <h2>🦺 SRIS SMK3 Simulation Dashboard (PP No. 50 Tahun 2012)</h2>
        <p>Sistem Informasi Risiko Strategis | Analisis Skor Insiden, Dampak Finansial, Efisiensi Produksi & Radar Kepatuhan 5 Pilar K3</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. DEFINISI NAMA KOLOM UTAMA (SIMULASI)
# ==========================================
col_insiden = 'skor_insiden_k3'
col_finansial = 'kerugian_finansial_juta'
col_efisiensi = 'efisiensi_produksi_persen'
col_pilar = 'pilar_pentagon'
col_target = 'skor_target'
col_aktual = 'skor_aktual'

# ==========================================
# 3. PEMBACAAN DATA AUTOMATIS / UNGGAHAN
# ==========================================
st.sidebar.header("📂 Data Source")
uploaded_file = st.sidebar.file_uploader("Unggah File Simulasi (.csv/.xlsx):", type=["csv", "xlsx"])

df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except Exception as e:
        st.sidebar.error(f"Gagal membaca file unggahan: {e}")

if df is None:
    for file in os.listdir('.'):
        if (file.endswith('.csv') or file.endswith('.xlsx')) and "simulasi" in file.lower():
            try:
                df = pd.read_csv(file) if file.endswith('.csv') else pd.read_excel(file)
                st.sidebar.info(f"💡 Otomatis memuat file workspace: {file}")
                break
            except:
                pass

# ==========================================
# 4. KONTROL MENU NAVIGASI (KEY-BASED)
# ==========================================
menu_options = {
    "Dashboard": "📊 Indikator Kinerja & Radar K3",
    "Chatbot": "🤖 SRIS K3 AI Consultant"
}
selected_menu_label = st.sidebar.radio("Pilih Navigasi Dashboard:", list(menu_options.values()))
current_menu = [k for k, v in menu_options.items() if v == selected_menu_label][0]

# ==========================================
# 5. PROSES & VISUALISASI DATA
# ==========================================
if df is not None:
    df.columns = [col.strip() for col in df.columns]
    st.sidebar.success("🔌 Simulasi Engine K3 Aktif")
    
    if current_menu == "Dashboard":
        st.subheader("📊 Indikator Kinerja & Dampak Operasional K3")
        
        avg_insiden = df[col_insiden].mean() if col_insiden in df.columns else 0.0
        total_rugi = df[col_finansial].sum() if col_finansial in df.columns else 0.0
        avg_efisiensi = df[col_efisiensi].mean() if col_efisiensi in df.columns else 0.0
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Rata-rata Skor Insiden K3", value=f"{avg_insiden:.1f} Poin", delta="Perlu Dimonitor", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Total Kerugian Finansial", value=f"Rp {total_rugi:.1f} Juta", delta="Beban Kumulatif", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Rata-rata Efisiensi Produksi", value=f"{avg_efisiensi:.1f} %", delta="Target Organisasi")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("##### Tren Skor Insiden vs Kerugian Finansial")
            fig1, ax1 = plt.subplots(figsize=(6, 3.5))
            if col_insiden in df.columns and col_finansial in df.columns:
                ax1.bar(df.index + 1, df[col_insiden], color='#e74c3c', alpha=0.7, label='Skor Insiden')
                ax2 = ax1.twinx()
                ax2.plot(df.index + 1, df[col_finansial], color='#2c3e50', marker='o', linewidth=2, label='Kerugian (Juta)')
                ax1.set_xlabel("ID Kejadian / Periode")
                ax1.set_ylabel("Skor Insiden", color='#e74c3c')
                ax2.set_ylabel("Kerugian (Rp Juta)", color='#2c3e50')
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close(fig1)
            
        with col_g2:
            st.write("##### Distribusi Efisiensi Produksi per Kasus")
            fig2, ax2 = plt.subplots(figsize=(6, 3.5))
            if col_efisiensi in df.columns:
                df[col_efisiensi].plot(kind='line', marker='s', color='#27ae60', linewidth=2, ax=ax2)
                ax2.axhline(y=85, color='red', linestyle='--', label='Batas Minimum Aman (85%)')
                ax2.set_ylabel("Persentase (%)")
                ax2.set_xlabel("ID Kejadian")
                ax2.legend()
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🕸️ Analisis Radar Pentagon K3 (Target vs Aktual)")
        
        if col_pilar in df.columns and col_target in df.columns and col_aktual in df.columns:
            df_pilar = df[[col_pilar, col_target, col_aktual]].dropna().copy()
            df_pilar = df_pilar[df_pilar[col_pilar].str.contains(r'\d', na=False)]
            
            if not df_pilar.empty:
                labels = df_pilar[col_pilar].tolist()
                target_scores = df_pilar[col_target].astype(float).tolist()
                actual_scores = df_pilar[col_aktual].astype(float).tolist()
                
                labels_loop = labels + [labels[0]]
                target_loop = target_scores + [target_scores[0]]
                actual_loop = actual_scores + [actual_scores[0]]
                angles = np.linspace(start=0, stop=2*np.pi, num=len(labels_loop))
                
                c_radar, c_table = st.columns([1.2, 1])
                with c_radar:
                    fig_radar, ax_radar = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
                    ax_radar.plot(angles, target_loop, color='#2980b9', linewidth=2, linestyle='--', label='Target Kepatuhan')
                    ax_radar.fill(angles, target_loop, color='#2980b9', alpha=0.1)
                    ax_radar.plot(angles, actual_loop, color='#27ae60', linewidth=2.5, marker='o', label='Aktual Capaian')
                    ax_radar.fill(angles, actual_loop, color='#27ae60', alpha=0.25)
                    ax_radar.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=8, fontweight='bold')
                    ax_radar.set_ylim(0, 5)
                    ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
                    st.pyplot(fig_radar)
                    plt.close(fig_radar)
                    
                with c_table:
                    st.write("##### Matriks Pemenuhan Kriteria Kebijakan PP 50/2012")
                    df_pilar['Gap'] = df_pilar[col_aktual] - df_pilar[col_target]
                    st.dataframe(df_pilar.set_index(col_pilar), use_container_width=True)
                    min_gap_idx = df_pilar['Gap'].idxmin()
                    st.error(f"⚠️ **Prioritas Koreksi:** Elemen **{df_pilar.loc[min_gap_idx, col_pilar]}** memerlukan perhatian khusus karena memiliki deviasi paling rendah.")

        st.markdown("<br>##### Master Data Log Simulasi Audit", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

    elif current_menu == "Chatbot":
        st.subheader("🤖 SRIS Executive K3 AI Consultant")
        st.info("Asisten AI siap menganalisis data log insiden dan performa pemenuhan 5 Pilar SMK3 organisasi Anda.")
        
        # Deteksi API Key dari Streamlit Secrets
        api_key_input = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else st.text_input("🔑 Masukkan Google Gemini API Key Anda:", type="password")
        
        if api_key_input:
            try:
                # Menggunakan sintaks SDK 'google-genai' terbaru
                from google import genai
                client = genai.Client(api_key=api_key_input)
                
                if "sim_chat_history" not in st.session_state:
                    st.session_state.sim_chat_history = []
                
                # Tampilkan riwayat chat terdahulu
                for chat in st.session_state.sim_chat_history:
                    if chat["role"] == "user":
                        st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {chat['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b> {chat['text']}</div>", unsafe_allow_html=True)
                
                user_query = st.chat_input("Tanyakan analisis kerugian finansial atau rekomendasi perbaikan 5 pilar K3...")
                
                if user_query:
                    st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {user_query}</div>", unsafe_allow_html=True)
                    
                    # Buat rangkuman string data untuk referensi konteks AI
                    string_data_audit = df.to_string(index=False)
                    
                    # Instruksi sistem terstruktur khusus SMK3
                    system_instruction = f"""
                    Anda adalah Senior HSE Management Consultant & Auditor Utama Sistem Manajemen Keselamatan dan Kesehatan Kerja (SMK3) PP No. 50 Tahun 2012.
                    Tugas Anda adalah menganalisis data log simulasi audit dan memberikan rekomendasi perbaikan (CAPA) tingkat tinggi kepada direksi perusahaan.
                    
                    --- DATA LOG SIMULASI OPERASIONAL & PILAR K3 ---
                    {string_data_audit[:15000]}
                    ------------------------------------------------
                    
                    Fokus analisis Anda meliputi pengendalian skor insiden, meminimalkan kerugian finansial, meningkatkan efisiensi produksi, serta menutup gap antara skor target dan aktual pada 5 elemen pilar K3.
                    Berikan jawaban yang taktis, profesional, menggunakan Bahasa Indonesia level eksekutif, dan langsung berfokus pada solusi mitigasi risiko operasional.
                    """
                    
                    with st.spinner("Menganalisis korelasi risiko operasional dan finansial..."):
                        # Sintaks eksekusi model Gemini 2.5 Flash yang benar
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_query,
                            config={'system_instruction': system_instruction}
                        )
                        bot_response = response.text
                    
                    st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b><br><br>{bot_response}</div>", unsafe_allow_html=True)
                    st.session_state.sim_chat_history.append({"role": "user", "text": user_query})
                    st.session_state.sim_chat_history.append({"role": "bot", "text": bot_response})
                    
            except Exception as e:
                st.error(f"Gagal menghubungkan ke AI Engine: {e}")
        else:
            st.warning("⚠️ Silakan masukkan Gemini API Key di atas atau daftarkan di Streamlit Secrets.")
else:
    st.error("🚨 Data tidak ditemukan!")
