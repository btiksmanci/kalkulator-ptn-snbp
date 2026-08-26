import html
import pandas as pd
import streamlit as st

# =========================================================
# KONFIGURASI
# =========================================================
st.set_page_config(
    page_title="Kalkulator PTN • Analisis Peluang",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# DESIGN SYSTEM + RESPONSIVE UI
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #f6f8fc;
    --surface: #ffffff;
    --surface-soft: #f8fafc;
    --text: #0f172a;
    --muted: #64748b;
    --muted-2: #94a3b8;
    --border: #e2e8f0;
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-soft: #eff6ff;
    --violet: #7c3aed;
    --success: #16a34a;
    --success-soft: #f0fdf4;
    --warning: #d97706;
    --warning-soft: #fffbeb;
    --danger: #dc2626;
    --danger-soft: #fef2f2;
    --shadow-sm: 0 1px 2px rgba(15, 23, 42, .04), 0 6px 18px rgba(15, 23, 42, .04);
    --shadow-md: 0 12px 35px rgba(37, 99, 235, .10);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: var(--bg);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit chrome where possible; keep app content intact. */
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* App header */
.app-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin: 0 0 2rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: .7rem;
    color: var(--text);
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -.02em;
}

.brand-mark {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: #fff;
    box-shadow: 0 8px 18px rgba(37, 99, 235, .20);
    font-size: 1.1rem;
}

.nav-note {
    color: var(--muted);
    font-size: .82rem;
    font-weight: 600;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #172554 0%, #1d4ed8 58%, #4f46e5 100%);
    border-radius: 28px;
    padding: 2.8rem;
    color: white;
    box-shadow: var(--shadow-md);
    margin-bottom: 1.25rem;
}

.hero:after {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    right: -130px;
    top: -180px;
    background: rgba(255,255,255,.08);
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .38rem .72rem;
    border-radius: 999px;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.16);
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.hero h1 {
    position: relative;
    z-index: 1;
    margin: 1rem 0 .7rem;
    color: #fff !important;
    font-size: clamp(2.1rem, 5vw, 4rem);
    line-height: 1.04;
    letter-spacing: -.045em;
    font-weight: 800;
}

.hero p {
    position: relative;
    z-index: 1;
    max-width: 650px;
    margin: 0;
    color: rgba(255,255,255,.82) !important;
    font-size: 1rem;
    line-height: 1.7;
}

/* Preview card */
.preview-wrap {
    display: flex;
    justify-content: flex-end;
    height: 100%;
    align-items: center;
}

.preview-card {
    position: relative;
    z-index: 2;
    width: min(100%, 320px);
    padding: 1.2rem;
    border-radius: 20px;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.20);
    backdrop-filter: blur(12px);
}

.preview-label {
    color: rgba(255,255,255,.72);
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .09em;
    text-transform: uppercase;
}

.preview-value {
    margin-top: .35rem;
    color: #fff;
    font-size: 2.6rem;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -.04em;
}

.preview-status {
    display: inline-flex;
    margin-top: .65rem;
    padding: .34rem .58rem;
    border-radius: 999px;
    background: rgba(255,255,255,.13);
    color: #fff;
    font-size: .72rem;
    font-weight: 700;
}

.preview-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-top: .85rem;
    padding-top: .75rem;
    border-top: 1px solid rgba(255,255,255,.13);
    color: rgba(255,255,255,.78);
    font-size: .76rem;
}

.preview-row strong { color: #fff; }

/* Selection section */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 1.35rem 1.4rem .8rem;
    box-shadow: var(--shadow-sm);
}

.section-heading {
    margin-bottom: .75rem;
}

.eyebrow {
    color: var(--primary);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .09em;
    text-transform: uppercase;
}

.section-title {
    margin: .28rem 0 0;
    color: var(--text);
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -.025em;
}

.step-pill {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    margin-bottom: .5rem;
    color: var(--muted);
    font-size: .72rem;
    font-weight: 700;
}

.step-number {
    display: inline-grid;
    place-items: center;
    width: 24px;
    height: 24px;
    border-radius: 8px;
    background: var(--primary-soft);
    color: var(--primary);
}

/* Native Streamlit inputs */
[data-testid="stSelectbox"] label {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: .86rem !important;
}

[data-testid="stSelectbox"] > div > div {
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    background: #fff !important;
    min-height: 50px !important;
    box-shadow: none !important;
}

[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #93c5fd !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.10) !important;
}

[data-testid="stSelectbox"] input {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Buttons */
div.stButton > button {
    min-height: 52px;
    border: 0 !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 18px rgba(37,99,235,.20) !important;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.03);
    box-shadow: 0 12px 24px rgba(37,99,235,.25) !important;
}

div.stButton > button:active {
    transform: translateY(0);
}

/* Result */
.result-top {
    margin: 2rem 0 1rem;
}

.result-eyebrow {
    color: var(--primary);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .10em;
    text-transform: uppercase;
}

.result-title {
    margin: .35rem 0 .25rem;
    color: var(--text);
    font-size: clamp(1.8rem, 4vw, 2.65rem);
    line-height: 1.1;
    letter-spacing: -.045em;
    font-weight: 800;
}

.result-subtitle {
    color: var(--muted);
    font-size: .95rem;
}

.badges {
    display: flex;
    flex-wrap: wrap;
    gap: .45rem;
    margin-top: .85rem;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: .3rem;
    padding: .4rem .68rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: #1d4ed8;
    border: 1px solid #dbeafe;
    font-size: .72rem;
    font-weight: 700;
}

/* Primary result */
.result-hero {
    position: relative;
    overflow: hidden;
    background: #fff;
    border: 1px solid #dbeafe;
    border-radius: 24px;
    padding: 1.75rem;
    box-shadow: var(--shadow-md);
}

.result-hero:after {
    content: "";
    position: absolute;
    right: -100px;
    bottom: -130px;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: #eff6ff;
}

.result-kicker {
    position: relative;
    z-index: 1;
    color: var(--muted);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
}

.result-number {
    position: relative;
    z-index: 1;
    margin: .35rem 0 .35rem;
    color: var(--primary);
    font-size: clamp(3.3rem, 8vw, 5rem);
    line-height: .98;
    font-weight: 800;
    letter-spacing: -.06em;
}

.result-number span {
    font-size: 1.15rem;
    letter-spacing: 0;
    color: var(--muted);
    font-weight: 700;
}

.status-chip {
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .42rem .72rem;
    border-radius: 999px;
    font-size: .74rem;
    font-weight: 800;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
}

.result-context {
    position: relative;
    z-index: 1;
    margin-top: .85rem;
    color: var(--muted);
    font-size: .82rem;
    line-height: 1.6;
}

/* Supporting metrics */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: .8rem;
    margin-top: .8rem;
}

.metric-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1rem;
}

.metric-icon {
    color: var(--muted);
    font-size: .78rem;
    font-weight: 800;
}

.metric-label {
    margin-top: .45rem;
    color: var(--muted);
    font-size: .72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .06em;
}

.metric-value {
    margin-top: .22rem;
    color: var(--text);
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -.035em;
}

.metric-value small {
    color: var(--muted);
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: 0;
}

/* Insight */
.insight {
    margin: 1rem 0;
    padding: 1.1rem 1.2rem;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: #fff;
}

