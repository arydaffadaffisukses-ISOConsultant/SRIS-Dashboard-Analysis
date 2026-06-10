elif menu == "🤖 SRIS Chatbot AI (Tanya Jawab Audit)":
        st.subheader("🤖 SRIS Executive AI Consultant")
        st.info("Asisten AI siap membantu Anda menganalisis temuan audit secara instan berbasis data & aspek Keamanan Informasi.")
        
        # Pengecekan API Key dari Streamlit Secrets
        if "GEMINI_API_KEY" in st.secrets:
            api_key_input = st.secrets["GEMINI_API_KEY"]
        else:
            api_key_input = st.text_input("🔑 Masukkan Google Gemini API Key Anda:", type="password")
        
        if api_key_input:
            try:
                from google import genai
                client = genai.Client(api_key=api_key_input)
                
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                for chat in st.session_state.chat_history:
                    if chat["role"] == "user":
                        st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {chat['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b> {chat['text']}</div>", unsafe_allow_html=True)
                
                user_query = st.chat_input("Ketik pertanyaan atau analisis temuan audit Bapak di sini...")
                
                if user_query:
                    st.markdown(f"<div class='chat-bubble-user'>🧑‍💼 <b>Anda:</b> {user_query}</div>", unsafe_allow_html=True)
                    
                    kolom_ks = [kolom_dept, kolom_temuan, kolom_status, kolom_annex]
                    ringkasan_data = df_filtered[[c for c in kolom_ks if c in df_filtered.columns]].to_string(index=False)
                    
                    # SYSTEM PROMPT DIOPTIMALKAN UNTUK STRATEGIC CYBERSECURITY & CIA TRIAD
                    system_instruction = f"""
                    Anda adalah SRIS Executive AI Consultant, seorang ahli strategi tata kelola keamanan informasi senior, auditor ISO 27001:2022, dan ahli SMK3.
                    Tugas Anda adalah menganalisis pertanyaan pengguna berbasis data audit berikut:
                    
                    --- DATA AUDIT AKTIF ---
                    {ringkasan_data}
                    --- AKHIR DATA ---
                    
                    Setiap memberikan jawaban atau analisis tata kelola/temuan, Anda WAJIB menyertakan blok taksonomi keamanan informasi di bagian paling atas jawaban Anda dengan format baku JSON atau Teks Terstruktur berikut:
                    
                    [TAG_ANALISIS]
                    - Cybersecurity Concept: [Pilih salah satu atau lebih: Identify / Protect / Detect / Respond / Recover]
                    - Pilar Security (CIA): [Pilih salah satu atau lebih: Confidentiality / Integrity / Availability]
                    - Operational Capability: [Pilih yang relevan: Governance & Risk, Asset Management, Human Security, Physical Security, Technology Protection, Incident Management, Business Continuity]
                    [AKHIR_TAG]
                    
                    Aturan Tambahan:
                    1. Berikan penjelasan taktis dalam Bahasa Indonesia profesional tingkat tinggi (Executive Level).
                    2. Hubungkan temuan atau aturan klausul dengan dampak risiko operasional/bisnis secara nyata.
                    """
                    
                    with st.spinner("Mengonfirmasi ke AI Cyber Security Engine..."):
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_query,
                            config={'system_instruction': system_instruction}
                        )
                        bot_response = response.text
                    
                    # LOGIKA PARSING STRATEGIS UNTUK MENAMPILKAN METRIK SECARA VISUAL DI STREAMLIT
                    # Memisahkan Tag Analisis agar bisa ditampilkan dalam box visual premium
                    if "[TAG_ANALISIS]" in bot_response:
                        try:
                            parts = bot_response.split("[AKHIR_TAG]")
                            tag_part = parts[0].replace("[TAG_ANALISIS]", "").strip()
                            isi_jawaban = parts[1].strip()
                            
                            # Tampilkan Box Metrik Atas
                            st.markdown("##### 🛡️ Klasifikasi Risiko & Kapabilitas Keamanan:")
                            lines = tag_part.split("\n")
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                val_cyber = next((line.split(":")[1].strip() for line in lines if "Cybersecurity Concept" in line), "N/A")
                                st.metric("Cybersecurity Concept", val_cyber)
                            with c2:
                                val_cia = next((line.split(":")[1].strip() for line in lines if "Pilar Security (CIA)" in line), "N/A")
                                st.metric("Pilar Security (CIA)", val_cia)
                            with c3:
                                val_op = next((line.split(":")[1].strip() for line in lines if "Operational Capability" in line), "N/A")
                                st.metric("Operational Capability", val_op)
                                
                            st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b><br><br>{isi_jawaban}</div>", unsafe_allow_html=True)
                        except:
                            st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b><br><br>{bot_response}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>SRIS AI:</b><br><br>{bot_response}</div>", unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append({"role": "user", "text": user_query})
                    st.session_state.chat_history.append({"role": "bot", "text": bot_response})
                    
            except Exception as error_ai:
                st.error(f"Gagal menghubungkan ke AI Engine: {error_ai}")
        else:
            st.warning("⚠️ Silakan masukkan Gemini API Key Anda terlebih dahulu untuk mengaktifkan fungsi Chatbot AI.")
    
