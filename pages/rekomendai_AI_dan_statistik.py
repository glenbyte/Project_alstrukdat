import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Statistik & Visualisasi Game")

if "data_game" not in st.session_state:
    st.session_state["data_game"] = [
        {"judul": "Valorant", "genre": "Shooter", "tahun": 2020, "ram": 4, "storage": 30},
        {"judul": "The Elder Scrolls V: Skyrim", "genre": "RPG", "tahun": 2011, "ram": 2, "storage": 6},
        {"judul": "Evil Within", "genre": "Horror", "tahun": 2017, "ram": 8, "storage": 40},
        {"judul": "Genshin Impact", "genre": "RPG", "tahun": 2020, "ram": 8, "storage": 130},
        {"judul": "League of Legends", "genre": "MOBA", "tahun": 2009, "ram": 8, "storage": 28}
    ]

df = pd.DataFrame(st.session_state["data_game"])

colA, colB = st.columns(2)

with colA:
    st.subheader("Jumlah Game per Genre")
    jumlah_genre = df["genre"].value_counts()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    warna_batang = ["#4F8BF9", "#2EC4B6", "#FF9F1C", "#E76F51"]
    bars = ax1.bar(jumlah_genre.index, jumlah_genre.values, color=warna_batang[:len(jumlah_genre)], width=0.55, edgecolor="none")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Genre")
    ax1.set_ylabel("Jumlah Game")
    for bar in bars:
        tinggi = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, tinggi + 0.08, f"{int(tinggi)}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig1)

with colB:
    st.subheader("Sebaran Ukuran Storage (GB)")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    counts, bins, patches = ax2.hist(df["storage"], bins=4, color="#7B61FF", edgecolor="white", linewidth=1.2)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", linestyle="--", alpha=0.35)
    ax2.set_axisbelow(True)
    ax2.set_xlabel("Storage (GB)")
    ax2.set_ylabel("Jumlah Game")
    plt.tight_layout()
    st.pyplot(fig2)

st.subheader("Rata-rata Kebutuhan RAM per Tahun Rilis")
tren_ram = df.groupby("tahun")["ram"].mean().sort_index()
fig3, ax3 = plt.subplots(figsize=(10, 3.8))
ax3.plot(tren_ram.index.astype(str), tren_ram.values, marker="o", markersize=7, linewidth=2.4, color="#00B4D8")
ax3.fill_between(tren_ram.index.astype(str), tren_ram.values, color="#00B4D8", alpha=0.12)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.grid(True, linestyle="--", alpha=0.35)
ax3.set_xlabel("Tahun Rilis")
ax3.set_ylabel("Rata-rata RAM (GB)")
for x_val, y_val in zip(tren_ram.index.astype(str), tren_ram.values):
    ax3.text(x_val, y_val + 0.25, f"{y_val:.1f} GB", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
st.pyplot(fig3)