.insight.warning { background: var(--warning-soft); border-color: #fde68a; }
.insight.danger { background: var(--danger-soft); border-color: #fecaca; }
.insight.success { background: var(--success-soft); border-color: #bbf7d0; }
.insight.info { background: #eff6ff; border-color: #bfdbfe; }

.insight-title {
    display: flex;
    align-items: center;
    gap: .5rem;
    color: var(--text);
    font-size: 1rem;
    font-weight: 800;
}

.insight p {
    margin: .45rem 0 0;
    color: var(--muted);
    font-size: .84rem;
    line-height: 1.65;
}

/* Comparison */
.comparison-heading {
    margin-top: 2rem;
}

.comparison-heading h2 {
    margin: .3rem 0 .25rem;
    color: var(--text);
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -.03em;
}

.comparison-heading p {
    margin: 0;
    color: var(--muted);
    font-size: .84rem;
}

.comparison-shell {
    margin-top: .85rem;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
}

/* HTML comparison table for better control */
.comparison-table-wrap {
    overflow-x: auto;
}

.comparison-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 820px;
}

.comparison-table th {
    padding: .85rem 1rem;
    text-align: left;
    background: #f8fafc;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .06em;
    text-transform: uppercase;
}

.comparison-table td {
    padding: .9rem 1rem;
    color: #334155;
    border-bottom: 1px solid #eef2f7;
    font-size: .78rem;
    vertical-align: middle;
}

.comparison-table tr:last-child td { border-bottom: 0; }
.comparison-table tr.current { background: #eff6ff; }
.comparison-table tr:hover { background: #f8fbff; }

.program-name {
    color: var(--text);
    font-weight: 700;
    line-height: 1.4;
}

.program-meta {
    margin-top: .2rem;
    color: var(--muted-2);
    font-size: .68rem;
}

.opportunity {
    color: var(--primary);
    font-weight: 800;
}

.ratio { color: var(--text); font-weight: 700; }

.mini-bar {
    width: 90px;
    height: 5px;
    margin-top: .35rem;
    overflow: hidden;
    border-radius: 999px;
    background: #e2e8f0;
}

.mini-bar > span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
}

.you-badge {
    display: inline-flex;
    margin-left: .4rem;
    padding: .18rem .42rem;
    border-radius: 999px;
    background: #dbeafe;
    color: #1d4ed8;
    font-size: .6rem;
    font-weight: 800;
    vertical-align: middle;
}

/* Mobile comparison cards */
.mobile-comparison { display: none; }

.mobile-program-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: .65rem;
}

.mobile-program-card.current {
    background: #eff6ff;
    border-color: #bfdbfe;
}

.mobile-program-title {
    color: var(--text);
    font-size: .88rem;
    line-height: 1.4;
    font-weight: 800;
}

.mobile-program-meta {
    margin-top: .25rem;
    color: var(--muted);
    font-size: .68rem;
}

.mobile-metrics {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: .55rem;
    margin-top: .8rem;
}

.mobile-metric {
    padding: .65rem;
    border-radius: 12px;
    background: rgba(248,250,252,.9);
}

.mobile-metric-label {
    color: var(--muted);
    font-size: .62rem;
    font-weight: 700;
    text-transform: uppercase;
}

.mobile-metric-value {
    margin-top: .18rem;
    color: var(--text);
    font-size: .9rem;
    font-weight: 800;
}

/* Footer */
.app-footer {
    margin-top: 2rem;
    padding-top: 1.1rem;
    border-top: 1px solid var(--border);
    color: var(--muted-2);
    font-size: .7rem;
    text-align: center;
}

/* Responsive */
@media (max-width: 900px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .hero { padding: 2rem; }
    .preview-wrap { justify-content: flex-start; margin-top: 1.5rem; }
}

@media (max-width: 700px) {
    .block-container { padding-top: .8rem; }
    .app-nav { margin-bottom: 1rem; }
    .nav-note { display: none; }
    .brand-mark { width: 34px; height: 34px; border-radius: 10px; }
    .hero { border-radius: 22px; padding: 1.5rem; }
    .hero h1 { font-size: 2.15rem; }
    .hero p { font-size: .88rem; }
    .preview-card { width: 100%; }
    .section-card { border-radius: 18px; padding: 1rem .95rem .65rem; }
    .metric-grid { grid-template-columns: 1fr; }
    .result-hero { border-radius: 20px; padding: 1.25rem; }
    .result-number { font-size: 3.7rem; }
    .comparison-table-wrap { display: none; }
    .mobile-comparison { display: block; padding: .8rem; }
    .desktop-only { display: none !important; }
}

@media (min-width: 701px) {
    .mobile-only { display: none !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DATA
# =========================================================
@st.cache_data

def load_data():
    df = pd.read_csv("MASTER_all_prodi.csv", sep=";", on_bad_lines="skip")
    df["DAYA_TAMPUNG_2026"] = pd.to_numeric(
        df["DAYA_TAMPUNG_2026"], errors="coerce"
    ).fillna(0).astype(int)
    df["PEMINAT_2025"] = pd.to_numeric(
        df["PEMINAT_2025"], errors="coerce"
    ).fillna(0).astype(int)

    df["PELUANG_PERSEN"] = df.apply(
        lambda r: round(
            (r["DAYA_TAMPUNG_2026"] / r["PEMINAT_2025"]) * 100, 2
        )
        if r["PEMINAT_2025"] > 0
        else 0.0,
        axis=1,
    )
    df["RASIO_PERSAINGAN"] = df.apply(
        lambda r: int(round(r["PEMINAT_2025"] / r["DAYA_TAMPUNG_2026"]))
        if r["DAYA_TAMPUNG_2026"] > 0
        else 0,
        axis=1,
    )
    return df


df = load_data()

# =========================================================
# HELPERS
# =========================================================
def fmt_int(value):
    return f"{int(value):,}".replace(",", ".")


def fmt_percent(value):
    return f"{float(value):.2f}%".replace(".", ",", 1)


def competition_meta(peluang):
    if peluang < 5.0:
        return {
            "label": "Sangat Ketat",
            "emoji": "🔴",
            "kind": "danger",
            "color": "#dc2626",
            "soft": "#fef2f2",
            "border": "#fecaca",
        }
    if peluang <= 15.0:
        return {
            "label": "Ketat / Tinggi",
            "emoji": "🟠",
            "kind": "warning",
            "color": "#d97706",
            "soft": "#fffbeb",
            "border": "#fde68a",
        }
    if peluang <= 30.0:
        return {
            "label": "Sedang / Moderat",
            "emoji": "🟡",
            "kind": "info",
            "color": "#2563eb",
            "soft": "#eff6ff",
            "border": "#bfdbfe",
        }
    return {
        "label": "Peluang Besar",
        "emoji": "🟢",
        "kind": "success",
        "color": "#16a34a",
        "soft": "#f0fdf4",
        "border": "#bbf7d0",
    }


def insight_copy(peluang, rasio, peminat):
    if peminat == 0:
        return (
            "info",
            "Belum ada data peminat",
            "Data peminat belum tercatat. Gunakan hasil ini sebagai informasi awal, bukan sebagai jaminan kelulusan.",
        )
    if peluang < 5.0:
        return (
            "danger",
            "Persaingannya sangat ketat",
            f"Peluang simulasi {fmt_percent(peluang)}. Sekitar {rasio} siswa bersaing untuk setiap 1 kursi yang tersedia.",
        )
    if peluang <= 15.0:
        return (
            "warning",
            "Persaingannya cukup ketat",
            f"Peluang simulasi {fmt_percent(peluang)}. Sekitar {rasio} siswa bersaing untuk setiap 1 kursi yang tersedia.",
        )
    if peluang <= 30.0:
        return (
            "info",
            "Persaingannya berada di level sedang",
            f"Peluang simulasi {fmt_percent(peluang)} dengan rasio sekitar 1 kursi : {rasio} siswa.",
        )
    return (
        "success",
        "Peluangnya relatif lebih besar",
        f"Peluang simulasi {fmt_percent(peluang)} dengan rasio sekitar 1 kursi : {rasio} siswa.",
    )


def render_comparison_table(alt_df, selected_prodi):
    # Keep the same ordering as the original app: highest opportunity first.
    rows = []
    max_opportunity = max(float(alt_df["PELUANG_PERSEN"].max()), 1.0)

    for _, row in alt_df.iterrows():
        name = html.escape(str(row["NAMA_PRODI"]))
        jenjang = html.escape(str(row["JENJANG"]))
        kode = html.escape(str(row["KODE_PRODI"]))
        opportunity = float(row["PELUANG_PERSEN"])
        ratio = int(row["RASIO_PERSAINGAN"])
        quota = int(row["DAYA_TAMPUNG_2026"])
        applicants = int(row["PEMINAT_2025"])
        is_current = str(row["NAMA_PRODI"]) == str(selected_prodi)
        current_badge = '<span class="you-badge">PILIHANMU</span>' if is_current else ""
        width = max(3, min(100, opportunity / max_opportunity * 100))

        rows.append(
            f"""
            <tr class="{'current' if is_current else ''}">
                <td>
                    <div class="program-name">{name}{current_badge}</div>
                    <div class="program-meta">{jenjang} · {kode}</div>
                </td>
                <td>
                    <div class="opportunity">{fmt_percent(opportunity)}</div>
                    <div class="mini-bar"><span style="width:{width:.1f}%"></span></div>
                </td>
                <td><span class="ratio">1 : {ratio}</span></td>
                <td>{fmt_int(quota)} kursi</td>
                <td>{fmt_int(applicants)} siswa</td>
            </tr>
            """
        )

    table = f"""
    <div class="comparison-shell desktop-only">
      <div class="comparison-table-wrap">
        <table class="comparison-table">
          <thead>
            <tr>
              <th>Program Studi</th>
              <th>Peluang</th>
              <th>Rasio</th>
              <th>Daya Tampung</th>
              <th>Peminat 2025</th>
            </tr>
          </thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </div>
    """
    st.markdown(table, unsafe_allow_html=True)

    mobile_cards = []
    for _, row in alt_df.iterrows():
        name = html.escape(str(row["NAMA_PRODI"]))
        jenjang = html.escape(str(row["JENJANG"]))
        kode = html.escape(str(row["KODE_PRODI"]))
        opportunity = float(row["PELUANG_PERSEN"])
        ratio = int(row["RASIO_PERSAINGAN"])
        quota = int(row["DAYA_TAMPUNG_2026"])
        applicants = int(row["PEMINAT_2025"])
        is_current = str(row["NAMA_PRODI"]) == str(selected_prodi)
        badge = '<span class="you-badge">PILIHANMU</span>' if is_current else ""
        mobile_cards.append(
            f"""
            <div class="mobile-program-card {'current' if is_current else ''}">
              <div class="mobile-program-title">{name} {badge}</div>
              <div class="mobile-program-meta">{jenjang} · {kode}</div>
              <div class="mobile-metrics">
                <div class="mobile-metric">
                  <div class="mobile-metric-label">Peluang</div>
                  <div class="mobile-metric-value">{fmt_percent(opportunity)}</div>
                </div>
                <div class="mobile-metric">
                  <div class="mobile-metric-label">Rasio</div>
                  <div class="mobile-metric-value">1 : {ratio}</div>
                </div>
                <div class="mobile-metric">
                  <div class="mobile-metric-label">Kursi</div>
                  <div class="mobile-metric-value">{fmt_int(quota)}</div>
                </div>
                <div class="mobile-metric">
                  <div class="mobile-metric-label">Peminat</div>
                  <div class="mobile-metric-value">{fmt_int(applicants)}</div>
                </div>
              </div>
            </div>
            """
        )

    st.markdown(
        f'<div class="mobile-comparison mobile-only">{"".join(mobile_cards)}</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# NAVIGATION
# =========================================================
st.markdown(
    """
<div class="app-nav">
  <div class="brand">
    <div class="brand-mark">🎓</div>
    <div>PTN<span style="color:#2563eb">Match</span></div>
  </div>
  <div class="nav-note">Analisis peluang & persaingan program studi</div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HOMEPAGE
# =========================================================
list_ptn = sorted(df["NAMA_PTN"].dropna().unique())

selected_ptn = st.session_state.get("selected_ptn_ui")
selected_prodi = st.session_state.get("selected_prodi_ui")

hero_col, preview_col = st.columns([1.55, 0.75], gap="large")
with hero_col:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">✦ SNBP · ANALISIS DATA</div>
          <h1>Seberapa kompetitif jurusan impianmu?</h1>
          <p>Cek peluang dan rasio persaingan PTN berdasarkan data daya tampung dan peminat. Pilih kampus, pilih jurusan, lalu lihat gambaran persaingannya.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with preview_col:
    preview_data = df.sort_values("PELUANG_PERSEN", ascending=False).iloc[0] if not df.empty else None
    if preview_data is not None:
        preview_opportunity = fmt_percent(preview_data["PELUANG_PERSEN"])
        preview_quota = fmt_int(preview_data["DAYA_TAMPUNG_2026"])
        preview_applicants = fmt_int(preview_data["PEMINAT_2025"])
    else:
        preview_opportunity = "—"
        preview_quota = "—"
        preview_applicants = "—"

    st.markdown(
        f"""
        <div class="preview-wrap">
          <div class="preview-card">
            <div class="preview-label">Contoh tampilan hasil</div>
            <div class="preview-value">{preview_opportunity}</div>
            <div class="preview-status">● Peluang simulasi</div>
            <div class="preview-row"><span>Daya tampung</span><strong>{preview_quota}</strong></div>
            <div class="preview-row"><span>Peminat</span><strong>{preview_applicants}</strong></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-heading">
  <div class="eyebrow">Mulai analisis</div>
  <div class="section-title">Cari PTN dan jurusan yang kamu incar</div>
</div>
""",
    unsafe_allow_html=True,
)

col_search1, col_search2 = st.columns(2, gap="large")
with col_search1:
    st.markdown('<div class="step-pill"><span class="step-number">01</span> UNIVERSITAS</div>', unsafe_allow_html=True)
    new_selected_ptn = st.selectbox(
        "Mau kuliah di mana?",
        list_ptn,
        index=None,
        placeholder="Cari atau pilih PTN...",
        key="selected_ptn_ui",
        label_visibility="visible",
    )

if new_selected_ptn:
    filtered_prodi_df = df[df["NAMA_PTN"] == new_selected_ptn]
    list_prodi = sorted(filtered_prodi_df["NAMA_PRODI"].dropna().unique())
else:
    filtered_prodi_df = pd.DataFrame()
    list_prodi = []

with col_search2:
    st.markdown('<div class="step-pill"><span class="step-number">02</span> PROGRAM STUDI</div>', unsafe_allow_html=True)
    new_selected_prodi = st.selectbox(
        "Jurusan yang kamu incar?",
        list_prodi,
        index=None,
        placeholder="Cari atau pilih jurusan...",
        disabled=(not new_selected_ptn),
        key="selected_prodi_ui",
        label_visibility="visible",
    )

st.markdown('<div style="height:.55rem"></div>', unsafe_allow_html=True)
btn_hitung = st.button("Lihat Peluang Saya  →", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RESULT
# =========================================================
if btn_hitung:
    if not new_selected_ptn or not new_selected_prodi:
        st.markdown(
            """
            <div class="insight warning">
              <div class="insight-title">⚠️ Pilihanmu belum lengkap</div>
              <p>Pilih universitas dan program studi terlebih dahulu agar hasil analisis bisa ditampilkan.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        target = filtered_prodi_df[filtered_prodi_df["NAMA_PRODI"] == new_selected_prodi].iloc[0]

        kuota = target["DAYA_TAMPUNG_2026"]
        peminat = target["PEMINAT_2025"]
        peluang = target["PELUANG_PERSEN"]
        rasio = target["RASIO_PERSAINGAN"]
        meta = competition_meta(peluang)
        insight_kind, insight_title, insight_text = insight_copy(peluang, rasio, peminat)

        st.markdown(
            f"""
            <div class="result-top">
              <div class="result-eyebrow">Hasil analisis</div>
              <div class="result-title">{html.escape(str(target['NAMA_PRODI']))}</div>
              <div class="result-subtitle">{html.escape(str(target['JENJANG']))} · {html.escape(str(target['NAMA_PTN']))}</div>
              <div class="badges">
                <span class="badge">🏛️ {html.escape(str(target['NAMA_PTN']))}</span>
                <span class="badge">🔑 Kode {html.escape(str(target['KODE_PRODI']))}</span>
                <span class="badge">🎨 Portofolio: {html.escape(str(target['JENIS_PORTOFOLIO']))}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Primary result + supporting metrics
        st.markdown(
            f"""
            <div class="result-hero">
              <div class="result-kicker">Peluang simulasi</div>
              <div class="result-number">{fmt_percent(peluang)}</div>
              <div class="status-chip" style="background:{meta['soft']}; color:{meta['color']}; border:1px solid {meta['border']};">
                <span class="status-dot" style="background:{meta['color']};"></span>
                {meta['emoji']} {meta['label']}
              </div>
              <div class="result-context">Berdasarkan <strong>{fmt_int(kuota)} kursi</strong> dan <strong>{fmt_int(peminat)} peminat</strong> pada data yang tersedia.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="metric-grid">
              <div class="metric-card">
                <div class="metric-icon">▦</div>
                <div class="metric-label">Daya tampung</div>
                <div class="metric-value">{fmt_int(kuota)} <small>kursi</small></div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">◉</div>
                <div class="metric-label">Peminat 2025</div>
                <div class="metric-value">{fmt_int(peminat)} <small>siswa</small></div>
              </div>
              <div class="metric-card">
                <div class="metric-icon">↔</div>
                <div class="metric-label">Rasio persaingan</div>
                <div class="metric-value">1 : {int(rasio)} <small>siswa/kursi</small></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Insight
        st.markdown(
            f"""
            <div class="insight {insight_kind}">
              <div class="insight-title">💡 {insight_title}</div>
              <p>{insight_text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Action guidance — descriptive, not a guarantee.
        if peminat == 0:
            action = "Data persaingan belum tersedia. Gunakan informasi ini sebagai gambaran awal dan cek kembali data resmi saat tersedia."
        elif peluang < 5:
            action = "Pilihan ini sangat kompetitif. Jadikan hasil sebagai bahan pertimbangan dan siapkan beberapa alternatif yang sesuai dengan targetmu."
        elif peluang <= 15:
            action = "Pilihan ini cukup kompetitif. Bandingkan dengan prodi lain di PTN yang sama untuk melihat alternatif dengan rasio yang berbeda."
        elif peluang <= 30:
            action = "Persaingannya berada di level sedang. Tetap bandingkan dengan pilihan lain agar kamu punya strategi yang lebih fleksibel."
        else:
            action = "Peluangnya relatif lebih besar dibanding banyak pilihan lain. Tetap gunakan data ini sebagai simulasi, bukan kepastian kelulusan."

        st.markdown(
            f"""
            <div class="insight info">
              <div class="insight-title">🎯 Apa artinya untukmu?</div>
              <p>{action}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Comparison
        st.markdown(
            f"""
            <div class="comparison-heading">
              <div class="eyebrow">Eksplorasi pilihan</div>
              <h2>Bandingkan dengan jurusan lain</h2>
              <p>Lihat program studi lain di {html.escape(str(new_selected_ptn))}, diurutkan dari peluang tertinggi ke yang paling ketat.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        alt_df = filtered_prodi_df.sort_values(by="PELUANG_PERSEN", ascending=False)
        render_comparison_table(alt_df, new_selected_prodi)

        st.markdown(
            """
            <div class="app-footer">
              Hasil ini merupakan simulasi berdasarkan data peminat dan daya tampung yang tersedia, bukan jaminan kelulusan.
            </div>
            """,
            unsafe_allow_html=True,
        )
