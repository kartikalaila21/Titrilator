import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="TITRILATOR",
    page_icon="🧪",
    layout="wide"
)

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
.stApp{
    background-color:#F5F7FA;
}
.judul{
    font-size:45px;
    font-weight:bold;
    text-align:center;
    color:#0B4F8A;
}
.subjudul{
    text-align:center;
    font-size:18px;
    color:#444;
    margin-bottom:30px;
}
.kartu{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.1);
    height:220px;
}
.kartu h3{
    color:#0B4F8A;
}
.kartu p{
    color:black;
    font-size:16px;
}
.hasil{
    padding:20px;
    background:#D4EDDA;
    border-left:6px solid green;
    border-radius:10px;
    font-size:20px;
    font-weight:bold;
    color:black;
}
section[data-testid="stSidebar"]{
    background:#0B4F8A;
}
section[data-testid="stSidebar"] *{
    color:white;
}
</style>
""",unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
if "riwayat" not in st.session_state:
    st.session_state.riwayat=[]

# ==========================================
# FUNGSI BANTU
# ==========================================
def simpan_riwayat(jenis, hasil):
    data={
        "Waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Jenis": jenis,
        "Hasil": hasil
    }
    st.session_state.riwayat.append(data)

def hitung_normalitas(mg, vt, be, fp):
    return mg/(vt*be*fp)

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class='judul'>🧪 TITRILATOR</div>
<div class='subjudul'>Aplikasi digital untuk perhitungan titrimetri secara cepat, akurat, dan interaktif</div>
""",unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
menu=st.sidebar.radio(
    "📌 Menu",
    ["🏠 Dashboard", "🧮 Kalkulator", "🎨 Simulasi Indikator", "📊 Interpretasi", "📈 Riwayat"]
)

# ==========================================
# DASHBOARD
# ==========================================
if menu=="🏠 Dashboard":
    st.header("Selamat Datang di TITRILATOR")
    
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("""
<div class='kartu'>
<h3>🔬 Asidimetri</h3>
<p>• Standarisasi NaOH<br>• Standarisasi HCl<br>• Kadar Campuran</p>
</div>
""",unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class='kartu'>
<h3>💜 Permanganometri</h3>
<p>• Standarisasi KMnO4<br>• Kadar Besi (Fe)</p>
</div>
""",unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class='kartu'>
<h3>💙 Kompleksiometri</h3>
<p>• Standarisasi EDTA<br>• Kesadahan Air</p>
</div>
""",unsafe_allow_html=True)
    
    c4,c5=st.columns(2)
    with c4:
        st.markdown("""
<div class='kartu'>
<h3>🟡 Iodometri</h3>
<p>• Standarisasi Na2S2O3<br>• Kadar Klor Aktif</p>
</div>
""",unsafe_allow_html=True)
    with c5:
        st.markdown("""
<div class='kartu'>
<h3>🎨 Indikator</h3>
<p>• Simulasi Warna<br>• Interpretasi</p>
</div>
""",unsafe_allow_html=True)
    
    st.info("""
📌 FITUR APLIKASI:
✅ Perhitungan Normalitas (N)
✅ Perhitungan Molaritas (M)  
✅ Perhitungan Kadar (% b/v)
✅ Kesadahan Air (ppm)
✅ Simulasi Indikator
✅ Interpretasi Hasil
✅ Riwayat Perhitungan
✅ Download CSV
""")

