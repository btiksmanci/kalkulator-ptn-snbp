import pandas as pd
import streamlit as st

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Kalkulator Rasio Peluang PTN",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS Modern & Professional UI (Fixed Dark/Light Mode Conflicts)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    /* Force Light Theme Base Container */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        color: #0F172A !important;
    }

    #MainMenu, footer, header, [data-testid="stHeader"] { 
        display: none !important; 
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1000px !important;
    }
    
    /* Gradient Banner Header */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
    }
    
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2rem;
        margin-bottom: 0.4rem;
    }
    
    .main-header p {
        color: #E0E7FF !important;
        font-size: 1rem;
        margin: 0;
    }

    /* Styling Metric Box (Card Stat) */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
        border-color: #CBD5E1;
    }
    
    .stat-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    
    .stat-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0F172A;
    }

    /* Styling Custom Button */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Badges Detail Jurusan */
    .badge-info {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #DBEAFE;
    }

    /* TABEL HTML STABIL (PENGGANTI ST.DATAFRAME YANG BLANK) */
    .custom-table-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow-x: auto;
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    table.custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
        text-align: left;
    }
    table.custom-table th {
        background-color: #F8FAFC;
        color: #475569;
        font-weight: 700;
        padding: 12px 16px;
        border-bottom: 1px solid #E2E8F0;
    }
    table.custom-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #F1F5F9;
        color: #0F172A;
    }
    table.custom-table tr:last-child td {
        border-bottom: none;
    }
    table.custom-table tr:hover {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# 3. Load Data dari CSV
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

# 4. Banner Header Utama
st.markdown("""
<div class="main-header">
    <h1>🎓 Analisis Peluang & Rasio PTN</h1>
    <p>Portal kalkulasi keketatan persaingan jurusan berdasarkan data resmi Daya Tampung & Peminat.</p>
</div>
""", unsafe_allow_html=True)

# 5. Form Pencarian Clean Card
col_search1, col_search2 = st.columns(2)

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

# 6. Logika Menampilkan Hasil
if btn_hitung:
    if not selected_ptn or not selected_prodi:
        st.warning("⚠️ **Mohon lengkapi pilihan**: Pilih Universitas dan Program Studi terlebih dahulu.")
    else:
        target = filtered_prodi_df[filtered_prodi_df['NAMA_PRODI'] == selected_prodi].iloc[0]

        kuota = target['DAYA_TAMPUNG_2026']
        peminat = target['PEMINAT_2025']
        peluang = target['PELUANG_PERSEN']
        rasio = target['RASIO_PERSAINGAN']

        # Header Hasil & Metadata
        st.markdown(f"## 📌 {target['NAMA_PRODI']} ({target['JENJANG']})")
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <span class="badge-info">🏛️ {target['NAMA_PTN']}</span>
            <span class="badge-info">🔑 Kode: {target['KODE_PRODI']}</span>
            <span class="badge-info">🎨 Portofolio: {target['JENIS_PORTOFOLIO']}</span>
        </div>
        """, unsafe_allow_html=True)

        # Dashboard Metric Cards (4 Kolom Rapi & Responsif)
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📦 Daya Tampung</div>
                <div class="stat-value">{kuota} <span style="font-size: 0.9rem; color: #64748B;">Kursi</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">👥 Peminat Lalu</div>
                <div class="stat-value">{peminat:,} <span style="font-size: 0.9rem; color: #64748B;">Siswa</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📊 Peluang Lulus</div>
                <div class="stat-value" style="color: #2563EB;">{peluang}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">⚖️ Rasio Persaingan</div>
                <div class="stat-value" style="color: #D97706;">1 : {rasio}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # Banner Rekomendasi & Tingkat Kesulitan
        if peminat == 0:
            st.info("ℹ️ **Jurusan Baru / Belum Ada Data Peminat**: Peluang relatif aman karena belum ada kompetisi tercatat.")
        elif peluang < 5.0:
            st.error(f"### 🔴 Kategori Persaingan: SANGAT KETAT (Super Favorit)\n"
                     f"Hanya **{peluang}%** dari total pendaftar yang diterima (Kamu harus menyisihkan **{rasio} orang** per kursi). "
                     f"Direkomendasikan sebagai **Pilihan 1** dengan strategi nilai yang sangat tinggi.")
        elif peluang <= 15.0:
            st.warning(f"### 🟠 Kategori Persaingan: KETAT / TINGGI\n"
                       f"Peluang diterima **{peluang}%** (Kamu harus menyisihkan sekitar **{rasio} orang** per kursi). "
                       f"Merupakan jurusan favorit yang butuh persiapan matang.")
        elif peluang <= 30.0:
            st.info(f"### 🟡 Kategori Persaingan: SEDANG / MODERAT\n"
                    f"Peluang diterima **{peluang}%** (Rasio persaingan **1 : {rasio}** orang). "
                    f"Sangat ideal dijadikan **Pilihan 1** atau **Pilihan 2** yang aman.")
        else:
            st.success(f"### 🟢 Kategori Persaingan: PELUANG BESAR\n"
                       f"Peluang kelulusan tergolong tinggi sebesar **{peluang}%** (Persaingan **1 : {rasio}** orang). "
                       f"Sangat direkomendasikan untuk pengaman di **Pilihan 2**.")

        st.divider()

        # Tabel Perbandingan Jurusan di PTN Sama (Menggunakan HTML Table yang Stabil)
        st.subheader(f"💡 Perbandingan Jurusan Lain di {selected_ptn}")
        st.caption("Daftar urutan jurusan dari yang paling tinggi persentase kelulusannya hingga yang paling ketat.")

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
                    <td>{row['PEMINAT_2025']:,} Pendaftar</td>
                    <td><span style="color: #2563EB; font-weight: 700;">{row['PELUANG_PERSEN']}%</span></td>
                    <td>1 : {row['RASIO_PERSAINGAN']}</td>
                </tr>
            """
        table_html += """
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
