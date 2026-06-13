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
        st.subheader("Monitoring Temuan & Status")
        c1, c2 = st.columns(2)
        with c1:
            status_col = next((c for c in df.columns if "Status" in c), None)
            if status_col:
                st.plotly_chart(px.pie(df, names=status_col, title="Temuan tiap departemen"), use_container_width=True)
        with c2:
            posisi_col = next((c for c in df.columns if "Posisi" in c), None)
            if posisi_col:
                st.plotly_chart(px.bar(df[posisi_col].value_counts().reset_index(), x=posisi_col, y='count', title="Kerugian tiap departemen"), use_container_width=True)

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
