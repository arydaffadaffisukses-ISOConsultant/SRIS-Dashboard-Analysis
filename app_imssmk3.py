import streamlit as st

# 1. Page Config WAJIB paling atas
st.set_page_config(page_title="SRIS Pro", layout="wide")

# 2. Banner menggunakan Header Standar Streamlit (Paling pasti muncul)
st.title("🛡️ Security Risk Intelligence System (SRIS)")
st.subheader("Executive Audit & Risk Management Dashboard")
st.markdown("---") # Garis pembatas profesional

# 3. Sidebar Filter
st.sidebar.header("🔍 Filter Dashboard")
# ... (sisa kode filter dan grafik Bapak)
