import streamlit as st
import json

if "spek_pc" not in st.session_state:
    st.session_state["spek_pc"] = {
        "nama": "Laptop Saya",
        "os": "Windows 10 / 11",
        "cpu": "Mid-Range (i5 / Ryzen 5)",
        "ram": 8,
        "vram": 4,
        "storage": 60
    }

st.title("Game Database")
st.write("Masukkan spesifikasi PC atau laptop kamu di bawah ini.")

file_json = st.file_uploader("Upload profil spek (.json) jika sudah ada", type=["json"])
if file_json is not None:
    if st.button("Muat File JSON"):
        data = json.load(file_json)
        st.session_state["spek_pc"] = data
        st.success("Profil dari file JSON berhasil dimuat.")

spek = st.session_state["spek_pc"]

nama = st.text_input("Nama Perangkat", value=spek["nama"])
os_pilihan = st.selectbox("Sistem Operasi", ["Windows 10 / 11", "Windows 7 / 8", "Linux", "macOS"])
cpu_pilihan = st.selectbox("Prosesor (CPU)", ["Entry-Level (i3 / Ryzen 3)", "Mid-Range (i5 / Ryzen 5)", "High-End (i7 / Ryzen 7)"])
ram = st.slider("RAM (GB)", 2, 64, int(spek["ram"]), step=2)
vram = st.number_input("VRAM GPU (GB)", 0, 24, int(spek["vram"]), step=1)
storage = st.number_input("Sisa Storage (GB)", 5, 2000, int(spek["storage"]), step=5)

if st.button("Simpan Spesifikasi"):
    if nama == "":
        st.error("Nama perangkat tidak boleh kosong.")
    else:
        st.session_state["spek_pc"] = {
            "nama": nama,
            "os": os_pilihan,
            "cpu": cpu_pilihan,
            "ram": ram,
            "vram": vram,
            "storage": storage
        }
        st.success("Spesifikasi berhasil disimpan.")

spek_aktif = st.session_state["spek_pc"]
st.subheader("Ringkasan Spek Aktif")
st.write("Perangkat:", spek_aktif["nama"])
st.write("OS:", spek_aktif["os"])
st.write("CPU:", spek_aktif["cpu"])
st.metric("RAM", f"{spek_aktif['ram']} GB")
st.metric("VRAM GPU", f"{spek_aktif['vram']} GB")
st.metric("Sisa Storage", f"{spek_aktif['storage']} GB")

hasil_json = json.dumps(spek_aktif, indent=2)
st.download_button("Download Profil JSON", hasil_json, file_name="profil_spek.json", mime="application/json")

if st.button("Lanjut ke Katalog Game"):
    st.switch_page("pages/Katalog_dan_Kompabilitas.py")