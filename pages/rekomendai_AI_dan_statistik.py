import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

API_URL = "https://www.freetogame.com/api/games"

st.set_page_config(page_title="AI, Statistik & Laporan - Preview", page_icon="📊", layout="wide")


@st.cache_data(ttl=300, show_spinner="Memuat data statistik FreeToGame...")
def load_stats_data() -> pd.DataFrame:
    resp = requests.get(API_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame()


st.title("📊 Rekomendasi AI, Statistik & Laporan (Tampilan Awal)")
st.caption("Kerangka tampilan awal untuk bagian AI, visualisasi Matplotlib, wishlist, dan ekspor laporan")

# 1. Bagian Rekomendasi AI (Preview)
st.subheader("1. Rekomendasi & Penjelasan AI (Tampilan Awal)")
pref_genre = st.text_input("Preferensi / kebutuhan game", placeholder="Contoh: Game shooter gratis untuk PC yang seru dimainkan mabar")
if st.button("Minta Rekomendasi AI (Preview)"):
    st.info(
        "Ini masih **tampilan awal (placeholder)**. Pada tahap integrasi Gemini API, input "
        f"'{pref_genre or 'preferensi kosong'}' beserta kandidat game dari FreeToGame API akan dikirim ke model Gemini."
    )

st.divider()

# 2. Bagian Statistik & Visualisasi (Preview dari data API)
st.subheader("2. Statistik Katalog FreeToGame (Tampilan Awal)")
try:
    df_api = load_stats_data()
except requests.RequestException as exc:
    st.warning(f"API belum dapat diakses ({exc}). Menampilkan data contoh lokal untuk preview grafik.")
    df_api = pd.DataFrame(
        {
            "genre": ["Shooter", "MMORPG", "MOBA", "Shooter", "RPG", "Sports"],
            "release_date": ["2021-05-01", "2020-03-10", "2019-11-20", "2022-08-15", "2021-01-12", "2023-06-01"],
        }
    )

if not df_api.empty and "genre" in df_api.columns:
    col_kiri, col_kanan = st.columns(2)

    with col_kiri:
        st.markdown("**Top 8 Genre Terbanyak (Bar Chart)**")
        top_genre = df_api["genre"].value_counts().head(8)
        fig1, ax1 = plt.subplots(figsize=(6, 3.8))
        ax1.bar(top_genre.index, top_genre.values, color="#4F8BF9")
        ax1.set_ylabel("Jumlah Game")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    with col_kanan:
        st.markdown("**Jumlah Game per Tahun Rilis (Line Chart)**")
        tahun = pd.to_datetime(df_api["release_date"], errors="coerce").dt.year.dropna().astype(int)
        if not tahun.empty:
            per_tahun = tahun.value_counts().sort_index().tail(10)
            fig2, ax2 = plt.subplots(figsize=(6, 3.8))
            ax2.plot(per_tahun.index.astype(str), per_tahun.values, marker="o", color="#2EC4B6")
            ax2.set_ylabel("Jumlah Game")
            plt.xticks(rotation=30, ha="right")
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)
        else:
            st.caption("Data tahun rilis tidak tersedia.")

st.divider()

# 3. Bagian Wishlist & Ekspor (Preview)
st.subheader("3. Wishlist & Ekspor Laporan (Tampilan Awal)")
wishlist_awal = pd.DataFrame(
    [
        {"judul": "Contoh Game 1", "genre": "Shooter", "platform": "PC (Windows)", "catatan": "Preview"},
        {"judul": "Contoh Game 2", "genre": "MMORPG", "platform": "PC (Windows)", "catatan": "Preview"},
    ]
)
st.data_editor(wishlist_awal, num_rows="dynamic", use_container_width=True)

e1, e2, e3 = st.columns(3)
e1.button("Export Excel (.xlsx) - Preview", disabled=True, use_container_width=True)
e2.button("Export PDF - Preview", disabled=True, use_container_width=True)
e3.button("Export JSON - Preview", disabled=True, use_container_width=True)