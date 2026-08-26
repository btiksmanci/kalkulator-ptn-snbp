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
# 2. CUSTOM CSS (DARK MODE COMPATIBLE & NO CUTOFF)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* FIX 1: HEADER TERPOTONG - Sesuaikan padding atas */
    .block-container {
        max-width: 1000px !important;
        padding-top: 3.5rem !important;
        padding-bottom: 4rem !important;
    }
    
    /* Header Banner */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 2.25rem 2rem;
        border-radius: 20px;
        color: white !important;
        margin-bottom: 1.75rem;
        box-shadow: 0 12px 28px -6px rgba(37, 99, 235, 0.25);
    }
    
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2rem;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }
    
    .main-header p {
        color: #DBEAFE !important;
        font-size: 0.98rem;
        margin: 0;
    }

    /* FIX 2: DARK MODE COMPATIBILITY - Gunakan background adaptif transparan */
    .stat-card {
        background-color: rgba(125, 125, 125, 0.08) !important;
        border: 1px solid rgba(125, 125, 125, 0.2) !important;
        padding: 1.1rem 1rem;
        border-radius: 14px;
        text-align: center;
        transition: all 0.2s ease-in-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-label {
        font-size: 0.78rem;
        font-weight: 700;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    
    .stat-value {
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .badge-info {
        display: inline-flex;
        align-items: center;
        background-color: rgba(125, 125, 125, 0.12);
        border: 1px solid rgba(125, 125, 125, 0.2);
        padding: 0.35rem 0.85rem;
        border-radius: 99px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    /* Custom Alert Card Adaptif Dark Mode */
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
    .alert-danger { background-color: rgba(239, 68, 68, 0.15); border-left: 5px solid #EF4444; }
    .alert-warning { background-color: rgba(249, 115, 22, 0.15); border-left: 5px solid #F97316; }
    .alert-info { background-color: rgba(59, 130, 246, 0.15); border-left: 5px solid #3B82F6; }
    .alert-success { background-color: rgba(34, 197, 94, 0.15); border-left: 5px solid #22C55E; }

    /* Custom Button */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.28) !important;
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
    st.error(f"⚠️ Gagal memuat data `MASTER_all_prodi.csv`. Error: {e}")
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
# 5. FORM PENCARIAN
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
# 6. LOGIKA HASIL & KARTU ADAPTIF
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

        # Title & Badges
        st.markdown(f"### 📌 {target['NAMA_PRODI']} ({target['JENJANG']})")
        st.markdown(f"""
        <div style="margin-bottom: 1.2rem;">
            <span class="badge-info">🏛️ {target['NAMA_PTN']}</span>
            <span class="badge-info">🔑 Kode: {target['KODE_PRODI']}</span>
            <span class="badge-info">🎨 Portofolio: {target['JENIS_PORTOFOLIO']}</span>
        </div>
        """, unsafe_allow_html=True)

        # Kartu Statistik Adaptif Dark Mode
        m1, m2, m3, m4 = st.columns(4, gap="small")
        
        with m1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📦 Daya Tampung</div>
                <div class="stat-value">{kuota} <span style="font-size: 0.85rem; opacity: 0.7;">Kursi</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">👥 Peminat Lalu</div>
                <div class="stat-value">{peminat_formatted} <span style="font-size: 0.85rem; opacity: 0.7;">Siswa</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📊 Peluang Lulus</div>
                <div class="stat-value" style="color: #3B82F6;">{peluang}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">⚖️ Rasio Persaingan</div>
                <div class="stat-value" style="color: #F59E0B;">1 : {rasio}</div>
            </div>
            """, unsafe_allow_html=True)

        # Alert Banner Adaptif
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
                Hanya <b>{peluang}%</b> pendaftar yang diterima (Menyisihkan <b>{rasio} orang</b> per kursi).<br>
                <b>Rekomendasi:</b> Cocok untuk <b>Pilihan 1</b> dengan nilai rapot/prestasi tinggi.
            </div>
            """, unsafe_allow_html=True)
        elif peluang <= 15.0:
            st.markdown(f"""
            <div class="alert-card alert-warning">
                <h4>🟠 Kategori Persaingan: KETAT / TINGGI</h4>
                Peluang diterima sebesar <b>{peluang}%</b> (Menyisihkan <b>{rasio} orang</b> per kursi).<br>
                <b>Rekomendasi:</b> Jurusan favorit, perhitungkan nilai secara matang.
            </div>
            """, unsafe_allow_html=True)
        elif peluang <= 30.0:
            st.markdown(f"""
            <div class="alert-card alert-info">
                <h4>🟡 Kategori Persaingan: SEDANG / MODERAT</h4>
                Peluang diterima sebesar <b>{peluang}%</b> (Rasio <b>1 : {rasio}</b>).<br>
                <b>Rekomendasi:</b> Ideal dijadikan <b>Pilihan 1</b> atau <b>Pilihan 2</b>.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-card alert-success">
                <h4>🟢 Kategori Persaingan: PELUANG BESAR</h4>
                Peluang kelulusan tinggi sebesar <b>{peluang}%</b> (Persaingan <b>1 : {rasio}</b>).<br>
                <b>Rekomendasi:</b> Ideal sebagai pengaman di <b>Pilihan 2</b>.
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # FIX 3: TABEL STABIL - Sort eksplisit dan reset_index()
        st.subheader(f"💡 Perbandingan Jurusan Lain di {selected_ptn}")
        st.caption("Daftar urutan jurusan dari persentase kelulusan tertinggi hingga yang paling ketat.")

        alt_df = (
            filtered_prodi_df
            .sort_values(by='PELUANG_PERSEN', ascending=False)
            .reset_index(drop=True)
        )

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
