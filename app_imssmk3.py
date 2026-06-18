import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Blok try-except yang benar
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Eror saat membaca file: {e}")
        st.stop() # Hentikan proses jika gagal baca file

    # Sekarang tab1, tab2 berada di luar try-except (sejajar dengan if)
    tab1, tab2 = st.tabs(["Dashboard Ringkasan", "Analisis Finansial"])

    with tab1:
        st.subheader("Jumlah Temuan per Departemen")
        dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
        dept_counts.columns = ['Departemen', 'Jumlah']
        fig = px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Analisis Kerugian Finansial")
        
        # Pembersihan angka untuk kolom kerugian
        import re
        def get_num(text):
            text = str(text)
            nums = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
            return float(nums[0]) if nums else 0

        df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_num)
        
        fig_scat = px.scatter(
            df, 
            x='Departemen Divisi/Area', 
            y='Kerugian_Val', 
            size='Kerugian_Val',
            color='Departemen Divisi/Area',
            hover_name='Detail Temuan Ketidaksesuaian'
        )
        st.plotly_chart(fig_scat, use_container_width=True)

else:
    st.info("Silakan upload file untuk memulai.")
