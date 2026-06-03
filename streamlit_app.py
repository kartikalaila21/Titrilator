import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# PAGE CONFIG & CUSTOM THEME
# ==========================================
st.set_page_config(
    page_title="Titrilator - Kalkulator Titrimetri",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    h1, h2, h3, h4 { color: #2C4E4B; font-family: 'Segoe UI', sans-serif; }
    div.stButton > button:first-child {
        background-color: #439A86; color: white; border-radius: 8px;
        border: none; padding: 8px 20px; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #2C4E4B; color: white; transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .result-box {
        background-color: #EBF7F5; padding: 20px; border-radius: 10px;
        border-left: 5px solid #439A86; margin-top: 15px;
    }
    section[data-testid="stSidebar"] { background-color: #F1F5F4; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
if 'riwayat_perhitungan' not in st.session_state:
    st.session_state.riwayat_perhitungan = []

# ==========================================
# FUNGSI BANTU
# ==========================================
def simpan_riwayat(jenis, sub, inp, hasil):
    entri = {
        'Waktu': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Jenis': jenis,
        'Sub': sub,
        'Input': inp,
        'Hasil': hasil
    }
    st.session_state.riwayat_perhitungan.append(entri)
    if len(st.session_state.riwayat_perhitungan) > 50:
        st.session_state.riwayat_perhitungan.pop(0)

def konversi_ke_gram(mgekivalen):
    return mgekivalen * 1e-3

def hitung_kadar_persen(massa_gram, volume_sampel_mL):
    return (massa_gram / volume_sampel_mL) * 100

# ==========================================
# HEADER APLIKASI
# ==========================================
st.title("🧪 Titrilator: Kalkulator Titrimetri Profesional")
st.markdown("""
Aplikasi perhitungan kuantitatif untuk praktikum kimia analisis - semua hasil sudah dikonversi 
ke dalam **Gram (g)** dan **% (b/v)** untuk kesesuaian pelaporan data analitik.
""")
st.markdown("---")

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.header("📌 Menu Navigasi")
    st.markdown("---")
    
    menu_utama = st.radio(
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
    if len(st.session_state.riwayat_perhitungan) > 0:
        st.metric("📈 Total Hitungan", len(st.session_state.riwayat_perhitungan))
        if st.button("🗑️ Clear Riwayat"):
            st.session_state.riwayat_perhitungan = []
            st.rerun()

# ==========================================
# MENU 1: HALAMAN UTAMA
# ==========================================
if menu_utama == "🏠 Halaman Utama":
    st.header("👋 Selamat Datang di Titrilator")
    
    st.markdown("""
    Aplikasi **Titrilator** berfungsi sebagai **alat bantu digital verifier** untuk memverifikasi 
    data perhitungan hasil praktikum kimia analisis kuantitatif (Titrimetri).
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🔬 Asidimetri & Alkalimetri**\n\n- Standarisasi NaOH\n- Standarisasi HCl\n- Kadar Campuran Warder")
    with col2:
        st.info("**💜 Permanganometri**\n\n- Standarisasi KMnO4\n- Kadar Besi (Fe)")
    with col3:
        st.info("**🟡 Iodometri**\n\n- Standarisasi Na2S2O3\n- Kadar Klor Aktif (Cl)")
    
    col4, col5 = st.columns(2)
    with col4:
        st.info("**💙 Kompleksiometri**\n\n- Standarisasi EDTA\n- Kesadahan Jumlah Air")
    with col5:
        st.info("**🎨 Fitur Lainnya**\n\n- Simulasi Warna Indikator\n- Riwayat Perhitungan")

# ==========================================
# MENU 2: KALKULATOR
# ==========================================
elif menu_utama == "🧮 Kalkulator Hitung":
    st.header("🧮 Kalkulator Parameter Titrasi")
    
    materi = st.selectbox(
        "📌 Pilih Metode Titrasi:",
        [
            "Asidimetri & Alkalimetri", 
            "Permanganometri", 
            "Iodometri", 
            "Kompleksiometri"
        ]
    )
    
    st.markdown("---")
    
    # ==========================
    # 1. ASIDIMETRI & ALKALIMETRI
    # ==========================
    if materi == "Asidimetri & Alkalimetri":
        sub_asidi = st.selectbox(
            "📋 Pilih Analisis:",
            [
                "Standarisasi NaOH dengan Asam Oksalat",
                "Standarisasi HCl dengan Boraks",
                "Penetapan Kadar Campuran Warder (NaOH & Na2CO3)"
            ]
        )
        
        # --- Standarisasi NaOH ---
        if sub_asidi == "Standarisasi NaOH dengan Asam Oksalat":
            st.subheader("⚗️ Standarisasi NaOH dengan Asam Oksalat")
            
            col1, col2 = st.columns(2)
            with col1:
                mg_baku = st.number_input("Bobot Asam Oksalat (mg)", min_value=0.0, value=630.0, step=0.1)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0)
            with col2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0)
                v_titran = st.number_input("Volume Titran NaOH (mL)", min_value=0.01, value=25.0)
            
            st.caption("BM: 126.07 g/mol | Valensi: 2 | BE: 63.035")
            
            if st.button("🚀 Hitung Normalitas NaOH", use_container_width=True):
                be = 126.07 / 2
                fp = v_labu / v_pipet
                n = mg_baku / (v_titran * be * fp)
                
                st.latex(r"N_{NaOH} = \frac{mg}{V \times BE \times fp}")
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Normalitas NaOH = <b>{n:.6f} N</b></h4>
                    BE = {be:.4f} | fp = {fp:.2f} | Penyebut = {v_titran*be*fp:.4f}
                </div>
                """, unsafe_allow_html=True)
                simpan_riwayat("Asidimetri", "Standar NaOH", {"mg": mg_baku, "V_titran": v_titran}, {"N": n})

        # --- Standarisasi HCl ---
        elif sub_asidi == "Standarisasi HCl dengan Boraks":
            st.subheader("⚗️ Standarisasi HCl dengan Boraks")
            
            col1, col2 = st.columns(2)
            with col1:
                mg_baku = st.number_input("Bobot Boraks (mg)", min_value=0.0, value=1500.0)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0)
            with col2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0)
                v_titran = st.number_input("Volume Titran HCl (mL)", min_value=0.01, value=25.0)
            
            st.caption("BM: 381.37 g/mol | Valensi: 2 | BE: 190.685")
            
            if st.button("🚀 Hitung Normalitas HCl", use_container_width=True):
                be = 381.37 / 2
                fp = v_labu / v_pipet
                n = mg_baku / (v_titran * be * fp)
                
                st.latex(r"N_{HCl} = \frac{mg}{V \times BE \times fp}")
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Normalitas HCl = <b>{n:.6f} N</b></h4>
                    BE = {be:.4f} | fp = {fp:.2f}
                </div>
                """, unsafe_allow_html=True)
                simpan_riwayat("Asidimetri", "Standar HCl", {"mg": mg_baku, "V_titran": v_titran}, {"N": n})

        # --- Campuran Warder ---
        elif sub_asidi == "Penetapan Kadar Campuran Warder (NaOH & Na2CO3)":
            st.subheader("⚗️ Kadar Campuran Warder")
            
            col1, col2 = st.columns(2)
            with col1:
                v_sampel = st.number_input("Volume Sampel (mL)", min_value=1.0, value=25.0)
                n_hcl = st.number_input("Normalitas HCl Std (N)", min_value=0.0, value=0.1000, format="%.4f")
            with col2:
                vol_a = st.number_input("Volume Titrasi I - PP (a mL)", min_value=0.0, value=15.0)
                vol_b = st.number_input("Volume Total - MO (b mL)", min_value=0.0, value=25.0)
            
            if st.button("🚀 Hitung Kadar Campuran", use_container_width=True):
                if vol_b < vol_a:
                    st.error("⚠️ Volume b tidak boleh lebih kecil dari a!")
                else:
                    be_na2co3 = 105.99 / 2
                    be_naoh = 40.00
                    
                    g_na2co3 = 2*(vol_b-vol_a) * n_hcl * be_na2co3 * 1e-3
                    g_naoh = ((2*vol_a)-vol_b) * n_hcl * be_naoh * 1e-3
                    pct_na2co3 = g_na2co3 / v_sampel * 100 * 1000
                    pct_naoh = g_naoh / v_sampel * 100 * 1000
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>✅ Hasil Analisis:</h4>
                        <ul>
                            <li><b>Na2CO3</b> = {g_na2co3:.6f} g ({pct_na2co3:.4f} %b/v)</li>
                            <li><b>NaOH</b> = {g_naoh:.6f} g ({pct_naoh:.4f} %b/v)</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    simpan_riwayat("Asidimetri", "Warder", {"V": v_sampel, "a": vol_a, "b": vol_b}, {"g_Na2CO3": g_na2co3, "g_NaOH": g_naoh})

    # ==========================
    # 2. PERMANGANOMETRI
    # ==========================
    elif materi == "Permanganometri":
        sub_permang = st.selectbox(
            "📋 Pilih Analisis:",
            [
                "Standarisasi KMnO4 dengan Asam Oksalat",
                "Penetapan Kadar Besi (Fe)"
            ]
        )
        
        # --- Standarisasi KMnO4 ---
        if sub_permang == "Standarisasi KMnO4 dengan Asam Oksalat":
            st.subheader("⚗️ Standarisasi KMnO4 dengan Asam Oksalat")
            
            col1, col2 = st.columns(2)
            with col1:
                mg_baku = st.number_input("Bobot Asam Oksalat (mg)", min_value=0.0, value=630.0)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0)
            with col2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0)
                v_titran = st.number_input("Volume KMnO4 (mL)", min_value=0.01, value=25.0)
            
            if st.button("🚀 Hitung Normalitas KMnO4", use_container_width=True):
                be = 126.07 / 2
                fp = v_labu / v_pipet
                n = mg_baku / (v_titran * be * fp)
                
                st.latex(r"N_{KMnO_4} = \frac{mg}{V \times BE \times fp}")
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Normalitas KMnO4 = <b>{n:.6f} N</b></h4>
                    BE = {be:.4f} | fp = {fp:.2f}
                </div>
                """, unsafe_allow_html=True)
                simpan_riwayat("Permanganometri", "Standar KMnO4", {"mg": mg_baku, "V": v_titran}, {"N": n})

        # --- Kadar Besi ---
        elif sub_permang == "Penetapan Kadar Besi (Fe)":
            st.subheader("⚗️ Kadar Besi (Fe)")
            
            col1, col2 = st.columns(2)
            with col1:
                v_sampel = st.number_input("Volume Sampel (mL)", min_value=1.0, value=25.0)
                n_kmno4 = st.number_input("Normalitas KMnO4 Std (N)", min_value=0.0, value=0.1000, format="%.4f")
            with col2:
                v_titran = st.number_input("Volume KMnO4 Terpakai (mL)", min_value=0.0, value=24.50)
            
            if st.button("🚀 Hitung Kadar Besi", use_container_width=True):
                be = 55.85
                g_fe = v_titran * n_kmno4 * be * 1e-3
                pct_fe = g_fe / v_sampel * 100 * 1000
                
                st.latex(r"\% Fe = \frac{V \times N \times BE}{V_{sampel}} \times 10^{-3} \times 100\%")
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Analisis:</h4>
                    <ul>
                        <li>Massa Fe = <b>{g_fe:.6f} g</b></li>
                        <li>Kadar Fe = <b>{pct_fe:.4f} % (b/v)</b></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                simpan_riwayat("Permanganometri", "Kadar Fe", {"V_sampel": v_sampel, "V_titran": v_titran}, {"g_Fe": g_fe, "%_Fe": pct_fe})

    # ==========================
    # 3. IODOMETRI
    # ==========================
    elif materi == "Iodometri":
        sub_iodo = st.selectbox(
            "📋 Pilih Analisis:",
            [
                "Standarisasi Natrium Tiosulfat dengan K2Cr2O7",
                "Penetapan Kadar Klor Aktif (Cl)"
            ]
        )
        
        # --- Standarisasi Tiosulfat ---
        if sub_iodo == "Standarisasi Natrium Tiosulfat dengan K2Cr2O7":
            st.subheader("⚗️ Standarisasi Na2S2O3 dengan K2Cr2O7")
            
            col1, col2 = st.columns(2)
            with col1:
                mg_baku = st.number_input("Bobot K2Cr2O7 (mg)", min_value=0.0, value=245.0)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100
