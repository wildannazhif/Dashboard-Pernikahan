# Install required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page configuration for a wider layout and title
st.set_page_config(layout="wide", page_title="Dashboard Analisis Data Time Series")

# Load the data into a Pandas DataFrame
try:
    df = pd.read_csv('Time - Copy.csv')
    df2 = pd.read_csv('Kecamatan.csv')
except FileNotFoundError:
    st.error("File 'Time - Copy.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan aplikasi.")
    st.stop()

# Ensure the 'date' column exists before proceeding
if 'date' not in df.columns:
    st.error("Kolom 'date' tidak ditemukan dalam file CSV.")
    st.stop()

# Convert 'date' column to datetime and set as index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Ensure the 'Jumlah' column exists before proceeding
if 'Jumlah' not in df.columns:
    st.error("Kolom 'Jumlah' tidak ditemukan dalam file CSV.")
    st.stop()

# Ubah nilai 0 di kolom 'Jumlah' menjadi NaN
df['Jumlah'] = df['Jumlah'].replace(0, np.nan)

# Sidebar for navigation
page = st.sidebar.radio(
    "Pilih Halaman",
    [
        ":house: Overview",
        ":bar_chart: Data",
        ":clipboard: Statistika Deskriptif",
        ":chart_with_upwards_trend: Visualisasi",
        ":writing_hand: Author",
    ]
)


if page == ":house: Overview":
    st.markdown("<h1 style='text-align: center;'>Dashboard Trend Pernikahan di Kabupaten Bekasi</h1>", unsafe_allow_html=True)
    st.markdown("""
Dashboard ini dibuat sebagai bagian dari laporan kerja praktik kami. Data yang dianalisis meliputi jumlah pernikahan per bulan di Kabupaten Bekasi selama periode 2020-2024, serta data pernikahan per kecamatan di Kabupaten Bekasi pada periode yang sama""")

elif page == ":bar_chart: Data":
    st.header("Data")
    st.subheader("Tabel Data")
    st.dataframe(df)

elif page == ":clipboard: Statistika Deskriptif":
    st.markdown("<h1 style='text-align: center;'>Statistika Deskriptif</h1>", unsafe_allow_html=True)

    # Ensure 'Jumlah' column exists before calculating statistics
    if 'Jumlah' in df.columns:
        # Calculate summary statistics for 'Jumlah' column
        jumlah_sum = df['Jumlah'].sum()
        jumlah_min = df['Jumlah'].min()
        jumlah_max = df['Jumlah'].max()
        jumlah_mean = df['Jumlah'].mean()
        jumlah_median = df['Jumlah'].median()
        jumlah_std = df['Jumlah'].std()
        jumlah_var = df['Jumlah'].var()
        jumlah_quantile_25 = df['Jumlah'].quantile(0.25)
        jumlah_quantile_75 = df['Jumlah'].quantile(0.75)

        # Display statistics in columns/boxes
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", f"{jumlah_sum:.2f}")
        with col2:
            st.metric("Minimum", f"{jumlah_min:.2f}")
        with col3:
            st.metric("Maksimum", f"{jumlah_max:.2f}")
        with col4:
            st.metric("Rata-rata", f"{jumlah_mean:.2f}") # Format to 2 decimal places

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("Median", f"{jumlah_median:.2f}")
        with col6:
            st.metric("Standar Deviasi", f"{jumlah_std:.2f}")
        with col7:
            st.metric("Varians", f"{jumlah_var:.2f}")
        with col8:
            st.metric("Rentang Interkuartil", f"{jumlah_quantile_75 - jumlah_quantile_25:.2f}")

        col9, col10 = st.columns(2)
        with col9:
            st.metric("Kuartil 25%", f"{jumlah_quantile_25:.2f}")
        with col10:
            st.metric("Kuartil 75%", f"{jumlah_quantile_75:.2f}")

    else:
        st.warning("Kolom 'Jumlah' tidak ditemukan untuk menampilkan statistik.")

