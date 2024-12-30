import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data
DATA_PATH = "G:\Tugas Ospek & Kuliah ITS\Dicoding 2024\day.csv"
data = pd.read_csv(DATA_PATH)

# Konfigurasi Streamlit
st.set_page_config(page_title="Dashboard Bike Sharing", page_icon="🚴", layout="wide")

# Gaya CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Beranda", "Visualisasi"])

if menu == "Beranda":
    st.title("Dashboard Bike Sharing")
    st.markdown(
        """
        ## Selamat Datang di Dashboard Bike Sharing 🚴‍♂️

        Dashboard ini dirancang untuk menganalisis data penyewaan sepeda harian berdasarkan berbagai faktor seperti musim, cuaca, suhu, dan lainnya.
        Dengan visualisasi interaktif, Anda dapat mengeksplorasi bagaimana berbagai faktor memengaruhi pola penggunaan sepeda.

        ### Tujuan Dashboard
        - Memberikan wawasan mendalam terkait pola penggunaan sepeda.
        - Menunjukkan pengaruh faktor cuaca, musim, dan hari kerja terhadap penyewaan sepeda.
        - Membantu memahami perilaku pengguna kasual dan terdaftar.
        """
    )

    # Highlight Data
    st.subheader("Informasi Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jumlah Baris", data.shape[0])
    with col2:
        st.metric("Jumlah Kolom", data.shape[1])
    with col3:
        st.metric("Total Penyewaan", f"{data['cnt'].sum():,}")

    st.divider()

    # Data Preview
    st.subheader("Data Preview")
    st.write(data.head())

    # Deskripsi Dataset
    st.subheader("Informasi Dataset")
    with st.expander("Klik untuk melihat deskripsi variabel"):
        st.markdown(
            """
            ### Deskripsi Variabel
            - **instant**: Index untuk data.
            - **dteday**: Tanggal pencatatan.
            - **season**: Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin).
            - **yr**: Tahun (0: 2011, 1: 2012).
            - **mnth**: Bulan (1 hingga 12).
            - **holiday**: Apakah hari tersebut hari libur.
            - **weekday**: Hari dalam seminggu.
            - **workingday**: Apakah hari tersebut adalah hari kerja.
            - **weathersit**: Kondisi cuaca (1: Cerah, 2: Berawan, 3: Hujan, 4: Hujan Lebat).
            - **temp**: Suhu normalisasi.
            - **atemp**: Suhu terasa.
            - **hum**: Kelembaban.
            - **windspeed**: Kecepatan angin.
            - **casual**: Pengguna kasual (non-member).
            - **registered**: Pengguna terdaftar (member).
            - **cnt**: Total penyewaan sepeda.
            """
        )

elif menu == "Visualisasi":
    st.title("Visualisasi Data 📊")
    
    # Penyewaan Sepeda berdasarkan Musim
    st.subheader("Penyewaan Sepeda berdasarkan Musim")
    fig1, ax1 = plt.subplots()
    sns.barplot(x='season', y='cnt', data=data, ax=ax1, palette='viridis')
    ax1.set_title("Penyewaan Sepeda per Musim")
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig1)

    st.markdown(
        """
        **Interpretasi:**
        - Penyewaan sepeda paling tinggi terjadi pada musim panas.
        - Musim panas memungkinkan pengguna lebih aktif bersepeda karena kondisi cuaca yang mendukung.
        """
    )

    st.divider()

    # Hubungan Suhu dan Penyewaan Sepeda
    st.subheader("Hubungan Suhu dan Penyewaan Sepeda")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', data=data, hue='season', ax=ax2, palette='viridis')
    ax2.set_title("Suhu vs Penyewaan Sepeda")
    ax2.set_xlabel("Suhu")
    ax2.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig2)

    st.markdown(
        """
        **Interpretasi:**
        - Terdapat korelasi positif antara suhu dan jumlah penyewaan sepeda.
        - Suhu yang lebih tinggi cenderung meningkatkan jumlah penyewaan sepeda.
        - Pengguna lebih nyaman bersepeda pada suhu yang hangat.
        """
    )

    st.divider()

    # Hari Kerja
    st.subheader("Penyewaan Sepeda pada Hari Kerja")
    fig3, ax3 = plt.subplots()
    sns.boxplot(x='workingday', y='cnt', data=data, ax=ax3, palette='Set2')
    ax3.set_title("Penyewaan Sepeda pada Hari Kerja vs Libur")
    ax3.set_xlabel("Hari Kerja (1 = Ya, 0 = Tidak)")
    ax3.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig3)

    st.markdown(
        """
        **Interpretasi:**
        - Penyewaan sepeda lebih banyak terjadi pada hari kerja dibandingkan hari libur.
        - Hal ini menunjukkan bahwa sepeda sering digunakan untuk aktivitas sehari-hari seperti pergi ke kantor atau sekolah.
        """
    )

# Footer
st.sidebar.info("Dashboard dibuat dengan Streamlit 📊")