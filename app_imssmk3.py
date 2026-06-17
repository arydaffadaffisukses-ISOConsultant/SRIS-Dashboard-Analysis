import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Audit Dashboard TDM", layout="wide")
st.title("📊 SRIS Dashboard: PT TDM Analysis")

# Upload File
uploaded_file = st.file_uploader("Upload File Audit Anda:", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # PENTING: Membersihkan nama kolom dari spasi yang tidak terlihat
        df.columns = df.columns.str.strip()
        
        # Tab utama
        tab1, tab2 = st.tabs(["📊 Dashboard Visual", "📋 Detail Data"])
        
        with tab1:
            st.subheader("Distribusi Temuan per Departemen")
            if 'Departemen Divisi/Area' in df.columns:
                fig = px.bar(df.groupby('Departemen Divisi/Area').size().reset_index(name='Jumlah'), 
                             x='Departemen Divisi/Area', y='Jumlah', color='Jumlah')
                st.plotly_chart(fig, use_container_width=True)
            
            # Sunburst Check
            strategi_col = [c for c in df.columns if 'Strategis' in c]
            taktis_col = [c for c in df.columns if 'Taktis' in c]
            
            if strategi_col and taktis_col:
                st.subheader("Korelasi Strategi vs Taktis")
                fig_sun = px.sunburst(df, path=[strategi_col[0], taktis_col[0]], 
                                      values=None) # Tambahkan angka jika ada kolom kerugian
                st.plotly_chart(fig_sun, use_container_width=True)
                
    except Exception as e:
        st.error(f"Terjadi kesalahan pada data: {e}")
        st.info("Pastikan nama kolom di Excel Bapak sesuai dengan yang terbaca oleh sistem.")
