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
# 2. DESIGN SYSTEM & MODERN STYLING (SINGLE LIGHT THEME)
# ==========================================
MODERN_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* BASE CONTAINER OVERRIDE */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0F172A !important;
    }

    #MainMenu, footer, header, [data-testid="stHeader"] { 
        display: none !important; 
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 860px !important;
    }

    /* HEADER & BRANDING */
    .brand-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .brand-logo {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #EFF6FF;
        color: #2563EB;
        font-weight: 800;
        font-size: 0.85rem;
        padding: 6px 16px;
        border-radius: 99px;
        border: 1px solid #DBEAFE;
        margin-bottom: 0.8rem;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #0F172A;
        line-height: 1.25;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        max-width: 540px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* CARD CONTAINER UNTUK FORM & METRICS */
    .card-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
        margin-bottom: 1.25rem;
    }

    /* LABEL SELECTBOX DIBUAT MODERN */
    .input-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #334155;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* CUSTOM STYLED BUTTON */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        height: 52px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
        margin-top: 0.5rem;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35) !important;
    }

    /* HERO RESULT CARD */
    .hero-result {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05);
        margin-top: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .hero-target {
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .hero-percent {
        font-size: 3.8rem;
        font-weight: 800;
        color: #2563EB;
        line-height: 1;
        letter-spacing: -1.5px;
        margin: 12px 0;
    }

    /* STATUS BADGES */
    .status-pill {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .status-sangat-ketat { background: #FEF2F2; color: #DC2626; border: 1px solid #FCA5A5; }
    .status-ketat { background: #FFF7ED; color: #EA580C; border: 1px solid #FDBA74; }
    .status-sedang { background: #FEFCE8; color: #CA8A04; border: 1px solid #FDE047; }
    .status-aman { background: #F0FDF4; color: #16A34A; border: 1px solid #86EFAC; }

    /* MINI METRICS CARD */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 1.25rem;
    }
    .metric-item {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-item-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
    }
    .metric-item-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }

    /* INSIGHT BOX */
    .insight-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* TABLE STYLES (PURE HTML - NEVER FAILS) */
    .table-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.75rem;
    }
    .custom-table-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    table.data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
        text-align: left;
    }
    table.data-table th {
        background: #F8FAFC;
        color: #475569;
        font-weight: 700;
        padding: 14px 16px;
        border-bottom: 1px solid #E2E8F0;
    }
    table.data-table td {
        padding: 14px 16px;
        border-bottom: 1px solid #F1F5F9;
        color: #0F172A;
    }
    table.data-table tr:last-child td {
        border-bottom: none;
    }
    table.data-table tr:hover {
        background-color: #F8FAFC;
    }

    /* RESPONSIVE DESIGN */
    @media (max-width: 640px) {
        .brand-title { font-size: 1.6rem; }
        .hero-percent { font-size: 3rem; }
        .metric-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown(MODERN_THEME_CSS, unsafe_allow_html=True)

# ==========================================
# 3. KONEKSI KODE DAN PEMROSESAN DATA
# ==========================================
@st.cache_data
def get_clean_data():
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

df = get_clean_data()

# ==========================================
# 4. BRANDING HEADER
# ==========================================
st.markdown("""
<div class="brand-header">
    <div class="brand-logo">🎓 PTNMatch</div>
    <h1 class="brand-title">Cek Peluang Kelulusan SNBP</h1>
    <p class="brand-subtitle">Analisis rasio keketatan dan peta persaingan jurusan impianmu berbasis data acuan resmi.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. INPUT SELECTION AREA
# ==========================================
st.markdown('<div class="card-box">', unsafe_allow_html=True)

col_ptn, col_prodi = st.columns(2, gap="medium")

with col_ptn:
    st.markdown('<div class="input-label">🏛️ Pilih Universitas (PTN)</div>', unsafe_allow_html=True)
    ptn_options = sorted(df['NAMA_PTN'].unique())
    selected_ptn = st.selectbox(
        "Pilih PTN",
        ptn_options,
        index=None,
        placeholder="Cari universitas...",
        label_visibility="collapsed"
    )

if selected_ptn:
    filtered_prodi_df = df[df['NAMA_PTN'] == selected_ptn]
    prodi_options = sorted(filtered_prodi_df['NAMA_PRODI'].unique())
else:
    filtered_prodi_df = pd.DataFrame()
    prodi_options = []

with col_prodi:
    st.markdown('<div class="input-label">📚 Pilih Program Studi (Jurusan)</div>', unsafe_allow_html=True)
    selected_prodi = st.selectbox(
        "Pilih Prodi",
        prodi_options,
        index=None,
        placeholder="Pilih universitas terlebih dahulu" if not selected_ptn else "Cari jurusan...",
        disabled=(not selected_ptn),
        label_visibility="collapsed"
    )

btn_analyze = st.button("Hitung Peluang Sekarang →", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. RESULTS & DASHBOARD DISPLAY
# ==========================================
if btn_analyze:
    if not selected_ptn or not selected_prodi:
        st.warning("⚠️ Silakan tentukan **Universitas** dan **Program Studi** terlebih dahulu.")
    else:
        target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

        kuota = target['DAYA_TAMPUNG_2026']
        peminat = target['PEMINAT_2025']
        peluang = target['PELUANG_PERSEN']
        rasio = target['RASIO_PERSAINGAN']

        # Klasifikasi Status Keketatan
        if peminat == 0:
            status_class = "status-aman"
            status_label = "🟢 PRODI BARU / BEBAS KETATAN"
        elif peluang < 5.0:
            status_class = "status-sangat-ketat"
            status_label = "🔴 SANGAT KETAT (HIGH RISK)"
        elif peluang <= 15.0:
            status_class = "status-ketat"
            status_label = "🟠 KETAT (FAVORIT)"
        elif peluang <= 30.0:
            status_class = "status-sedang"
            status_label = "🟡 SEDANG (MODERAT)"
        else:
            status_class = "status-aman"
            status_label = "🟢 PELUANG BESAR (SAFE)"

        # 1. Main Hero Card
        st.markdown(f"""
        <div class="hero-result">
            <div class="hero-target">{target['NAMA_PTN']} — {target['NAMA_PRODI']} ({target['JENJANG']})</div>
            <div class="hero-percent">{peluang}%</div>
            <div class="status-pill {status_class}">{status_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Metric Breakdown Grid
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-item-label">🪑 Kuota 2026</div>
                <div class="metric-item-val">{kuota} <span style="font-size:0.85rem; font-weight:600; color:#64748B;">Kursi</span></div>
            </div>
            <div class="metric-item">
                <div class="metric-item-label">👥 Peminat 2025</div>
                <div class="metric-item-val">{peminat:,} <span style="font-size:0.85rem; font-weight:600; color:#64748B;">Siswa</span></div>
            </div>
            <div class="metric-item">
                <div class="metric-item-label">⚖️ Rasio Keketatan</div>
                <div class="metric-item-val">1 : {rasio}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Actionable UX Insights
        st.markdown(f"""
        <div class="insight-card">
            <strong style="color: #0F172A;">💡 Catatan Strategi:</strong><br>
            Untuk lulus di jurusan ini, kamu harus bersaing dan menyisihkan setidaknya <b>{rasio} orang</b> per 1 kursi. 
            {"Gunakan jurusan ini sebagai <b>Pilihan 1</b> saja dan siapkan jurusan pengaman di Pilihan 2." if peluang <= 15.0 else "Jurusan ini relatif potensial untuk dijadikan pilihan aman."}
        </div>
        """, unsafe_allow_html=True)

        # 4. Pure HTML Table (Antigagal / Clean Render)
        st.markdown(f'<div class="table-section-title">💡 Jurusan Lain di {target["NAMA_PTN"]} (Diurutkan dari Terlonggar)</div>', unsafe_allow_html=True)

        alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)

        table_rows_html = ""
        for _, r in alt_df.iterrows():
            is_selected = (r['NAMA_PRODI'] == selected_prodi)
            row_bg = "background-color: #EFF6FF;" if is_selected else ""
            badge_target = ' <span style="background:#2563EB; color:#FFF; font-size:0.7rem; padding:2px 6px; border-radius:4px; margin-left:4px;">INCARANMU</span>' if is_selected else ""
            
            table_rows_html += f"""
            <tr style="{row_bg}">
                <td><b>{r['KODE_PRODI']}</b></td>
                <td><b>{r['NAMA_PRODI']}</b> {badge_target}</td>
                <td>{r['JENJANG']}</td>
                <td>{r['DAYA_TAMPUNG_2026']} Kursi</td>
                <td>{r['PEMINAT_2025']:,}</td>
                <td><strong style="color: #2563EB;">{r['PELUANG_PERSEN']}%</strong></td>
                <td>1 : {r['RASIO_PERSAINGAN']}</td>
            </tr>
            """

        full_table_html = f"""
        <div class="custom-table-card">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Kode</th>
                        <th>Program Studi</th>
                        <th>Jenjang</th>
                        <th>Daya Tampung</th>
                        <th>Peminat</th>
                        <th>Peluang</th>
                        <th>Rasio</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>
        """
        st.markdown(full_table_html, unsafe_allow_html=True)
