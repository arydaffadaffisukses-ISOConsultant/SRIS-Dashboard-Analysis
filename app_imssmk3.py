import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="SRIS Audit Dashboard", layout="wide")
st.title("🛡️ SRIS Audit & Maturity Dashboard")

# 1. Upload File
uploaded_file = st.sidebar.file_uploader("Upload Data Audit (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Deteksi format file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # 2. Sidebar Navigasi
    menu = st.sidebar.radio("Pilih Analisis", ["Dashboard Temuan", "Pentagon Maturity Analysis"])
    
    if menu == "Dashboard Temuan":
        st.subheader("Distribusi Temuan per Departemen")
        fig_bar = px.bar(df['Departemen'].value_counts().reset_index(), x='index', y='Departemen')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.subheader("Data Detail")
        st.dataframe(df, use_container_width=True)

    elif menu == "Pentagon Maturity Analysis":
        st.subheader("🕸️ Pentagon Maturity Analysis")
        
        # Asumsi kolom data: Regulasi, Finansial, Integritas, Operasional, Reputasi
        cols = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        if all(c in df.columns for c in cols):
            # Hitung rata-rata tiap pilar
            values = df[cols].mean().values.tolist()
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=cols,
                fill='toself',
                line_color='blue'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pastikan file Anda memiliki 5 kolom: Regulasi, Finansial, Integritas, Operasional, Reputasi (berisi angka 1-5).")

else:
    st.info("Silakan unggah dokumen CSV atau Excel untuk memulai.")
