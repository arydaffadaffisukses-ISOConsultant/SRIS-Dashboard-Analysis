import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Audit Engine")

# --- UPLOAD DATA ---
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Menampilkan DataFrame agar Bapak tahu apakah data terbaca
    st.write("### Data Preview", df.head())

    # --- GRAFIK TEMUAN PER DEPARTEMEN ---
    st.subheader("📊 Temuan per Departemen")
    fig1, ax1 = plt.subplots()
    # Menggunakan kolom 'Departemen' sesuai data Bapak
    df['Departemen'].value_counts().plot(kind='bar', color='#1e5631', ax=ax1)
    st.pyplot(fig1)

    # --- GRAFIK TINGKAT RISIKO ---
    st.subheader("⚠️ Distribusi Tingkat Risiko")
    fig2, ax2 = plt.subplots()
    df['Tingkat Risiko'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    st.pyplot(fig2)
else:
    st.info("Silakan upload file CSV audit di sidebar.")
