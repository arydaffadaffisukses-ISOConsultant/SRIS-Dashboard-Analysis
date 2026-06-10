# ==========================================
# 3. CORE PROCESSING ENGINE & DATA CLEANING
# ==========================================
if df is not None:
    df.columns = [col.strip() for col in df.columns]
    
    kolom_dept = 'Departemen Divisi/Area'
    kolom_status = 'Posisi Status NC'
    kolom_cyber = 'Cybersecurity Concepts'
    kolom_annex = 'Kategori Kontrol ( Annex A ) ISO 27001'
    kolom_auditor = 'Nama Auditor'
    kolom_standar = 'STANDARD'
    kolom_temuan = 'Detail Temuan Ketidaksesuaian'
    kolom_no_annex = 'No Annex dan No Control ( ISO 27001)'
    
    # Standardisasi Divisi MR
    if kolom_dept in df.columns:
        df[kolom_dept] = df[kolom_dept].astype(str).str.strip()
        mapping_mr = {
            'Management Representatif /MR': 'Management Representative (MR)',
            'MR Management Representatif': 'Management Representative (MR)',
            'MR': 'Management Representative (MR)'
        }
        df[kolom_dept] = df[kolom_dept].replace(mapping_mr)
    
    # Ekstraksi Skor Pentagon
    pilar_skor = {
        'P1_Regulasi': 'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
        'P2_Finansial': 'Skoring Pentagon Analisis [P2- Finansial & Kerugian]',
        'P3_Integritas': 'Skoring Pentagon Analisis [P3- Integritas data & System]',
        'P4_Operasional': 'Skoring Pentagon Analisis [P4- Operational]',
        'P5_Reputasi': 'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
    }
    for key, nama_kolom in pilar_skor.items():
        if nama_kolom in df.columns:
            df[key] = df[nama_kolom].astype(str).str.extract(r'(\d+)')[0].astype(float)
            df[key] = df[key].fillna(0.0)
        else:
            df[key] = 0.0

    st.sidebar.success("🔌 Status Data: Terhubung")
    st.sidebar.info(f"ℹ️ {status_pembacaan}")
    
    # Panel Kontrol Utama
    st.sidebar.header("🎛️ Panel Kontrol")
    if kolom_dept in df.columns:
        list_dept = ["Semua Departemen"] + sorted(list(df[kolom_dept].dropna().unique()))
        selected_dept = st.sidebar.selectbox("Pilih Departemen/Divisi:", list_dept)
        if selected_dept != "Semua Departemen":
            df_filtered = df[df[kolom_dept] == selected_dept]
        else:
            df_filtered = df.copy()
    else:
        df_filtered = df.copy()

    # ==========================================
    # DISINI TEMPATNYA! MENYIMPAN KE SESSION STATE
    # ==========================================
    st.session_state['df_filtered_saved'] = df_filtered
    st.session_state['df'] = df
        
    menu = st.sidebar.radio("Pilih Navigasi Dashboard:", [
        "📊 Ringkasan Eksekutif & Status Temuan",
        "🕸️ Analisis Radar Pentagon (SRIS Model)",
        "🔍 Audit Deep Dive & Manajemen Annex A",
        "🤖 SRIS Chatbot AI (Tanya Jawab Audit)"
    ])
