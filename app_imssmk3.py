import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import google.generativeai as genai

# Konfigurasi halaman
st.set_page_config(layout="wide")
st.title("🛡️ SRIS Integrated Audit Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload Database (Excel/CSV):", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df.columns = [col.strip() for col in df.columns]
    
    # --- MEMBUAT TAB ---
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
      menu = st.sidebar.radio("Pilih Analisis", ["Executive Summary", "Pentagon & Risk Treatment"])

    if menu == "Executive Summary":
        st.subheader("Distribusi Temuan & Estimasi Kerugian")
        
        col1, col2 = st.columns(2)
        with col1:
            # Cari kolom departemen
            dep_col = next((c for c in df.columns if "Departemen" in c), df.columns[3])
            fig_bar = px.bar(df[dep_col].value_counts().reset_index(), x=dep_col, y='count', title="Jumlah Temuan per Departemen")
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            # Estimasi Kerugian (Mencari kolom yang mengandung kata 'Kerugian')
            loss_col = next((c for c in df.columns if "Kerugian" in c or "Finansial" in c), None)
            if loss_col:
                fig_loss = px.pie(df, values=loss_col, names=dep_col, title="Estimasi Kerugian Finansial per Departemen")
                st.plotly_chart(fig_loss, use_container_width=True)
            else:
                st.warning("Kolom 'Estimasi Kerugian' tidak ditemukan.")

    with tab2:
        st.subheader("Pentagon Maturity & Risk Treatment")
        cols_p = df.columns[6:11]
        values = df[cols_p].mean().tolist()
        fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'], fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)

    with tab3:
        st.subheader("AI Root Cause Analysis & CAPA")
        temuan_col = "Detail Temuan Ketidaksesuaian" # Sesuaikan dengan nama kolom asli Bapak
        if temuan_col in df.columns:
            selected_temuan = st.selectbox("Pilih Temuan untuk dianalisis:", df[temuan_col].dropna().unique())
            if st.button("Generate Analisis AI"):
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Analisis akar masalah dan buatkan rencana CAPA untuk temuan: {selected_temuan}")
                st.markdown(response.text)
        else:
            st.error(f"Kolom '{temuan_col}' tidak ditemukan.")

else:
    st.info("Silakan unggah file untuk memulai.")
