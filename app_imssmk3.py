import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from google import genai

st.set_page_config(page_title="SRIS Data Hub", layout="wide")
st.title("📊 Security Risk Intelligence System (SRIS)")

# --- UPLOAD & LOAD DATA ---
uploaded_file = st.sidebar.file_uploader("📂 Hubungkan Database (Excel/CSV):", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df.columns = [col.strip() for col in df.columns]

    # --- GRAFIK 1: DISTRIBUSI TEMUAN PER DEPARTEMEN ---
    st.subheader("🎯 Analisis Distribusi Temuan")
    if 'Departemen Divisi/Area' in df.columns:
        fig_bar = px.bar(df['Departemen Divisi/Area'].value_counts().reset_index(), 
                         x='Departemen Divisi/Area', y='count', 
                         title="Jumlah Temuan per Departemen")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- GRAFIK 2: PENTAGON ANALYSIS (Radar Chart) ---
    st.subheader("🕸️ Pentagon Maturity Analysis")
    # Mengambil kolom 6 sampai 10 sesuai struktur data Bapak
    cols_pentagon = df.columns[6:11] 
    if len(cols_pentagon) >= 5:
        avg_scores = df[cols_pentagon].mean().tolist()
        labels = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=avg_scores, theta=labels, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.warning("Data untuk Pentagon Analysis tidak ditemukan/kurang.")

    # --- AI CONSULTANT ---
    st.markdown("---")
    st.subheader("🤖 SRIS AI Consultant")
    api_key = st.sidebar.text_input("Gemini API Key:", type="password")
    if api_key:
        client = genai.Client(api_key=api_key)
        prompt = st.chat_input("Tanyakan analisis data...")
        if prompt:
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            st.write(response.text)
else:
    st.info("Silakan upload file database untuk memunculkan grafik.")
