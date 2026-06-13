import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Sidebar Upload
uploaded_file = st.sidebar.file_uploader("Upload File Audit", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # 1. PAKSA DATA JADI ANGKA (Penting agar Pentagon Jalan)
    cols_pentagon = ['P1_Regulasi', 'P2_Finansial', 'P3_Integritas', 'P4_Operasional', 'P5_Reputasi']
    for col in cols_pentagon:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0 # Jika kolom tidak ada, beri nilai 0
            
    # Navigasi
    nav = st.sidebar.radio("Navigasi", ["Dashboard", "Pentagon Analysis"])
    
    if nav == "Dashboard":
        st.write("### Data Audit", df.head())
        
    elif nav == "Pentagon Analysis":
        st.subheader("🕸️ Pentagon Risk Analysis")
        
        # Hitung Rata-rata
        vals = [df[c].mean() for c in cols_pentagon]
        
        # Plotly Radar Chart
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'],
            fill='toself'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Silakan upload file CSV untuk memulai.")
