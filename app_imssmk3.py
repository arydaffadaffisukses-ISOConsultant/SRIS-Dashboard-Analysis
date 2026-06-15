import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Load Data
# Ganti 'data_temuan.csv' dengan nama file asli Bapak
uploaded_file = st.file_uploader("Upload file CSV data temuan:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.title("Dashboard Analisis SRIS")
    
    # Membuat 2 kolom untuk layout grafik agar rapi
    col1, col2 = st.columns(2)
    
    # GRAFIK 1: Distribusi temuan berdasarkan departemen
    with col1:
        st.subheader("1. Distribusi Temuan per Departemen")
        fig1 = px.pie(df, names='Departemen', title='Persentase Temuan per Dept')
        st.plotly_chart(fig1, use_container_width=True)
        
    # GRAFIK 2: Estimasi kerugian berdasarkan temuan
    with col2:
        st.subheader("2. Estimasi Kerugian")
        fig2 = px.bar(df, x='Departemen', y='Kerugian', title='Total Estimasi Kerugian')
        st.plotly_chart(fig2, use_container_width=True)
        
    # GRAFIK 3: Implementation risk maturity
    st.subheader("3. Risk Maturity Level")
    fig3 = px.box(df, x='Departemen', y='Risk_Maturity_Score', title='Tingkat Kematangan Risiko')
    st.plotly_chart(fig3, use_container_width=True)
    
    # GRAFIK 4: Pengendalian resiko
    st.subheader("4. Efektivitas Pengendalian Risiko")
    fig4 = px.scatter(df, x='Risk_Maturity_Score', y='Kerugian', color='Departemen', size='Kerugian')
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("Silakan upload file CSV untuk melihat dasbor.")
