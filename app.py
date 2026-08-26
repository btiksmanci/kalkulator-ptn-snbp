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
# DESIGN SYSTEM — stable Streamlit layout
# =========================================================
st.markdown(
    r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#f6f8fc;
  --surface:#ffffff;
  --surface-soft:#f8fafc;
  --text:#101828;
  --muted:#667085;
  --muted-2:#98a2b3;
  --border:#e4e7ec;
  --primary:#2563eb;
  --primary-dark:#1d4ed8;
  --primary-soft:#eff6ff;
  --green:#15803d;
  --green-soft:#f0fdf4;
  --yellow:#b45309;
  --yellow-soft:#fffbeb;
  --red:#b42318;
  --red-soft:#fef3f2;
  --shadow:0 12px 32px rgba(16,24,40,.06);
}

html, body, [class*="css"]{font-family:'Plus Jakarta Sans',sans-serif;}
.stApp{background:var(--bg);color:var(--text);}
.block-container{max-width:1160px;padding:24px 28px 48px;}
#MainMenu, footer{visibility:hidden;}
header[data-testid="stHeader"]{visibility:hidden;height:0;}

/* app header */
.appbar{height:44px;display:flex;align-items:center;justify-content:space-between;margin-bottom:26px;}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);font-size:16px;font-weight:800;letter-spacing:-.02em;}
.brand-icon{width:36px;height:36px;display:grid;place-items:center;border-radius:11px;background:var(--primary);color:#fff;font-size:17px;box-shadow:0 6px 16px rgba(37,99,235,.20);}
.appbar-note{font-size:11px;color:var(--muted);font-weight:600;}

/* hero */
.hero{position:relative;overflow:hidden;background:linear-gradient(135deg,#183b92 0%,#2563eb 62%,#3b82f6 100%);border-radius:22px;padding:38px 42px;color:#fff;box-shadow:0 18px 42px rgba(37,99,235,.16);}
.hero:before{content:"";position:absolute;width:360px;height:360px;border-radius:50%;right:-150px;top:-180px;background:rgba(255,255,255,.08);}
.hero:after{content:"";position:absolute;width:180px;height:180px;border-radius:50%;right:110px;bottom:-130px;background:rgba(255,255,255,.05);}
.hero-inner{position:relative;z-index:1;max-width:760px;}
.hero-kicker{display:inline-flex;align-items:center;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.20);font-size:9px;font-weight:800;letter-spacing:.08em;}
.hero-title{margin:17px 0 12px;color:#fff;font-size:clamp(36px,4.4vw,54px);line-height:1.02;font-weight:800;letter-spacing:-.055em;max-width:780px;}
.hero-copy{margin:0;color:rgba(255,255,255,.84);font-size:14px;line-height:1.7;max-width:680px;}
.hero-steps{position:relative;z-index:1;display:flex;gap:9px;flex-wrap:wrap;margin-top:25px;}
.hero-step{display:flex;align-items:center;gap:7px;padding:8px 11px;border-radius:10px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.14);font-size:10px;font-weight:700;color:rgba(255,255,255,.88);}
.hero-step b{width:20px;height:20px;display:grid;place-items:center;border-radius:6px;background:rgba(255,255,255,.16);font-size:9px;}

/* section */
.section{margin-top:30px;}
.eyebrow{color:var(--primary);font-size:9px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;}
.section-title{margin-top:5px;font-size:22px;font-weight:800;letter-spacing:-.035em;color:var(--text);}
.section-copy{margin-top:5px;color:var(--muted);font-size:12px;line-height:1.6;}

/* selection card — only the surrounding Streamlit container gets the border */
.step-label{margin-bottom:7px;display:flex;align-items:center;gap:7px;color:var(--text);font-size:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;}
.step-num{width:24px;height:24px;display:grid;place-items:center;border-radius:8px;background:var(--primary-soft);color:var(--primary);font-size:9px;}
[data-testid="stSelectbox"] label{color:var(--text)!important;font-size:12px!important;font-weight:700!important;}
[data-testid="stSelectbox"] > div > div{min-height:48px!important;border-radius:11px!important;border:1px solid var(--border)!important;background:#fff!important;box-shadow:none!important;}
[data-testid="stSelectbox"] > div > div:focus-within{border-color:#84aafc!important;box-shadow:0 0 0 3px rgba(37,99,235,.09)!important;}
[data-testid="stSelectbox"] input{font-family:'Plus Jakarta Sans',sans-serif!important;}

/* buttons */
div.stButton > button{min-height:50px;border:0!important;border-radius:11px!important;background:var(--primary)!important;color:#fff!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:12px!important;font-weight:800!important;box-shadow:0 7px 16px rgba(37,99,235,.17)!important;transition:all .18s ease!important;}
div.stButton > button:hover{background:var(--primary-dark)!important;transform:translateY(-1px);box-shadow:0 10px 20px rgba(37,99,235,.22)!important;}

/* result */
.result-header{margin-top:30px;padding-bottom:17px;}
.result-title{margin-top:5px;font-size:clamp(28px,4vw,40px);line-height:1.08;font-weight:800;letter-spacing:-.045em;color:var(--text);}
.result-subtitle{margin-top:6px;color:var(--muted);font-size:12px;}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;}
.badge{display:inline-flex;align-items:center;padding:6px 9px;border-radius:999px;background:#fff;border:1px solid var(--border);color:#475467;font-size:9px;font-weight:700;}

.result-card{background:#fff;border:1px solid #dbe5ff;border-radius:18px;padding:25px 27px;box-shadow:var(--shadow);height:100%;}
.result-label{color:var(--muted);font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;}
.result-number{margin-top:5px;color:var(--primary);font-size:clamp(58px,7vw,78px);line-height:.98;font-weight:800;letter-spacing:-.065em;}
.status{display:inline-flex;align-items:center;gap:7px;margin-top:12px;padding:7px 10px;border-radius:999px;font-size:10px;font-weight:800;}
.dot{width:7px;height:7px;border-radius:50%;}
.result-context{margin-top:13px;color:var(--muted);font-size:11px;line-height:1.65;}

.explain-card{height:100%;padding:22px;border:1px solid var(--border);border-radius:18px;background:#fff;}
.explain-kicker{font-size:9px;color:var(--primary);font-weight:800;letter-spacing:.1em;text-transform:uppercase;}
.explain-title{margin-top:7px;font-size:18px;font-weight:800;letter-spacing:-.025em;}
.explain-copy{margin-top:8px;color:var(--muted);font-size:11px;line-height:1.7;}
.explain-ratio{margin-top:18px;padding:12px 13px;border-radius:12px;background:var(--surface-soft);border:1px solid #eef0f4;color:var(--text);font-size:11px;font-weight:700;}
.explain-ratio strong{font-size:18px;color:var(--primary);}

.metric{background:#fff;border:1px solid var(--border);border-radius:15px;padding:16px;min-height:100px;}
.metric-label{color:var(--muted);font-size:9px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;}
.metric-value{margin-top:8px;color:var(--text);font-size:23px;line-height:1.1;font-weight:800;letter-spacing:-.035em;}
.metric-unit{color:var(--muted);font-size:10px;font-weight:700;}

.insight{border-radius:15px;padding:15px 17px;border:1px solid var(--border);}
.insight-title{color:var(--text);font-size:13px;font-weight:800;}
.insight-copy{margin-top:5px;color:var(--muted);font-size:11px;line-height:1.65;}
.insight.warning{background:var(--yellow-soft);border-color:#f3d38b;}
.insight.danger{background:var(--red-soft);border-color:#f0b8b3;}
.insight.success{background:var(--green-soft);border-color:#b8dfc3;}
.insight.info{background:var(--primary-soft);border-color:#cbdcff;}

.compare-head{margin-top:30px;padding-bottom:11px;}
.compare-title{margin-top:5px;font-size:21px;font-weight:800;letter-spacing:-.03em;}
.compare-copy{margin-top:5px;color:var(--muted);font-size:11px;line-height:1.6;}

/* table */
.table-shell{background:#fff;border:1px solid var(--border);border-radius:15px;overflow:hidden;box-shadow:0 4px 16px rgba(16,24,40,.03);}
.table-scroll{overflow-x:auto;}
table.ptn-table{width:100%;border-collapse:collapse;min-width:760px;}
table.ptn-table th{padding:11px 13px;background:#f8fafc;color:#667085;border-bottom:1px solid var(--border);text-align:left;font-size:9px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;}
table.ptn-table td{padding:12px 13px;border-bottom:1px solid #f0f2f5;color:#475467;font-size:10px;vertical-align:middle;}
table.ptn-table tr:last-child td{border-bottom:0;}
table.ptn-table tr.current td{background:#f4f7ff;}
.program{color:var(--text);font-weight:700;line-height:1.4;}
.meta{margin-top:3px;color:#98a2b3;font-size:8px;}
.current-tag{display:inline-block;margin-left:5px;padding:3px 6px;border-radius:999px;background:#dbe8ff;color:#3159bd;font-size:7px;font-weight:800;vertical-align:middle;}
.opp{color:var(--primary);font-weight:800;}
.ratio{color:var(--text);font-weight:800;}
.bar{width:72px;height:4px;margin-top:5px;border-radius:999px;background:#e9edf4;overflow:hidden;}
.bar span{display:block;height:100%;border-radius:999px;background:var(--primary);}

.footer-note{margin-top:24px;padding-top:15px;border-top:1px solid var(--border);color:#98a2b3;text-align:center;font-size:9px;line-height:1.6;}

/* Streamlit containers: keep them visually neutral and predictable */
[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--border)!important;border-radius:18px!important;background:#fff!important;}
[data-testid="stVerticalBlockBorderWrapper"] > div{padding:0!important;}

@media(max-width:800px){
  .block-container{padding:18px 18px 40px;}
  .hero{padding:28px 24px;border-radius:19px;}
  .hero-title{font-size:36px;}
  .hero-copy{font-size:13px;}
}
@media(max-width:640px){
  .block-container{padding:14px 14px 32px;}
  .appbar{margin-bottom:17px;}
  .appbar-note{display:none;}
  .hero{padding:24px 20px;}
  .hero-title{font-size:32px;}
  .hero-steps{gap:7px;}
  .hero-step{font-size:9px;}
  .result-card{padding:21px;border-radius:16px;}
  .result-number{font-size:56px;}
  .explain-card{margin-top:10px;}
  .metric{min-height:92px;}
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
st.markdown('''<div class="appbar"><div class="brand"><div class="brand-icon">🎓</div><div>Kalkulator <span style="color:#2563eb">PTN</span></div></div><div class="appbar-note">Analisis peluang & persaingan program studi</div></div>''', unsafe_allow_html=True)

# =========================================================
# HOME / INPUT
# =========================================================
list_ptn = sorted(df["NAMA_PTN"].dropna().unique())

st.markdown('''
<div class="hero">
  <div class="hero-inner">
    <div class="hero-kicker">SNBP · ANALISIS DATA</div>
    <div class="hero-title">Seberapa kompetitif jurusan impianmu?</div>
    <p class="hero-copy">Cek peluang dan rasio persaingan berdasarkan daya tampung dan peminat. Pilih PTN dan jurusanmu untuk mendapatkan gambaran yang lebih jelas.</p>
    <div class="hero-steps">
      <div class="hero-step"><b>01</b> Pilih PTN</div>
      <div class="hero-step"><b>02</b> Pilih jurusan</div>
      <div class="hero-step"><b>03</b> Lihat peluang</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="section"><div class="eyebrow">Mulai analisis</div><div class="section-title">Pilih PTN dan jurusan yang kamu incar</div><div class="section-copy">Gunakan pilihan di bawah untuk melihat estimasi peluang dan tingkat persaingan.</div></div>', unsafe_allow_html=True)

with st.container(border=True):
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="step-label"><span class="step-num">01</span>Universitas</div>', unsafe_allow_html=True)
        selected_ptn = st.selectbox(
            "Mau kuliah di mana?",
            list_ptn,
            index=None,
            placeholder="Cari atau pilih PTN...",
            key="selected_ptn_ui",
            label_visibility="visible",
        )

    if selected_ptn:
        filtered_prodi_df = df[df["NAMA_PTN"] == selected_ptn]
        list_prodi = sorted(filtered_prodi_df["NAMA_PRODI"].dropna().unique())
    else:
        filtered_prodi_df = pd.DataFrame()
        list_prodi = []

    with c2:
        st.markdown('<div class="step-label"><span class="step-num">02</span>Program Studi</div>', unsafe_allow_html=True)
        selected_prodi = st.selectbox(
            "Jurusan yang kamu incar?",
            list_prodi,
            index=None,
            placeholder="Cari atau pilih jurusan...",
            disabled=not bool(selected_ptn),
            key="selected_prodi_ui",
            label_visibility="visible",
        )

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    btn_hitung = st.button("Lihat Peluang Saya  →", use_container_width=True)

# =========================================================
# RESULT
# =========================================================
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.markdown('<div style="height:20px"></div><div class="insight warning"><div class="insight-title">Pilihanmu belum lengkap</div><div class="insight-copy">Pilih universitas dan program studi terlebih dahulu agar hasil analisis bisa ditampilkan.</div></div>', unsafe_allow_html=True)
    else:
        target = filtered_prodi_df[filtered_prodi_df["NAMA_PRODI"] == selected_prodi].iloc[0]

        kuota = target["DAYA_TAMPUNG_2026"]
        peminat = target["PEMINAT_2025"]
        peluang = target["PELUANG_PERSEN"]
        rasio = target["RASIO_PERSAINGAN"]
        meta = competition_meta(peluang)
        insight_kind, insight_title, insight_text = insight_copy(peluang, rasio, peminat)

        st.markdown(f'''
        <div class="result-header">
          <div class="eyebrow">Hasil analisis</div>
          <div class="result-title">{html.escape(str(target["NAMA_PRODI"]))}</div>
          <div class="result-subtitle">{html.escape(str(target["JENJANG"]))} · {html.escape(str(target["NAMA_PTN"]))}</div>
          <div class="badges">
            <span class="badge">{html.escape(str(target["NAMA_PTN"]))}</span>
            <span class="badge">Kode {html.escape(str(target["KODE_PRODI"]))}</span>
            <span class="badge">Portofolio: {html.escape(str(target["JENIS_PORTOFOLIO"]))}</span>
          </div>
        </div>
        ''', unsafe_allow_html=True)

        r1, r2 = st.columns([1.35, .85], gap="medium")
        with r1:
            st.markdown(f'''
            <div class="result-card">
              <div class="result-label">Peluang simulasi</div>
              <div class="result-number">{fmt_percent(peluang)}</div>
              <div class="status" style="background:{meta["soft"]};color:{meta["color"]};border:1px solid {meta["border"]};"><span class="dot" style="background:{meta["color"]}"></span>{meta["label"]}</div>
              <div class="result-context">Berdasarkan <strong>{fmt_int(kuota)} kursi</strong> dan <strong>{fmt_int(peminat)} peminat</strong> pada data yang tersedia.</div>
            </div>
            ''', unsafe_allow_html=True)
        with r2:
            st.markdown(f'''
            <div class="explain-card">
              <div class="explain-kicker">Cara membaca hasil</div>
              <div class="explain-title">Sekitar {int(rasio)} siswa untuk 1 kursi.</div>
              <div class="explain-copy">Angka peluang adalah estimasi berbasis perbandingan daya tampung dan peminat. Gunakan sebagai bahan pertimbangan, bukan sebagai kepastian kelulusan.</div>
              <div class="explain-ratio"><strong>1 : {int(rasio)}</strong> &nbsp; rasio persaingan</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3, gap="medium")
        with m1:
            st.markdown(f'<div class="metric"><div class="metric-label">Daya tampung</div><div class="metric-value">{fmt_int(kuota)} <span class="metric-unit">kursi</span></div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric"><div class="metric-label">Peminat 2025</div><div class="metric-value">{fmt_int(peminat)} <span class="metric-unit">siswa</span></div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric"><div class="metric-label">Rasio persaingan</div><div class="metric-value">1 : {int(rasio)} <span class="metric-unit">siswa/kursi</span></div></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight {insight_kind}"><div class="insight-title">{insight_title}</div><div class="insight-copy">{insight_text}</div></div>', unsafe_allow_html=True)

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
        st.markdown(f'<div style="height:10px"></div><div class="insight info"><div class="insight-title">Apa artinya untukmu?</div><div class="insight-copy">{action}</div></div>', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="compare-head">
          <div class="eyebrow">Eksplorasi pilihan</div>
          <div class="compare-title">Bandingkan dengan jurusan lain</div>
          <div class="compare-copy">Lihat program studi lain di {html.escape(str(selected_ptn))}, diurutkan dari peluang tertinggi ke yang paling ketat.</div>
        </div>
        ''', unsafe_allow_html=True)

        alt_df = filtered_prodi_df.sort_values(by="PELUANG_PERSEN", ascending=False)
        render_table(alt_df, selected_prodi)

        st.markdown('<div class="footer-note">Hasil ini merupakan simulasi berdasarkan data peminat dan daya tampung yang tersedia, bukan jaminan kelulusan.</div>', unsafe_allow_html=True)