# ==========================================
# KALKULATOR
# ==========================================
elif menu=="🧮 Kalkulator":
    st.header("🧮 Kalkulator Titrimetri")
    
    metode=st.selectbox(
        "Pilih Metode",
        ["Asidimetri & Alkalimetri", "Permanganometri", "Iodometri", "Kompleksiometri"]
    )
    
    st.markdown("---")
    
    # ASIDIMETRI
    if metode=="Asidimetri & Alkalimetri":
        submenu=st.selectbox(
            "Pilih Analisis",
            ["Standarisasi NaOH", "Standarisasi HCl", "Kadar Campuran Warder"]
        )
        
        if submenu=="Standarisasi NaOH":
            st.subheader("⚗️ Standarisasi NaOH")
            c1,c2=st.columns(2)
            with c1:
                mg=st.number_input("Bobot Asam Oksalat (mg)", value=630.0)
                labu=st.number_input("Volume Labu (mL)", value=100.0)
            with c2:
                pipet=st.number_input("Volume Pipet (mL)", value=25.0)
                vt=st.number_input("Volume Titran (mL)", value=25.0)
            
            if st.button("Hitung"):
                be=126.07/2
                fp=labu/pipet
                hasil=hitung_normalitas(mg,vt,be,fp)
                st.markdown(f"<div class='hasil'>Normalitas NaOH = {hasil:.5f} N</div>",unsafe_allow_html=True)
                simpan_riwayat("NaOH", f"{hasil:.5f} N")
        
        elif submenu=="Standarisasi HCl":
            st.subheader("⚗️ Standarisasi HCl")
            c1,c2=st.columns(2)
            with c1:
                mg=st.number_input("Bobot Boraks (mg)", value=1500.0)
                labu=st.number_input("Volume Labu (mL)", value=100.0)
            with c2:
                pipet=st.number_input("Volume Pipet (mL)", value=25.0)
                vt=st.number_input("Volume Titran (mL)", value=25.0)
            
            if st.button("Hitung"):
                be=381.37/2
                fp=labu/pipet
                hasil=hitung_normalitas(mg,vt,be,fp)
                st.markdown(f"<div class='hasil'>Normalitas HCl = {hasil:.5f} N</div>",unsafe_allow_html=True)
                simpan_riwayat("HCl", f"{hasil:.5f} N")
        
        elif submenu=="Kadar Campuran Warder":
            st.subheader("⚗️ Kadar Campuran NaOH & Na2CO3")
            c1,c2=st.columns(2)
            with c1:
                vsampel=st.number_input("Volume Sampel (mL)", value=25.0)
                n_hcl=st.number_input("Normalitas HCl (N)", value=0.1, format="%.4f")
            with c2:
                vol_a=st.number_input("Volume a - PP (mL)", value=15.0)
                vol_b=st.number_input("Volume b - MO (mL)", value=25.0)
            
            if st.button("Hitung"):
                if vol_b < vol_a:
                    st.error("Volume b tidak boleh lebih kecil dari a!")
                else:
                    be_na2co3=105.99/2
                    be_naoh=40.00
                    g_na2co3=2*(vol_b-vol_a)*n_hcl*be_na2co3*1e-3
                    g_naoh=((2*vol_a)-vol_b)*n_hcl*be_naoh*1e-3
                    pct_na2co3=(g_na2co3/vsampel)*100*1000
                    pct_naoh=(g_naoh/vsampel)*100*1000
                    st.markdown(f"<div class='hasil'>Na2CO3 = {pct_na2co3:.4f}% | NaOH = {pct_naoh:.4f}%</div>",unsafe_allow_html=True)
                    simpan_riwayat("Warder", f"Na2CO3:{pct_na2co3:.4f}%, NaOH:{pct_naoh:.4f}%")

    # PERMANGANOMETRI
    elif metode=="Permanganometri":
        submenu=st.selectbox("Pilih Analisis", ["Standarisasi KMnO4", "Kadar Besi (Fe)"])
        
        if submenu=="Standarisasi KMnO4":
            st.subheader("⚗️ Standarisasi KMnO4")
            c1,c2=st.columns(2)
            with c1:
                mg=st.number_input("Bobot Asam Oksalat (mg)", value=630.0)
                labu=st.number_input("Volume Labu (mL)", value=100.0)
            with c2:
                pipet=st.number_input("Volume Pipet (mL)", value=25.0)
                vt=st.number_input("Volume KMnO4 (mL)", value=25.0)
            
            if st.button("Hitung"):
                be=126.07/2
                fp=labu/pipet
                hasil=hitung_normalitas(mg,vt,be,fp)
                st.markdown(f"<div class='hasil'>Normalitas KMnO4 = {hasil:.5f} N</div>",unsafe_allow_html=True)
                simpan_riwayat("KMnO4", f"{hasil:.5f} N")
        
        elif submenu=="Kadar Besi (Fe)":
            st.subheader("⚗️ Kadar Besi (Fe)")
            c1,c2=st.columns(2)
            with c1:
                vsampel=st.number_input("Volume Sampel (mL)", value=25.0)
                n_kmno4=st.number_input("Normalitas KMnO4 (N)", value=0.1, format="%.4f")
            with c2:
                vt=st.number_input("Volume Titran (mL)", value=24.50)
            
            if st.button("Hitung"):
                be_fe=55.85
                gram=vt*n_kmno4*be_fe*1e-3
                pct=(gram/vsampel)*100*1000
                st.markdown(f"<div class='hasil'>Massa Fe = {gram:.5f} g | Kadar = {pct:.4f}%</div>",unsafe_allow_html=True)
                simpan_riwayat("Fe", f"{pct:.4f}%")

    # IODOMETRI
    elif metode=="Iodometri":
        submenu=st.selectbox("Pilih Analisis", ["Standarisasi Na2S2O3", "Kadar Klor Aktif"])
        
        if submenu=="Standarisasi Na2S2O3":
            st.subheader("⚗️ Standarisasi Na2S2O3")
            c1,c2=st.columns(2)
            with c1:
                mg=st.number_input("Bobot K2Cr2O7 (mg)", value=245.0)
                labu=st.number_input("Volume Labu (mL)", value=100.0)
            with c2:
                pipet=st.number_input("Volume Pipet (mL)", value=25.0)
                vt=st.number_input("Volume Titran (mL)", value=25.0)
            
            if st.button("Hitung"):
                be=294.19/6
                fp=labu/pipet
                hasil=hitung_normalitas(mg,vt,be,fp)
                st.markdown(f"<div class='hasil'>Normalitas Na2S2O3 = {hasil:.5f} N</div>",unsafe_allow_html=True)
                simpan_riwayat("Na2S2O3", f"{hasil:.5f} N")
        
        elif submenu=="Kadar Klor Aktif":
            st.subheader("⚗️ Kadar Klor Aktif (Cl)")
            c1,c2=st.columns(2)
            with c1:
                vsampel=st.number_input("Volume Sampel (mL)", value=5.0)
                n_tio=st.number_input("Normalitas Na2S2O3 (N)", value=0.1, format="%.4f")
            with c2:
                vt=st.number_input("Volume Titran (mL)", value=15.20)
            
            if st.button("Hitung"):
                be_cl=35.453/2
                gram=vt*n_tio*be_cl*1e-3
                pct=(gram/vsampel)*100*1000
                st.markdown(f"<div class='hasil'>Massa Cl = {gram:.5f} g | Kadar = {pct:.4f}%</div>",unsafe_allow_html=True)
                simpan_riwayat("Cl", f"{pct:.4f}%")

    # KOMPLEKSIOMETRI
    elif metode=="Kompleksiometri":
        submenu=st.selectbox("Pilih Analisis", ["Standarisasi EDTA", "Kesadahan Air"])
        
        if submenu=="Standarisasi EDTA":
            st.subheader("⚗️ Standarisasi EDTA")
            c1,c2=st.columns(2)
            with c1:
                mg=st.number_input("Bobot CaCO3 (mg)", value=100.0)
                labu=st.number_input("Volume Labu (mL)", value=100.0)
            with c2:
                pipet=st.number_input("Volume Pipet (mL)", value=25.0)
                vt=st.number_input("Volume EDTA (mL)", value=25.0)
            
            if st.button("Hitung"):
                bm=100.09
                fp=labu/pipet
                hasil=mg/(vt*bm*fp)
                st.markdown(f"<div class='hasil'>Molaritas EDTA = {hasil:.5f} M</div>",unsafe_allow_html=True)
                simpan_riwayat("EDTA", f"{hasil:.5f} M")
        
        elif submenu=="Kesadahan Air":
            st.subheader("⚗️ Kesadahan Air")
            c1,c2=st.columns(2)
            with c1:
                v_edta=st.number_input("Volume EDTA (mL)", value=10.0)
                m_edta=st.number_input("Molaritas EDTA", value=0.01, format="%.4f")
            with c2:
                v_sampel=st.number_input("Volume Sampel Air (mL)", value=50.0)
            
            if st.button("Hitung"):
                hasil=(v_edta*m_edta*100.09*1000)/v_sampel
                st.markdown(f"<div class='hasil'>Kesadahan = {hasil:.2f} ppm</div>",unsafe_allow_html=True)
                simpan_riwayat("Kesadahan", f"{hasil:.2f} ppm")

