import pandas as pd
import streamlit as st

# Setup Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Peluang PTN",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INJEKSI CUSTOM CSS UNTUK DESAIN MODERN & CLEAN ---
st.markdown("""
<style>
    /* Mengubah Font & Main Container */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Menyembunyikan Sidebar & Header Streamlit Bawaan */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Styling Tombol Utama */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Custom Card Metric Styling */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-unit {
        font-size: 13px;
        color: #94a3b8;
        font-weight: 400;
    }

    /* Container Hasil */
    .result-box {
        background: #f8fafc;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load Data dari CSV
@st.cache_data
def load_data():
    df = pd.read_csv('MASTER_all_prodi.csv', sep=';', on_bad_lines='skip')
    df['DAYA_TAMPUNG_2026'] = pd.to_numeric(df['DAYA_TAMPUNG_2026'], errors='coerce').fillna(0).astype(int)
    df['PEMINAT_2025'] = pd.to_numeric(df['PEMINAT_2025'], errors='coerce').fillna(0).astype(int)
    
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

# --- HEADER APP ---
st.markdown("<h1 style='text-align: center; color: #1e293b; font-weight: 700; font-size: 28px;'>🎓 Kalkulator Peluang & Persaingan PTN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-bottom: 24px;'>Analisis ketatnya persaingan jurusan impianmu secara real-time</p>", unsafe_allow_html=True)

# --- FORM PENCARIAN ---
with st.container():
    col_search1, col_search2 = st.columns(2)

    with col_search1:
        list_ptn = sorted(df['NAMA_PTN'].unique())
        selected_ptn = st.selectbox(
            "🏛️ Pilih Universitas / PTN", 
            list_ptn, 
            index=None, 
            placeholder="Ketik atau pilih kampus..."
        )

    if selected_ptn:
        filtered_prodi_df = df[df['NAMA_PTN'] == selected_ptn]
        list_prodi = sorted(filtered_prodi_df['NAMA_PRODI'].unique())
    else:
        filtered_prodi_df = pd.DataFrame()
        list_prodi = []

    with col_search2:
        selected_prodi = st.selectbox(
            "📚 Pilih Program Studi", 
            list_prodi, 
            index=None, 
            placeholder="Ketik atau pilih jurusan...",
            disabled=(not selected_ptn)
        )

    st.write("")
    btn_hitung = st.button("🔍 Hitung Peluang Kelulusan", use_container_width=True)

# --- LOGIKA TAMPILAN HASIL ---
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.warning("⚠️ Silakan pilih Universitas dan Program Studi terlebih dahulu.")
    else:
        target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

        kuota = target['DAYA_TAMPUNG_2026']
        peminat = target['PEMINAT_2025']
        peluang = target['PELUANG_PERSEN']
        rasio = target['RASIO_PERSAINGAN']

        st.markdown("<hr style='margin: 24px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
        
        # Judul Jurusan
        st.markdown(f"""
        <div style='background: white; padding: 20px; border-radius: 16px; border-left: 5px solid #2563eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 20px;'>
            <h2 style='margin:0; font-size: 20px; color: #0f172a;'>📌 {target['NAMA_PRODI']} ({target['JENJANG']})</h2>
            <p style='margin:4px 0 0 0; color: #64748b; font-size: 13px;'>🏛️ <b>{target['NAMA_PTN']}</b> &nbsp;|&nbsp; Kode: <code>{target['KODE_PRODI']}</code> &nbsp;|&nbsp; Portofolio: <b>{target['JENIS_PORTOFOLIO']}</b></p>
        </div>
        """, unsafe_allow_html=True)

        # GRID METRIK (Tampil 2x2 di Mobile, 4 Kolom di Desktop)
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>📦 Daya Tampung</div>
                <div class='metric-value'>{kuota} <span class='metric-unit'>Kursi</span></div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>👥 Peminat (2025)</div>
                <div class='metric-value'>{peminat} <span class='metric-unit'>Siswa</span></div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>📊 Peluang Diterima</div>
                <div class='metric-value' style='color: #2563eb;'>{peluang}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>⚖️ Rasio Persaingan</div>
                <div class='metric-value'>1 : {rasio} <span class='metric-unit'>Orang</span></div>
            </div>
            """, unsafe_allow_html=True)

        # BADGE STATUS KEKETATAN
        if peminat == 0:
            st.info("ℹ️ **Jurusan Baru / Belum Ada Data Peminat**: Peluang relatif aman karena belum ada kompetisi tercatat.")
        elif peluang < 5.0:
            st.error(f"🔴 **Tingkat Persaingan: SANGAT KETAT** — Hanya **{peluang}%** pendaftar diterima. Kamu harus menyisihkan sekitar **{rasio} orang** per kursi.")
        elif peluang <= 15.0:
            st.warning(f"🟠 **Tingkat Persaingan: TINGGI** — Peluang diterima **{peluang}%** (Persaingan 1 banding **{rasio} orang**). Butuh persiapan matang.")
        elif peluang <= 30.0:
            st.info(f"🟡 **Tingkat Persaingan: SEDANG** — Peluang diterima **{peluang}%** (Persaingan 1 banding **{rasio} orang**). Baik untuk Pilihan 1 atau 2.")
        else:
            st.success(f"🟢 **Tingkat Persaingan: MODERAT / PELUANG BESAR** — Peluang tinggi sebesar **{peluang}%** (Persaingan 1 banding **{rasio} orang**). Sangat aman.")

        # TABEL PERBANDINGAN JURUSAN SEJENIS
        st.write("")
        st.markdown(f"<h4 style='color: #1e293b; font-size: 16px; font-weight: 700;'>💡 Perbandingan Jurusan Lain di {selected_ptn}</h4>", unsafe_allow_html=True)

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
