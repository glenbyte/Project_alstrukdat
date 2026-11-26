<<<<<<< HEAD
import pandas as pd
import requests
import streamlit as st

FREETOGAME_GAMES_URL = "https://www.freetogame.com/api/games"
FREETOGAME_GAME_DETAIL_URL = "https://www.freetogame.com/api/game"

st.set_page_config(
    page_title="Free To Play Game Database - Preview",
    page_icon="🎮",
    layout="wide",
)
=======
git checkout fitur
import streamlit as st
import json
>>>>>>> 7354d86db9072dc07d797c81d5d2abbd3b4797da

if "spek_pc" not in st.session_state:
    st.session_state["spek_pc"] = {
        "nama": "Laptop Saya",
        "os": "Windows 10 / 11",
        "cpu": "Mid-Range (i5 / Ryzen 5)",
        "ram": 8,
        "vram": 4,
        "storage": 60
    }

<<<<<<< HEAD
@st.cache_data(ttl=300, show_spinner="Mengambil data dari FreeToGame API...")
def ambil_data_freetogame(platform: str | None = None, category: str | None = None) -> list[dict]:
    """Mengambil daftar game dari FreeToGame Public API (GET /api/games)."""
    params = {}
    if platform and platform != "All":
        params["platform"] = platform.lower()
    if category and category != "All":
        params["category"] = category.lower()

    response = requests.get(FREETOGAME_GAMES_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else []


def ambil_detail_game_freetogame(game_id: int) -> dict:
    """Mengambil detail satu game dari FreeToGame API (GET /api/game?id=...)."""
    response = requests.get(FREETOGAME_GAME_DETAIL_URL, params={"id": game_id}, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {}


# Inisialisasi state sementara untuk preview UI
if "user_aktif" not in st.session_state:
    st.session_state["user_aktif"] = "Guest (Mode Preview)"
if "last_genre" not in st.session_state:
    st.session_state["last_genre"] = "Shooter"

st.title("🎮 Free To Play Game Database")
st.caption("Tampilan Awal (Preview UI) • Sumber Data: FreeToGame API (https://www.freetogame.com/api-doc)")

st.info(
    f"Status sesi sementara: **{st.session_state['user_aktif']}** | "
    f"Genre terakhir dicari (dummy): **{st.session_state['last_genre']}**. "
    "Gunakan menu halaman di sidebar kiri untuk melihat rancangan halaman lainnya."
)

try:
    games = ambil_data_freetogame()
    df_games = pd.DataFrame(games)
except requests.RequestException as exc:
    st.error(f"Gagal terhubung ke FreeToGame API: {exc}")
    df_games = pd.DataFrame()

# Ringkasan metrik awal
col1, col2, col3, col4 = st.columns(4)
if not df_games.empty:
    col1.metric("Total Game (API)", f"{len(df_games):,}")
    col2.metric("Jumlah Genre Unik", f"{df_games['genre'].nunique()}" if "genre" in df_games else "-")
    col3.metric("Platform Tersedia", f"{df_games['platform'].nunique()}" if "platform" in df_games else "-")
    col4.metric("Genre Serupa (Preview)", st.session_state["last_genre"])
else:
    col1.metric("Total Game (API)", "0")
    col2.metric("Jumlah Genre Unik", "-")
    col3.metric("Platform Tersedia", "-")
    col4.metric("Genre Serupa (Preview)", st.session_state["last_genre"])

st.divider()

# Preview bagian "Game Serupa Berdasarkan Genre Terakhir Dicari" di Beranda
st.subheader(f"Game Serupa — Genre: {st.session_state['last_genre']} (Tampilan Awal)")

genre_pilihan = st.selectbox(
    "Ubah genre preview di beranda (sementara):",
    options=["Shooter", "MMORPG", "MOBA", "Strategy", "RPG", "Sports", "Racing", "Fighting"],
    index=0,
)
st.session_state["last_genre"] = genre_pilihan

if not df_games.empty and "genre" in df_games.columns:
    serupa = df_games[df_games["genre"].astype(str).str.lower() == genre_pilihan.lower()].head(6)
    if serupa.empty:
        st.warning(f"Tidak ada game dengan genre '{genre_pilihan}' pada cuplikan data saat ini.")
    else:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(serupa.iterrows()):
            with cols[idx % 3]:
                if row.get("thumbnail"):
                    st.image(row["thumbnail"], use_container_width=True)
                st.markdown(f"**{row.get('title', 'Tanpa Judul')}**")
                st.caption(f"{row.get('genre', '-')} • {row.get('platform', '-')} • Rilis: {row.get('release_date', '-')}")
                st.write(row.get("short_description", ""))
=======
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
>>>>>>> 7354d86db9072dc07d797c81d5d2abbd3b4797da
