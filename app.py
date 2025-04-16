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
    ]
)


if page == ":house: Overview":
    st.markdown("<h1 style='text-align: center;'>Overview</h1>", unsafe_allow_html=True)
    st.markdown("""
    Halaman ini memberikan gambaran umum tentang data time series yang tersedia.
    Anda dapat melihat tren nilai, moving average, dan metode forecasting lainnya.
    Gunakan navigasi di sidebar untuk melihat bagian yang berbeda dari dashboard.
    """)

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
    st.markdown("<h1 style='text-align: center;'>Time Series Plot</h1>", unsafe_allow_html=True)

    # Tombol untuk memilih kolom yang akan divisualisasikan
    columns_to_plot = st.multiselect("Kolom:", df.columns, default=['Jumlah'])

    if columns_to_plot:
        fig = px.line(df, y=columns_to_plot, title='Timeseries Plot',
                      labels={'date': 'Tanggal', 'value': 'Nilai'},
                      template="plotly_white")
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pilih setidaknya satu kolom untuk menampilkan grafik.")
    st.markdown("<h1 style='text-align: center;'>Barplot perkecamatan</h1>", unsafe_allow_html=True)
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
                                        labels={'district': 'Kecamatan', selected_year: f'Jumlah Tahun {selected_year}'},
                                        template="plotly_white",
                                        color_discrete_sequence=px.colors.sequential.Viridis) # Tambahkan parameter ini
                st.plotly_chart(fig_kecamatan, use_container_width=True)
            else:
                st.warning(f"Kolom tahun '{selected_year}' tidak ditemukan dalam data.")
        else:
            st.warning("Tidak ada data tahun yang tersedia untuk ditampilkan.")
    else:
        st.warning("Kolom 'district' tidak ditemukan dalam data untuk membuat bar plot kecamatan.")


    # Contoh tombol aksi


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Dibuat dengan Streamlit")