elif page == ":chart_with_upwards_trend: Visualisasi":
    st.markdown("<h2 style='text-align: center;'>Peramalan Jumlah Pernikahan Perbulan Menggunakan Metode Time Series</h2>", unsafe_allow_html=True)

    # Tombol untuk memilih kolom yang akan divisualisasikan
    columns_to_plot = st.multiselect("Kolom:", df.columns, default=['Jumlah'])

    if columns_to_plot:
        fig = px.line(df, y=columns_to_plot, title='Time Series Plot',
                      labels={'date': 'Tanggal', 'value': 'Jumlah Pernikahan'},
                      template="plotly_white")
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pilih setidaknya satu kolom untuk menampilkan grafik.")
    
    # Tambahkan barplot tahunan
    st.markdown("<h2 style='text-align: center;'>Jumlah Pernikahan Kabupaten Bekasi Pertahun dari 2020-2024</h2>", unsafe_allow_html=True)
    
    # Asumsikan df memiliki datetime index atau kolom tanggal
    if 'date' in df.columns:
        # Jika ada kolom date, gunakan itu
        df_yearly = df.copy()
        df_yearly['year'] = pd.DatetimeIndex(df_yearly['date']).year
    else:
        # Jika tidak ada kolom date, asumsikan menggunakan index datetime
        df_yearly = df.copy()
        df_yearly['year'] = df_yearly.index.year
    
    # Hitung jumlah per tahun
    yearly_counts = df_yearly.groupby('year')['Jumlah'].sum().reset_index()
    
    # Buat barplot tahunan
    fig_yearly = px.bar(yearly_counts, x='year', y='Jumlah',
                        title='Jumlah Pernikahan per Tahun',
                        labels={'year': 'Tahun', 'Jumlah': 'Jumlah Pernikahan'},
                        template="plotly_white",
                        color_discrete_sequence=px.colors.sequential.Plasma)
    
    fig_yearly.update_layout(xaxis=dict(tickmode='linear'))
    st.plotly_chart(fig_yearly, use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>Jumlah Pernikahan Kabupaten Bekasi Perkecamatan</h2>", unsafe_allow_html=True)
    # Pastikan df2 sudah terdefinisi dan memiliki kolom yang sesuai
    if 'district' in df2.columns:
        # Ambil daftar tahun yang tersedia dari kolom df2 (selain 'district')
        available_years = [col for col in df2.columns if col != 'district']
        if available_years:
            # Tambahkan selectbox untuk memilih tahun
            selected_year = st.selectbox("Pilih Tahun:", available_years, index=len(available_years) - 1) # Default ke tahun terakhir

            if selected_year in df2.columns:
                fig_kecamatan = px.bar(df2, x='district', y=selected_year,
                                        title=f'Jumlah Data per Kecamatan ({selected_year})',
                                        labels={'district': 'Kecamatan', selected_year: f'Jumlah Pernikahan Tahun {selected_year}'},
                                        template="plotly_white",
                                        color_discrete_sequence=px.colors.sequential.Viridis)
                st.plotly_chart(fig_kecamatan, use_container_width=True)
            else:
                st.warning(f"Kolom tahun '{selected_year}' tidak ditemukan dalam data.")
        else:
            st.warning("Tidak ada data tahun yang tersedia untuk ditampilkan.")
    else:
        st.warning("Kolom 'district' tidak ditemukan dalam data untuk membuat bar plot kecamatan.")    # Contoh tombol aksi
elif page == ":writing_hand: Author":
    nama_file_foto1 = 'foto1.JPG'
    nama_file_foto2 = 'foto2.jpg'

    st.markdown("<h2 style='text-align: center;'>Author</h2>", unsafe_allow_html=True)

    # Buat dua kolom dengan lebar yang sama
    kolom1, kolom2 = st.columns(2)

    # Tampilkan gambar pertama di kolom pertama
    with kolom1:
        try:
            st.image(nama_file_foto1, caption='Wildan Nazhif Irsyadi (5003221109)')
        except Exception as e:
            st.error(f"Gagal memuat {nama_file_foto1}: {e}")
            st.info("Pastikan file gambar ada di lokasi yang benar.")
        # Tampilkan gambar kedua di kolom kedua
    with kolom2:
        try:
            st.image(nama_file_foto2, caption='Ahmad Alrifai (5003221108)')
        except Exception as e:
            st.error(f"Gagal memuat {nama_file_foto2}: {e}")
            st.info("Pastikan file gambar ada di lokasi yang benar.")


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Departemen Statistika ITS")