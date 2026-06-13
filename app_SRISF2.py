import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Load Data
csv_data = '''Timestamp,Auditor,Lokasi/Unit,Departemen,Temuan,Kategori,Tingkat Risiko,Rekomendasi Perbaikan,Status,Tenggat Waktu,Catatan Auditor
2026-06-01 09:00:00,Budi Santoso,Gudang A,Logistik,APAR kadaluarsa,Fasilitas,Medium,Ganti APAR baru,Open,2026-06-15,Segera dilakukan penggantian
2026-06-01 10:30:00,Siti Aminah,Area Produksi,Produksi,Operator tanpa sarung tangan,K3,High,Sosialisasi APD,Closed,2026-06-03,Sudah ditindaklanjuti
2026-06-01 13:15:00,Budi Santoso,Kantor Pusat,HRD,Data karyawan tidak terenkripsi,Sistem,High,Implementasi enkripsi data,Open,2026-06-30,Perlu koordinasi dengan IT
2026-06-02 08:45:00,Andi Wijaya,Workshop,Maintenance,Kabel terkelupas,K3,Critical,Perbaikan instalasi listrik,Open,2026-06-05,Bahaya tinggi
2026-06-02 11:20:00,Siti Aminah,Gudang B,Logistik,Forklift tanpa lampu,Fasilitas,Medium,Perbaikan lampu forklift,In Progress,2026-06-10,Menunggu sparepart'''

df = pd.read_csv(io.StringIO(csv_data))
# Definisi fungsi untuk mengambil skor rata-rata per dimensi
def get_dimensi_score(dimensi_name):
    # Filter data berdasarkan Kategori (dimensi) dan ambil rata-rata skornya
    val = df[df['Kategori'] == dimensi_name]['Score'].mean()
    # Jika tidak ada data, kembalikan nilai 0 agar tidak error
    return val if pd.notnull(val) else 0
# 2. Persiapan Data (Mapping)
bobot = {'Critical': 5, 'High': 3, 'Medium': 2, 'Low': 1}
maturity_map = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
df['Score'] = df['Tingkat Risiko'].map(bobot)
df['Est_Kerugian_Jt'] = df['Tingkat Risiko'].map({'Critical': 100, 'High': 50, 'Medium': 20, 'Low': 5})
df['Maturity_Score'] = df['Tingkat Risiko'].map(maturity_map)
maturity_df = df.groupby('Departemen')['Maturity_Score'].mean().reset_index()

# 3. Definisikan Grafik (fig1, fig2, fig3, fig4)
fig1, ax1 = plt.subplots()
sns.countplot(data=df, x='Departemen', hue='Departemen', palette='viridis', legend=False, ax=ax1)
ax1.set_title('Jumlah Temuan')

fig2, ax2 = plt.subplots()
df.groupby('Departemen')['Est_Kerugian_Jt'].sum().plot(kind='bar', color='salmon', ax=ax2)
ax2.set_title('Estimasi Kerugian (Juta)')

fig3, ax3 = plt.subplots()
sns.barplot(data=maturity_df, x='Departemen', y='Maturity_Score', hue='Departemen', palette='magma', legend=False, ax=ax3)
ax3.set_title('Risk Maturity Index')

# Definisi label dengan tambahan P1-P5
labels = ['P1: Regulasi', 'P2: Finansial', 'P3: Integritas Data', 'P4: Operasional', 'P5: Reputasi']
values = [get_dimensi_score(cat) for cat in ['Regulasi', 'Finansial', 'Integritas Data', 'Operasional', 'Reputasi']]

# Pastikan values menutup lingkaran
values += values[:1]
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig4, ax4 = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
ax4.fill(angles, values, color='teal', alpha=0.25)
ax4.plot(angles, values, color='teal', linewidth=2)

# Mengatur label P1-P5
ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels, size=10, fontweight='bold')
ax4.set_title('Pentagon Analisis (Dimensi Risiko)', pad=20, fontsize=12)

# Menambah jarak agar tidak mepet
ax4.tick_params(axis='x', pad=15)

# 4. Tampilkan di Streamlit
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
    st.pyplot(fig3)
with col2:
    st.pyplot(fig2)
    st.pyplot(fig4)