# ==========================================
# SIMULASI INDIKATOR
# ==========================================
elif menu=="🎨 Simulasi Indikator":
    st.header("🎨 Simulasi Indikator")
    
    indikator={
        "Fenolftalein": [8.3, 10, "Tidak berwarna → Merah muda"],
        "Metil Orange": [3.1, 4.4, "Merah → Kuning"],
        "Metil Merah": [4.2, 6.3, "Merah → Kuning"],
        "EBT (Eriochrome Black T)": [7, 11, "Merah anggur → Biru"]
    }
    
    pilih=st.selectbox("Pilih Indikator", list(indikator.keys()))
    ph=st.slider("Pilih pH", 0.0, 14.0, 7.0)
    
    data=indikator[pilih]
    ph_min, ph_max = data[0], data[1]
    
    if ph < ph_min:
        warna = "Tidak berwarna"
    elif ph > ph_max:
        warna = data[2].split("→ ")[1]
    else:
        warna = "Transisi"
    
    st.info(f"""
    **Indikator:** {pilih}
    **Rentang pH:** {ph_min} - {ph_max}
    **Perubahan:** {data[2]}
    **pH dipilih:** {ph}
    **Warna:** {warna}
    """)

# ==========================================
# INTERPRETASI
# ==========================================
elif menu=="📊 Interpretasi":
    st.header("📊 Interpretasi Hasil")
    
    nilai=st.number_input("Masukkan Normalitas", value=0.1, format="%.4f")
    
    if nilai < 0.09:
        st.warning("Larutan terlalu encer - pertimbangkan untuk mengencerkan")
    elif nilai > 0.11:
        st.error("Larutan terlalu pekat - pertimbangkan untuk mengencerkan")
    else:
        st.success("Normalitas sesuai standar")

# ==========================================
# RIWAYAT
# ==========================================
elif menu=="📈 Riwayat":
    st.header("📈 Riwayat Perhitungan")
    
    if len(st.session_state.riwayat) > 0:
