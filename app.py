import pandas as pd
import streamlit as st

# ==========================================
# 1. INITIALIZATION & STREAMLIT CONFIG
# ==========================================
st.set_page_config(
    page_title="PTNMatch — Analisis Peluang & Rasio PTN",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. DESIGN SYSTEM & MODERN CSS (STYLING)
# ==========================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Reset & Hide Streamlit Default UI */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A;
    }
    
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1140px !important;
    }

    /* Custom Header / Navbar */
    .app-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .app-brand {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .app-brand span {
        color: #2563EB;
    }
    .app-nav-links {
        display: flex;
        gap: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748B;
    }

    /* Hero Section Layout */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EFF6FF;
        border: 1px solid #DBEAFE;
        color: #2563EB;
        padding: 6px 14px;
        border-radius: 99px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.25;
        color: #0F172A;
        letter-spacing: -1px;
        margin-bottom: 0.8rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748B;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* Preview Analytics Box (Hero Right Visual) */
    .preview-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.05);
    }
    .preview-tag {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .preview-score {
        font-size: 2.8rem;
        font-weight: 800;
        color: #2563EB;
        margin: 8px 0;
    }

    /* Input Step Container */
    .step-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px 28px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.03);
        margin-bottom: 1.5rem;
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
    }
    .step-num {
        background: #EFF6FF;
        color: #2563EB;
        font-size: 0.8rem;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 8px;
    }
    .step-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        height: 54px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35) !important;
    }

    /* Primary Result Hero Card */
    .result-hero {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 36px 24px;
        text-align: center;
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.05);
        margin-bottom: 1.5rem;
    }
    .result-hero-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .result-hero-value {
        font-size: 4.2rem;
        font-weight: 800;
        color: #2563EB;
        letter-spacing: -2px;
        line-height: 1.1;
        margin: 12px 0;
    }
    .badge-status {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .status-ketat { background: #FEF2F2; color: #EF4444; border: 1px solid #FCA5A5; }
    .status-sedang { background: #FFFBEB; color: #F59E0B; border: 1px solid #FCD34D; }
    .status-longgar { background: #F0FDF4; color: #16A34A; border: 1px solid #86EFAC; }

    /* Metric Cards Grid */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
        height: 100%;
    }
    .metric-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 6px;
    }

    /* Insight Card */
    .insight-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 2rem;
    }
    
    /* Footer & Disclaimer */
    .disclaimer-box {
        font-size: 0.82rem;
        color: #94A3B8;
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E2E8F0;
    }

    /* Mobile Adaptations */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.85rem; }
        .result-hero-value { font-size: 3.2rem; }
        .app-nav-links { display: none; }
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 3. BACKEND DATA LOGIC (UNCHANGED 100%)
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('MASTER_all_prodi.csv', sep=';', on_bad_lines='skip')
    df['DAYA_TAMPUNG_2026'] = pd.to_numeric(df['DAYA_TAMPUNG_2026'], errors='coerce').fillna(0).astype(int)
    df['PEMINAT_2025'] = pd.to_numeric(df['PEMINAT_2025'], errors='coerce').fillna(0).astype(int)
    
    # Formula Peluang (%)
    df['PELUANG_PERSEN'] = df.apply(
        lambda r: round((r['DAYA_TAMPUNG_2026'] / r['PEMINAT_2025']) * 100, 2) if r['PEMINAT_2025'] > 0 else 0.0, 
        axis=1
    )
    # Formula Rasio Persaingan
    df['RASIO_PERSAINGAN'] = df.apply(
        lambda r: int(round(r['PEMINAT_2025'] / r['DAYA_TAMPUNG_2026'])) if r['DAYA_TAMPUNG_2026'] > 0 else 0,
        axis=1
    )
    return df

df = load_data()

