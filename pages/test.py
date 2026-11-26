import hashlib
import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Akun & Riwayat Pencarian", page_icon="👤", layout="wide")


def hash_password(password: str) -> str:
    """Mengubah password teks menjadi hash SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validasi_password(password: str) -> tuple[bool, str]:
    """Memeriksa syarat password: min. 8 karakter, 1 angka, dan 1 simbol spesial."""
    if len(password) < 8:
        return False, "Password harus memiliki minimal 8 karakter."
    if not re.search(r"\d", password):
        return False, "Password harus mengandung minimal 1 angka (0-9)."
    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Password harus mengandung minimal 1 simbol spesial (misalnya !@#$%^&*)."
    return True, ""


# Inisialisasi data akun sementara di session_state
if "akun_pengguna" not in st.session_state:
    st.session_state["akun_pengguna"] = {
        "neo_demo": {
            "tanggal_lahir": "2006-05-12",
            "password_hash": hash_password("Neo@1234"),
        },
        "glen_demo": {
            "tanggal_lahir": "2006-08-21",
            "password_hash": hash_password("Glen#1234"),
        },
    }

if "user_aktif" not in st.session_state:
    st.session_state["user_aktif"] = None

# Inisialisasi data riwayat pencarian sementara (hanya nama akun, nama game, dan genre)
if "riwayat_pencarian" not in st.session_state:
    st.session_state["riwayat_pencarian"] = [
        {"Nama Akun": "neo_demo", "Nama Game": "Valorant", "Genre": "Shooter"},
        {"Nama Akun": "glen_demo", "Nama Game": "Genshin Impact", "Genre": "RPG"},
    ]

st.title("👤 Register, Login & Riwayat Pencarian")

if st.session_state["user_aktif"]:
    col_status, col_logout = st.columns([4, 1])
    col_status.success(f"Sedang login sebagai: **{st.session_state['user_aktif']}**")
    if col_logout.button("Logout", use_container_width=True):
        st.session_state["user_aktif"] = None
        st.rerun()
else:
    st.info("Status saat ini: **Belum Login** (akun demo tersedia: `neo_demo` / `Neo@1234` atau `glen_demo` / `Glen#1234`).")

tab_login, tab_register, tab_riwayat = st.tabs(["Login", "Register", "Riwayat Pencarian"])

# --- 1. HALAMAN LOGIN ---
with tab_login:
    st.subheader("Masuk ke Akun")
    with st.form("form_login"):
        username_login = st.text_input("Nama Akun")
        password_login = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")

        if submit_login:
            akun_input = username_login.strip()
            if not akun_input or not password_login:
                st.error("Nama akun dan password wajib diisi.")
            elif akun_input not in st.session_state["akun_pengguna"]:
                st.error(f"Nama akun '{akun_input}' tidak terdaftar. Silakan periksa kembali atau daftar akun baru.")
            elif st.session_state["akun_pengguna"][akun_input]["password_hash"] != hash_password(password_login):
                st.error("Password yang dimasukkan salah. Silakan coba lagi.")
            else:
                st.session_state["user_aktif"] = akun_input
                st.success(f"Login berhasil! Selamat datang, **{akun_input}**.")
                st.rerun()

# --- 2. HALAMAN REGISTER ---
with tab_register:
    st.subheader("Buat Akun Baru")
    with st.form("form_register"):
        username_reg = st.text_input("Nama Akun Unik")
        tgl_lahir = st.date_input("Tanggal Ulang Tahun")
        pass_reg = st.text_input("Password (min. 8 karakter, 1 angka, 1 simbol)", type="password")
        pass_konf = st.text_input("Konfirmasi Password", type="password")
        submit_reg = st.form_submit_button("Daftar")

        if submit_reg:
            akun_baru = username_reg.strip()
            valid_pass, pesan_pass = validasi_password(pass_reg)

            if not akun_baru:
                st.error("Nama akun tidak boleh kosong.")
            elif " " in akun_baru:
                st.error("Nama akun tidak boleh mengandung spasi.")
            elif akun_baru in st.session_state["akun_pengguna"]:
                st.error(f"Nama akun '{akun_baru}' sudah digunakan. Pilih nama akun lain.")
            elif not valid_pass:
                st.error(f"Password tidak memenuhi ketentuan: {pesan_pass}")
            elif pass_reg != pass_konf:
                st.error("Konfirmasi password tidak cocok dengan password yang dimasukkan.")
            else:
                st.session_state["akun_pengguna"][akun_baru] = {
                    "tanggal_lahir": str(tgl_lahir),
                    "password_hash": hash_password(pass_reg),
                }
                st.success(f"Registrasi berhasil untuk akun **{akun_baru}**! Silakan masuk melalui tab Login.")

# --- 3. TAMPILAN RIWAYAT PENCARIAN ---
with tab_riwayat:
    st.subheader("Riwayat Pencarian Game")

    df_riwayat = pd.DataFrame(st.session_state["riwayat_pencarian"])

    if st.session_state["user_aktif"]:
        df_tampil = df_riwayat[df_riwayat["Nama Akun"] == st.session_state["user_aktif"]]
    else:
        st.caption("Login terlebih dahulu untuk melihat riwayat khusus akunmu. Menampilkan seluruh riwayat sementara:")
        df_tampil = df_riwayat

    if df_tampil.empty:
        st.warning("Belum ada riwayat pencarian untuk akun ini.")
    else:
        st.dataframe(
            df_tampil[["Nama Akun", "Nama Game", "Genre"]],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.markdown("**Simulasi Tambah Riwayat Pencarian (Preview)**")
    with st.form("form_tambah_riwayat"):
        col1, col2 = st.columns(2)
        nama_game_cari = col1.text_input("Nama Game yang Dicari", placeholder="Contoh: Overwatch 2")
        genre_cari = col2.selectbox(
            "Genre Game",
            ["Shooter", "MMORPG", "MOBA", "Strategy", "RPG", "Sports", "Racing", "Fighting"],
        )
        tambah_riwayat = st.form_submit_button("Simpan ke Riwayat")

        if tambah_riwayat:
            if not nama_game_cari.strip():
                st.warning("Masukkan nama game terlebih dahulu.")
            else:
                pemilik = st.session_state["user_aktif"] or "Guest"
                st.session_state["riwayat_pencarian"].append(
                    {
                        "Nama Akun": pemilik,
                        "Nama Game": nama_game_cari.strip(),
                        "Genre": genre_cari,
                    }
                )
                st.rerun()