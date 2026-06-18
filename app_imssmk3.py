import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        
        # Fungsi pembersihan angka
        def get_num(text):
            text = str(text)
            nums = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
            return float(nums[0]) if nums else 0

        df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_num)
        
        # Inisialisasi 3 Tab
        tab1, tab2, tab3 = st.tabs(["Dashboard Ringkasan", "Analisis Finansial", "AI Analyst"])

        with tab1:
            st.subheader("Jumlah Temuan per Departemen")
            dept_counts = df['Departemen Divisi/Area'].value_counts().reset_index()
            dept_counts.columns = ['Departemen', 'Jumlah']
            fig = px.bar(dept_counts, x='Departemen', y='Jumlah', color='Jumlah')
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Analisis Kerugian Finansial")
            fig_scat = px.scatter(
                df, x='Departemen Divisi/Area', y='Kerugian_Val', size='Kerugian_Val',
                color='Departemen Divisi/Area', hover_name='Detail Temuan Ketidaksesuaian'
            )
            st.plotly_chart(fig_scat, use_container_width=True)

        with # Tab 3: AI Analyst
        with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        
        if user_api_key:
            try:
                genai.configure(api_key=user_api_key)
                models_info = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_names = [m.name for m in models_info]
                
                if model_names:
                    model_name = st.selectbox("Pilih Model AI:", model_names, index=0)
                    if "Detail Temuan Ketidaksesuaian" in df.columns:
                        selected = st.selectbox("Pilih Temuan untuk Dianalisis:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
                        if st.button("Generate Analisis AI"):
                            with st.spinner("AI sedang menganalisis..."):
                                model = genai.GenerativeModel(model_name)
                                response = model.generate_content(f"Analisis akar masalah dan berikan rekomendasi perbaikan profesional untuk temuan: {selected}")
                                st.markdown("### Hasil Analisis AI:")
                                st.markdown(response.text)

else:
    st.info("Silakan upload file untuk memulai.")
