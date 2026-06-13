import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("SRIS Audit App")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data berhasil diunggah!")
    
    # Pentagon Data Check
    cols = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
    if all(c in df.columns for c in cols):
        values = df[cols].mean().tolist()
        fig = go.Figure(data=go.Scatterpolar(r=values, theta=cols, fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
        st.plotly_chart(fig)
    else:
        st.write("Kolom yang ditemukan:", df.columns.tolist())
        st.error("Pastikan file punya kolom: Regulasi, Finansial, Integritas, Operasional, Reputasi")
