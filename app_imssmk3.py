import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="SRIS Audit Dashboard", layout="wide")

st.title("🛡️ SRIS Audit & Risk Intelligence")

# 1. Mock Data (Ganti bagian ini dengan load file CSV/Excel Bapak)
data = {
    'Departemen': ['Logistik', 'Produksi', 'HRD', 'Maintenance', 'Logistik', 'Produksi'],
    'Standard': ['ISO 9001', 'ISO 45001', 'ISO 9001', 'ISO 45001', 'ISO 14001', 'ISO 9001'],
    'Estimasi_Kerugian_Jt': [50, 20, 10, 100, 30, 40],
    'P1_Regulasi': [4, 2, 3, 5, 2, 4],
    'P2_Finansial': [3, 1, 2, 5, 3, 2],
    'P3_Integritas': [4, 3, 4, 3, 2, 4],
    'P4_Operasional': [2, 5, 2, 4, 3, 2],
    'P5_Reputasi': [3, 2, 3, 4, 3, 3]
}
df = pd.DataFrame(data)

# Sidebar Filter
dept = st.sidebar.selectbox("Pilih Departemen", ["Semua"] + list(df['Departemen'].unique()))
df_f = df if dept == "Semua" else df[df['Departemen'] == dept]

# --- VISUALISASI ---
col1, col2 = st.columns(2)

with col1:
    # 1. Grafik Temuan per Departemen
    st.subheader("📊 Temuan per Departemen")
    fig, ax = plt.subplots()
    sns.countplot(data=df_f, y='Departemen', palette='viridis', ax=ax)
    st.pyplot(fig)

    # 2. Grafik Standar ISO
    st.subheader("📋 Distribusi Standar ISO")
    fig2, ax2 = plt.subplots()
    df_f['Standard'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    st.pyplot(fig2)

with col2:
    # 3. Estimasi Kerugian
    st.subheader("💰 Estimasi Kerugian (Jt)")
    st.bar_chart(df_f.groupby('Departemen')['Estimasi_Kerugian_Jt'].sum())

    # 4. Pentagon Analysis (Radar Chart)
    st.subheader("🕸️ Pentagon Risk Analysis")
    labels = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
    stats = [df_f['P1_Regulasi'].mean(), df_f['P2_Finansial'].mean(), df_f['P3_Integritas'].mean(), 
             df_f['P4_Operasional'].mean(), df_f['P5_Reputasi'].mean()]
    
    fig3, ax3 = plt.subplots(subplot_kw={'projection': 'polar'})
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    ax3.plot(angles, stats, 'o-', linewidth=2)
    ax3.fill(angles, stats, alpha=0.25)
    ax3.set_xticks(angles[:-1], labels)
    st.pyplot(fig3)

# 5. Detail Temuan
st.subheader("📝 Detail Data Audit")
st.dataframe(df_f, use_container_width=True)
