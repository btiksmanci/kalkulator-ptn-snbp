import pandas as pd
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN WEB
# ==========================================
st.set_page_config(
    page_title="Kalkulator Rasio Peluang PTN",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CUSTOM CSS (PRECISION & MODERN UI)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Reset & Base Styling */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #0F172A;
    }
    
    /* Batasi Lebar Maksimal Kontainer Utama agar Presisi & Rapi di Tengah */
    .block-container {
        max-width: 1000px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }
    
    /* Header & Branding Banner */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 2.25rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.75rem;
        box-shadow: 0 12px 28px -6px rgba(37, 99, 235, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2rem;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .main-header p {
        color: #DBEAFE !important;
        font-size: 0.98rem;
        font-weight: 400;
        margin: 0;
        line-height: 1.5;
    }

    /* Container Card Form Pencarian */
    .search-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }

    /* Badge Metadata */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .badge-info {
        display: inline-flex;
        align-items: center;
        background: #F1F5F9;
        color: #334155;
        padding: 0.35rem 0.85rem;
        border-radius: 99px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid #E2E8F0;
    }

    /* Grid Metric Cards Presisi */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 1.1rem 1rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.2s ease-in-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.08);
        border-color: #CBD5E1;
    }
    
    .stat-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    
    .stat-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }
    
    .stat-unit {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
    }

    /* Custom Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.28) !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.38) !important;
        transform: translateY(-1px);
    }

    /* Custom Alert/Recommendation Card Style */
    .alert-card {
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        margin-top: 1.25rem;
        margin-bottom: 1.5rem;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .alert-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 1.05rem;
        font-weight: 700;
    }
    .alert-danger {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        color: #991B1B;
    }
    .alert-warning {
        background-color: #FFF7ED;
        border-left: 5px solid #F97316;
        color: #9A3412;
    }
    .alert-info {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        color: #1E40AF;
    }
    .alert-success {
        background-color: #F0FDF4;
        border-left: 5px solid #22C55E;
        color: #166534;
    }

    /* Penyesuaian st.dataframe agar border lebih halus */
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD DATA DARI CSV
# ==========================================
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

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Gagal memuat data `MASTER_all_prodi.csv`. Pastikan file berada di direktori yang sama.\n\n*Error: {e}*")
    st.stop()

# ==========================================
# 4. BANNER HEADER UTAMA
# ==========================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Analisis Peluang & Rasio PTN</h1>
    <p>Portal kalkulasi keketatan persaingan jurusan berdasarkan data resmi Daya Tampung & Peminat.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. FORM PENCARIAN CLEAN CARD
# ==========================================
col_search1, col_search2 = st.columns(2, gap="medium")

with col_search1:
    list_ptn = sorted(df['NAMA_PTN'].unique())
    selected_ptn = st.selectbox(
        "🏫 Pilih Universitas / PTN Target", 
        list_ptn, 
        index=None, 
        placeholder="Cari atau pilih PTN..."
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
        placeholder="Cari atau pilih Jurusan...",
        disabled=(not selected_ptn)
    )

st.write("")
btn_hitung = st.button("📊 Analisis Peluang Kelulusan", use_container_width=True)
st.write("")

