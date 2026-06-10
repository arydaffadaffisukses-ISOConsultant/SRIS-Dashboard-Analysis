import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.title("SRIS Engine Data Advisor")

uploaded_file = st.file_uploader("Upload Dokumen (PDF, Excel, atau CSV)", type=["pdf", "xlsx", "csv"])

if uploaded_file is not None:
    # 1. Jika File adalah PDF
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages])
        st.write("PDF berhasil dibaca. Masukkan pertanyaan Bapak:")
        query = st.text_input("Pertanyaan:")
        if query:
            if query.lower() in text.lower():
                st.success("Informasi ditemukan!")
                st.write(text[text.lower().find(query.lower()):text.lower().find(query.lower())+500] + "...")
            else:
                st.warning("Kata kunci tidak ditemukan.")

    # 2. Jika File adalah Excel
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        st.write("Data Excel berhasil dimuat:")
        st.dataframe(df)
        st.write("Statistik Data:", df.describe())

    # 3. Jika File adalah CSV
    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.write("Data CSV berhasil dimuat:")
        st.dataframe(df)
        st.write("Statistik Data:", df.describe())


   
    
       
