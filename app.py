import pandas as pd
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="PTNMatch — Analisis Peluang SNBP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. DESIGN SYSTEM & CSS modern UI
# ==========================================
STYLING_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Reset & Base Styling */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1E293B !important;
    }

    /* Sembunyikan Header bawaan Streamlit */
    #MainMenu, footer, header, [data-testid="stHeader"] { 
        display: none !important; 
    }

    /* Container Margin */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 900px !important;
    }

    /* Top Navigation / Brand Banner */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-logo {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    .brand-logo span { color: #3B82F6; }
    .nav-badge {
        background: #EFF6FF;
        color: #2563EB;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 99px;
        border: 1px solid #BFDBFE;
    }

    /* Hero Section */
    .hero-box {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        line-height: 1.25;
        margin-bottom: 0.75rem;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #64748B;
        max-width: 540px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Form Container Card */
    .form-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.04);
        margin-bottom: 2rem;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        height: 50px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
    }

    /* Main Target Result Box */
    .target-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }
    .target-header {
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .target-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0F172A;
        margin: 4px 0 16px 0;
    }
    .chance-number {
        font-size: 3.8rem;
        font-weight: 800;
        color: #2563EB;
        line-height: 1;
        margin-bottom: 12px;
    }
    
    /* Status Badges */
    .status-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.3px;
    }
    .status-ketat { background: #FEF2F2; color: #DC2626; border: 1px solid #FCA5A5; }
    .status-sedang { background: #FFFBEB; color: #D97706; border: 1px solid #FCD34D; }
    .status-longgar { background: #F0FDF4; color: #16A34A; border: 1px solid #86EFAC; }

    /* Key Statistics Cards */
    .grid-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .stat-item {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .stat-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
    }
    .stat-val {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }

    /* Analysis / Insight Box */
    .insight-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* Custom Responsive Table */
    .table-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        overflow-x: auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    table.clean-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
        text-align: left;
    }
    table.clean-table th {
        background-color: #F8FAFC;
        color: #475569;
        font-weight: 700;
        padding: 14px 16px;
        border-bottom: 1px solid #E2E8F0;
    }
    table.clean-table td {
        padding: 14px 16px;
        border-bottom: 1px solid #F1F5F9;
        color: #0F172A;
    }
    table.clean-table tr:last-child td {
        border-bottom: none;
    }
    table.clean-table tr:hover {
        background-color: #F8FAFC;
    }
</style>
"""
st.markdown(STYLING_CSS, unsafe_allow_html=True)

# ==========================================
# 3. KONEKSI & OLAHI DATA CSV
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('MASTER_all_prodi.csv', sep=';', on_bad_lines='skip')
    df['DAYA_TAMPUNG_2026'] = pd.to_numeric(df['DAYA_TAMPUNG_2026'], errors='coerce').fillna(0).astype(int)
    df['PEMINAT_2025'] = pd.to_numeric(df['PEMINAT_2025'], errors='coerce').fillna(0).astype(int)
    
    # Kalkulasi Peluang %
    df['PELUANG_PERSEN'] = df.apply(
        lambda r: round((r['DAYA_TAMPUNG_2026'] / r['PEMINAT_2025']) * 100, 2) if r['PEMINAT_2025'] > 0 else 0.0, 
        axis=1
    )
    # Kalkulasi Rasio (1 : N)
    df['RASIO_PERSAINGAN'] = df.apply(
        lambda r: int(round(r['PEMINAT_2025'] / r['DAYA_TAMPUNG_2026'])) if r['DAYA_TAMPUNG_2026'] > 0 else 0,
        axis=1
    )
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Gagal memuat file `MASTER_all_prodi.csv`. Pastikan file berada di direktori yang sama.")
    st.stop()

# ==========================================
# 4. TOP BAR & HERO SECTION
# ==========================================
st.markdown("""
<div class="top-nav">
    <div class="brand-logo">🎓 PTN<span>Match</span></div>
    <div class="nav-badge">SNBP 2026</div>
</div>
<div class="hero-box">
    <h1 class="hero-title">Berapa besar peluang kelulusanmu?</h1>
    <p class="hero-subtitle">Analisis rasio persaingan dan keketatan jurusan impian berdasarkan data daya tampung resmi.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. INPUT PENCARIAN (CARD CONTAINER)
# ==========================================
st.markdown('<div class="form-card">', unsafe_allow_html=True)
c1, c2 = st.columns(2, gap="medium")

with c1:
    list_ptn = sorted(df['NAMA_PTN'].unique())
    selected_ptn = st.selectbox(
        "🏫 Universitas (PTN)", 
        list_ptn, 
        index=None, 
        placeholder="Cari Kampus..."
    )

if selected_ptn:
    filtered_prodi_df = df[df['NAMA_PTN'] == selected_ptn]
    list_prodi = sorted(filtered_prodi_df['NAMA_PRODI'].unique())
else:
    filtered_prodi_df = pd.DataFrame()
    list_prodi = []

with c2:
    selected_prodi = st.selectbox(
        "📚 Program Studi (Jurusan)", 
        list_prodi, 
        index=None, 
        placeholder="Pilih Kampus dahulu..." if not selected_ptn else "Cari Jurusan...",
        disabled=(not selected_ptn)
    )

st.write("")
btn_hitung = st.button("Hitung Peluang Sekarang →", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. DASHBOARD HASIL ANALISIS
# ==========================================
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.warning("⚠️ Silakan tentukan **Universitas** dan **Program Studi** terlebih dahulu.")
    else:
        target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

        kuota = target['DAYA_TAMPUNG_2026']
        peminat = target['PEMINAT_2025']
        peluang = target['PELUANG_PERSEN']
        rasio = target['RASIO_PERSAINGAN']

        # Klasifikasi Keketatan
        if peluang < 5.0:
            status_class = "status-ketat"
            status_label = "🔴 SANGAT KETAT"
            desc_text = f"Peluang lulus kamu tergolong sangat kecil. Setiap 1 kursi diperebutkan oleh <b>{rasio} pendaftar</b>."
        elif peluang <= 15.0:
            status_class = "status-ketat"
            status_label = "🟠 KETAT"
            desc_text = f"Persaingan tergolong tinggi. Kamu harus menyingkirkan sekitar <b>{rasio} pesaing</b> per kursi."
        elif peluang <= 30.0:
            status_class = "status-sedang"
            status_label = "🟡 SEDANG / MODERAT"
            desc_text = f"Tingkat persaingan moderat. Opsi yang cukup baik untuk dijadikan Pilihan 1 atau 2."
        else:
            status_class = "status-longgar"
            status_label = "🟢 PELUANG BESAR"
            desc_text = f"Persaingan relatif lebih aman. Sangat direkomendasikan sebagai pilihan pengaman."

        # Hero Card Output Peluang
        st.markdown(f"""
        <div class="target-box">
            <div class="target-header">{target['NAMA_PTN']} — {target['JENJANG']}</div>
            <div class="target-title">{target['NAMA_PRODI']}</div>
            <div class="chance-number">{peluang}%</div>
            <div class="status-pill {status_class}">{status_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # 3 Grid Stat Utama
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">📦 Kuota 2026</div>
                <div class="stat-val">{kuota} <span style="font-size:0.8rem; color:#64748B;">Kursi</span></div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">👥 Peminat 2025</div>
                <div class="stat-val">{peminat:,} <span style="font-size:0.8rem; color:#64748B;">Siswa</span></div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">⚖️ Rasio Kampus</div>
                <div class="stat-val">1 : {rasio}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Insight Box Summary
        st.markdown(f"""
        <div class="insight-card">
            <b>💡 Insights untuk kamu:</b><br>
            {desc_text} Untuk prodi <b>{target['NAMA_PRODI']}</b>, daya tampung tahun ini adalah <b>{kuota} kursi</b> 
            dengan total peminat tahun lalu sebanyak <b>{peminat:,} siswa</b>.
        </div>
        """, unsafe_allow_html=True)

        # Tabel Pembanding Jurusan Lain
        st.markdown(f"""
        <h3 style="font-size:1.15rem; font-weight:800; color:#0F172A; margin-top:2rem; margin-bottom:0.5rem;">
            🔍 Alternatif Jurusan Lain di {selected_ptn}
        </h3>
        <p style="font-size:0.85rem; color:#64748B; margin-bottom:1rem;">
            Urutan program studi berdasarkan persentase peluang dari yang paling aman hingga terketat:
        </p>
        """, unsafe_allow_html=True)

        alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)

        table_html = """
        <div class="table-card">
            <table class="clean-table">
                <thead>
                    <tr>
                        <th>Kode</th>
                        <th>Program Studi</th>
                        <th>Jenjang</th>
                        <th>Kuota 2026</th>
                        <th>Peminat 2025</th>
                        <th>Peluang (%)</th>
                        <th>Rasio</th>
                    </tr>
                </thead>
                <tbody>
        """
        for _, row in alt_df.iterrows():
            is_selected = (row['NAMA_PRODI'] == selected_prodi)
            bg_style = "background-color: #EFF6FF;" if is_selected else ""
            
            table_html += f"""
                <tr style="{bg_style}">
                    <td><b>{row['KODE_PRODI']}</b></td>
                    <td>{row['NAMA_PRODI']} {'(Jurusan Pilihanmu)' if is_selected else ''}</td>
                    <td><span style="background:#F1F5F9; padding:2px 6px; border-radius:4px; font-size:0.75rem;">{row['JENJANG']}</span></td>
                    <td>{row['DAYA_TAMPUNG_2026']} Kursi</td>
                    <td>{row['PEMINAT_2025']:,}</td>
                    <td><b style="color: #2563EB;">{row['PELUANG_PERSEN']}%</b></td>
                    <td>1 : {row['RASIO_PERSAINGAN']}</td>
                </tr>
            """
        table_html += """
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