# Helper UI Components
def render_header():
    st.markdown("""
    <div class="app-navbar">
        <div class="app-brand">🎓 PTN<span>Match</span></div>
        <div class="app-nav-links">
            <span>Panduan</span>
            <span>Tentang Data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hero():
    col1, col2 = st.columns([1.3, 1], gap="large")
    with col1:
        st.markdown("""
        <div class="hero-badge">✨ SNBP 2026 • DATA RESMI TERKINI</div>
        <h1 class="hero-title">Seberapa kompetitif jurusan impianmu?</h1>
        <p class="hero-subtitle">Cek peluang kelulusan dan rasio persaingan PTN secara presisi berdasarkan analisis data kuota dan peminat resmi.</p>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="preview-card">
            <div class="preview-tag">COMPETITION INDEX PREVIEW</div>
            <div class="preview-score">78<span style="font-size:1.2rem; color:#64748B;">/100</span></div>
            <div style="font-weight:700; color:#EF4444; margin-bottom:12px;">● Kompetitif (Ketat)</div>
            <div style="font-size:0.88rem; color:#64748B; display:flex; justify-shadow:space-between; gap:20px;">
                <span>Peminat: <b>1.188</b></span>
                <span>Kuota: <b>112</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

render_header()
render_hero()
st.write("")

# ==========================================
# 4. INPUT JOURNEY (STEP 01 & STEP 02)
# ==========================================
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
    <span style="font-weight:700; font-size:1.1rem;">Langkah Analisis</span>
    <span style="font-size:0.85rem; font-weight:700; color:#2563EB;">01 PTN ➔ 02 PRODI ➔ 03 HASIL</span>
</div>
""", unsafe_allow_html=True)

col_s1, col_s2 = st.columns(2, gap="medium")

with col_s1:
    st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <span class="step-num">STEP 01</span>
            <span class="step-title">UNIVERSITAS</span>
        </div>
        <p style="font-size:0.88rem; color:#64748B; margin-bottom:10px;">Mau kuliah di mana?</p>
    """, unsafe_allow_html=True)
    
    list_ptn = sorted(df['NAMA_PTN'].unique())
    selected_ptn = st.selectbox(
        "Pilih PTN", 
        list_ptn, 
        index=None, 
        placeholder="🔍 Cari universitas...",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

if selected_ptn:
    filtered_prodi_df = df[df['NAMA_PTN'] == selected_ptn]
    list_prodi = sorted(filtered_prodi_df['NAMA_PRODI'].unique())
else:
    filtered_prodi_df = pd.DataFrame()
    list_prodi = []

with col_s2:
    st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <span class="step-num">STEP 02</span>
            <span class="step-title">PROGRAM STUDI</span>
        </div>
        <p style="font-size:0.88rem; color:#64748B; margin-bottom:10px;">Jurusan yang kamu incar?</p>
    """, unsafe_allow_html=True)
    
    selected_prodi = st.selectbox(
        "Pilih Prodi", 
        list_prodi, 
        index=None, 
        placeholder="🔍 Cari program studi..." if selected_ptn else "Pilih universitas terlebih dahulu",
        disabled=(not selected_ptn),
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
btn_hitung = st.button("Analisis Peluang →", use_container_width=True)

# ==========================================
# 5. RESULT PAGE REDESIGN
# ==========================================
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.warning("⚠️ Silakan pilih Universitas dan Program Studi terlebih dahulu.")
    else:
        target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

        kuota = target['DAYA_TAMPUNG_2026']
        peminat = target['PEMINAT_2025']
        peluang = target['PELUANG_PERSEN']
        rasio = target['RASIO_PERSAINGAN']

        # Determine Badge Style & Category
        if peluang < 5.0:
            status_class = "status-ketat"
            status_label = "🔴 SANGAT KETAT (Super Favorit)"
        elif peluang <= 15.0:
            status_class = "status-ketat"
            status_label = "🟠 KETAT / TINGGI"
        elif peluang <= 30.0:
            status_class = "status-sedang"
            status_label = "🟡 SEDANG / MODERAT"
        else:
            status_class = "status-longgar"
            status_label = "🟢 PELUANG BESAR"

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Result Header Metadata
        st.markdown(f"""
        <div style="margin-bottom: 0.5rem; font-size: 0.8rem; font-weight:700; color:#2563EB; letter-spacing:1px;">HASIL ANALISIS</div>
        <h2 style="font-size: 2rem; font-weight:800; margin:0; color:#0F172A;">{target['NAMA_PRODI']}</h2>
        <p style="font-size: 1rem; color:#64748B; margin-top:4px; margin-bottom:1.5rem;">
            {target['JENJANG']} • <b>{target['NAMA_PTN']}</b> &nbsp;|&nbsp; 
            <span style="background:#F1F5F9; padding:2px 8px; border-radius:6px; font-size:0.85rem;">Kode {target['KODE_PRODI']}</span> &nbsp;|&nbsp;
            <span style="background:#F1F5F9; padding:2px 8px; border-radius:6px; font-size:0.85rem;">Portofolio: {target['JENIS_PORTOFOLIO']}</span>
        </p>
        """, unsafe_allow_html=True)

        # Primary Focal Point (Main Opportunity Hero)
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">PELUANG SIMULASI</div>
            <div class="result-hero-value">{peluang}%</div>
            <div class="badge-status {status_class}">{status_label}</div>
            <p style="color:#64748B; font-size:0.95rem; margin-top:16px;"><b>{kuota}</b> kursi tersedia diperebutkan <b>{peminat:,}</b> peminat</p>
        </div>
        """, unsafe_allow_html=True)

        # Metric Cards (3 Card System)
        mc1, mc2, mc3 = st.columns(3, gap="medium")
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🪑 DAYA TAMPUNG</div>
                <div class="metric-val">{kuota} <span style="font-size:0.9rem; color:#64748B; font-weight:600;">kursi</span></div>
            </div>
            """, unsafe_allow_html=True)

        with mc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">👥 PEMINAT LALU</div>
                <div class="metric-val">{peminat:,} <span style="font-size:0.9rem; color:#64748B; font-weight:600;">siswa</span></div>
            </div>
            """, unsafe_allow_html=True)

        with mc3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🔥 RASIO PERSAINGAN</div>
                <div class="metric-val">1 : {rasio} <span style="font-size:0.9rem; color:#64748B; font-weight:600;">orang</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Actionable Insight Box
        st.markdown(f"""
        <div class="insight-card">
            <h4 style="margin:0 0 8px 0; font-weight:700; color:#0F172A;">💡 Apa artinya?</h4>
            <p style="color:#475569; font-size:0.95rem; line-height:1.6; margin-bottom:16px;">
                Sekitar <b>{rasio} siswa</b> bersaing untuk memperebutkan 1 kursi. 
                Dengan peluang sebesar <b>{peluang}%</b>, persaingan jurusan ini tergolong <b>{status_label.split(' ')[1]}</b>.
            </p>
            <h4 style="margin:0 0 8px 0; font-weight:700; color:#0F172A;">🎯 Apa yang bisa kamu lakukan?</h4>
            <p style="color:#475569; font-size:0.95rem; line-height:1.6; margin:0;">
                Jurusan ini tergolong kompetitif. Pastikan pilihanmu sesuai dengan profil akademik dan pertimbangkan beberapa alternatif PTN/program studi di bawah ini sebagai opsi cadangan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Table Comparison Section
        st.markdown(f"""
        <h3 style="font-weight:800; color:#0F172A; margin-bottom:4px;">Bandingkan dengan jurusan lain</h3>
        <p style="color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;">Lihat pilihan lain di {selected_ptn} dan temukan alternatif dengan tingkat persaingan berbeda.</p>
        """, unsafe_allow_html=True)

        alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)

        # Highlight Row Current Program
        st.dataframe(
            alt_df[['KODE_PRODI', 'NAMA_PRODI', 'JENJANG', 'DAYA_TAMPUNG_2026', 'PEMINAT_2025', 'PELUANG_PERSEN', 'RASIO_PERSAINGAN']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "KODE_PRODI": st.column_config.TextColumn("Kode"),
                "NAMA_PRODI": st.column_config.TextColumn("Program Studi"),
                "JENJANG": st.column_config.TextColumn("Jenjang"),
                "DAYA_TAMPUNG_2026": st.column_config.NumberColumn("Daya Tampung", format="%d Kursi"),
                "PEMINAT_2025": st.column_config.NumberColumn("Peminat", format="%d"),
                "PELUANG_PERSEN": st.column_config.ProgressColumn("Peluang (%)", format="%.2f%%", min_value=0, max_value=100),
                "RASIO_PERSAINGAN": st.column_config.NumberColumn("Rasio", format="1 : %d")
            }
        )

# Footer Disclaimer
st.markdown("""
<div class="disclaimer-box">
    ⚠️ Hasil ini merupakan simulasi berdasarkan data peminat dan daya tampung yang tersedia, bukan jaminan kelulusan resmi.
</div>
""", unsafe_allow_html=True)
