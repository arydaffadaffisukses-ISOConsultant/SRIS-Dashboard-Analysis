import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="SRIS Pro Dashboard", layout="wide")

# --- SIDEBAR: UPLOAD DATA ---
st.sidebar.header("📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Unggah File Audit (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.sidebar.success("Data berhasil dimuat!")
else:
    # Data dummy sebagai cadangan jika belum upload
    df = pd.DataFrame({'Departemen': ['Logistik', 'Produksi'], 'Klausul': ['4.1', '5.2'], 'Skor': [3, 4]})

# --- LOGIKA ANALISIS MATURITAS ---
def calculate_maturity(df):
    # Asumsi: Skor maturitas ada di kolom 'Skor' 1-5
    avg_score = df['Skor'].mean()
    if avg_score >= 4: return "Optimal (Level 4-5)", "green"
    elif avg_score >= 2: return "Defined (Level 2-3)", "orange"
    else: return "Initial (Level 1)", "red"

# --- MAIN DASHBOARD ---
st.title("🛡️ SRIS Integrated Engine")

tab1, tab2, tab3 = st.tabs(["Executive Summary", "Risk Pentagon", "Maturity Analysis"])

with tab1:
    st.subheader("📊 Temuan & Kerugian")
    # Tampilkan grafik temuan dan kerugian di sini
    
with tab3:
    st.subheader("📈 Risk Maturity Analysis")
    if 'Skor' in df.columns:
        level, color = calculate_maturity(df)
        st.metric("Tingkat Maturitas Organisasi", level)
        # Visualisasi Maturitas
        fig, ax = plt.subplots()
        sns.barplot(x='Departemen', y='Skor', data=df, palette='Blues_d')
        st.pyplot(fig)
    else:
        st.warning("Pastikan file memiliki kolom 'Skor' untuk analisis maturitas.")
