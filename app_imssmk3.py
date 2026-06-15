import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

st.set_page_config(page_title="SRIS Dashboard", layout="wide")
st.title("📊 SRIS Dashboard Analysis")

uploaded_file = st.file_uploader("Upload file CSV/Excel Data Audit:", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # --- PENTING: PEMBERSIH DATA ---
        # Ini akan mengubah format teks/mata uang menjadi angka (integer/float)
        target_col = 'Estimasi Kerugian Finansial Atas Temuan Audit'
        if target_col in df.columns:
            df[target_col] = df[target_col].replace(r'[^0-9.]', '', regex=True)
            df[target_col] = pd.to_numeric(df[target_col], errors='coerce').fillna(0)
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    # Tab 1: Dashboard Ringkasan
    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns([1, 1]) # Membagi layar menjadi dua
        
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
            # Menampilkan tabel interaktif yang berisi keterangan temuan
            if "Detail Temuan Ketidaksesuaian" in df.columns:
                # Kita pilih kolom yang relevan agar tabel tidak terlalu lebar
                tabel_temuan = df[['Departemen Divisi/Area', 'Detail Temuan Ketidaksesuaian']]
                st.dataframe(
                    tabel_temuan, 
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Kolom 'Detail Temuan Ketidaksesuaian' tidak ditemukan di data.")
    with tab2:
        # (Bagian Pentagon tetap sama)
        st.subheader("🕸️ Pentagon & Risk Analysis")
        # ... kode radar chart Anda ...

    with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        if user_api_key:
            try:
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                if "Detail Temuan Ketidaksesuaian" in df.columns:
                    selected = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
                    if st.button("Generate Analisis AI"):
                        with st.spinner("AI sedang berpikir..."):
                            response = model.generate_content(f"Analisis akar masalah: {selected}")
                            st.markdown(response.text)
            except Exception as e:
                st.error(f"Error AI: {e}")
