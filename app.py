import pandas as pd
import streamlit as st

# Setup Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Rasio Peluang PTN",
    page_icon="🎓",
    layout="wide"
)

# Load Data dari CSV
@st.cache_data
def load_data():
    df = pd.read_csv('MASTER_all_prodi.csv', sep=';', on_bad_lines='skip')
    df['DAYA_TAMPUNG_2026'] = pd.to_numeric(df['DAYA_TAMPUNG_2026'], errors='coerce').fillna(0).astype(int)
    df['PEMINAT_2025'] = pd.to_numeric(df['PEMINAT_2025'], errors='coerce').fillna(0).astype(int)
    
    # Hitung Persentase Peluang & Rasio Persaingan Dibulatkan
    df['PELUANG_PERSEN'] = df.apply(
        lambda r: round((r['DAYA_TAMPUNG_2026'] / r['PEMINAT_2025']) * 100, 2) if r['PEMINAT_2025'] > 0 else 0.0, 
        axis=1
    )
    df['RASIO_PERSAINGAN'] = df.apply(
        lambda r: int(round(r['PEMINAT_2025'] / r['DAYA_TAMPUNG_2026'])) if r['DAYA_TAMPUNG_2026'] > 0 else 0,
        axis=1
    )
    return df

df = load_data()

# Header Utama
st.title("🎓 Kalkulator Rasio Persaingan & Peluang PTN")
st.markdown("Cek persentase peluang lulus dan rasio ketatnya persaingan jurusan targetmu berdasarkan data resmi Daya Tampung & Peminat.")
st.divider()

# --- FORM PENCARIAN DI HALAMAN UTAMA (Bukan Sidebar) ---
st.subheader("🔍 Cari & Pilih Jurusan Target")

col_search1, col_search2 = st.columns(2)

with col_search1:
    list_ptn = sorted(df['NAMA_PTN'].unique())
    selected_ptn = st.selectbox("1. Pilih Universitas / PTN", list_ptn)

# Filter prodi berdasarkan PTN pilihan
filtered_prodi_df = df[df['NAMA_PTN'] == selected_ptn]
list_prodi = sorted(filtered_prodi_df['NAMA_PRODI'].unique())

with col_search2:
    selected_prodi = st.selectbox("2. Pilih Program Studi", list_prodi)

st.divider()

# Ambil data spesifik jurusan terpilih
target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

kuota = target['DAYA_TAMPUNG_2026']
peminat = target['PEMINAT_2025']
peluang = target['PELUANG_PERSEN']
rasio = target['RASIO_PERSAINGAN']

# --- TAMPILAN ANALISIS KAMPUS & JURUSAN ---
st.subheader(f"📌 {target['NAMA_PRODI']} ({target['JENJANG']})")
st.caption(f"🏛️ **{target['NAMA_PTN']}** | Kode Prodi: `{target['KODE_PRODI']}` | Portofolio: `{target['JENIS_PORTOFOLIO']}`")

col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Daya Tampung (Kuota)", f"{kuota} Kursi")
col2.metric("👥 Peminat Tahun Lalu", f"{peminat} Pendaftar")
col3.metric("📊 Persentase Peluang", f"{peluang}%")
col4.metric("⚖️ Rasio Persaingan", f"1 : {rasio} Orang")

st.write("")

# --- ANALISIS TINGKAT KESULITAN / KEKETATAN ---
if peminat == 0:
    st.info("ℹ️ **Jurusan Baru / Belum Ada Data Peminat**: Peluang relatif aman karena belum ada kompetisi tercatat.")
elif peluang < 5.0:
    st.error(f"### 🔴 Tingkat Persaingan: SANGAT KETAT (Super Favorit)\n"
             f"Hanya **{peluang}%** dari total pendaftar yang diterima (Kamu harus menyisihkan **{rasio} orang** untuk mendapatkan 1 kursi). "
             f"Direkomendasikan sebagai **Pilihan 1** dengan strategi nilai yang sangat kuat.")
elif peluang <= 15.0:
    st.warning(f"### 🟠 Tingkat Persaingan: KETAT / TINGGI\n"
               f"Peluang diterima **{peluang}%** (Kamu harus menyisihkan sekitar **{rasio} orang** per kursi). "
               f"Merupakan jurusan favorit yang butuh persiapan matang.")
elif peluang <= 30.0:
    st.info(f"### 🟡 Tingkat Persaingan: SEDANG\n"
            f"Peluang diterima **{peluang}%** (Rasio persaingan **1 : {rasio}** orang). "
            f"Sangat baik dijadikan **Pilihan 1** atau **Pilihan 2** yang aman.")
else:
    st.success(f"### 🟢 Tingkat Persaingan: MODERAT / PELUANG BESAR\n"
               f"Peluang kelulusan tergolong tinggi sebesar **{peluang}%** (Persaingan **1 : {rasio}** orang). "
               f"Sangat direkomendasikan untuk menunjang aman di **Pilihan 2**.")

st.divider()

# --- REKOMENDASI JURUSAN SEJENIS / PTN SAMA ---
st.subheader(f"💡 Perbandingan Jurusan Lain di {selected_ptn}")
st.markdown("Berikut urutan jurusan dari yang paling longgar (Peluang Terbesar) hingga paling ketat di kampus ini:")

# Tabel Seluruh Prodi di Kampus Terpilih
alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)

st.dataframe(
    alt_df[['KODE_PRODI', 'NAMA_PRODI', 'JENJANG', 'DAYA_TAMPUNG_2026', 'PEMINAT_2025', 'PELUANG_PERSEN', 'RASIO_PERSAINGAN']],
    use_container_width=True,
    hide_index=True,
    column_config={
        "KODE_PRODI": "Kode",
        "NAMA_PRODI": "Program Studi",
        "JENJANG": "Jenjang",
        "DAYA_TAMPUNG_2026": "Kuota 2026",
        "PEMINAT_2025": "Peminat 2025",
        "PELUANG_PERSEN": "Peluang Lulus (%)",
        "RASIO_PERSAINGAN": "Persaingan (1 : N)"
    }
)
