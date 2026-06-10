import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("🛡️ SRIS Dashboard Analytics")

# Load data
uploaded_file = st.file_uploader("Upload CSV Audit", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Bersihkan nama kolom dari spasi berlebih
    df.columns = [c.strip() for c in df.columns]

    st.session_state["df"] = df
    st.success(f"Data termuat: {len(df)} baris.")

if "df" in st.session_state:
    df = st.session_state["df"]

    # Fungsi Kalkulasi Risiko
    def hitung_uang(x):
        x = str(x)
        if 'Tinggi' in x: return 55000000
        if 'Sedang' in x: return 25000000
        return 5000000

    df['Uang_Hitung'] = df['Estimasi Kerugian Perusahaan akibat audit Ini'].apply(hitung_uang)

    # Chatbot UI
    user_input = st.chat_input("Tanya statistik departemen (ketik 'pareto'):")

    if user_input:
        with st.chat_message("user"): st.write(user_input)

        # Analisis Data
        analisis_dept = df.groupby('Departemen Divisi/Area')['Uang_Hitung'].sum().sort_values(ascending=False).reset_index()
        analisis_dept['Kumulatif_Persen'] = (analisis_dept['Uang_Hitung'].cumsum() / analisis_dept['Uang_Hitung'].sum()) * 100

        with st.chat_message("assistant"):
            st.write("Berikut adalah visualisasi statistik risiko per departemen:")

            # Tab Visualisasi
            tab1, tab2 = st.tabs(["📊 Pareto", "📈 Bar Horizontal"])

            with tab1:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=analisis_dept['Departemen Divisi/Area'], y=analisis_dept['Uang_Hitung'], name="Kerugian (Rp)"))
                fig.add_trace(go.Scatter(x=analisis_dept['Departemen Divisi/Area'], y=analisis_dept['Kumulatif_Persen'], name="Kumulatif (%)", yaxis="y2", mode="lines+markers"))
                fig.update_layout(yaxis2=dict(overlaying="y", side="right", range=[0, 110]))
                st.plotly_chart(fig)

            with tab2:
                fig_h = go.Figure(go.Bar(x=analisis_dept['Uang_Hitung'], y=analisis_dept['Departemen Divisi/Area'], orientation='h'))
                st.plotly_chart(fig_h)
