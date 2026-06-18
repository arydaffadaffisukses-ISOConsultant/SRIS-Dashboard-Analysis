import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🛡️ SRIS Dashboard Analytics")

uploaded_file = st.file_uploader("Upload File CSV/Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # 1. Load data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        
        # 2. Pembersihan Data Kerugian (Ambil angka dari teks "Sedang ( Rp 10 juta ... )")
        # Fungsi ini mengambil angka pertama yang ditemukan di dalam string
        import re
        def get_num(text):
            text = str(text)
            nums = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
            return float(nums[0]) if nums else 0

        df['Kerugian_Val'] = df['Estimasi Kerugian Finansial Atas Temuan Audit'].apply(get_num)
        
       # --- Tab 2: Pentagon & Risk ---
    with tab2:
        st.subheader("🕸️ Pentagon & Risk Analysis")
        cols_pentagon = [
            'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]', 
            'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]', 
            'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]', 
            'Skoring Pentagon Analisis [P4- Operasional]', 
            'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
        ]
        
        def clean_and_map(val):
            val_str = str(val).strip().lower()
            if any(x in val_str for x in ['rendah', 'low', '1']): return 1
            if any(x in val_str for x in ['cukup', 'medium', '2']): return 2
            if any(x in val_str for x in ['sedang', '3']): return 3
            if any(x in val_str for x in ['baik', 'high', '4']): return 4
            if any(x in val_str for x in ['sangat baik', 'excellent', '5']): return 5
            return 0

        for col in cols_pentagon:
            if col in df.columns: df[col] = df[col].apply(clean_and_map)
        
        avg_scores = df[cols_pentagon].mean().values
        categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
        fig_radar = go.Figure(go.Scatterpolar(r=avg_scores, theta=categories, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 5])), title="Rata-rata Skor Pentagon")
        st.plotly_chart(fig_radar, use_container_width=True)

        st.subheader("📈 Korelasi Finansial")
        # Bersihkan data untuk grafik
        df['Kerugian_Clean'] = pd.to_numeric(df['Estimasi Kerugian Finansial Atas Temuan Audit'], errors='coerce').fillna(0)
        
        # Gunakan kategori sebagai sumbu X agar tidak berantakan
        fig_bubble = px.scatter(df, 
                                x='Departemen Divisi/Area', 
                                y='Kerugian_Clean',
                                size='Kerugian_Clean', 
                                color='Departemen Divisi/Area',
                                hover_name='Detail Temuan Ketidaksesuaian', 
                                template="plotly_white",
                                title="Estimasi Kerugian per Departemen")
        st.plotly_chart(fig_bubble, use_container_width=True)

       # --- Tab 3: AI Analyst ---
       with tab3:
        st.subheader("🤖 AI Root Cause Analysis")
        user_api_key = st.text_input("Masukkan Google API Key:", type="password")
        
        if user_api_key:
            try:
                genai.configure(api_key=user_api_key)
                if "Detail Temuan Ketidaksesuaian" in df.columns:
                    selected = st.selectbox("Pilih Temuan untuk Dianalisis:", df["Detail Temuan Ketidaksesuaian"].dropna().unique())
                    if st.button("Generate Analisis AI"):
                        with st.spinner("AI sedang bekerja..."):
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            response = model.generate_content(f"Analisis akar masalah dan berikan rekomendasi perbaikan profesional untuk temuan: {selected}")
                            st.markdown("### Hasil Analisis AI:")
                            st.write(response.text)
