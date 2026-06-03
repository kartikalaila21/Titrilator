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

# =====================================================
# SESSION
# =====================================================

if "riwayat" not in st.session_state:
    st.session_state.riwayat=[]


# =====================================================
# FUNGSI
# =====================================================

def simpan_riwayat(jenis,hasil):

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

    st.session_state.riwayat.append(data)



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

    return (
    v_edta*
    m_edta*
    100.09*
    1000
    )/v_sampel


# =====================================================
# HEADER
# =====================================================

st.markdown("""

<div class='judul'>
🧪 TITRILATOR
</div>

<div class='subjudul'>

Aplikasi digital untuk membantu
perhitungan titrimetri secara cepat,
akurat, dan interaktif

</div>

""",unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

menu=st.sidebar.radio(

"📌 Menu",

[
"🏠 Dashboard",
"🧮 Kalkulator",
"🎨 Simulasi Indikator",
"📊 Interpretasi",
"📈 Riwayat"
]

)

# =====================================================
# DASHBOARD
# =====================================================

if menu=="🏠 Dashboard":

    st.header(
    "Selamat Datang di TITRILATOR"
    )

    c1,c2,c3=st.columns(3)

    with c1:

        st.markdown("""

<div class='kartu'>
<h3>🔬 Asidimetri</h3>

<p>

• Standarisasi NaOH<br>
• Standarisasi HCl

</p>

</div>

""",unsafe_allow_html=True)

    with c2:

        st.markdown("""

<div class='kartu'>
<h3>💜 Permanganometri</h3>

<p>

• KMnO₄<br>
• Analisis Fe

</p>

</div>

""",unsafe_allow_html=True)

    with c3:

        st.markdown("""

<div class='kartu'>
<h3>💙 Kompleksiometri</h3>

<p>

• EDTA<br>
• Kesadahan Air

</p>

</div>

""",unsafe_allow_html=True)


    st.info("""

Fitur aplikasi:

✅ Perhitungan normalitas

✅ Simulasi indikator

✅ Interpretasi hasil

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

        if st.button("Hitung"):

            be=126.07/2
            fp=labu/pipet

            hasil=hitung_normalitas(
            mg,vt,be,fp
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

        vt=st.number_input(
        "Volume Titran",
        value=25.0
        )

        if st.button("Hitung"):

            be=381.37/2
            fp=labu/pipet

            hasil=hitung_normalitas(
            mg,vt,be,fp
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

        if st.button("Hitung"):

            hasil=hitung_kesadahan(
            v_edta,
            m_edta,
            v_sampel
            )

            st.markdown(
f"<div class='hasil'>Kesadahan Air = {hasil:.2f} ppm</div>",
unsafe_allow_html=True
)

            simpan_riwayat(
            "Kesadahan",
            hasil
            )

# =====================================================
# SIMULASI INDIKATOR
# =====================================================

elif menu=="🎨 Simulasi Indikator":

    st.header(
    "Simulasi Indikator"
    )

    indikator={

    "Fenolftalein":[8.3,10,"Tidak berwarna → Merah muda"],

    "Metil Orange":[3.1,4.4,"Merah → Kuning"],

    "Metil Merah":[4.2,6.3,"Merah → Kuning"],

    "EBT":[7,11,"Merah anggur → Biru"]

    }

    pilih=st.selectbox(
    "Pilih indikator",
    list(indikator.keys())
    )

    ph=st.slider(
    "Pilih pH",
    0.0,
    14.0,
    7.0
    )

    data=indikator[pilih]

    st.info(
f"""
Rentang pH : {data[0]} - {data[1]}

Perubahan warna:
{data[2]}

pH dipilih:
{ph}
"""
)

# =====================================================
# INTERPRETASI
# =====================================================

elif menu=="📊 Interpretasi":

    nilai=st.number_input(
    "Masukkan normalitas",
    value=0.1
    )

    if nilai<0.09:

        st.warning(
        "Larutan terlalu encer"
        )

    elif nilai>0.11:

        st.error(
        "Larutan terlalu pekat"
        )

    else:

        st.success(
        "Normalitas sesuai (~0.1 N)"
        )


# =====================================================
# RIWAYAT
# =====================================================

elif menu=="📈 Riwayat":

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
        "riwayat_titrilator.csv",
        "text/csv"
        )

    else:

        st.warning(
        "Belum ada riwayat"
        )
