import streamlit as st
import pandas as pd
import time

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Titrilator v3.0",
    page_icon="🧪",
    layout="wide"
)

# ======================================
# CSS
# ======================================

st.markdown("""
<style>

.main{
background-color:#F8F9FA;
}

.result-box{
padding:15px;
background-color:#EBF7F5;
border-radius:10px;
border-left:5px solid teal;
}

</style>
""",unsafe_allow_html=True)

# ======================================
# SESSION
# ======================================

if "riwayat" not in st.session_state:
    st.session_state.riwayat=[]

# ======================================
# FUNCTION
# ======================================

def validasi(*angka):

    for x in angka:

        if x<=0:
            st.error("❌ Input harus lebih dari 0")
            return False

    return True


def simpan(jenis,hasil):

    data={

    "Waktu":
    time.strftime("%Y-%m-%d %H:%M:%S"),

    "Jenis":
    jenis,

    "Hasil":
    hasil

    }

    st.session_state.riwayat.append(data)



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

    ppm=(

    v_edta*
    m_edta*
    100.09*
    1000

    )/v_sampel

    return ppm


# ======================================
# HEADER
# ======================================

st.title("🧪 TITRILATOR v3.0")

st.write("""

Aplikasi digital untuk membantu
perhitungan titrimetri dan analisis
kimia kuantitatif secara cepat,
akurat, dan interaktif.

""")

st.divider()

# ======================================
# SIDEBAR
# ======================================

menu=st.sidebar.radio(

"Menu",

[
"🏠 Dashboard",
"🧮 Kalkulator",
"🎨 Simulasi Indikator",
"📈 Riwayat"
]

)

# ======================================
# DASHBOARD
# ======================================

if menu=="🏠 Dashboard":

    st.header(
    "Selamat Datang di TITRILATOR"
    )

    col1,col2,col3=st.columns(3)

    with col1:

        st.info("""
🔬 Asidimetri

• Standarisasi NaOH

• Standarisasi HCl
""")

    with col2:

        st.info("""
💜 Permanganometri

• KMnO₄

• Fe
""")

    with col3:

        st.info("""
💙 Kompleksiometri

• EDTA

• Kesadahan
""")



# ======================================
# KALKULATOR
# ======================================

elif menu=="🧮 Kalkulator":

    metode=st.selectbox(

    "Pilih metode",

    [

    "Standarisasi NaOH",

    "Standarisasi HCl",

    "Kesadahan Air"

    ]

    )

# ======================================
# NaOH
# ======================================

    if metode=="Standarisasi NaOH":

        st.subheader(
        "Standarisasi NaOH"
        )

        mg=st.number_input(
        "Bobot Asam Oksalat (mg)",
        min_value=0.0,
        value=630.0,
        step=0.1
        )

        labu=st.number_input(
        "Volume Labu (mL)",
        min_value=0.0,
        value=100.0,
        step=0.1
        )

        pipet=st.number_input(
        "Volume Pipet (mL)",
        min_value=0.0,
        value=25.0,
        step=0.1
        )

        titran=st.number_input(
        "Volume Titran (mL)",
        min_value=0.0,
        value=25.0,
        step=0.1
        )

        if st.button(
        "Hitung NaOH",
        key="naoh"
        ):

            if validasi(
            mg,
            labu,
            pipet,
            titran
            ):

                be=126.07/2

                fp=labu/pipet

                hasil=hitung_normalitas(
                mg,
                titran,
                be,
                fp
                )

                st.success(
                f"Normalitas NaOH = {hasil:.5f} N"
                )

                simpan(
                "NaOH",
                hasil
                )


# ======================================
# HCl
# ======================================

    elif metode=="Standarisasi HCl":

        mg=st.number_input(
        "Bobot Boraks (mg)",
        min_value=0.0,
        value=1500.0,
        step=0.1
        )

        labu=st.number_input(
        "Volume Labu (mL)",
        min_value=0.0,
        value=100.0,
        step=0.1
        )

        pipet=st.number_input(
        "Volume Pipet (mL)",
        min_value=0.0,
        value=25.0,
        step=0.1
        )

        titran=st.number_input(
        "Volume Titran (mL)",
        min_value=0.0,
        value=25.0,
        step=0.1
        )

        if st.button(
        "Hitung HCl",
        key="hcl"
        ):

            if validasi(
            mg,
            labu,
            pipet,
            titran
            ):

                be=381.37/2

                fp=labu/pipet

                hasil=hitung_normalitas(
                mg,
                titran,
                be,
                fp
                )

                st.success(
                f"Normalitas HCl = {hasil:.5f} N"
                )

                simpan(
                "HCl",
                hasil
                )


# ======================================
# KESADAHAN
# ======================================

    elif metode=="Kesadahan Air":

        v_edta=st.number_input(
        "Volume EDTA (mL)",
        min_value=0.0,
        value=10.0,
        step=0.1
        )

        m_edta=st.number_input(
        "Molaritas EDTA",
        min_value=0.0,
        value=0.01,
        step=0.001
        )

        v_sampel=st.number_input(
        "Volume Sampel (mL)",
        min_value=0.0,
        value=50.0,
        step=0.1
        )

        if st.button(
        "Hitung Kesadahan",
        key="kesadahan"
        ):

            if validasi(
            v_edta,
            m_edta,
            v_sampel
            ):

                ppm=hitung_kesadahan(
                v_edta,
                m_edta,
                v_sampel
                )

                st.success(
                f"Kesadahan = {ppm:.2f} ppm"
                )

                simpan(
                "Kesadahan",
                ppm
                )

# ======================================
# SIMULASI INDIKATOR
# ======================================

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

    "Fenolftalein":[8.3,10],
    "Metil Orange":[3.1,4.4],
    "Metil Merah":[4.2,6.3],
    "EBT":[7,11]

    }

    pilih=st.selectbox(
    "Pilih indikator",
    list(indikator.keys())
    )

    bawah=indikator[pilih][0]
    atas=indikator[pilih][1]

    if pH<bawah:
        warna="Warna awal"

    elif pH>atas:
        warna="Warna akhir"

    else:
        warna="Sedang berubah"

    st.info(f"""

Indikator : {pilih}

Rentang pH : {bawah}-{atas}

Status : {warna}

pH : {pH}

""")


# ======================================
# RIWAYAT
# ======================================

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
