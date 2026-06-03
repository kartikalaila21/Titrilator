<think>
The user wants to change the application name from "ChemiCalc" to "Titrilator". I need to update all occurrences of "ChemiCalc" in the code to "Titrilator". Let me rewrite the complete code with this change.
</think>

Berikut kode lengkap aplikasi ChemiCalc (sekarang bernama **Titrilator**) yang sudah diperbaiki dan dilengkapi:

```python
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import io

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
    .warning-box { background-color: #FFF3CD; padding: 15px; border-radius: 8px; border-left: 4px solid #FFC107; }
    .error-box { background-color: #F8D7DA; padding: 15px; border-radius: 8px; border-left: 4px solid #DC3545; }
    .success-box { background-color: #D4EDDA; padding: 15px; border-radius: 8px; border-left: 4px solid #28A745; }
    section[data-testid="stSidebar"] { background-color: #F1F5F4; }
    .metric-card { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'riwayat_perhitungan' not in st.session_state:
    st.session_state.riwayat_perhitungan = []

if 'data_hasil' not in st.session_state:
    st.session_state.data_hasil = {}

# ==========================================
# FUNGSI BANTU
# ==========================================
def simpan_riwayat(jenis, sub, inp, hasil):
    """Simpan perhitungan ke riwayat"""
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
    """Konversi miligram ekuivalen ke gram"""
    return mgekivalen * 1e-3

def hitung_kadar_persen(massa_gram, volume_sampel_mL):
    """Hitung kadar dalam % b/v"""
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
    st.subheader("ℹ️ Info Aplikasi")
    st.markdown("""
    **Titrilator v1.0**
    
    Fitur:
    - ✅ Standarisasi (N & M)
    - ✅ Kadar Sampel (g & %)
    - ✅ Simulasi Warna
    - ✅ Riwayat Otomatis
    - ✅ Ekspor CSV
    """)
    
    if len(st.session_state.riwayat_perhitungan) > 0:
        st.markdown("---")
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
    
    Semua parameter perhitungan kadar sampel telah dikonversi secara standar:
    - **Gram (g)** untuk massa absolut
    - **% (b/v)** untuk konsentrasi relatif
    - **ppm** untuk kesadahan air
    """)
    
    # Fitur yang tersedia
    st.subheader("🚀 Menu Perhitungan yang Tersedia:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("""
        **🔬 Asidimetri & Alkalimetri**
        - Standarisasi NaOH (Asam Oksalat)
        - Standarisasi HCl (Boraks)
        - Kadar Campuran Warder
        """)
    with col2:
        st.info("""
        **💜 Permanganometri**
        - Standarisasi KMnO₄
        - Kadar Besi (Fe)
        """)
    with col3:
        st.info("""
        **🟡 Iodometri**
        - Standarisasi Na₂S₂O₃
        - Kadar Klor Aktif (Cl)
        """)
    
    col4, col5 = st.columns(2)
    with col4:
        st.info("""
        **💙 Kompleksiometri**
        - Standarisasi EDTA
        - Kesadahan Jumlah Air
        """)
    with col5:
        st.info("""
        **🎨 Fitur Lainnya**
        - Simulasi Warna Indikator
        - Riwayat Perhitungan
        - Panduan Penggunaan
        """)

# ==========================================
# MENU 2: KALKULATOR HITUNG
# ==========================================
elif menu_utama == "🧮 Kalkulator Hitung":
    st.header("🧮 Kalkulator Parameter Titrasi")
    
    # Pilih Metode
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
            st.caption("Reaksi: C₂H₂O₄·2H₂O + 2NaOH → Na₂C₂O₄ + 4H₂O")
            
            col1, col2 = st.columns(2)
            with col1:
                mg_baku = st.number_input("Bobot Asam Oksalat (mg)", min_value=0.0, value=630.0, step=0.1)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0, step=1.0)
            with col2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0, step=0.1)
                v_titran = st.number_input("Volume Titran NaOH (mL)", min_value=0.01, value=25.0, step=0.1)
            
            st.caption(f"**BM Asam Oksalat:** 126.07 g/mol | **Valensi:** 2 | **BE:** {126.07/2:.4f}")
            
            if st.button("🚀 Hitung Normalitas NaOH", use_container_width=True):
                be_oksalat = 126.07 / 2
                fp = v_labu / v_pipet
                penyebut = v_titran * be_oksalat * fp
                n_naoh = mg_baku / penyebut
                massa_aliquot = (mg_baku / fp) * 1e-3
                
                st.markdown("### 📐 Rumus:")
                st.latex(r"N_{NaOH} = \frac{mg_{baku}}{V_{titran} \times BE \times fp}")
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Standarisasi:</h4>
                    <big>Normalitas NaOH = <b>{n_naoh:.6f} N</b></big><br><br>
                    <b>Detail:</b><br>
                    • BE = {be_oksalat:.4f} | fp = {fp:.2f}<br>
                    • Penyebut = {penyebut:.4f}<br>
                    • Massa C₂H₂O₄·2H₂O dalam aliquot = {massa_aliquot:.6f} g
                </div>
                """, unsafe_allow_html=True)
                
                simpan_riwayat("Asidimetri", "Standarisasi NaOH", 
                    {"mg_baku": mg_baku, "V_labu": v_labu, "V_pipet": v_pipet, "V_titran": v_titran},
                    {"N_NaOH": n_naoh, "BE": be_oksalat, "fp": fp})

        # --- Standarisasi HCl ---
        elif sub_asidi == "Standarisasi HCl dengan Boraks":
            st.subheader("⚗️ Standarisasi HCl dengan Boraks")
            st.caption("Reaksi: Na₂B₄O₇·10H₂O + 2HCl → 2H₃BO₃ + 2NaCl + 5H₂O")
            
            col1, col2 = st.columns(2)
            with col1:
                mg_baku = st.number_input("Bobot Boraks (mg)", min_value=0.0, value=1500.0, step=0.1)
                v_labu = st.number_input("Volume Labu Takar (mL)", min_value=1.0, value=100.0, step=1.0)
            with col2:
                v_pipet = st.number_input("Volume Pipet Aliquot (mL)", min_value=1.0, value=25.0, step=0.1)
                v_titran = st.number_input("Volume Titran HCl (mL)", min_value=0.01, value=25.0, step=0.1)
            
            st.caption(f"**BM Boraks:** 381.37 g/mol | **Valensi:** 2 | **BE:** {381.37/2:.4f}")
            
            if st.button("🚀 Hitung Normalitas HCl", use_container_width=True):
                be_boraks = 381.37 / 2
                fp = v_labu / v_pipet
                penyebut = v_titran * be_boraks * fp
                n_hcl = mg_baku / penyebut
                
                st.markdown("### 📐 Rumus:")
                st.latex(r"N_{HCl} = \frac{mg_{baku}}{V_{titran} \times BE \times fp}")
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Standarisasi:</h4>
                    <big>Normalitas HCl = <b>{n_hcl:.6f} N</b></big><br><br>
                    <b>Detail:</b><br>
                    • BE = {be_boraks:.4f} | fp = {fp:.2f}<br>
                    • Penyebut = {penyebut:.4f}
                </div>
                """, unsafe_allow_html=True)
                
                simpan_riwayat("Asidimetri", "Standarisasi HCl",
                    {"mg_baku": mg_baku, "V_labu": v_labu, "V_pipet": v_pipet, "V_titran": v_titran},
                    {"N_HCl": n_hcl, "BE": be_boraks, "fp": fp})

        # --- Campuran Warder ---
        elif sub_asidi == "Penetapan Kadar Campuran Warder (NaOH & Na2CO3)":
            st.subheader("⚗️ Kadar Campuran Warder (NaOH & Na₂CO₃)")
            st.caption("Titik akhir: a = PP (merah muda), b = MO (biru ke abu-abu)")
            
            col1, col2 = st.columns(2)
            with col1:
                v_sampel = st.number_input("Volume Sampel (mL)", min_value=1.0, value=25.0)
                n_hcl = st.number_input("Normalitas HCl Standar (N)", min_value=0.0, value=0.1000, format="%.4f")
            with col2:
                vol_a = st.number_input("Volume Titrasi I - PP (a mL)", min_value=0.0, value=15.0)
                vol_b = st.number_input("Volume Total Buret - MO (b mL)", min_value=0.0, value=25.0)
            
            if st.button("🚀 Hitung Kadar Campuran", use_container_width=True):
                if vol_b < vol_a:
                    st.error("⚠️ Volume b tidak boleh lebih kecil dari volume a!")
                else:
                    be_na2co3 = 105.99 / 2
                    be_naoh = 40.00
                    
                    # Na2CO3
                    mgeq_na2co3 = 2 * (vol_b - vol_a) * n_hcl * be_na2co3
                    g_na2co3 = konversi_ke_gram(mgeq_na2co3)
                    pct_na2co3 = hitung_kadar_persen(g_na2co3, v_sampel)
                    
                    # NaOH
                    mgeq_naoh = ((2 * vol_a) - vol_b) * n_hcl * be_naoh
                    g_naoh = konversi_ke_gram(mgeq_naoh)
                    pct_naoh = hitung_kadar_persen(g_naoh, v_sampel)
                    
                    st.markdown("### 📐 Rumus:")
                    st.latex(r"\% = \frac{V \times N \times BE}{V_{sampel}} \times 10^{-3} \times 100\%")
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>✅ Hasil Analisis:</h4>
                        <ul>
                            <li><b>Na₂CO₃</b> = {g_na2co3:.6f} g (<b>{pct_na2co3:.4f} %b/v</b>)</li>
                            <li><b>NaOH</b> = {g_naoh:.6f} g (<b>{pct_naoh:.4f} %b/v</b>)</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    simpan_riwayat("Asidimetri", "Warder",
                        {"V_sampel": v_sampel, "N_HCl": n_hcl, "a": vol_a, "b": vol_b},
                        {"g_Na2CO3": g_na2co3, "g_NaOH": g_naoh, "%_Na2CO3": pct_na2co3, "%_NaOH": pct_naoh})

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
            st.subheader("⚗️ Standarisasi KMnO₄ dengan Asam Oksalat")
            st.caption("Reaksi: 5C₂O₄²⁻ + 2MnO₄⁻ + 16H⁺ →
