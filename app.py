import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# --- PENGATURAN HALAMAN WEB ---
st.set_page_config(page_title="SRIS AI Enterprise", page_icon="🛡️", layout="wide")

# --- MENU NAVIGATION (SIDEBAR) ---
st.sidebar.title("🛡️ SRIS Core Engine")
st.sidebar.markdown("*Version 2.0 - Enterprise Edition*")
st.sidebar.divider()
menu = st.sidebar.radio("Pilih Modul Aplikasi:", ["📂 Upload Data & Train AI", "🤖 Asisten Chatbot AI ISO"])

# --- MODUL 1: UPLOAD DATA & PREDIKSI ---
if menu == "📂 Upload Data & Train AI":
    st.title("📂 Integrasi Data Klien & Pelatihan AI Mandiri")
    st.subheader("Unggah file CSV audit klien untuk mengkalibrasi Otak AI SRIS")
    st.divider()
    
    # 1. TOMBOL UPLOAD CSV KLIEN
    uploaded_file = st.file_uploader("Pilih file CSV Data Audit Klien Bapak:", type=["csv"])
    
    if uploaded_file is not None:
        # Membaca data CSV asli dari klien
        df_client = pd.read_csv(uploaded_file)
        
        st.success("✅ Data Klien Berhasil Dimasukkan!")
        st.markdown("### 📋 Cuplikan Data Riil Klien (5 Baris Pertama)")
        st.dataframe(df_client.head()) # Menampilkan tabel data klien secara interaktif
        
        # VALIDASI APALAKAH KOLOMNYA SESUAI STANDARD SRIS
        required_cols = ['Dampak_Finansial_Rp', 'Status_Temuan']
        if all(col in df_client.columns for col in required_cols):
            
            st.divider()
            st.markdown("### 🧠 Proses Training AI Berbasis Data Klien")
            
            # 2. FEATURE ENGINEERING OTOMATIS (DATA PREPARATION)
            # Mengubah target teks menjadi angka biner (Label Encoding)
            df_client['Status_Angka'] = df_client['Status_Temuan'].map({'Minor': 0, 'Major': 1})
            
            # Jika ada data kosong, langsung dibersihkan
            df_client = df_client.dropna(subset=['Status_Angka', 'Dampak_Finansial_Rp'])
            
            X = df_client[['Dampak_Finansial_Rp']]
            y = df_client['Status_Angka']
            
            # Standardisasi Skala Finansial (Scaling)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Melatih Otak AI dengan Data Riil Klien
            model_ai = LogisticRegression(class_weight='balanced')
            model_ai.fit(X_scaled, y)
            
            st.info("🤖 Otak AI SRIS Berhasil Dikalibrasi Menggunakan Pola Risiko Klien Bapak!")
            
            st.divider()
            
            # 3. INTERAKSI PREDIKSI LAPANGAN
            st.markdown("### 🔮 Simulasi Alat Deteksi Risiko Instan")
            input_uang = st.slider(
                "Geser untuk Tes Dampak Finansial Temuan Baru (Rp):", 
                min_value=int(df_client['Dampak_Finansial_Rp'].min()), 
                max_value=int(df_client['Dampak_Finansial_Rp'].max()), 
                value=int(df_client['Dampak_Finansial_Rp'].median()),
                step=1000000,
                format="Rp %d"
            )
            
            # Kalkulasi AI
            input_df = pd.DataFrame({'Dampak_Finansial_Rp': [input_uang]})
            input_scaled = scaler.transform(input_df)
            prediksi = model_ai.predict(input_scaled)[0]
            probabilitas = model_ai.predict_proba(input_scaled)[0]
            
            # Tampilan Hasil Visual
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Keputusan AI:")
                if prediksi == 1:
                    st.error("⚠️ MAJOR (Risiko Tinggi / Kritis)")
                    keyakinan = probabilitas[1] * 100
                else:
                    st.success("✅ MINOR (Risiko Rendah / Biasa)")
                    keyakinan = probabilitas[0] * 100
                st.metric(label="Tingkat Keyakinan Prediksi", value=f"{keyakinan:.2f}%")
                
            with col2:
                st.markdown("#### Grafik Probabilitas (%)")
                chart_data = pd.DataFrame({
                    'Kategori': ['MINOR', 'MAJOR'],
                    'Probabilitas': [probabilitas[0]*100, probabilitas[1]*100]
                }).set_index('Kategori')
                st.bar_chart(chart_data, color="#2a9d8f")
                
        else:
            st.error(f"⚠️ Format File Salah! Pastikan CSV klien memiliki kolom: {required_cols}")
            
    else:
        st.warning("👋 Silakan unggah file CSV data masa lalu klien Bapak di atas untuk memulai analisa.")

# --- MODUL 2: CHATBOT AI ---
elif menu == "🤖 Asisten Chatbot AI ISO":
    st.title("🤖 Asisten Konten & Klausul ISO (SRIS Chatbot)")
    st.subheader("Diskusikan Rekomendasi Tindakan Perbaikan (CAPA) Secara Instan")
    st.divider()
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Halo Pak! Server SRIS v2.0 Enterprise siap membantu. Klausul ISO mana yang mau kita bedah malam ini?"}]
        
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]): st.write(msg["content"])
            
    user_input = st.chat_input("Ketik pertanyaan Bapak di sini...")
    if user_input:
        with st.chat_message("user"): st.write(user_input)
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            with st.spinner("AI sedang merumuskan analisa risiko..."):
                teks_cari = user_input.lower()
                if "8.1" in teks_cari or "operasional" in teks_cari:
                    response = "Analisis SRIS: Untuk temuan pada Klausul 8.1, langkah mitigasi wajibnya meliputi: 1. Evaluasi ulang HIRADC/IBPR di area kerja, 2. Memperketat implementasi JSA (Job Safety Analysis), dan 3. Melakukan re-briefing prosedur kerja aman."
                elif "major" in teks_cari or "kritis" in teks_cari:
                    response = "Peringatan Sistem SRIS: Temuan berkategori MAJOR menandakan kegagalan sistemik. Segera terbitkan Formulir CPAR dan lakukan Root Cause Analysis (RCA) menggunakan metode 5-Whys."
                else:
                    response = f"Rekomendasi taktis SRIS untuk topik '{user_input}' adalah mengumpulkan bukti implementasi lapangan (logbook/foto visual) untuk diverifikasi sebelum audit eksternal dilaksanakan."
                st.write(response)
                st.session_state["messages"].append({"role": "assistant", "content": response})
''')

print("--- FILE APP.PY ENTERPRISE BERHASIL DI-UPGRADE ---")
