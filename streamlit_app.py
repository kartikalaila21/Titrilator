```python
import streamlit as st
import pandas as pd
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="ChemiCalc v3.0",
    page_icon="🧪",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.main {
    background-color:#F7F9FA;
}

.result-box{
    background-color:#EBF7F5;
    padding:15px;
    border-radius:10px;
    border-left:5px solid #439A86;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if 'riwayat' not in st.session_state:
    st.session_state.riwayat=[]

# ==========================================
# FUNCTIONS
# ==========================================

def validasi_input(*angka):
    for x in angka:
        if x <= 0:
            st.error("❌ Nilai harus lebih dari 0")
            return False
    return True


def simpan_riwayat(jenis,hasil):

    data={

        "Waktu":time.strftime(
        "%Y-%m-%d %H:%M:%S"),

        "Jenis":jenis,

        "Hasil":hasil
    }

    st.session_state.riwayat.append(data)



def hitung_normalitas(
mg_baku,
volume_titran,
be,
fp):

    return mg_baku/(volume_titran*be*fp)



def hitung_kesadahan(
v_edta,
m_edta,
v_sampel):

    BM_CACO3=100.09

    ppm=(
        v_edta*
        m_edta*
        BM_CACO3*
        1000
    )/v_sampel

    return ppm


# ==========================================
# TITLE
# ==========================================

st.title("🧪 ChemiCalc v3.0")
st.write(
"Kalkulator praktikum kimia analisis kuantitatif"
)

st.divider()

# ==========================================
# SIDEBAR
# ==========================================

menu=st.sidebar.radio(

"Pilih Menu",

[
"🏠 Halaman Utama",
"🧮 Kalkulator",
"🎨 Simulasi Indikator",
"📈 Riwayat"
]

)

# ==========================================
# HALAMAN UTAMA
# ==========================================

if menu=="🏠 Halaman Utama":

    st.header("Selamat Datang")

    col1,col2,col3=st.columns(3)

    with col1:
        st.info("""
🔬 Asidimetri
- Standarisasi NaOH
- Standarisasi HCl
""")

    with col2:
        st.info("""
💜 Permanganometri
- KMnO₄
- Fe
""")

    with col3:
        st.info("""
💙 Kompleksiometri
- EDTA
- Kesadahan
""")


# ==========================================
# KALKULATOR
# ==========================================

elif menu=="🧮 Kalkulator":

    metode=st.selectbox(

        "Pilih Metode",

        [
        "Standarisasi NaOH",
        "Standarisasi HCl",
        "Kesadahan Air"
        ]
    )

# =====================================
# NaOH
# =====================================

    if metode=="Standarisasi NaOH":

        st.subheader(
        "Standarisasi NaOH"
        )

        mg=st.number_input(
        "Bobot Asam Oksalat (mg)",
        value=630.0
        )

        labu=st.number_input(
        "Volume Labu (mL)",
        value=100.0
        )

        pipet=st.number_input(
        "Volume Pipet (mL)",
        value=25.0
        )

        titran=st.number_input(
        "Volume Titran (mL)",
        value=25.0
        )

        if st.button(
        "Hitung NaOH"
        ):

            if validasi_input(
            mg,
            labu,
            pipet,
            titran
            ):

                be=126.07/2
                fp=labu/pipet

                hasil=(
                hitung_normalitas(
                mg,
                titran,
                be,
                fp
                )
                )

                st.success(
                f"Normalitas = {hasil:.5f} N"
                )

                simpan_riwayat(
                "NaOH",
                hasil
                )


# =====================================
# HCl
# =====================================

    elif metode=="Standarisasi HCl":

        mg=st.number_input(
        "Bobot Boraks (mg)",
        value=1500.0
        )

        labu=st.number_input(
        "Volume Labu (mL)",
        value=100.0
        )

        pipet=st.number_input(
        "Volume Pipet (mL)",
        value=25.0
        )

        titran=st.number_input(
        "Volume Titran (mL)",
        value=25.0
        )

        if st.button(
        "Hitung HCl"
        ):

            if validasi_input(
            mg,
            labu,
            pipet,
            titran
            ):

                be=381.37/2
                fp=labu/pipet

                hasil=(
                hitung_normalitas(
                mg,
                titran,
                be,
                fp
                )
                )

                st.success(
                f"Normalitas HCl = {hasil:.5f} N"
                )

                simpan_riwayat(
                "HCl",
                hasil
                )

# =====================================
# KESADAHAN
# =====================================

    elif metode=="Kesadahan Air":

        v_edta=st.number_input(
        "Volume EDTA (mL)",
        value=10.0
        )

        m_edta=st.number_input(
        "Molaritas EDTA",
        value=0.01
        )

        v_sampel=st.number_input(
        "Volume Sampel (mL)",
        value=50.0
        )

        if st.button(
        "Hitung Kesadahan"
        ):

            if validasi_input(
            v_edta,
            m_edta,
            v_sampel
            ):

                ppm=(
                hitung_kesadahan(
                v_edta,
                m_edta,
                v_sampel
                )
                )

                st.success(
                f"Kesadahan = {ppm:.2f} ppm"
                )

                simpan_riwayat(
                "Kesadahan",
                ppm
                )


# ==========================================
# SIMULASI INDIKATOR
# ==========================================

elif menu=="🎨 Simulasi Indikator":

    st.header(
    "Simulasi Indikator"
    )

    pH=st.slider(
    "Pilih pH",
    0.0,
    14.0,
    7.0
    )

    indikator={

    "Fenolftalein":[8.3,10,"Tidak berwarna → Merah muda"],

    "Metil Orange":[3.1,4.4,"Merah → Kuning"],

    "Metil Merah":[4.2,6.3,"Merah → Kuning"],

    "EBT":[7,11,"Merah anggur → Biru"]

    }

    pilih=st.selectbox(
    "Indikator",
    list(indikator.keys())
    )

    bawah=indikator[pilih][0]
    atas=indikator[pilih][1]

    warna=indikator[pilih][2]

    st.info(
f"""
Rentang pH : {bawah}-{atas}

Perubahan Warna :
{warna}

pH dipilih:
{pH}
"""
)


# ==========================================
# RIWAYAT
# ==========================================

elif menu=="📈 Riwayat":

    st.header(
    "Riwayat Perhitungan"
    )

    if len(
    st.session_state.riwayat
    )>0:

        df=pd.DataFrame(
        st.session_state.riwayat
        )

        st.dataframe(df)

        csv=df.to_csv(
        index=False
        )

        st.download_button(

        "⬇ Download CSV",

        csv,

        "riwayat.csv",

        "text/csv"

        )

    else:

        st.warning(
        "Belum ada riwayat"
        )
```
