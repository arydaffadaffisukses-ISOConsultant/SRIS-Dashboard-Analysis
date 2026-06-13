import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Integrated Audit Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload Database (Excel/CSV):", type=["xlsx", "csv"])

if uploaded_file:
    # 1. Load & Bersihkan Data
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df.columns = [col.strip() for col in df.columns]
    
    # 2. Sidebar Navigasi
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

    elif menu == "Pentagon & Risk Treatment":
        st.subheader("🕸️ Pentagon Maturity & Risk Control")
        
        # Pentagon (Kolom 6-10)
        cols_p = df.columns[6:11]
        values = df[cols_p].mean().tolist()
        labels = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Risk Treatment Table
        st.subheader("📋 Status Risk Treatment & Pengendalian")
        # Mencari kolom yang relevan dengan status/rencana
        display_cols = [c for c in df.columns if any(x in c for x in ['Temuan', 'Status', 'Posisi'])]
        st.dataframe(df[display_cols], use_container_width=True)

else:
    st.info("Silakan unggah file untuk memulai.")
