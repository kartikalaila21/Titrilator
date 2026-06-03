import streamlit as st
import pandas as pd
import numpy as np
import time

# ==========================================
# PAGE CONFIG & CUSTOM THEME (SOFT COLORS)
# ==========================================
st.set_page_config(
    page_title="ChemiCalc v2.3 - Kalkulator Titrimetri",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk warna soft pastel dan efek tambahan
st.markdown("""
    <style>
    /* Background Utama */
    .main {
        background-color: #F8F9FA;
    }
    
    /* Heading Styles */
    h1, h2, h3, h4, h5 {
        color: #2C4E4B;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Button Styling */
    div.stButton > button:first-child {
        background-color: #439A86;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #2C4E4B;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Result Box */
    .result-box {
        background-color: #EBF7F5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #439A86;
        margin-top: 15px;
    }
    
    /* Warning Box */
    .warning-box {
        background-color: #FFF3CD;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #FFC107;
    }
    
    /* Error Box */
    .error-box {
        background-color: #F8D7DA;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #DC3545;
    }
    
    /* Success Box */
    .success-box {
        background-color: #D4EDDA;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28A745;
    }
    
    /* Info Text */
    .info-text {
        color: #5A737E;
        font-size: 14px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F1F5F4;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #439A86;
        color: white;
        border-radius: 4px 4px 0px 0px;
    }
    
    /* Input number styling */
    div.stNumberInput > div > div > input {
        border-radius: 6px;
    }
    
    /* DataFrame styling */
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #439A86;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI SESSION STATE
# ==========================================
if 'riwayat_perhitungan' not in st.session_state:
    st.session_state.riwayat_perhitungan = []

if 'hitung_terakhir' not in st.session_state:
    st.session_state.hitung_terakhir = {}

# ==========================================
# FUNGSI BANTU
# ==========================================
def hitung_normalitas(bm_baku, mg_baku, v_titran, fp, valensi=1):
    """Hitung normalitas dariData Baku"""
    be = bm_baku / valensi
    penyebut = v_titran * be * fp
    return mg_baku / penyebut, be, penyebut

def format_hasil(teks, nilai, satuan=""):
    """Format hasil dengan styling"""
    return f"**{teks}:** {nilai:.6f} {satuan}"

def simpan_ke_riwayat(jenis, sub_jenis, input_dict, hasil_dict):
    """Simpan perhitungan ke riwayat"""
    entri = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'jenis': jenis,
        'sub_jenis': sub_jenis,
        'input': input_dict,
        'hasil': hasil_dict
    }
    st.session_state.riwayat_perhitungan.append(entri)
    # Batasi riwayat maksimal 50 entri
    if len(st.session_state.riwayat_perhitungan) > 50:
        st.session_state.riwayat_perhitungan.pop(0)

def rumus_latex(jenis):
    """Kembalikan rumus LaTeX berdasarkan jenis"""
    rumus = {
        'standarisasi_n': r"N = \frac{mg_{baku}}{V_{titran} \times BE \times fp}",
        'standarisasi_m': r"M = \frac{mg_{baku}}{V_{titran} \times BM \times fp}",
        'kadar_persen': r"\% = \left( \frac{V_{titran} \times N \times BE}{V_{sampel}} \right) \times 10^{-3} \times 100\%",
        'kadar_gram': r"g = \left( \frac{V_{titran} \times N \times BE}{V_{sampel}} \right) \times 10^{-3}",
        'kesadahan': r"Kesadahan = \frac{V_{EDTA} \times M_{EDTA} \times BM_{CaCO_3}}{V_{sampel}} \times 10^3 \, ppm"
    }
    return rumus.get(jenis, "")

# ==========================================
# HEADER UTAMA
# ==========================================
st.title("🧪 ChemiCalc v2.3: Kalkulator Titrimetri Profesional")
st.write("Aplikasi perhitungan kuantitatif untuk praktikum kimia analisis -所有 hasil perhitungan sudah dikonversi ke dalam **Gram (g)** dan **% (b/v)** untuk pelaporan data analitik yang akurat.")
st.write("---")

# ==========================================
# NAVIGATION DI SIDEBAR
# ==========================================
with st.sidebar:
    st.header("📌 Menu Navigasi")
    st.markdown("---")
    menu_utama = st.sidebar.radio(
        "🗂️ Pilih Halaman:",
        [
            "🏠 Halaman Utama", 
            "🧮 Kalkulator Hitung", 
            "📊 Riwayat Perhitungan",
            "🎨 Simulasi Indikator",
            "📖 Panduan Penggunaan"
        ]
    )
    
    st.markdown("---")
    with st.expander("ℹ️ Info Aplikasi", expanded=True):
        st.markdown("""
        **ChemiCalc v2.3**
        
        Fitur Utama:
        - ✅ Perhitungan Standarisasi (N & M)
        - ✅ Perhitungan Kadar Sampel
        - ✅ Simulasi Warna Indikator
        - ✅ Riwayat Perhitungan
        - ✅ Konversi Otomatis ke Gram
        
        **Catatan:** 
        Semua hasil telah dikonversi ke dalam satuan Gram (g) untuk kesesuaian standar pelaporan.
        """)
    
    # Statistik riwayat
    if len(st.session_state.riwayat_perhitungan) > 0:
        st.markdown("---")
        st.metric("📈 Total Perhitungan", len(st.session_state.riwayat_perhitungan))

# ==========================================
# MENU 1: HALAMAN UTAMA
# ==========================================
if menu_utama == "🏠 Halaman Utama":
    # Welcome Section
    st.header("👋 Selamat Datang di ChemiCalc")
    st.markdown("""
    Aplikasi ini berfungsi sebagai **alat bantu digital verifier** untuk memverifikasi data perhitungan hasil praktikum kimia analisis kuantitatif (Titrimetri). 
    
    Semua parameter perhitungan kadar sampel telah dikonversi secara standar ke dalam:
    - **Gram (g)** untuk massa absolut
    - **% (b/v)** untuk konsentrasi relatif
    - **ppm** untuk kesadahan air
    """)
    
    # Features Grid
    st.subheader("🚀 Fitur yang Tersedia:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔬 Asidimetri & Alkalimetri
        - Standarisasi NaOH (Asam Oksalat)
        - Standarisasi HCl (Boraks)
        - Kadar Campuran Warder
        """)
        
    with col2:
        st.markdown("""
        ### 💜 Permanganometri
        - Standarisasi KMnO₄
        - Kadar Besi (Fe)
        """)
        
    with col3:
        st.markdown("""
        ### 🟡 Iodometri
        - Standarisasi Na₂S₂O₃
        - Kadar Klor Aktif (Cl)
        """)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        ### 💙 Kompleksiometri
        - Standarisasi EDTA
        - Kesadahan Jumlah Air
        """)
        
    with col5:
        st.markdown("""
        ### 🎨 Simulasi Indikator
        - Visualisasi Warna
        - pH Range Indicator
        """)
        
    with col6:
        st.markdown("""
        ### 📊 Riwayat
        - Simpan Hasil
        - Ekspor ke CSV
        """)
    
    # Info Penting
    st.info("""
    📌 **INFORMASI PENTING:**
    - Nilai **BE (Bilang Ekuivalen)** = BM / Valensi
    - Konversi mg ke g menggunakan factor **10⁻³**
    - Untuk perhitungan kadar (%) dikali dengan **100**
    - Kesadahan air dalam **ppm** = mg/L = 10⁻³ g/mL × 10³ = mg/L = ppm
    """)

# ==========================================
# MENU 2: KALKULATOR HITUNG
# ==========================================
elif menu_utama == "🧮 Kalkulator Hitung":
    st.header("🧮 Kalkulator Parameter Titrasi")
    
    # Selector Metode Utama
    materi = st.selectbox(
        "📌 Pilih Metode Titrasi:",
        [
            "Asidimetri & Alkalimetri", 
            "Permanganometri", 
            "Iodometri", 
            "Kompleksiometri"
        ],
        help="Pilih metode titrasi yang akan dilakukan"
    )
    
    st.write("---")
    
    # ------------------------------------------
    # 1. ASIDIMETRI & ALKALIMETRI
    # ------------------------------------------
    if materi == "Asidimetri & Alkalimetri":
        sub_asidi = st.selectbox(
            "📋 Pilih Analisis:",
            [
                "Standarisasi NaOH dengan Asam Oksalat",
                "Standarisasi HCl dengan Boraks",
                "Penetapan Kadar Campuran Warder (NaOH & Na2CO3)"
            ]
        )
        
        if sub_asidi == "Standarisasi NaOH dengan Asam Oksalat":
            st.subheader("⚗️ Standarisasi NaOH")
            st.caption("Metode: Titrasi Asam Oksalat dihidrat (C₂H₂O₄·2H₂O) dengan NaOH")
            
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                mg_baku = st.number_input("Bobot Asam Oksalat dihidrat (mg)", min_value=0.0, value=630.0, step=0.1, help="Masukkan bobot baku dalam miligram")
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0, step=1.0)
            with col_in2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0, step=0.1)
                v_titran = st.number_input("Volume Titran NaOH (mL)", min_value=0.01, value=25.0, step=0.1)
                
            st.caption(f"**BE Asam Oksalat dihidrat:** {126.07/2:.3f} (BM: 126.07 g/mol, val: 2)")
            
            if st.button("🚀 Hitung Normalitas NaOH", use_container_width=True):
                be_oksalat = 126.07 / 2  
                fp = v_labu / v_pipet    
                penyebut = v_titran * be_oksalat * fp
                n_naoh = mg_baku / penyebut
                
                st.markdown("### 📐 Rumus Perhitungan:")
                st.latex(r"N_{NaOH} = \frac{mg_{baku}}{V_{titran} \times BE \times fp}")
                
                # Tampilan Hasil
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Standarisasi:</h4>
                    <big>Normalitas NaOH = <b>{n_naoh:.6f} N</b></big><br><br>
                    <b>Detail Variabel:</b><br>
                    - Bobot Baku = <b>{mg_baku:.2f} mg</b><br>
                    - BE Asam Oksalat Dihidrat = <b>{be_oksalat:.4f}</b><br>
                    - Faktor Pengenceran (fp) = <b>{fp:.2f}</b><br>
                    - Nilai Penyebut = <b>{penyebut:.4f}</b><br>
                    <hr>
                    <i>Massa C₂H₂O₄·2H₂O dalam aliquot = {(mg_baku/fp)*1e-3:.4f} g</i>
                </div>
                """, unsafe_allow_html=True)
                
                # Simpan ke riwayat
                simpan_ke_riwayat(
                    "Asidimetri", 
                    "Standarisasi NaOH",
                    {"mg_baku": mg_baku, "v_labu": v_labu, "v_pipet": v_pipet, "v_titran": v_titran},
                    {"Normalitas_NaOH": n_naoh, "BE": be_oksalat, "fp": fp}
                )

        elif sub_asidi == "Standarisasi HCl dengan Boraks":
            st.subheader("⚗️ Standarisasi HCl")
            st.caption("Metode: Titrasi Boraks (Na₂B₄O₇·10H₂O) dengan HCl")
            
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                mg_baku = st.number_input("Bobot Boraks (mg)", min_value=0.0, value=1500.0, step=0.1)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0, step=1.0)
            with col_in2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0, step=0.1)
                v_titran = st.number_input("Volume Titran HCl (mL)", min_value=0.01, value=25.0, step=0.1)
            
            st.caption(f"**BE Boraks:** {381.37/2:.3f} (BM: 381.37 g/mol, val: 2)")
            
            if st.button("🚀 Hitung Normalitas HCl", use_container_width=True):
                be_boraks = 381.37 / 2  
                fp = v_labu / v_pipet
                penyebut = v_titran * be_boraks * fp
                n_hcl = mg_baku / penyebut
                
                st.markdown("### 📐 Rumus Perhitungan:")
                st.latex(r"N_{HCl} = \frac{mg_{baku}}{V_{titran} \times BE \times fp}")
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Standarisasi:</h4>
            
