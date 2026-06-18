import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Baca data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # FUNGSI PEMBERSIH DATA (ANGKA MURNI)
        def get_only_number(val):
            val_str = str(val)
            # Ambil angka pertama yang muncul dalam string (misal "2" dari "2, Minor")
            nums = re.findall(r'\d+', val_str)
            return float(nums[0]) if nums else 0

        # Bersihkan kedua kolom yang jadi masalah
        df['Maturity_Clean'] = df['Implementation Risk Maturity'].apply(get_only_number)
        df['Kerugian_Clean'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_only_number)

        tab1, tab2, tab3 = st.tabs(["Dashboard", "Analisis Finansial", "AI Analyst"])

        with tab1:
            st.subheader("Jumlah Temuan per Departemen")
            dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
            fig = px.bar(dept_counts, x='Departemen Divisi/Area', y='count')
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Korelasi Risiko vs Kerugian")
            # Gunakan kolom yang sudah bersih (Maturity_Clean dan Kerugian_Clean)
            fig_bubble = px.scatter(
                df, 
                x='Maturity_Clean', 
                y='Kerugian_Clean',
                size='Maturity_Clean', 
                color='Departemen Divisi/Area',
                hover_name='Detail Temuan Ketidaksesuaian',
                size_max=40,
                template="plotly_white"
            )
            st.plotly_chart(fig_bubble, use_container_width=True)

        with tab3:
            st.subheader("🤖 AI Root Cause Analysis")
            user_api_key = st.text_input("Masukkan Google API Key:", type="password")
            if user_api_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=user_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    selected = st.selectbox("Pilih Temuan:", df["Detail Temuan Ketidaksesuaian"].unique())
                    if st.button("Generate Analisis"):
                        res = model.generate_content(f"Analisis akar masalah: {selected}")
                        st.write(res.text)
                except Exception as e:
                    st.error(f"Error AI: {e}")

    except Exception as e:
        st.error(f"Eror saat memproses data: {e}")
