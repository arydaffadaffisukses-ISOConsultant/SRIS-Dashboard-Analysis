with tab2:
    st.subheader("🕸️ Pentagon & Risk Analysis")
        
    # 1. Pentagon Analysis (Radar Chart)
    st.markdown("### Pentagon Analysis Radar")
    cols_pentagon = [
        'Skoring Pentagon Analisis [P1- Regulasi & Kepatuhan]',
        'Skoring Pentagon Analisis [P2- Finansial (Budget & KerugianFinansial)]',
        'Skoring Pentagon Analisis [P3- Integritas data & Keselarasan System]',
        'Skoring Pentagon Analisis [P4- Operasional]',
        'Skoring Pentagon Analisis [P5 Reputasi & Nama Baik]'
    ]
        
    # Pastikan data berupa angka (jika masih teks, kode ini mungkin perlu penyesuaian)
    avg_scores = df[cols_pentagon].mean().values
    categories = ['Regulasi', 'Finansial', 'Integritas', 'Operasional', 'Reputasi']
        
    import plotly.graph_objects as go
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
          r=avg_scores,
          theta=categories,
          fill='toself',
          line_color='#636EFA'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    st.plotly_chart(fig_radar, use_container_width=True)

    # 2. Implementation Risk Maturity
    st.markdown("### Implementation Risk Maturity")
    fig3 = px.bar(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', 
                  title='Tingkat Kematangan Risiko per Departemen',
                  color='Departemen Divisi/Area')
    st.plotly_chart(fig3, use_container_width=True)
        
    # 3. Hubungan Risiko & Kerugian
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
