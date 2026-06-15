import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(layout="wide")
st.title("SRIS Dashboard Analysis")

# 2. Upload Data
uploaded_file = st.file_uploader("Upload file CSV/Excel data temuan:", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Membaca data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Membersihkan spasi pada kolom
    df.columns = df.columns.str.strip()

    # 3. Membuat Tab
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

    with tab1:
        st.subheader("Analisis Temuan")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.subheader("Estimasi Kerugian")
            
            # Kita hitung dulu jumlah temuan per kategori untuk setiap departemen
            # Ini akan membuat grafik jauh lebih kaya warna
            fig2 = px.histogram(
                df, 
                x='Departemen Divisi/Area', 
                color='Estimasi Kerugian Finansial Atas Temuan Audit',
                barmode='group', # Mengelompokkan batang agar berdampingan
                title='Komposisi Kerugian per Departemen',
                color_discrete_sequence=px.colors.qualitative.Set2 # Pilihan palet warna yang menarik
            )
            
            fig2.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig2, use_container_width=True)

     with tab2:
         st.subheader("🕸️ Pentagon & Risk Analysis")
        
         # --- Bagian 1: Pentagon Analysis (Radar Chart) ---
         st.markdown("### Pentagon Analysis Radar")
         # Mengambil rata-rata nilai skoring pentagon dari data (asumsi kolom sudah angka)
         # Jika kolom Bapak namanya berbeda, silakan sesuaikan
         cols_pentagon = [
             'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
             'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]',
             'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]',
             'Skoring Pentagon Analisis [P4- Operasional]',
             'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
         ]
        
         # Menghitung rata-rata skor per aspek
         avg_scores = df[cols_pentagon].mean().values
         categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
         import plotly.graph_objects as go
         fig_radar = go.Figure()
         fig_radar.add_trace(go.Scatterpolar(
               r=avg_scores,
               theta=categories,
               fill='toself',
               line_color='#636EFA',
              marker=dict(size=8)
         ))
         fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
         st.plotly_chart(fig_radar, use_container_width=True)

         # --- Bagian 2: Implementation Risk Maturity ---
         st.markdown("### Implementation Risk Maturity")
         fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', 
                       title='Tingkat Kematangan Risiko per Departemen',
                       color='Departemen Divisi/Area')
         st.plotly_chart(fig3, use_container_width=True)
        
         # --- Bagian 3: Hubungan Risiko & Kerugian ---
         st.markdown("### Hubungan Risiko & Kerugian")
         fig4 = px.scatter(
            df, 
            x='Implementation Risk Maturity', 
            y='Estimasi Kerugian Finansial Atas Temuan Audit', 
            color='Departemen Divisi/Area',
            size='Implementation Risk Maturity',
            hover_data=['Detail Temuan Ketidaksesuaian'],
            title='Bubble Analysis: Risiko vs Kerugian',
            opacity=0.7,
            template="plotly_white"
        )
        st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.subheader("AI Root Cause Analysis & CAPA")
        user_api_key = st.text_input("Masukkan API Key:", type="password")
        temuan_col = "Detail Temuan Ketidaksesuaian"
        
        if temuan_col in df.columns:
            selected_temuan = st.selectbox("Pilih Temuan:", df[temuan_col].dropna().unique())
            
            if st.button("Generate Analisis AI"):
                if not user_api_key:
                    st.warning("Masukkan API Key terlebih dahulu!")
                else:
                    try:
                        # Langkah 1: Konfigurasi
                        genai.configure(api_key=user_api_key)
                        
                        # Langkah 2: Deteksi model yang tersedia
                        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
                        
                        if not available_models:
                            st.error("API Key tidak menemukan model yang tersedia. Pastikan kunci sudah benar dan aktif.")
                        else:
                            st.write("Menggunakan model:", available_models[0])
                            model = genai.GenerativeModel(available_models[0])
                            
                            # Langkah 3: Generate
                            response = model.generate_content(f"Analisis akar masalah dan rencana CAPA untuk: {selected_temuan}")
                            st.markdown(response.text)
                            
                    except Exception as e:
                        st.error(f"Error AI: {e}")

else:
    st.info("Silakan upload file CSV atau Excel Bapak di atas untuk memulai.")