# ==========================================
# 6. LOGIKA MENAMPILKAN HASIL
# ==========================================
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.warning("⚠️ **Mohon lengkapi pilihan**: Pilih Universitas dan Program Studi terlebih dahulu.")
    else:
        target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

        kuota = target['DAYA_TAMPUNG_2026']
        peminat = target['PEMINAT_2025']
        peluang = target['PELUANG_PERSEN']
        rasio = target['RASIO_PERSAINGAN']
        
        peminat_formatted = f"{peminat:,}".replace(",", ".")

        # Header Hasil & Metadata Badge
        st.markdown(f"### 📌 {target['NAMA_PRODI']} ({target['JENJANG']})")
        st.markdown(f"""
        <div class="badge-container">
            <span class="badge-info">🏛️ {target['NAMA_PTN']}</span>
            <span class="badge-info">🔑 Kode: {target['KODE_PRODI']}</span>
            <span class="badge-info">🎨 Portofolio: {target['JENIS_PORTOFOLIO']}</span>
        </div>
        """, unsafe_allow_html=True)

        # Dashboard Metric Cards Presisi (4 Kolom Rapi)
        m1, m2, m3, m4 = st.columns(4, gap="small")
        
        with m1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📦 Daya Tampung</div>
                <div class="stat-value">{kuota} <span class="stat-unit">Kursi</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">👥 Peminat Lalu</div>
                <div class="stat-value">{peminat_formatted} <span class="stat-unit">Siswa</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📊 Peluang Lulus</div>
                <div class="stat-value" style="color: #2563EB;">{peluang}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">⚖️ Rasio Persaingan</div>
                <div class="stat-value" style="color: #D97706;">1 : {rasio}</div>
            </div>
            """, unsafe_allow_html=True)

        # Banner Rekomendasi & Strategi (Tampilan Card Elegan)
        if peminat == 0:
            st.markdown("""
            <div class="alert-card alert-info">
                <h4>ℹ️ Kategori: Jurusan Baru / Belum Ada Data Peminat</h4>
                Peluang relatif aman karena belum ada kompetisi tercatat di periode sebelumnya.
            </div>
            """, unsafe_allow_html=True)
        elif peluang < 5.0:
            st.markdown(f"""
            <div class="alert-card alert-danger">
                <h4>🔴 Kategori Persaingan: SANGAT KETAT (Super Favorit)</h4>
                Hanya <b>{peluang}%</b> dari total pendaftar yang diterima (Kamu harus menyisihkan <b>{rasio} orang</b> per kursi).<br>
                <b>Rekomendasi:</b> Cocok untuk <b>Pilihan 1</b> jika kamu memiliki nilai rapor/prestasi unggulan.
            </div>
            """, unsafe_allow_html=True)
        elif peluang <= 15.0:
            st.markdown(f"""
            <div class="alert-card alert-warning">
                <h4>🟠 Kategori Persaingan: KETAT / TINGGI</h4>
                Peluang diterima sebesar <b>{peluang}%</b> (Kamu harus menyisihkan sekitar <b>{rasio} orang</b> per kursi).<br>
                <b>Rekomendasi:</b> Merupakan jurusan favorit yang memerlukan analisis nilai matang.
            </div>
            """, unsafe_allow_html=True)
        elif peluang <= 30.0:
            st.markdown(f"""
            <div class="alert-card alert-info">
                <h4>🟡 Kategori Persaingan: SEDANG / MODERAT</h4>
                Peluang diterima sebesar <b>{peluang}%</b> dengan rasio persaingan <b>1 : {rasio}</b>.<br>
                <b>Rekomendasi:</b> Sangat ideal dijadikan <b>Pilihan 1</b> atau <b>Pilihan 2</b> yang rasional.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-card alert-success">
                <h4>🟢 Kategori Persaingan: PELUANG BESAR</h4>
                Peluang kelulusan tergolong tinggi sebesar <b>{peluang}%</b> (Persaingan <b>1 : {rasio}</b>).<br>
                <b>Rekomendasi:</b> Sangat ideal digunakan sebagai jurusan pengaman di <b>Pilihan 2</b>.
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Tabel Perbandingan Jurusan di PTN Sama
        st.subheader(f"💡 Perbandingan Jurusan Lain di {selected_ptn}")
        st.caption("Daftar urutan jurusan dari persentase kelulusan tertinggi hingga yang paling ketat.")

        alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)

        st.dataframe(
            alt_df[['KODE_PRODI', 'NAMA_PRODI', 'JENJANG', 'DAYA_TAMPUNG_2026', 'PEMINAT_2025', 'PELUANG_PERSEN', 'RASIO_PERSAINGAN']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "KODE_PRODI": "Kode",
                "NAMA_PRODI": "Program Studi",
                "JENJANG": "Jenjang",
                "DAYA_TAMPUNG_2026": st.column_config.NumberColumn("Kuota 2026", format="%d Kursi"),
                "PEMINAT_2025": st.column_config.NumberColumn("Peminat 2025", format="%d Pendaftar"),
                "PELUANG_PERSEN": st.column_config.NumberColumn("Peluang (%)", format="%.2f%%"),
                "RASIO_PERSAINGAN": st.column_config.NumberColumn("Rasio (1 : N)", format="1 : %d")
            }
        )
