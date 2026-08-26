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
# 2. STRICT FORCE LIGHT THEME CSS
# ==========================================
FORCE_LIGHT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* PAKSA OVERRIDE CORE STREAMLIT CONTAINER */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], .main, .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    #MainMenu, footer, header, [data-testid="stHeader"] { 
        visibility: hidden !important; 
        height: 0 !important; 
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 800px !important;
        background-color: #F8FAFC !important;
    }

    /* NAVBAR */
    .app-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .app-brand {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #0F172A !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .app-brand span { color: #2563EB; }

    /* HERO SECTION */
    .hero-container {
        text-align: center;
        margin: 0.5rem 0 2rem 0;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EFF6FF;
        color: #2563EB;
        padding: 6px 16px;
        border-radius: 99px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        border: 1px solid #DBEAFE;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.25;
        letter-spacing: -0.7px;
        color: #0F172A !important;
        margin-bottom: 0.6rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #64748B !important;
        line-height: 1.55;
        max-width: 560px;
        margin: 0 auto;
    }

    /* CARD INPUT WRAPPER */
    .input-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
        margin-bottom: 1rem;
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.3rem;
    }
    .step-num {
        background: #EFF6FF;
        color: #2563EB;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .step-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #0F172A !important;
    }
    .step-desc {
        font-size: 0.82rem;
        color: #64748B !important;
        margin-bottom: 0.8rem;
    }

    /* CUSTOM STREAMLIT SELECTBOX - PAKSA TERANG */
    div[data-baseweb="select"] > div {
        background-color: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        min-height: 44px !important;
    }
    div[data-baseweb="select"] * {
        color: #0F172A !important;
        fill: #0F172A !important;
    }
    div[data-baseweb="select"]:hover > div {
        border-color: #2563EB !important;
        background-color: #FFFFFF !important;
    }

    /* BUTTON ACTION */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        height: 50px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35) !important;
    }

    /* RESULT HERO CARD */
    .result-hero {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px;
        padding: 26px 20px;
        text-align: center;
        box-shadow: 0 10px 25px -3px rgba(15, 23, 42, 0.06);
        margin: 1.5rem 0 1rem 0;
    }
    .result-hero-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .result-hero-value {
        font-size: 3.6rem;
        font-weight: 800;
        color: #2563EB !important;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin: 8px 0;
    }
    .badge-status {
        display: inline-block;
        padding: 5px 16px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .status-ketat { background: #FEF2F2 !important; color: #EF4444 !important; border: 1px solid #FCA5A5 !important; }
    .status-sedang { background: #FFFBEB !important; color: #D97706 !important; border: 1px solid #FCD34D !important; }
    .status-longgar { background: #F0FDF4 !important; color: #16A34A !important; border: 1px solid #86EFAC !important; }

    /* METRICS */
    .metric-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
    }
    .metric-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B !important;
        text-transform: uppercase;
    }
    .metric-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A !important;
        margin-top: 2px;
    }

    /* INSIGHT */
    .insight-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px;
        padding: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
    }

    /* DATAFRAME OVERRIDE LIGHT */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
    }

    /* FOOTER */
    .disclaimer-box {
        font-size: 0.8rem;
        color: #64748B !important;
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid #E2E8F0;
    }

    /* MOBILE OPTIMIZATION */
    @media (max-width: 640px) {
        .hero-title { font-size: 1.55rem; }
        .hero-subtitle { font-size: 0.85rem; }
        .result-hero-value { font-size: 2.8rem; }
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    }
</style>
"""
st.markdown(FORCE_LIGHT_CSS, unsafe_allow_html=True)

# ==========================================
# 3. BACKEND DATA LOGIC
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

df = load_data()

# ==========================================
# 4. NAVBAR HEADER
# ==========================================
st.markdown("""
<div class="app-navbar">
    <div class="app-brand">🎓 PTN<span>Match</span></div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ SNBP 2026 • DATA RESMI TERKINI</div>
    <h1 class="hero-title">Seberapa kompetitif jurusan impianmu?</h1>
    <p class="hero-subtitle">Cek peluang kelulusan dan rasio persaingan PTN secara presisi berdasarkan analisis data resmi.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. INPUT FORM
# ==========================================
col_s1, col_s2 = st.columns(2, gap="small")

with col_s1:
    st.markdown("""
    <div class="input-card">
        <div class="step-header">
            <span class="step-num">STEP 01</span>
            <span class="step-title">UNIVERSITAS</span>
        </div>
        <div class="step-desc">Mau kuliah di mana?</div>
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
    <div class="input-card">
        <div class="step-header">
            <span class="step-num">STEP 02</span>
            <span class="step-title">PROGRAM STUDI</span>
        </div>
        <div class="step-desc">Jurusan yang kamu incar?</div>
    """, unsafe_allow_html=True)
    
    selected_prodi = st.selectbox(
        "Pilih Prodi", 
        list_prodi, 
        index=None, 
        placeholder="🔍 Cari prodi..." if selected_ptn else "Pilih PTN dahulu",
        disabled=(not selected_ptn),
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

btn_hitung = st.button("Analisis Peluang →", use_container_width=True)

# ==========================================
# 6. HASIL ANALISIS
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

        if peluang < 5.0:
            status_class = "status-ketat"
            status_label = "🔴 SANGAT KETAT"
        elif peluang <= 15.0:
            status_class = "status-ketat"
            status_label = "🟠 KETAT"
        elif peluang <= 30.0:
            status_class = "status-sedang"
            status_label = "🟡 SEDANG"
        else:
            status_class = "status-longgar"
            status_label = "🟢 PELUANG BESAR"

        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">{target['NAMA_PTN']} — {target['NAMA_PRODI']}</div>
            <div class="result-hero-value">{peluang}%</div>
            <div class="badge-status {status_class}">{status_label}</div>
            <p style="color:#64748B; font-size:0.88rem; margin-top:12px;"><b>{kuota}</b> kuota diperebutkan oleh <b>{peminat:,}</b> peminat</p>
        </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3, gap="small")
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🪑 KUOTA 2026</div>
                <div class="metric-val">{kuota}</div>
            </div>
            """, unsafe_allow_html=True)

        with mc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">👥 PEMINAT 2025</div>
                <div class="metric-val">{peminat:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with mc3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🔥 RASIO</div>
                <div class="metric-val">1 : {rasio}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card">
            <h4 style="margin:0 0 6px 0; font-weight:700; font-size:0.95rem; color:#0F172A;">💡 Analisis Peluang</h4>
            <p style="color:#64748B; font-size:0.88rem; line-height:1.55; margin:0;">
                Rasio persaingan prodi ini adalah <b>1 : {rasio}</b>. Setiap 1 kursi diperebutkan oleh {rasio} pendaftar. 
                Pertimbangkan prodi alternatif dengan rasio lebih longgar di bawah ini sebagai opsi aman.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<h4 style="font-weight:700; font-size:1rem; margin-top:1.5rem; margin-bottom:0.5rem; color:#0F172A;">Opsi Prodi Lain di PTN Ini</h4>""", unsafe_allow_html=True)

        alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)

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

# Disclaimer Footer
st.markdown("""
<div class="disclaimer-box">
    ⚠️ Data berdasarkan simulasi estimasi resmi. Hasil ini bukan jaminan kelulusan mutlak.
</div>
""", unsafe_allow_html=True)
