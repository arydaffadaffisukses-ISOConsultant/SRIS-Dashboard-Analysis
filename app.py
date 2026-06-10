if menu == "📊 Ringkasan Eksekutif & Status Temuan":
        st.subheader(f"📊 Metrik Utama Hasil Audit - Mode: {sris_mode}")
        total_temuan = len(df_filtered)
        if kolom_status in df_filtered.columns:
            open_nc = len(df_filtered[df_filtered[kolom_status].astype(str).str.contains('Open|On Progress', case=False, na=False)])
            closed_nc = total_temuan - open_nc
        else:
            open_nc = total_temuan; closed_nc = 0
            
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Total Temuan Kasus", value=f"{total_temuan} Temuan")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Open / Process", value=f"{open_nc} Kasus", delta="Risk Exposure", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric(label="Status Closed (Selesai)", value=f"{closed_nc} Kasus", delta="Mitigated")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # =========================================================
        # LOGIKA OTOMATISASI GRAFIK SECARA DINAMIS (SMART FILTERING)
        # =========================================================
        
        # Cek apakah kolom taksonomi cyber security tersedia dan memiliki data resmi
        has_cyber_cols = (kolom_cyber in df_filtered.columns and not df_filtered[kolom_cyber].isna().all()) and \
                         (kolom_pilar in df_filtered.columns and not df_filtered[kolom_pilar].isna().all()) and \
                         (kolom_ops in df_filtered.columns and not df_filtered[kolom_ops].isna().all())

        if has_cyber_cols:
            # TAMPILKAN 4 GRAFIK CYBER SECURITY JIKA KOLOMNYA ADA (ISO 27001)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### 🏢 Distribusi Temuan Berdasarkan Departemen")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#0a4b78', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1); plt.close(fig1)
            with col_g2:
                st.write("##### 🛡️ Profil Temuan Berdasarkan Cybersecurity Concepts")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_cyber].value_counts().plot(kind='bar', color='#00a8cc', edgecolor='black', ax=ax2)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig2); plt.close(fig2)

            st.markdown("<br>", unsafe_allow_html=True)
            col_g3, col_g4 = st.columns(2)
            with col_g3:
                st.write("##### 🔑 Distribusi Pillars Information Security (CIA)")
                fig3, ax3 = plt.subplots(figsize=(6, 3.5))
                pilar_series = df_filtered[kolom_pilar].dropna().astype(str).str.split(',\s*').explode()
                pilar_series.value_counts().plot(kind='bar', color='#4b86b4', edgecolor='black', ax=ax3)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig3); plt.close(fig3)
            with col_g4:
                st.write("##### ⚙️ Distribusi Berdasarkan Operational Capabilities")
                fig4, ax4 = plt.subplots(figsize=(6, 3.5))
                df_filtered[kolom_ops].value_counts().plot(kind='bar', color='#2a9d8f', edgecolor='black', ax=ax4)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig4); plt.close(fig4)

        else:
            # KONDISI JIKA DATA ADALAH SMK3 / ISO LAINNYA (GRAFIK CYBER DISEMBUNYIKAN)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write("##### 🏢 Distribusi Temuan Pelanggaran per Departemen/Area")
                fig1, ax1 = plt.subplots(figsize=(6, 3.5))
                if kolom_dept in df_filtered.columns:
                    df_filtered[kolom_dept].value_counts().sort_values(ascending=True).plot(kind='barh', color='#1e5631', ax=ax1)
                plt.tight_layout()
                st.pyplot(fig1); plt.close(fig1)
            with col_g2:
                st.write("##### ⚠️ Breakdown Volume Berdasarkan Standar / Kriteria Regulasi")
                fig2, ax2 = plt.subplots(figsize=(6, 3.5))
                
                # Gunakan kolom kriteria pemenuhan hukum/standar yang ada
                kolom_kriteria_aktif = 'Nomor Kriteria' if 'Nomor Kriteria' in df_filtered.columns else \
                                      ('Nomor Kriteria ' if 'Nomor Kriteria ' in df_filtered.columns else kolom_standar)
                
                if kolom_kriteria_aktif in df_filtered.columns:
                    df_filtered[kolom_kriteria_aktif].value_counts().head(10).plot(kind='bar', color='#4c9a2a', edgecolor='black', ax=ax2)
                    plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig2); plt.close(fig2)
