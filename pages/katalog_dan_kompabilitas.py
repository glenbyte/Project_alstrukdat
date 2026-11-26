import pandas as pd
import requests
import streamlit as st

API_URL = "https://www.freetogame.com/api/games"

st.set_page_config(page_title="Katalog Game & Filter - Preview", page_icon="🗂️", layout="wide")


@st.cache_data(ttl=300, show_spinner="Memuat katalog FreeToGame...")
def load_katalog() -> list[dict]:
    resp = requests.get(API_URL, timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    return payload if isinstance(payload, list) else []


st.title("🗂️ Katalog Game & Filter (Tampilan Awal)")
st.caption("Data langsung dari FreeToGame API • Logika filter & sorting masih tahap tampilan awal")

try:
    raw_games = load_katalog()
    df = pd.DataFrame(raw_games)
except requests.RequestException as exc:
    st.error(f"Gagal memuat data dari FreeToGame API: {exc}")
    st.stop()

if df.empty:
    st.warning("Data katalog kosong.")
    st.stop()

# Sidebar filter sesuai rancangan awal
with st.sidebar:
    st.header("Filter & Urutkan (Preview)")
    keyword = st.text_input("Cari judul game", placeholder="Contoh: combat, war, shooter...")

    genre_list = ["Semua"] + sorted(df["genre"].dropna().unique().tolist())
    selected_genre = st.selectbox("Genre", genre_list)

    platform_list = ["Semua"] + sorted(df["platform"].dropna().unique().tolist())
    selected_platform = st.selectbox("Platform", platform_list)

    tahun_series = pd.to_datetime(df["release_date"], errors="coerce").dt.year.dropna().astype(int)
    if not tahun_series.empty:
        min_th, max_th = int(tahun_series.min()), int(tahun_series.max())
        selected_year_range = st.slider("Rentang Tahun Rilis", min_value=min_th, max_value=max_th, value=(min_th, max_th))
    else:
        selected_year_range = None

    sort_algo = st.selectbox("Algoritma Sorting (Placeholder)", ["Merge Sort", "Quick Sort"])
    sort_by = st.selectbox("Urutkan Berdasarkan", ["title", "release_date", "genre"])
    sort_order = st.radio("Urutan", ["Ascending", "Descending"], horizontal=True)

# Filter sederhana untuk preview
filtered = df.copy()
if keyword.strip():
    filtered = filtered[filtered["title"].astype(str).str.contains(keyword.strip(), case=False, na=False)]
if selected_genre != "Semua":
    filtered = filtered[filtered["genre"] == selected_genre]
if selected_platform != "Semua":
    filtered = filtered[filtered["platform"] == selected_platform]
if selected_year_range is not None:
    th_col = pd.to_datetime(filtered["release_date"], errors="coerce").dt.year
    filtered = filtered[
        th_col.isna() | ((th_col >= selected_year_range[0]) & (th_col <= selected_year_range[1]))
    ]

ascending = sort_order == "Ascending"
if sort_by in filtered.columns:
    filtered = filtered.sort_values(by=sort_by, ascending=ascending, na_position="last")

st.info(f"Menampilkan **{len(filtered)}** dari **{len(df)}** game • Mode sorting terpilih: **{sort_algo}**")

kolom_tampil = [c for c in ["id", "title", "genre", "platform", "release_date", "publisher", "developer"] if c in filtered.columns]
st.dataframe(filtered[kolom_tampil], use_container_width=True, hide_index=True)