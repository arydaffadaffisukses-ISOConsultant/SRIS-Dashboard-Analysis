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

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temuan Per Departemen")
            df_temuan = df.groupby('Departemen Divisi/Area').size().reset_index(name='Jumlah')
            df_temuan = df_temuan.sort_values(by='Jumlah', ascending=False)
            colors = ['red' if i == 0 else 'royalblue' for i in range(len(df_temuan))]
            fig_bar = px.bar(df_temuan, x='Departemen Divisi/Area', y='Jumlah', color_discrete_sequence=['royalblue'])
            fig_bar.update_traces(marker_color=colors)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("Top 3 Departemen: Kerugian Tertinggi")
            df_kerugian = df.groupby('Departemen Divisi/Area')[target_col].sum().reset_index()
            df_kerugian = df_kerugian.sort_values(by=target_col, ascending=False)
            
            # Logika Top 3 + Lainnya
            if len(df_kerugian) > 3:
                top_3 = df_kerugian.head(3).copy()
                others_val = df_kerugian.iloc[3:][target_col].sum()
                if others_val > 0:
                    others = pd.DataFrame({'Departemen Divisi/Area': ['Lainnya'], target_col: [others_val]})
                    df_plot = pd.concat([top_3, others])
                else:
                    df_plot = top_3
            else:
                df_plot = df_kerugian

            fig_pie = px.pie(df_plot, names='Departemen Divisi/Area', values=target_col, hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)

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
