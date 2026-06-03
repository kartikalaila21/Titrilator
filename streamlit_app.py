import streamlit as st
import pandas as pd
import time

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="TITRILATOR v3.0",
    page_icon="🧪",
    layout="wide"
)

# ==========================================
# TAMPILAN CSS
# ==========================================

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#f5f7fa,#e8f0ff);
}

.judul{
font-size:42px;
font-weight:bold;
text-align:center;
color:#0F4C81;
}

.subjudul{
font-size:18px;
text-align:center;
color:#444;
margin-bottom:30px;
}

.kartu{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 3px 10px rgba(0,0,0,0.1);
margin:10px;
}

.hasil{
background:#D4EDDA;
padding:20px;
border-radius:15px;
border-left:6px solid green;
font-size:18px;
font-weight:bold;
}

section[data-testid="stSidebar"]{
background:#0F4C81;
}

</style>
""",unsafe_allow_html=True)

# ==========================================
# SESSION
# ==========================================

if "riwayat" not in st.session_state:
    st.session_state.riwayat=[]

# ==========================================
# FUNGSI
# ==========================================

def validasi(*nilai):

    for x in nilai:

        if x<=0:

            st.error(
            "Input harus lebih dari nol"
            )

            return False

    return True


def simpan_riwayat(
jenis,
hasil):

    data={

    "Waktu":
    time.strftime(
    "%d-%m-%Y %H:%M:%S"
    ),

    "Jenis":
    jenis,

    "Hasil":
    hasil

    }

    st.session_state.riwayat.append(
    data
    )


def hitung_normalitas(
mg,
titran,
be,
fp):

    return mg/(titran*be*fp)


def hitung_kesadahan(
v_edta,
m_edta,
v_sampel):

    return (
    v_edta*
    m_edta*
    100.09*
    1000
    )/v_sampel


# ==========================================
# HEADER
# ==========================================

st.markdown("""

<div class='judul'>
🧪 TITRILATOR v3.0
</div>

<div class='subjudul'>
Aplikasi digital titrimetri untuk membantu
praktikum kimia analisis kuantitatif
secara cepat, akurat, dan interaktif
</div>

""",unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

menu=st.sidebar.radio(

"Menu",

[
"🏠 Dashboard",
"🧮 Kalkulator",
"🎨 Simulasi Indikator",
"📈 Riwayat"
]

)

# ==========================================
# DASHBOARD
# ==========================================

if menu=="🏠 Dashboard":

    st.header(
    "Selamat Datang di TITRILATOR"
    )

    c1,c2,c3=st.columns(3)

    with c1:

        st.markdown("""

<div class='kartu'>

<h3>🔬 Asidimetri</h3>

✅ Standarisasi NaOH

✅ Standarisasi HCl

</div>

""",unsafe_allow_html=True)

    with c2:

        st.markdown("""

<div class='kartu'>

<h3>💜 Permanganometri</h3>

✅ KMnO₄

✅ Fe

</div>

""",unsafe_allow_html=True)

    with c3:

        st.markdown("""

<div class='kartu'>

<h3>💙 Kompleksiometri</h3>

✅ EDTA

✅ Kesadahan Air

</div>

""",unsafe_allow_html=True)

    st.info("""

Fitur aplikasi:

• Perhitungan normalitas

• Perhitungan kesadahan

• Simulasi indikator

• Penyimpanan riwayat

• Download hasil CSV

""")


# ==========================================
# KALKULATOR
# ==========================================

elif menu=="🧮 Kalkulator":

    metode=st.selectbox(

    "Pilih metode",

    [
    "Standarisasi NaOH",
    "Standarisasi HCl",
    "Kesadahan Air"
    ]

    )


    if metode=="Standarisasi NaOH":

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

            be=126.07/2
            fp=labu/pipet

            hasil=hitung_normalitas(
            mg,
            titran,
            be,
            fp
            )

            st.markdown(
f"<div class='hasil'>Normalitas NaOH = {hasil:.5f} N</div>",
unsafe_allow_html=True
)

            simpan_riwayat(
            "NaOH",
            hasil
            )


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

            be=381.37/2
            fp=labu/pipet

            hasil=hitung_normalitas(
            mg,
            titran,
            be,
            fp
            )

            st.markdown(
f"<div class='hasil'>Normalitas HCl = {hasil:.5f} N</div>",
unsafe_allow_html=True
)

            simpan_riwayat(
            "HCl",
            hasil
            )


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

            hasil=hitung_kesadahan(
            v_edta,
            m_edta,
            v_sampel
            )

            st.markdown(
f"<div class='hasil'>Kesadahan = {hasil:.2f} ppm</div>",
unsafe_allow_html=True
)

            simpan_riwayat(
            "Kesadahan",
            hasil
            )

# ==========================================
# SIMULASI INDIKATOR
# ==========================================

elif menu=="🎨 Simulasi Indikator":

    pH=st.slider(
    "Pilih pH",
    0.0,
    14.0,
    7.0
    )

    st.write(
    f"Nilai pH : {pH}"
    )

# ==========================================
# RIWAYAT
# ==========================================

elif menu=="📈 Riwayat":

    if len(
    st.session_state.riwayat
    )>0:

        df=pd.DataFrame(
        st.session_state.riwayat
        )

        st.dataframe(df)

        csv=df.to_csv(
        index=False
        ).encode(
        "utf-8"
        )

        st.download_button(
        "Download CSV",
        csv,
        "riwayat_titrilator.csv"
        )

    else:

        st.warning(
        "Belum ada riwayat"
        )
