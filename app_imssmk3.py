import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="SRIS Data Hub", layout="wide")
st.title("📊 Security Risk Intelligence System (SRIS)")

uploaded_file = st.sidebar.file_uploader("Upload File Database (Excel/CSV):", type=["xlsx", "csv"])

if uploaded_file is not None:
    # 1. Loading Data
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        df.columns = [col.strip() for col in df.columns] # Bersihkan spasi di nama kolom
        
        st.success("Data berhasil dimuat!")
        
        # 2. Grafik Distribusi Temuan
        st.subheader("🎯 Distribusi Temuan per Departemen")
        if 'Departemen Divisi/Area' in df.columns:
            fig_bar = px.bar(df['Departemen Divisi/Area'].value_counts().reset_index(), 
                             x='Departemen Divisi/Area', y='count')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Kolom 'Departemen Divisi/Area' tidak ditemukan.")

        # 3. Pentagon Analysis
        st.subheader("🕸️ Pentagon Maturity Analysis")
        # Mengambil 5 kolom skoring (indeks 6-10 sesuai screenshot Bapak)
        cols_pentagon = df.columns[6:11]
        
        if len(cols_pentagon) >= 5:
            avg_vals = df[cols_pentagon].mean().tolist()
            labels = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=avg_vals, theta=labels, fill='toself'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.warning("Data untuk Pentagon tidak ditemukan. Pastikan ada 5 kolom skoring.")
            
    except Exception as e:
        st.error(f"Error memproses file: {e}")
else:
    st.info("Silakan unggah file database untuk memulai.")
