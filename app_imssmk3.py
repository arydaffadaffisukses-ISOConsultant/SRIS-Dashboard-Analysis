import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Audit Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload CSV Audit", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Navigasi
    menu = st.sidebar.radio("Navigasi", ["Dashboard Temuan", "Pentagon Analysis (Maturitas)"])

    if menu == "Dashboard Temuan":
        st.subheader("Distribusi Temuan per Departemen")
        fig, ax = plt.subplots()
        sns.countplot(data=df, y='Departemen', palette='viridis', ax=ax)
        st.pyplot(fig)
        
        st.subheader("Detail Temuan")
        st.dataframe(df, use_container_width=True)

    elif menu == "Pentagon Analysis (Maturitas)":
        st.subheader("🕸️ Pentagon Risk Maturity Analysis")
        # Asumsi kolom di CSV: P1_Regulasi, P2_Finansial, P3_Integritas, P4_Operasional, P5_Reputasi
        cols = ['P1_Regulasi', 'P2_Finansial', 'P3_Integritas', 'P4_Operasional', 'P5_Reputasi']
        
        # Validasi kolom agar tidak error
        if all(c in df.columns for c in cols):
            vals = [df[c].mean() for c in cols]
            fig = go.Figure(data=go.Scatterpolar(r=vals, theta=['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi'], fill='toself'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("File CSV Anda belum memiliki kolom untuk Pentagon (P1_Regulasi, P2_Finansial, dst).")
            st.write("Pastikan data memiliki 5 kolom skor tersebut.")

else:
    st.info("Silakan unggah file CSV audit.")
