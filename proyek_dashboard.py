import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Membaca data
DATA_PATH = "day.csv"
data = pd.read_csv(DATA_PATH)

# Konfigurasi Streamlit
st.set_page_config(page_title="Dashboard Bike Sharing", page_icon="🚴", layout="wide")

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
        - Menunjukkan pengaruh faktor seperti musim, hari kerja, dan hari libur terhadap penyewaan sepeda.
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
    st.write(data.drop(columns=["instant"]).head())

    # Deskripsi Dataset
    st.subheader("Informasi Dataset")
    with st.expander("Klik untuk melihat deskripsi variabel"):
        st.markdown(
            """
            ### Deskripsi Variabel
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

    # Filter Tahun
    year_filter = st.sidebar.selectbox("Pilih Tahun", options=["2011", "2012", "Gabungan 2011-2012"], index=2)

    # Filter Data Berdasarkan Tahun
    if year_filter == "2011":
        filtered_data = data[data["yr"] == 0]
    elif year_filter == "2012":
        filtered_data = data[data["yr"] == 1]
    else:
        filtered_data = data

    # Penyewaan Sepeda Berdasarkan Musim
    st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Musim")
    seasonal_data = filtered_data.groupby("season")["cnt"].sum()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=seasonal_data.index, y=seasonal_data.values, palette="viridis", ax=ax1)
    ax1.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim")
    ax1.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig1)

    st.markdown(f"**Jumlah Penyewaan per Musim (Tahun: {year_filter}):**")
    for season, jumlah in zip(["Spring", "Summer", "Fall", "Winter"], seasonal_data.values):
        st.markdown(f"- {season}: {jumlah:,}")

    st.divider()

    # Trend Analysis
    st.subheader("Trend Penyewaan Sepeda Harian")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    daily_counts = filtered_data.groupby("dteday")["cnt"].sum()
    daily_counts.plot(kind="line", ax=ax2)
    ax2.set_title(f"Trend Penyewaan Sepeda Harian ({year_filter})")
    ax2.set_xlabel("Tanggal")
    ax2.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig2)

    st.divider()

    # Filter Bulan
    month_filter = st.sidebar.slider("Pilih Bulan", min_value=1, max_value=12, value=1)

    # Filter Data Berdasarkan Bulan
    month_data = filtered_data[filtered_data["mnth"] == month_filter]

    # Penyewaan Sepeda Berdasarkan Hari Kerja
    st.subheader(f"Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja (Bulan: {month_filter})")
    workingday_data = month_data.groupby("workingday")["cnt"].sum()
    fig3, ax3 = plt.subplots()
    sns.barplot(x=workingday_data.index, y=workingday_data.values, palette="muted", ax=ax3)
    ax3.set_title("Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja")
    ax3.set_xticklabels(["Hari Libur", "Hari Kerja"])
    ax3.set_xlabel("Hari Kerja")
    ax3.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig3)

    st.markdown(f"**Jumlah Penyewaan Berdasarkan Hari Kerja (Bulan: {month_filter}):**")
    for label, jumlah in zip(["Hari Libur", "Hari Kerja"], workingday_data.values):
        st.markdown(f"- {label}: {jumlah:,}")
