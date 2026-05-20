import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Konfigurasi Halaman (Mobile Friendly)
st.set_page_config(page_title="Cari Toko", page_icon="🔍", layout="centered")

st.title("Pencarian Database Toko 🏪")
st.markdown("Ketik nama toko untuk melihat apakah sales sudah pernah berkunjung.")

# 2. Setup Koneksi ke Google Sheets
# Ganti URL dengan link spreadsheet Database_Master Anda
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/ID_SPREADSHEET_ANDA/edit"

# Menggunakan cache agar aplikasi tidak loading ulang data dari awal setiap kali ngetik
@st.cache_data(ttl=600) # Data di-refresh setiap 10 menit (600 detik)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Asumsi: Kolom A adalah Nama Toko, Kolom B adalah Alamat
    df = conn.read(spreadsheet=SPREADSHEET_URL, usecols=[0, 1])
    # Bersihkan baris yang kosong
    df = df.dropna(how="all") 
    return df

try:
    df = load_data()
    # Pastikan nama kolom sesuai dengan baris pertama di Google Sheets Anda
    nama_kolom_toko = df.columns[0]  
    nama_kolom_alamat = df.columns[1]

    # 3. Buat Search Bar
    search_query = st.text_input("🔍 Masukkan Nama Toko:", placeholder="Contoh: 3 JAYA")

    # 4. Logika Pencarian
    if search_query:
        # Filter dataframe berdasarkan input (case-insensitive)
        mask = df[nama_kolom_toko].astype(str).str.contains(search_query, case=False, na=False)
        result = df[mask]

        if not result.empty:
            st.success(f"Ditemukan {len(result)} toko yang mirip!")
            
            # Tampilan hasil bergaya "Card" agar enak dibaca di HP
            for index, row in result.iterrows():
                with st.container():
                    st.markdown(f"### 🏬 {row[nama_kolom_toko]}")
                    st.markdown(f"**📍 Alamat:** {row[nama_kolom_alamat]}")
                    st.divider() # Garis pemisah antar hasil
        else:
            st.warning("Toko tidak ditemukan. Ini adalah prospek baru! 🚀")

except Exception as e:
    st.error(f"Terjadi kesalahan saat mengambil data: {e}")
