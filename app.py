import streamlit as st
from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.title("SMK3 Clause Advisor")
st.write("Unggah dokumen SMK3 Bapak untuk mulai bertanya.")

uploaded_file = st.file_uploader("Upload PDF SMK3 PP 50 2012", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    
    query = st.text_input("Apa yang ingin Bapak tanyakan tentang klausul SMK3?")
    
    if query:
        # Pencarian sederhana berdasarkan kata kunci
        if query.lower() in text.lower():
            st.success("Informasi ditemukan!")
            # Menampilkan potongan teks yang relevan
            start_index = text.lower().find(query.lower())
            st.write(text[start_index:start_index+500] + "...")
        else:
            st.warning("Mohon maaf, kata kunci tidak ditemukan dalam dokumen.")

st.sidebar.info("Modul Minggu ke-1: Membaca standar secara otomatis.")

   
    
       
