```python
import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="ChemiCalc v3.0",
    page_icon="🧪",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main{
background-color:#F7F9FA;
}

.result-box{
background-color:#EBF7F5;
padding:15px;
border-radius:10px;
border-left:5px solid #439A86;
}

</style>
""",unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if 'riwayat_perhitungan' not in st.session_state:
    st.session_state.riwayat_perhitungan=[]


# =====================================
# FUNGSI
# =====================================

def validasi_input(*nilai):

    for i in nilai:

        if i<=0:
            st.error("❌ Input harus > 0")
            return False

    return True


def simpan_ke_riwayat(
jenis,
sub_jenis,
input_data,
hasil_data):

    data={

    "timestamp":
    time.strftime(
    "%Y-%m-%d %H:%M:%S"),

    "jenis":jenis,
    "sub_jenis":sub_jenis,
    "input":input_data,
    "hasil":hasil_data

    }

    st.session_state.riwayat_perhitungan.append(data)



def export_csv():

    if len(
    st.session_state.riwayat_perhitungan
    )>0:

        data=[]

        for item in st.session_state.riwayat_perhitungan:

            row={

            "Waktu":
            item['timestamp'],

            "Jenis":
            item['jenis'],

            "Sub":
            item['sub_jenis']

            }

            row.update(item['hasil'])

            data.append(row)

        df=pd.DataFrame(data)

        csv=df.to_csv(
        index=False
        )

        st.download_button(
        "⬇ Download CSV",
        csv,
        "riwayat_chemicalc.csv",
        "text/csv"
        )



def hitung_normalitas(
mg_baku,
v_titran,
be,
fp):

    return mg_baku/(v_titran*be*fp)



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


# =====================================
# JUDUL
# =====================================

st.title(
"🧪 ChemiCalc v3.0"
)

st.write(
"""
Aplikasi perhitungan
kimia analisis kuantitatif
berbasis titrimetri
"""
)

st.divider()


# =====================================
# SIDEBAR
# =====================================

menu=st.sidebar.radio(

"Pilih Menu",

[
"🏠 Halaman Utama",
"🧮 Kalkulator",
"🎨 Simulasi Indikator",
"📈 Riwayat"
]

)

# =====================================
# HALAMAN UTAMA
# =====================================

if menu=="🏠 Halaman Utama":

    st.header(
    "Selamat Datang"
    )

    col1,col2,col3=st.columns(3)

    with col1:

        st.info(
        """
        🔬 Asidimetri
        - Standarisasi NaOH
        - Standarisasi HCl
        """
        )

    with col2:

        st.info(
        """
        💜 Permanganometri
        - KMnO4
        - Fe
        """
        )

    with col3:

        st.info(
        """
        💙 Kompleksiometri
        - EDTA
        - Kesadahan
        """
        )


# =====================================
# KALKULATOR
# =====================================

elif menu=="🧮 Kalkulator":

    metode=st.selectbox(

    "Pilih Metode",

    [
    "Standarisasi NaOH",
    "Standarisasi HCl",
    "Kesadahan Air"
    ]

    )



# ================================
# NaOH
# ================================

    if metode=="Standarisasi NaOH":

        st.subheader(
        "Standarisasi NaOH"
        )

        mg=st.number_input(
        "Bobot Asam Oksalat (mg)",
        value=630.0
        )

        labu=st.number_input(
        "Volume labu",
        value=100.0
        )

        pipet=st.number_input(
        "Volume pipet",
        value=25.0
        )

        titran=st.number_input(
        "Volume titran",
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

                if hasil<0.09:

                    st.warning(
                    "Normalitas terlalu rendah"
                    )

                elif hasil>0.11:

                    st.warning(
                    "Normalitas terlalu tinggi"
                    )

                else:

                    st.success(
                    "Normalitas sesuai"
                    )


                simpan_ke_riwayat(

                "Asidimetri",
                "NaOH",

                {
                "mg":mg
                },

                {
                "N":hasil
                }

                )



# ================================
# HCl
# ================================

    elif metode=="Standarisasi HCl":

        mg=st.number_input(
        "Bobot Boraks (mg)",
        value=1500.0
        )

        labu=st.number_input(
        "Volume labu",
        value=100.0
        )

        pipet=st.number_input(
        "Volume pipet",
        value=25.0
        )

        titran=st.number_input(
        "Volume titran",
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



# ================================
# KESADAHAN
# ================================

    elif metode=="Kesadahan Air":

        v_edta=st.number_input(
        "Volume EDTA",
        value=10.0
        )

        m_edta=st.number_input(
        "Molaritas EDTA",
        value=0.01
        )

        v_sampel=st.number_input(
        "Volume sampel",
        value=50.0
        )

        if st.button(
        "Hitung Kesadahan"
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



# =====================================
# SIMULASI INDIKATOR
# =====================================

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

    "Fenolftalein":
    {
    "range":[8.3,10],
    "warna":
    ["Tidak berwarna",
    "Merah muda"]
    },

    "Metil Orange":
    {
    "range":[3.1,4.4],
    "warna":
    ["Merah",
    "Kuning"]
    },

    "Metil Merah":
    {
    "range":[4.2,6.3],
    "warna":
    ["Merah",
    "Kuning"]
    },

    "EBT":
    {
    "range":[7,11],
    "warna":
    ["Merah anggur",
    "Biru"]
    }

    }

    pilih=st.selectbox(
    "Indikator",
    list(indikator.keys())
    )

    bawah=indikator[pilih]["range"][0]
    atas=indikator[pilih]["range"][1]

    if pH<bawah:

        warna=indikator[pilih]["warna"][0]

    elif pH>atas:

        warna=indikator[pilih]["warna"][1]

    else:

        warna="Perubahan warna"

    st.info(

    f"""
    pH = {pH}

    Rentang = {bawah}-{atas}

    Warna = {warna}
    """
    )


# =====================================
# RIWAYAT
# =====================================

elif menu=="📈 Riwayat":

    st.header(
    "Riwayat"
    )

    if len(
    st.session_state.riwayat_perhitungan
    )>0:

        st.dataframe(
        pd.DataFrame(
        st.session_state.riwayat_perhitungan
        )
        )

        export_csv()

    else:

        st.warning(
        "Belum ada data"
        )
```
