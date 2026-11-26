import io
import json
from fpdf import FPDF
import pandas as pd
import streamlit as st

st.divider()
st.subheader("Wishlist & Ekspor")

if "wishlist_game" not in st.session_state:
    st.session_state["wishlist_game"] = [
        {"judul": "The Elder Scrolls V: Skyrim", "genre": "RPG", "tahun": 2011, "ram": 2, "storage": "6"},
        {"judul": "League of Legends", "genre": "MOBA", "tahun": 2009, "ram": 8, "storage": "25-30"},
    ]

df_wish = st.data_editor(
    pd.DataFrame(st.session_state["wishlist_game"]),
    num_rows="dynamic",
    use_container_width=True,
)

df_bersih = df_wish.dropna(how="all").copy()
if "judul" in df_bersih.columns:
    df_bersih = df_bersih[df_bersih["judul"].notna() & (df_bersih["judul"].astype(str).str.strip() != "")]

data_bersih = df_bersih.to_dict(orient="records")
st.session_state["wishlist_game"] = data_bersih

buf_xlsx = io.BytesIO()
with pd.ExcelWriter(buf_xlsx, engine="openpyxl") as w:
    df_bersih.to_excel(w, index=False)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", "B", 13)
pdf.cell(0, 10, "Daftar Wishlist Game", ln=True)
pdf.set_font("Helvetica", "B", 10)
pdf.cell(0, 8, "Judul | Genre | Tahun | RAM | Storage", ln=True)
pdf.set_font("Helvetica", size=10)

for _, r in df_bersih.iterrows():
    judul = "-" if pd.isna(r.get("judul")) else str(r.get("judul"))
    genre = "-" if pd.isna(r.get("genre")) else str(r.get("genre"))
    tahun = "-" if pd.isna(r.get("tahun")) else str(int(r.get("tahun")))
    ram = "-" if pd.isna(r.get("ram")) else f"{r.get('ram')}GB"
    storage = "-" if pd.isna(r.get("storage")) else f"{r.get('storage')}GB"
    baris = f"{judul} | {genre} | {tahun} | {ram} | {storage}"
    pdf.cell(0, 8, baris.encode("latin-1", errors="replace").decode("latin-1"), ln=True)

c1, c2, c3 = st.columns(3)
c1.download_button("Excel", buf_xlsx.getvalue(), "wishlist.xlsx", use_container_width=True)
c2.download_button("PDF", bytes(pdf.output()), "wishlist.pdf", use_container_width=True)
c3.download_button("JSON", json.dumps(data_bersih, indent=2, ensure_ascii=False), "wishlist.json", use_container_width=True)