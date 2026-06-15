# Pastikan tidak ada spasi di awal baris untuk baris-baris berikut:

tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ringkasan", "🕸️ Pentagon & Risk", "🤖 AI Analyst"])

with tab1:
    st.subheader("Analisis Temuan")
    df.columns = df.columns.str.strip()
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(df, names='Departemen Divisi/Area', title='Distribusi Temuan')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(df, x='Departemen Divisi/Area', y='Estimasi Kerugian Finansial Atas Temuan Audit', title='Estimasi Kerugian')
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Risk & Maturity")
    fig3 = px.box(df, x='Departemen Divisi/Area', y='Implementation Risk Maturity', title='Tingkat Kematangan Risiko')
    st.plotly_chart(fig3, use_container_width=True)
    fig4 = px.scatter(df, x='Implementation Risk Maturity', y='Estimasi Kerugian Finansial Atas Temuan Audit', color='Departemen Divisi/Area', title='Hubungan Risiko & Kerugian')
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("AI Root Cause Analysis & CAPA")
    # Bagian AI tetap di sini
