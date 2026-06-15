with tab1:
        st.subheader("Analisis Temuan")
        # Membersihkan spasi di nama kolom
        df.columns = df.columns.str.strip()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Grafik 1: Distribusi berdasarkan Departemen
            fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan per Departemen')
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            # Grafik 2: Kerugian (Gunakan kolom ke-15)
            fig2 = px.bar(df, x='Departemen Divisi/Area', y='Estimasi Kerugian Finansial Atas Temuan Audit', title='Estimasi Kerugian per Departemen')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Risk & Maturity")
        # Grafik 3: Risk Maturity (Kolom ke-8)
        fig3 = px.box(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', title='Tingkat Kematangan Risiko')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Grafik 4: Pengendalian Resiko (Kolom ke-17)
        fig4 = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', color='Departemen Divisi/Area', title='Hubungan Risiko & Kerugian')
        st.plotly_chart(fig4, use_container_width=True)
