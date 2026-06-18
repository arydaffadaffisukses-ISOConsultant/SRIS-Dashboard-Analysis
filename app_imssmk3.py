import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("📊 SRIS Dashboard Analysis")

# Upload File
uploaded_file = st.file_uploader("Upload file CSV/Excel Data Audit:", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    # Tab 1: Dashboard Ringkasan
    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Distribusi Temuan per Departemen")
            df_temuan = df.groupby('Departemen Divisi/Area').size().reset_index(name='Jumlah')
            df_temuan = df_temuan.sort_values(by='Jumlah', ascending=False)
            
            # Warna: Merah untuk tertinggi, biru untuk lainnya
            colors = ['red' if i == 0 else 'royalblue' for i in range(len(df_temuan))]
            fig_bar = px.bar(df_temuan, x='Departemen Divisi/Area', y='Jumlah', color_discrete_sequence=['royalblue'])
            fig_bar.update_traces(marker_color=colors)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("Detail Temuan Ketidaksesuaian")
            if "Detail Temuan Ketidaksesuaian" in df.columns:
                tabel_temuan = df[['Departemen Divisi/Area', 'Detail Temuan Ketidaksesuaian']]
                st.dataframe(tabel_temuan, use_container_width=True, hide_index=True)
            else:
                st.warning("Kolom 'Detail Temuan Ketidaksesuaian' tidak ditemukan.")

    # Tab 2: Pentagon & Risk
    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        cols_pentagon = [
            'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 
            'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 
            'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 
            'Skoring Pentagon Analisis [P4- Operasional]', 
            'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
        ]
        
        def clean_and_map(val):
            val_str = str(val).strip().lower()
            if any(x in val_str for x in ['rendah', 'low', '1']): return 1
            if any(x in val_str for x in ['cukup', 'medium', '2']): return 2
            if any(x in val_str for x in ['sedang', '3']): return 3
            if any(x in val_str for x in ['baik', 'high', '4']): return 4
            if any(x in val_str for x in ['sangat baik', 'excellent', '5']): return 5
            return 0

        for col in cols_pentagon:
            if col in df.columns: df[col] = df[col].apply(clean_and_map)
        
        avg_scores = df[cols_pentagon].mean().values
        categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure(go.Scatterpolar(r=avg_scores, theta=categories, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 5])), title="Rata-rata Skor Pentagon")
        st.plotly_chart(fig_radar, use_container_width=True)

        st.subheader("📈 Hubungan Risiko vs Kerugian Finansial")
        # 1. Pastikan kolom diubah menjadi angka terlebih dahulu (jika gagal, jadi 0)
df['Implementation Risk Maturity'] = pd.to_numeric(df['Implementation Risk Maturity'], errors='coerce').fillna(0)
df['Estimasi Kerugian Finansial Atas Temuan Audit'] = pd.to_numeric(df['Estimasi Kerugian Finansial Atas Temuan Audit'], errors='coerce').fillna(0)

# 2. Sekarang baru buat grafik (gunakan angka konstan untuk size agar tidak error)
# 1. Pastikan kolom diubah menjadi angka terlebih dahulu (jika gagal, jadi 0)
df['Implementation Risk Maturity'] = pd.to_numeric(df['Implementation Risk Maturity'], errors='coerce').fillna(0)
df['Estimasi Kerugian Finansial Atas Temuan Audit'] = pd.to_numeric(df['Estimasi Kerugian Finansial Atas Temuan Audit'], errors='coerce').fillna(0)

# 2. Sekarang baru buat grafik (gunakan angka konstan untuk size agar tidak error)
fig_bubble = px.scatter(df, 
                        x='Implementation Risk Maturity', 
                        y='Estimasi Kerugian Finansial Atas Temuan Audit',
                        size_max=40, 
                        color='Departemen Divisi/Area',
                        hover_name='Departemen Divisi/Area', 
                        template="plotly_white")

    # Tab 3: AI Analyst
    with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        
        if user_api_key:
            try:
                genai.configure(api_key=user_api_key)
                models_info = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_names = [m.name for m in models_info]
                
                if model_names:
                    model_name = st.selectbox("Pilih Model AI:", model_names, index=0)
                    if "Detail Temuan Ketidaksesuaian" in df.columns:
                        selected = st.selectbox("Pilih Temuan untuk Dianalisis:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
                        if st.button("Generate Analisis AI"):
                            with st.spinner("AI sedang menganalisis..."):
                                model = genai.GenerativeModel(model_name)
                                response = model.generate_content(f"Analisis akar masalah dan berikan rekomendasi perbaikan profesional untuk temuan: {selected}")
                                st.markdown("### Hasil Analisis AI:")
                                st.markdown(response.text)
                    else:
                        st.error("Kolom 'Detail Temuan Ketidaksesuaian' tidak ditemukan di file Anda.")
            except Exception as e:
                st.error(f"Error AI: {e}")
