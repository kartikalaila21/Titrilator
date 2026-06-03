import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="TITRILATOR",
    page_icon="🧪",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
background-color:#F5F7FA;
}

/* Judul */

.judul{
font-size:50px;
font-weight:bold;
text-align:center;
color:#0B4F8A;
}

.subjudul{

text-align:center;
font-size:18px;
color:#444;
margin-bottom:35px;

}

/* Kartu */

.kartu{

background:white;
padding:20px;
border-radius:20px;

box-shadow:
0px 4px 15px rgba(
0,
0,
0,
0.1
);

height:220px;

}

.kartu h3{

color:#0B4F8A;

}

.kartu p{

color:black;
font-size:16px;

}

/* hasil */

.hasil{

padding:20px;

background:#D4EDDA;

border-left:
6px solid green;

border-radius:10px;

font-size:22px;

font-weight:bold;

color:black;

}

/* sidebar */

section[data-testid="stSidebar"]{

background:#0B4F8A;

}

section[data-testid="stSidebar"] *{

color:white;

}

</style>

""",unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================

if "riwayat" not in st.session_state:

    st.session_state.riwayat=[]


# =====================================================
# FUNGSI
# =====================================================

def simpan_riwayat(
jenis,
hasil
):

    data={

    "Waktu":
    datetime.now().strftime(
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
vt,
be,
fp
):

    return mg/(vt*be*fp)



def hitung_kesadahan(
v_edta,
m_edta,
v_sampel
):

    ppm=(
    v_edta*
    m_edta*
    100.09*
    1000
    )/v_sampel

    return ppm


# =====================================================
# HEADER
# =====================================================

st.markdown("""

<div class='judul'>

🧪 TITRILATOR

</div>

<div class='subjudul'>

Aplikasi digital untuk membantu
perhitungan titrimetri secara
cepat, akurat, dan interaktif

</div>

""",unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

menu=st.sidebar.radio(

"📌 Pilih Menu",

[
"🏠 Dashboard",
"🧮 Kalkulator",
"🎨 Simulasi Indikator",
"📈 Riwayat"
]

)

# =====================================================
# DASHBOARD
# =====================================================

if menu=="🏠 Dashboard":

    st.header(
    "Selamat Datang"
    )

    c1,c2,c3=st.columns(3)

    with c1:

        st.markdown("""

<div class='kartu'>

<h3>🔬 Asidimetri</h3>

<p>

• Standarisasi NaOH

• Standarisasi HCl

</p>

</div>

""",unsafe_allow_html=True)

    with c2:

        st.markdown("""

<div class='kartu'>

<h3>💜 Permanganometri</h3>

<p>

• Standarisasi KMnO₄

• Analisis Fe

</p>

</div>

""",unsafe_allow_html=True)


    with c3:

        st.markdown("""

<div class='kartu'>

<h3>💙 Kompleksiometri</h3>

<p>

• EDTA

• Kesadahan Air

</p>

</div>

""",unsafe_allow_html=True)

    st.divider()

    st.info("""

Fitur aplikasi:

✅ Perhitungan normalitas

✅ Perhitungan kesadahan

✅ Simulasi indikator

✅ Riwayat perhitungan

✅ Download CSV

""")


# =====================================================
# KALKULATOR
# =====================================================

elif menu=="🧮 Kalkulator":

    metode=st.selectbox(

    "Pilih Metode",

    [

    "Standarisasi NaOH",
    "Standarisasi HCl",
    "Kesadahan Air"

    ]

    )

    # =================================

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

        vt=st.number_input(
        "Volume Titran (mL)",
        value=25.0
        )

        if st.button(
        "Hitung"
        ):

            be=126.07/2
            fp=labu/pipet

            hasil=hitung_normalitas(
            mg,
            vt,
            be,
            fp
            )

            st.markdown(

f"""
<div class='hasil'>

Normalitas NaOH

<br><br>

{hasil:.5f} N

</div>
""",

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

        vt=st.number_input(
        "Volume Titran",
        value=25.0
        )

        if st.button(
        "Hitung"
        ):

            be=381.37/2
            fp=labu/pipet

            hasil=hitung_normalitas(
            mg,
            vt,
            be,
            fp
            )

            st.markdown(

f"""
<div class='hasil'>

Normalitas HCl

<br><br>

{hasil:.5f} N

</div>
""",

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
        "Hitung"
        ):

            hasil=hitung_kesadahan(
            v_edta,
            m_edta,
            v_sampel
            )

            st.markdown(

f"""
<div class='hasil'>

Kesadahan Air

<br><br>

{hasil:.2f} ppm

</div>
""",

unsafe_allow_html=True
)

            simpan_riwayat(
            "Kesadahan",
            hasil
            )


# =====================================================
# SIMULASI
# =====================================================

elif menu=="🎨 Simulasi Indikator":

    st.subheader(
    "Simulasi pH"
    )

    ph=st.slider(
    "Pilih pH",
    0.0,
    14.0,
    7.0
    )

    st.metric(
    "Nilai pH",
    ph
    )


# =====================================================
# RIWAYAT
# =====================================================

elif menu=="📈 Riwayat":

    st.subheader(
    "Riwayat"
    )

    if len(
    st.session_state.riwayat
    )>0:

        df=pd.DataFrame(
        st.session_state.riwayat
        )

        st.dataframe(
        df,
        use_container_width=True
        )

        csv=df.to_csv(
        index=False
        ).encode(
        "utf-8"
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
