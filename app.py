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

# State untuk Simpan Tema (Default: Light)
if "theme" not in st.session_state:
    st.session_state.theme = "☀️ Terang"

# ==========================================
# 2. THEME CONFIG & DYNAMIC CSS
# ==========================================
is_dark = st.session_state.theme == "🌙 Gelap"

# Variables berdasarkan Tema
bg_body = "#0F172A" if is_dark else "#F8FAFC"
bg_card = "#1E293B" if is_dark else "#FFFFFF"
bg_input = "#334155" if is_dark else "#F1F5F9"
text_main = "#F8FAFC" if is_dark else "#0F172A"
text_sub = "#94A3B8" if is_dark else "#64748B"
border_color = "#334155" if is_dark else "#E2E8F0"
navbar_border = "#1E293B" if is_dark else "#E2E8F0"

CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: {bg_body} !important;
        color: {text_main} !important;
    }}
    
    #MainMenu, footer, header {{visibility: hidden; height: 0;}}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 880px !important;
    }}

    /* Custom Navbar */
    .app-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid {navbar_border};
    }}
    .app-brand {{
        font-size: 1.35rem;
        font-weight: 800;
        color: {text_main};
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .app-brand span {{ color: #2563EB; }}

    /* Hero Center Aligned */
    .hero-container {{
        text-align: center;
        margin-bottom: 2.2rem;
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {'#1E293B' if is_dark else '#EFF6FF'};
        border: 1px solid {'#334155' if is_dark else '#DBEAFE'};
        color: #3B82F6;
        padding: 6px 16px;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }}
    .hero-title {{
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.25;
        color: {text_main};
        letter-spacing: -0.8px;
        margin-bottom: 0.8rem;
    }}
    .hero-subtitle {{
        font-size: 0.98rem;
        color: {text_sub};
        line-height: 1.6;
        max-width: 620px;
        margin: 0 auto;
    }}

    /* Card Wrapper Presisi */
    .custom-step-box {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }}
    .step-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.3rem;
    }}
    .step-num {{
        background: {'#334155' if is_dark else '#EFF6FF'};
        color: #3B82F6;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
    }}
    .step-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {text_main};
    }}
    .step-desc {{
        font-size: 0.85rem;
        color: {text_sub};
        margin-bottom: 0.8rem;
    }}

    /* Penyesuaian Presisi Selectbox Streamlit */
    div[data-baseweb="select"] > div {{
        background-color: {bg_input} !important;
        border: 1.5px solid {border_color} !important;
        border-radius: 12px !important;
        color: {text_main} !important;
        transition: all 0.2s ease-in-out !important;
    }}
    div[data-baseweb="select"] * {{
        color: {text_main} !important;
    }}
    div[data-baseweb="select"]:hover > div {{
        border-color: #3B82F6 !important;
    }}

    /* Button Styling */
    div.stButton > button {{
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        height: 52px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease !important;
        margin-top: 10px;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    }}

    /* Primary Result Card */
    .result-hero {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 24px;
        padding: 30px 24px;
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    .result-hero-label {{
        font-size: 0.85rem;
        font-weight: 700;
        color: {text_sub};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .result-hero-value {{
        font-size: 3.8rem;
        font-weight: 800;
        color: #3B82F6;
        letter-spacing: -2px;
        line-height: 1.1;
        margin: 10px 0;
    }}
    .badge-status {{
        display: inline-block;
        padding: 6px 18px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.9rem;
    }}
    .status-ketat {{ background: {'#451A1A' if is_dark else '#FEF2F2'}; color: #EF4444; border: 1px solid #FCA5A5; }}
    .status-sedang {{ background: {'#45321A' if is_dark else '#FFFBEB'}; color: #F59E0B; border: 1px solid #FCD34D; }}
    .status-longgar {{ background: {'#1A4526' if is_dark else '#F0FDF4'}; color: #16A34A; border: 1px solid #86EFAC; }}

    /* Metric Cards Grid */
    .metric-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 16px;
        height: 100%;
    }}
    .metric-title {{
        font-size: 0.75rem;
        font-weight: 700;
        color: {text_sub};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .metric-val {{
        font-size: 1.4rem;
        font-weight: 800;
        color: {text_main};
        margin-top: 4px;
    }}

    /* Insight Card */
    .insight-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 2rem;
    }}
    
    /* Footer Disclaimer */
    .disclaimer-box {{
        font-size: 0.82rem;
        color: {text_sub};
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid {border_color};
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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
# 4. NAVBAR & TOGGLE THEME
# ==========================================
col_nav1, col_nav2 = st.columns([3, 1], vertical_alignment="center")
with col_nav1:
    st.markdown("""
    <div class="app-brand">🎓 PTN<span>Match</span></div>
    """, unsafe_allow_html=True)

with col_nav2:
    selected_theme = st.segmented_control(
        "Tema",
        ["☀️ Terang", "🌙 Gelap"],
        default=st.session_state.theme,
        label_visibility="collapsed"
    )
    if selected_theme and selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

# Hero Section Centered
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ SNBP 2026 • DATA RESMI TERKINI</div>
    <h1 class="hero-title">Seberapa kompetitif jurusan impianmu?</h1>
    <p class="hero-subtitle">Cek peluang kelulusan dan rasio persaingan PTN secara presisi berdasarkan analisis data kuota dan peminat resmi.</p>
</div>
""", unsafe_allow_html=True)

# Progress Indicator
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.8rem;">
    <span style="font-weight:700; font-size:0.95rem; color:{text_main};">Langkah Analisis</span>
    <span style="font-size:0.85rem; font-weight:700; color:#3B82F6;">01 PTN ➔ 02 PRODI ➔ 03 HASIL</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. INPUT STEP CARDS (PRESISI & MULTI-THEME)
# ==========================================
col_s1, col_s2 = st.columns(2, gap="medium")

with col_s1:
    st.markdown("""
    <div class="custom-step-box">
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
    <div class="custom-step-box">
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
        placeholder="🔍 Cari program studi..." if selected_ptn else "Pilih universitas terlebih dahulu",
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
        
        st.markdown(f"""
        <div style="margin-bottom: 0.5rem; font-size: 0.8rem; font-weight:700; color:#3B82F6; letter-spacing:1px;">HASIL ANALISIS</div>
        <h2 style="font-size: 1.9rem; font-weight:800; margin:0; color:{text_main};">{target['NAMA_PRODI']}</h2>
        <p style="font-size: 0.92rem; color:{text_sub}; margin-top:4px; margin-bottom:1.5rem;">
            {target['JENJANG']} • <b>{target['NAMA_PTN']}</b> &nbsp;|&nbsp; 
            <span style="background:{bg_input}; padding:2px 8px; border-radius:6px; font-size:0.85rem;">Kode {target['KODE_PRODI']}</span> &nbsp;|&nbsp;
            <span style="background:{bg_input}; padding:2px 8px; border-radius:6px; font-size:0.85rem;">Portofolio: {target['JENIS_PORTOFOLIO']}</span>
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">PELUANG SIMULASI</div>
            <div class="result-hero-value">{peluang}%</div>
            <div class="badge-status {status_class}">{status_label}</div>
            <p style="color:{text_sub}; font-size:0.95rem; margin-top:16px;"><b>{kuota}</b> kursi tersedia diperebutkan <b>{peminat:,}</b> peminat</p>
        </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3, gap="medium")
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🪑 DAYA TAMPUNG</div>
                <div class="metric-val">{kuota} <span style="font-size:0.85rem; color:{text_sub}; font-weight:600;">kursi</span></div>
            </div>
            """, unsafe_allow_html=True)

        with mc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">👥 PEMINAT LALU</div>
                <div class="metric-val">{peminat:,} <span style="font-size:0.85rem; color:{text_sub}; font-weight:600;">siswa</span></div>
            </div>
            """, unsafe_allow_html=True)

        with mc3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🔥 RASIO PERSAINGAN</div>
                <div class="metric-val">1 : {rasio} <span style="font-size:0.85rem; color:{text_sub}; font-weight:600;">orang</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card">
            <h4 style="margin:0 0 8px 0; font-weight:700; color:{text_main};">💡 Apa artinya?</h4>
            <p style="color:{text_sub}; font-size:0.95rem; line-height:1.6; margin-bottom:16px;">
                Sekitar <b>{rasio} siswa</b> bersaing untuk memperebutkan 1 kursi. 
                Dengan peluang sebesar <b>{peluang}%</b>, persaingan jurusan ini tergolong <b>{status_label.split(' ')[1]}</b>.
            </p>
            <h4 style="margin:0 0 8px 0; font-weight:700; color:{text_main};">🎯 Apa yang bisa kamu lakukan?</h4>
            <p style="color:{text_sub}; font-size:0.95rem; line-height:1.6; margin:0;">
                Jurusan ini tergolong kompetitif. Pastikan pilihanmu sesuai dengan profil akademik dan pertimbangkan beberapa alternatif PTN/program studi di bawah ini sebagai opsi cadangan.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <h3 style="font-weight:800; color:{text_main}; margin-bottom:4px;">Bandingkan dengan jurusan lain</h3>
        <p style="color:{text_sub}; font-size:0.9rem; margin-bottom:1.5rem;">Lihat pilihan lain di {selected_ptn} dan temukan alternatif dengan tingkat persaingan berbeda.</p>
        """, unsafe_allow_html=True)

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
st.markdown(f"""
<div class="disclaimer-box">
    ⚠️ Hasil ini merupakan simulasi berdasarkan data peminat dan daya tampung yang tersedia, bukan jaminan kelulusan resmi.
</div>
""", unsafe_allow_html=True)
