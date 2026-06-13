import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Integrated Audit Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload Database (Excel/CSV):", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df.columns = [col.strip() for col in df.columns]
    
    menu = st.sidebar.radio("Navigasi", ["Dashboard Ringkasan", "Pentagon & Risk Status"])

    if menu == "Dashboard Ringkasan":
        st.subheader("📊 Monitoring Status & Posisi Temuan")
        
        col1, col2 = st.columns(2)
        with col1:
            # Visualisasi Status Temuan
            status_col = next((c for c in df.columns if "Status" in c), None)
            if status_col:
                fig_status = px.pie(df, names=status_col, title="Status Temuan (Open/Closed)")
                st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Visualisasi Posisi Status NC
            posisi_col = next((c for c in df.columns if "Posisi" in c), None)
            if posisi_col:
                fig_posisi = px.bar(df[posisi_col].value_counts().reset_index(), x=posisi_col, y='count', title="Posisi/Progress Status NC")
                st.plotly_chart(fig_posisi, use_container_width=True)

    elif menu == "Pentagon & Risk Treatment":
        st.subheader("🕸️ Pentagon Maturity & Risk Treatment")
        
        # Pentagon (Kolom 6-10)
        cols_p = df.columns[6:11]
        values = df[cols_p].mean().tolist()
        labels = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Tabel Detail Temuan, Posisi, dan Status
        st.subheader("📋 Detail Tindakan Perbaikan")
        display_cols = [c for c in df.columns if any(x in c for x in ['Temuan', 'Status', 'Posisi', 'Rekomendasi'])]
        st.dataframe(df[display_cols], use_container_width=True)

else:
    st.info("Silakan unggah file untuk memulai.")
