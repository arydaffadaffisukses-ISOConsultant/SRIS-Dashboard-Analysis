import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Audit & Financial Risk Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload CSV Audit", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 1. METRIK UTAMA (Jumlah Temuan)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Temuan", len(df))
    col2.metric("Total Estimasi Kerugian", f"Rp {df['Estimasi_Kerugian_Jt'].sum():,.0f} Jt")
    col3.metric("Temuan Open", len(df[df['Status']=='Open']))

    tab1, tab2 = st.tabs(["Distribusi & Kerugian", "Risk Treatment & Control"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Temuan per Departemen")
            fig, ax = plt.subplots()
            df['Departemen'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
            st.pyplot(fig)
        with c2:
            st.subheader("Estimasi Kerugian per Departemen")
            st.bar_chart(df.groupby('Departemen')['Estimasi_Kerugian_Jt'].sum())

    with tab2:
        st.subheader("Risk Treatment & Pengendalian")
        # Menampilkan tabel khusus untuk status pengendalian
        st.write("Daftar Tindakan Perbaikan dan Status Pengendalian:")
        st.dataframe(df[['Temuan', 'Rekomendasi Perbaikan', 'Status', 'Tingkat Risiko']], use_container_width=True)
        
        # Grafik status risk treatment
        st.subheader("Distribusi Status Pengendalian")
        fig2, ax2 = plt.subplots()
        df['Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
        st.pyplot(fig2)

else:
    st.info("Silakan unggah file CSV audit untuk melihat dasbor.")
