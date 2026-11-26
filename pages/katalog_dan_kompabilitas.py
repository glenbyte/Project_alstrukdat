import streamlit as st

st.title("Katalog Game & Cek Kompatibilitas")

if "spek_pc" not in st.session_state:
    st.warning("Silakan isi spesifikasi perangkat di halaman utama terlebih dahulu.")
    if st.button("Kembali ke Beranda"):
        st.switch_page("main.py")
else:
    spek = st.session_state["spek_pc"]
    st.write("Perangkat aktif:", spek["nama"])
    st.write("OS:", spek["os"], "| CPU:", spek["cpu"])
    st.write("RAM:", spek["ram"], "GB | VRAM:", spek["vram"], "GB | Storage:", spek["storage"], "GB")