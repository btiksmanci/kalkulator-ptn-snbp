import html
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Kalkulator PTN • Analisis Peluang",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# DESIGN SYSTEM
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --bg:#f7f8fc;
  --surface:#ffffff;
  --surface-2:#f8fafc;
  --text:#172033;
  --muted:#667085;
  --border:#e7eaf0;
  --primary:#2857d9;
  --primary-dark:#1f46b5;
  --primary-soft:#eef4ff;
  --green:#159447;
  --green-soft:#ecfdf3;
  --yellow:#c77800;
  --yellow-soft:#fff8e6;
  --red:#d14343;
  --red-soft:#fff0f0;
  --shadow:0 8px 30px rgba(20,35,70,.06);
}

html, body, [class*="css"] { font-family:'Plus Jakarta Sans', sans-serif; }
.stApp { background:var(--bg); color:var(--text); }
.block-container { max-width:1180px; padding:22px 28px 44px; }
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }

/* ---------- top bar ---------- */
.appbar { display:flex; align-items:center; justify-content:space-between; margin-bottom:28px; }
.brand { display:flex; align-items:center; gap:10px; color:var(--text); font-weight:800; font-size:17px; letter-spacing:-.02em; }
.brand-icon { width:38px; height:38px; display:grid; place-items:center; border-radius:12px; background:var(--primary); color:#fff; box-shadow:0 7px 18px rgba(40,87,217,.22); font-size:18px; }
.appbar-note { color:var(--muted); font-size:12px; font-weight:600; }

/* ---------- hero ---------- */
.hero-wrap { background:linear-gradient(135deg,#1e3a8a 0%,#2857d9 58%,#3d73e8 100%); border-radius:24px; padding:34px; color:#fff; min-height:300px; box-shadow:0 16px 38px rgba(40,87,217,.14); position:relative; overflow:hidden; }
.hero-wrap:after { content:""; position:absolute; width:330px; height:330px; border-radius:50%; background:rgba(255,255,255,.08); right:-120px; top:-150px; }
.hero-kicker { position:relative; z-index:1; display:inline-flex; padding:7px 11px; border-radius:999px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.16); color:rgba(255,255,255,.9); font-size:10px; font-weight:800; letter-spacing:.09em; }
.hero-title { position:relative; z-index:1; margin:18px 0 12px; color:#fff; font-size:clamp(34px,4.2vw,54px); line-height:1.03; font-weight:800; letter-spacing:-.045em; max-width:720px; }
.hero-copy { position:relative; z-index:1; margin:0; max-width:670px; color:rgba(255,255,255,.82); font-size:14px; line-height:1.7; }

.preview { background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.2); border-radius:20px; padding:22px; color:#fff; box-shadow:0 10px 30px rgba(0,0,0,.08); }
.preview-label { font-size:10px; font-weight:800; letter-spacing:.08em; color:rgba(255,255,255,.72); text-transform:uppercase; }
.preview-number { margin-top:7px; font-size:48px; line-height:1; font-weight:800; letter-spacing:-.05em; }
.preview-status { margin-top:10px; display:inline-block; padding:6px 9px; border-radius:999px; background:rgba(255,255,255,.13); font-size:10px; font-weight:700; }
.preview-line { display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,.14); margin-top:15px; padding-top:12px; font-size:11px; color:rgba(255,255,255,.72); }
.preview-line strong { color:#fff; }

/* ---------- selection ---------- */
.section-space { height:18px; }
.section-head { margin:0 0 14px; }
.eyebrow { color:var(--primary); font-size:10px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
.section-title { margin-top:5px; color:var(--text); font-size:22px; font-weight:800; letter-spacing:-.03em; }
.section-copy { margin-top:5px; color:var(--muted); font-size:13px; line-height:1.6; }
.step-label { margin-bottom:7px; display:flex; align-items:center; gap:7px; color:var(--text); font-size:11px; font-weight:800; letter-spacing:.04em; text-transform:uppercase; }
.step-num { width:24px; height:24px; display:grid; place-items:center; border-radius:8px; background:var(--primary-soft); color:var(--primary); font-size:10px; }

[data-testid="stSelectbox"] label { color:var(--text)!important; font-size:13px!important; font-weight:700!important; }
[data-testid="stSelectbox"] > div > div { min-height:48px!important; border-radius:12px!important; border:1px solid var(--border)!important; background:#fff!important; box-shadow:none!important; }
[data-testid="stSelectbox"] > div > div:focus-within { border-color:#9bb8ff!important; box-shadow:0 0 0 3px rgba(40,87,217,.10)!important; }
[data-testid="stSelectbox"] input { font-family:'Plus Jakarta Sans',sans-serif!important; }

div.stButton > button { min-height:50px; border:0!important; border-radius:12px!important; background:var(--primary)!important; color:#fff!important; font-family:'Plus Jakarta Sans',sans-serif!important; font-size:13px!important; font-weight:800!important; box-shadow:0 8px 18px rgba(40,87,217,.18)!important; }
div.stButton > button:hover { background:var(--primary-dark)!important; }

/* ---------- result ---------- */
.result-header { padding:8px 0 18px; }
.result-title { margin-top:6px; color:var(--text); font-size:clamp(28px,4vw,42px); line-height:1.08; font-weight:800; letter-spacing:-.045em; }
.result-subtitle { margin-top:6px; color:var(--muted); font-size:13px; }
.badges { display:flex; flex-wrap:wrap; gap:7px; margin-top:13px; }
.badge { display:inline-flex; align-items:center; padding:6px 9px; border-radius:999px; background:#fff; border:1px solid var(--border); color:#526070; font-size:10px; font-weight:700; }

.result-card { background:#fff; border:1px solid #dce6ff; border-radius:22px; padding:28px; box-shadow:var(--shadow); }
.result-label { color:var(--muted); font-size:10px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
.result-number { margin-top:5px; color:var(--primary); font-size:clamp(58px,8vw,82px); line-height:.98; font-weight:800; letter-spacing:-.065em; }
.status { display:inline-flex; align-items:center; gap:7px; margin-top:12px; padding:7px 11px; border-radius:999px; font-size:11px; font-weight:800; }
.dot { width:7px; height:7px; border-radius:50%; }
.result-context { margin-top:14px; color:var(--muted); font-size:12px; line-height:1.65; }

.metric { background:#fff; border:1px solid var(--border); border-radius:16px; padding:17px; min-height:108px; }
.metric-label { color:var(--muted); font-size:10px; font-weight:800; letter-spacing:.06em; text-transform:uppercase; }
.metric-value { margin-top:8px; color:var(--text); font-size:24px; line-height:1.1; font-weight:800; letter-spacing:-.035em; }
.metric-unit { color:var(--muted); font-size:11px; font-weight:700; }

.insight { border-radius:17px; padding:17px 19px; border:1px solid var(--border); }
.insight-title { color:var(--text); font-size:14px; font-weight:800; }
.insight-copy { margin-top:5px; color:var(--muted); font-size:12px; line-height:1.65; }
.insight.warning { background:var(--yellow-soft); border-color:#f2d58b; }
.insight.danger { background:var(--red-soft); border-color:#efb4b4; }
.insight.success { background:var(--green-soft); border-color:#b7e3c7; }
.insight.info { background:var(--primary-soft); border-color:#c8d8ff; }

.compare-head { margin-top:28px; padding-bottom:10px; }
.compare-title { margin-top:5px; font-size:22px; font-weight:800; letter-spacing:-.03em; }
.compare-copy { margin-top:5px; color:var(--muted); font-size:12px; line-height:1.6; }

/* custom table */
.table-shell { background:#fff; border:1px solid var(--border); border-radius:16px; overflow:hidden; }
.table-scroll { overflow-x:auto; }
table.ptn-table { width:100%; border-collapse:collapse; min-width:760px; }
table.ptn-table th { padding:12px 14px; background:#f8fafc; color:#7a8494; border-bottom:1px solid var(--border); text-align:left; font-size:9px; font-weight:800; letter-spacing:.07em; text-transform:uppercase; }
table.ptn-table td { padding:13px 14px; border-bottom:1px solid #eef1f5; color:#475467; font-size:11px; vertical-align:middle; }
table.ptn-table tr:last-child td { border-bottom:0; }
table.ptn-table tr.current td { background:#f2f6ff; }
.program { color:var(--text); font-weight:700; line-height:1.4; }
.meta { margin-top:3px; color:#98a2b3; font-size:9px; }
.current-tag { display:inline-block; margin-left:6px; padding:3px 6px; border-radius:999px; background:#dce8ff; color:#3159bd; font-size:8px; font-weight:800; }
.opp { color:var(--primary); font-weight:800; }
.ratio { color:var(--text); font-weight:800; }
.bar { width:80px; height:4px; margin-top:5px; border-radius:999px; background:#e9edf4; overflow:hidden; }
.bar span { display:block; height:100%; border-radius:999px; background:var(--primary); }

.footer-note { margin-top:24px; padding-top:15px; border-top:1px solid var(--border); color:#98a2b3; text-align:center; font-size:10px; line-height:1.6; }

/* Keep markdown from creating weird inherited spacing */
.element-container:has(.appbar), .element-container:has(.hero-wrap), .element-container:has(.result-card) { margin-bottom:0!important; }

@media(max-width:900px){
  .block-container { padding:18px 18px 36px; }
  .hero-wrap { padding:26px; }
}
@media(max-width:640px){
  .block-container { padding:14px 14px 30px; }
  .appbar { margin-bottom:18px; }
  .appbar-note { display:none; }
  .hero-wrap { border-radius:20px; padding:22px 20px; min-height:0; }
  .hero-title { font-size:35px; }
  .hero-copy { font-size:13px; }
  .preview { margin-top:4px; }
  .result-card { border-radius:18px; padding:22px; }
  .result-number { font-size:58px; }
  .metric { min-height:96px; }
  .compare-title { font-size:20px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DATA — unchanged logic
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("MASTER_all_prodi.csv", sep=";", on_bad_lines="skip")
    df["DAYA_TAMPUNG_2026"] = pd.to_numeric(df["DAYA_TAMPUNG_2026"], errors="coerce").fillna(0).astype(int)
    df["PEMINAT_2025"] = pd.to_numeric(df["PEMINAT_2025"], errors="coerce").fillna(0).astype(int)
    df["PELUANG_PERSEN"] = df.apply(
        lambda r: round((r["DAYA_TAMPUNG_2026"] / r["PEMINAT_2025"]) * 100, 2)
        if r["PEMINAT_2025"] > 0 else 0.0,
        axis=1,
    )
    df["RASIO_PERSAINGAN"] = df.apply(
        lambda r: int(round(r["PEMINAT_2025"] / r["DAYA_TAMPUNG_2026"]))
        if r["DAYA_TAMPUNG_2026"] > 0 else 0,
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
        return {"label":"Sangat Ketat", "color":"#d14343", "soft":"#fff0f0", "border":"#efb4b4", "kind":"danger"}
    if peluang <= 15.0:
        return {"label":"Ketat / Tinggi", "color":"#c77800", "soft":"#fff8e6", "border":"#f2d58b", "kind":"warning"}
    if peluang <= 30.0:
        return {"label":"Sedang / Moderat", "color":"#2857d9", "soft":"#eef4ff", "border":"#c8d8ff", "kind":"info"}
    return {"label":"Peluang Besar", "color":"#159447", "soft":"#ecfdf3", "border":"#b7e3c7", "kind":"success"}


def insight_copy(peluang, rasio, peminat):
    if peminat == 0:
        return "info", "Belum ada data peminat", "Data peminat belum tercatat. Gunakan hasil ini sebagai informasi awal, bukan sebagai jaminan kelulusan."
    if peluang < 5.0:
        return "danger", "Persaingannya sangat ketat", f"Peluang simulasi {fmt_percent(peluang)}. Sekitar {rasio} siswa bersaing untuk setiap 1 kursi yang tersedia."
    if peluang <= 15.0:
        return "warning", "Persaingannya cukup ketat", f"Peluang simulasi {fmt_percent(peluang)}. Sekitar {rasio} siswa bersaing untuk setiap 1 kursi yang tersedia."
    if peluang <= 30.0:
        return "info", "Persaingannya berada di level sedang", f"Peluang simulasi {fmt_percent(peluang)} dengan rasio sekitar 1 kursi : {rasio} siswa."
    return "success", "Peluangnya relatif lebih besar", f"Peluang simulasi {fmt_percent(peluang)} dengan rasio sekitar 1 kursi : {rasio} siswa."


def render_table(alt_df, selected_prodi):
    max_opp = max(float(alt_df["PELUANG_PERSEN"].max()), 1.0)
    rows = []
    for _, row in alt_df.iterrows():
        name = html.escape(str(row["NAMA_PRODI"]))
        jenjang = html.escape(str(row["JENJANG"]))
        kode = html.escape(str(row["KODE_PRODI"]))
        opp = float(row["PELUANG_PERSEN"])
        ratio = int(row["RASIO_PERSAINGAN"])
        quota = int(row["DAYA_TAMPUNG_2026"])
        applicants = int(row["PEMINAT_2025"])
        current = str(row["NAMA_PRODI"]) == str(selected_prodi)
        tag = '<span class="current-tag">PILIHANMU</span>' if current else ''
        width = max(3, min(100, opp / max_opp * 100))
        rows.append(f"""
        <tr class="{'current' if current else ''}">
          <td><div class="program">{name}{tag}</div><div class="meta">{jenjang} · {kode}</div></td>
          <td><div class="opp">{fmt_percent(opp)}</div><div class="bar"><span style="width:{width:.1f}%"></span></div></td>
          <td><span class="ratio">1 : {ratio}</span></td>
          <td>{fmt_int(quota)} kursi</td>
          <td>{fmt_int(applicants)} siswa</td>
        </tr>""")
    st.markdown(
        f'''<div class="table-shell"><div class="table-scroll"><table class="ptn-table"><thead><tr><th>Program Studi</th><th>Peluang</th><th>Rasio</th><th>Daya Tampung</th><th>Peminat 2025</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></div>''',
        unsafe_allow_html=True,
    )

# =========================================================
# APP BAR
# =========================================================
st.markdown('''<div class="appbar"><div class="brand"><div class="brand-icon">🎓</div><div>Kalkulator <span style="color:#2857d9">PTN</span></div></div><div class="appbar-note">Analisis peluang & persaingan program studi</div></div>''', unsafe_allow_html=True)

# =========================================================
# HOME / INPUT
# =========================================================
list_ptn = sorted(df["NAMA_PTN"].dropna().unique())

hero_left, hero_right = st.columns([1.65, 0.75], gap="large")
with hero_left:
    st.markdown('''<div class="hero-wrap"><div class="hero-kicker">SNBP · ANALISIS DATA</div><div class="hero-title">Seberapa kompetitif jurusan impianmu?</div><p class="hero-copy">Cek peluang dan rasio persaingan PTN berdasarkan data daya tampung dan peminat. Pilih kampus, pilih jurusan, lalu lihat gambaran persaingannya.</p></div>''', unsafe_allow_html=True)
with hero_right:
    preview = df.sort_values("PELUANG_PERSEN", ascending=False).iloc[0] if not df.empty else None
    if preview is not None:
        st.markdown(f'''<div class="preview"><div class="preview-label">Contoh hasil analisis</div><div class="preview-number">{fmt_percent(preview["PELUANG_PERSEN"])}</div><div class="preview-status">● Peluang simulasi</div><div class="preview-line"><span>Daya tampung</span><strong>{fmt_int(preview["DAYA_TAMPUNG_2026"])} kursi</strong></div><div class="preview-line"><span>Peminat</span><strong>{fmt_int(preview["PEMINAT_2025"])} siswa</strong></div></div>''', unsafe_allow_html=True)

st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
st.markdown('''<div class="section-head"><div class="eyebrow">Mulai analisis</div><div class="section-title">Pilih PTN dan jurusan yang kamu incar</div><div class="section-copy">Mulai dari universitas, lalu pilih program studi untuk melihat estimasi peluangnya.</div></div>''', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown('<div class="step-label"><span class="step-num">01</span>Universitas</div>', unsafe_allow_html=True)
    selected_ptn = st.selectbox("Mau kuliah di mana?", list_ptn, index=None, placeholder="Cari atau pilih PTN...", key="selected_ptn_ui", label_visibility="visible")

if selected_ptn:
    filtered_prodi_df = df[df["NAMA_PTN"] == selected_ptn]
    list_prodi = sorted(filtered_prodi_df["NAMA_PRODI"].dropna().unique())
else:
    filtered_prodi_df = pd.DataFrame()
    list_prodi = []

with c2:
    st.markdown('<div class="step-label"><span class="step-num">02</span>Program Studi</div>', unsafe_allow_html=True)
    selected_prodi = st.selectbox("Jurusan yang kamu incar?", list_prodi, index=None, placeholder="Cari atau pilih jurusan...", disabled=not bool(selected_ptn), key="selected_prodi_ui", label_visibility="visible")

st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
btn_hitung = st.button("Lihat Peluang Saya  →", use_container_width=True)

# =========================================================
# RESULT
# =========================================================
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.markdown('<div class="insight warning"><div class="insight-title">Pilihanmu belum lengkap</div><div class="insight-copy">Pilih universitas dan program studi terlebih dahulu agar hasil analisis bisa ditampilkan.</div></div>', unsafe_allow_html=True)
    else:
        target = filtered_prodi_df[filtered_prodi_df["NAMA_PRODI"] == selected_prodi].iloc[0]
        kuota = target["DAYA_TAMPUNG_2026"]
        peminat = target["PEMINAT_2025"]
        peluang = target["PELUANG_PERSEN"]
        rasio = target["RASIO_PERSAINGAN"]
        meta = competition_meta(peluang)
        insight_kind, insight_title, insight_text = insight_copy(peluang, rasio, peminat)

        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)
        st.markdown(f'''<div class="result-header"><div class="eyebrow">Hasil analisis</div><div class="result-title">{html.escape(str(target["NAMA_PRODI"]))}</div><div class="result-subtitle">{html.escape(str(target["JENJANG"]))} · {html.escape(str(target["NAMA_PTN"]))}</div><div class="badges"><span class="badge">{html.escape(str(target["NAMA_PTN"]))}</span><span class="badge">Kode {html.escape(str(target["KODE_PRODI"]))}</span><span class="badge">Portofolio: {html.escape(str(target["JENIS_PORTOFOLIO"]))}</span></div></div>''', unsafe_allow_html=True)

        st.markdown(f'''<div class="result-card"><div class="result-label">Peluang simulasi</div><div class="result-number">{fmt_percent(peluang)}</div><div class="status" style="background:{meta["soft"]};color:{meta["color"]};border:1px solid {meta["border"]};"><span class="dot" style="background:{meta["color"]}"></span>{meta["label"]}</div><div class="result-context">Berdasarkan <strong>{fmt_int(kuota)} kursi</strong> dan <strong>{fmt_int(peminat)} peminat</strong> pada data yang tersedia.</div></div>''', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3, gap="medium")
        with m1:
            st.markdown(f'''<div class="metric"><div class="metric-label">Daya tampung</div><div class="metric-value">{fmt_int(kuota)} <span class="metric-unit">kursi</span></div></div>''', unsafe_allow_html=True)
        with m2:
            st.markdown(f'''<div class="metric"><div class="metric-label">Peminat 2025</div><div class="metric-value">{fmt_int(peminat)} <span class="metric-unit">siswa</span></div></div>''', unsafe_allow_html=True)
        with m3:
            st.markdown(f'''<div class="metric"><div class="metric-label">Rasio persaingan</div><div class="metric-value">1 : {int(rasio)} <span class="metric-unit">siswa/kursi</span></div></div>''', unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown(f'''<div class="insight {insight_kind}"><div class="insight-title">{insight_title}</div><div class="insight-copy">{insight_text}</div></div>''', unsafe_allow_html=True)

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
        st.markdown(f'''<div style="height:10px"></div><div class="insight info"><div class="insight-title">Apa artinya untukmu?</div><div class="insight-copy">{action}</div></div>''', unsafe_allow_html=True)

        st.markdown(f'''<div class="compare-head"><div class="eyebrow">Eksplorasi pilihan</div><div class="compare-title">Bandingkan dengan jurusan lain</div><div class="compare-copy">Lihat program studi lain di {html.escape(str(selected_ptn))}, diurutkan dari peluang tertinggi ke yang paling ketat.</div></div>''', unsafe_allow_html=True)
        alt_df = filtered_prodi_df.sort_values(by="PELUANG_PERSEN", ascending=False)
        render_table(alt_df, selected_prodi)

        st.markdown('<div class="footer-note">Hasil ini merupakan simulasi berdasarkan data peminat dan daya tampung yang tersedia, bukan jaminan kelulusan.</div>', unsafe_allow_html=True)
