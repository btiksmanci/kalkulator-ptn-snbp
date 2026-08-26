import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="PTNMatch — Analisis Peluang & Rasio PTN",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CLEAN & STABLE MODERN LIGHT THEME CSS
# ==========================================
CLEAN_UI_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* BASE APP LAYOUT */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }
    
    #MainMenu, footer, header, [data-testid="stHeader"] { 
        display: none !important; 
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 800px !important;
    }

    /* BRANDING NAVBAR */
    .app-navbar {
        display: flex;
        align-items: center;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .app-brand {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0F172A;
    }
    .app-brand span { color: #2563EB; }

    /* HERO SECTION */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero-badge {
        display: inline-block;
        background: #EFF6FF;
        color: #2563EB;
        padding: 6px 16px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
        border: 1px solid #DBEAFE;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.25;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* STEP HEADER CARDS */
    .step-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    .step-badge {
        background: #EFF6FF;
        color: #2563EB;
        font-size: 0.7rem;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .step-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #0F172A;
    }
    .step-sub {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 2px;
    }

    /* BUTTON CUSTOMIZATION */
    div.stButton > button {
        background: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        height: 48px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        background: #1D4ED8 !important;
    }

    /* RESULT HERO CARD */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 1.5rem 0 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .result-sub {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .result-val {
        font-size: 3.5rem;
        font-weight: 800;
        color: #2563EB;
        line-height: 1.1;
        margin: 8px 0;
    }
    
    .badge-status {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .status-ketat { background: #FEF2F2; color: #EF4444; border: 1px solid #FCA5A5; }
    .status-sedang { background: #FFFBEB; color: #D97706; border: 1px solid #FCD34D; }
    .status-longgar { background: #F0FDF4; color: #16A34A; border: 1px solid #86EFAC; }

    /* METRIC CARDS */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }
    .metric-head {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
    }
    .metric-body {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 2px;
    }

    /* INSIGHT BOX */
    .insight-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #475569;
        line-height: 1.5;
    }

    /* CUSTOM STABLE HTML TABLE */
    .custom-table-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow-x: auto;
        margin-top: 10px;
    }
    table.custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
        text-align: left;
    }
    table.custom-table th {
        background-color: #F8FAFC;
        color: #475569;
        font-weight: 700;
        padding: 12px 14px;
        border-bottom: 1px solid #E2E8F0;
    }
    table.custom-table td {
        padding: 12px 14px;
        border-bottom: 1px solid #F1F5F9;
        color: #0F172A;
    }
    table.custom-table tr:last-child td {
        border-bottom: none;
    }
    table.custom-table tr:hover {
        background-color: #F8FAFC;
    }

    .disclaimer {
        text-align: center;
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E2E8F0;
    }
</style>
"""
st.markdown(CLEAN_UI_CSS, unsafe_allow_html=True)

# ==========================================
# 3. LOAD DATA
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
# 4. HEADER & HERO
# ==========================================
st.markdown("""
<div class="app-navbar">
    <div class="app-brand">🎓 PTN<span>Match</span></div>
</div>
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
    <div class="step-box">
        <span class="step-badge">STEP 01</span>
        <span class="step-title">UNIVERSITAS</span>
        <div class="step-sub">Mau kuliah di mana?</div>
    </div>
    """, unsafe_allow_html=True)
    list_ptn = sorted(df['NAMA_PTN'].unique())
    selected_ptn = st.selectbox("Pilih PTN", list_ptn, index=None, placeholder="🔍 Cari universitas...", label_visibility="collapsed")

if selected_ptn:
    filtered_prodi_df = df[df['NAMA_PTN'] == selected_ptn]
    list_prodi = sorted(filtered_prodi_df['NAMA_PRODI'].unique())
else:
    filtered_prodi_df = pd.DataFrame()
    list_prodi = []

with col_s2:
    st.markdown("""
    <div class="step-box">
        <span class="step-badge">STEP 02</span>
        <span class="step-title">PROGRAM STUDI</span>
        <div class="step-sub">Jurusan yang kamu incar?</div>
    </div>
    """, unsafe_allow_html=True)
    selected_prodi = st.selectbox(
        "Pilih Prodi", 
        list_prodi, 
        index=None, 
        placeholder="🔍 Cari prodi..." if selected_ptn else "Pilih PTN dahulu",
        disabled=(not selected_ptn),
        label_visibility="collapsed"
    )

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
        <div class="result-card">
            <div class="result-sub">{target['NAMA_PTN']} — {target['NAMA_PRODI']}</div>
            <div class="result-val">{peluang}%</div>
            <div class="badge-status {status_class}">{status_label}</div>
            <p style="color:#64748B; font-size:0.85rem; margin-top:10px; margin-bottom:0;">
                <b>{kuota}</b> kuota diperebutkan oleh <b>{peminat:,}</b> peminat
            </p>
        </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3, gap="small")
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-head">🪑 KUOTA 2026</div>
                <div class="metric-body">{kuota}</div>
            </div>
            """, unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-head">👥 PEMINAT 2025</div>
                <div class="metric-body">{peminat:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-head">🔥 RASIO</div>
                <div class="metric-body">1 : {rasio}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-box">
            <b style="color:#0F172A;">💡 Analisis Peluang:</b><br>
            Rasio persaingan prodi ini adalah <b>1 : {rasio}</b> (Setiap 1 kursi diperebutkan oleh {rasio} pendaftar). 
            Pertimbangkan prodi alternatif dengan rasio lebih longgar di bawah ini sebagai opsi aman.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<h4 style="font-size:0.95rem; font-weight:700; color:#0F172A; margin-top:1.5rem;">Opsi Prodi Lain di PTN Ini</h4>""", unsafe_allow_html=True)

        # TABEL NATIVE HTML UNTUK TAMPILAN 100% STABIL & BEBAS DARK-MODE BUG
        alt_df = filtered_prodi_df.sort_values(by='PELUANG_PERSEN', ascending=False)
        
        table_html = """
        <div class="custom-table-container">
            <table class="custom-table">
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
            table_html += f"""
                <tr>
                    <td><b>{row['KODE_PRODI']}</b></td>
                    <td>{row['NAMA_PRODI']}</td>
                    <td>{row['JENJANG']}</td>
                    <td>{row['DAYA_TAMPUNG_2026']} Kursi</td>
                    <td>{row['PEMINAT_2025']:,}</td>
                    <td><b>{row['PELUANG_PERSEN']}%</b></td>
                    <td>1 : {row['RASIO_PERSAINGAN']}</td>
                </tr>
            """
        table_html += """
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="disclaimer">
    ⚠️ Data berdasarkan simulasi estimasi resmi. Hasil ini bukan jaminan kelulusan mutlak.
</div>
""", unsafe_allow_html=True)
