import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
data = pd.read_csv('https://raw.githubusercontent.com/zyoohere/analisis-data-dicoding/refs/heads/main/day_df_clean.csv')

# Sidebar
st.sidebar.header('Filter Data')
selected_season = st.sidebar.multiselect('Pilih Musim', data['season'].unique(), default=data['season'].unique())
selected_month = st.sidebar.multiselect('Pilih Bulan', data['month'].unique(), default=data['month'].unique())
selected_year = st.sidebar.multiselect('Pilih Tahun', data['year'].unique(), default=data['year'].unique())
selected_weathersit = st.sidebar.multiselect('Pilih Kondisi Cuaca', data['weathersit'].unique(), default=data['weathersit'].unique())
temp_range = st.sidebar.slider('Rentang Suhu', float(data['temp'].min()), float(data['temp'].max()), (float(data['temp'].min()), float(data['temp'].max())))
humidity_range = st.sidebar.slider('Rentang Kelembapan', float(data['humidity'].min()), float(data['humidity'].max()), (float(data['humidity'].min()), float(data['humidity'].max())))
windspeed_range = st.sidebar.slider('Rentang Kecepatan Angin', float(data['windspeed'].min()), float(data['windspeed'].max()), (float(data['windspeed'].min()), float(data['windspeed'].max())))

# Filter data
filtered_data = data[(data['season'].isin(selected_season)) & (data['month'].isin(selected_month))]
filtered_data = data[(data['year'].isin(selected_year)) & 
                     (data['weathersit'].isin(selected_weathersit)) &
                     (data['temp'].between(*temp_range)) &
                     (data['humidity'].between(*humidity_range)) &
                     (data['windspeed'].between(*windspeed_range))]

#menampilkan kontak saya
st.sidebar.title("Contact Me")
st.sidebar.markdown("""
                    - 📧 **Email:** [triotahri99@gmail.com](mailto:triotahri99@gmail.com)
                    - 💼 **LinkedIn:** [Trio Tahril Rifandi](https://www.linkedin.com/in/triotahrill/)
                    - 🛠️ **Github:** [Zyoohere](https://github.com/zyoohere/analisis-data-dicoding)
                    """)

# Menambahkan teks penjelasan di sidebar
st.sidebar.markdown("For inquiries and collaborations, feel free to contact me!")

#Kata kata hari ini
st.sidebar.title(" 🌟 **Quotes of the Day**")
st.sidebar.markdown("""
> "Life is like riding a bicycle. To keep your balance, you must keep moving.” —Albert Einstein  
""")

#Dashboard
st.title('Dashboard Bike Sharing')
st.markdown('**Analisis Data Penyewaan Sepeda dengan Visualisasi.**')


col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Penyewaan', filtered_data['count'].sum())
with col2:
    st.metric('Pengguna Kasual', filtered_data['casual'].sum())
with col3:
    st.metric('Pengguna Terdaftar', filtered_data['registered'].sum())

col1, col2 = st.columns(2)
# Bar Chart - Distribusi pengguna
with col1:
            st.subheader('Distribusi Pengguna')
            user_data = filtered_data[['casual', 'registered']].sum().reset_index()
            user_data.columns = ['User Type', 'Count']
            plt.figure(figsize=(6, 4))
            sns.barplot(data=user_data, x='User Type', y='Count', palette='viridis')
            plt.title('Distribusi Pengguna')
            plt.ylabel('Jumlah Penyewaan')
            st.pyplot(plt)
    
# Area Chart - Pengguna Kasual vs. Terdaftar
with col2:
            st.subheader('Distribusi Pengguna Kasual vs. Terdaftar')
            user_trend = filtered_data[['casual', 'registered']].sum()
            st.area_chart(user_trend)

# Line Chart - Penyewaan sepeda setiap hari berdasarkan musim
st.subheader('Tren Penyewaan Sepeda Berdasarkan Musim')
plt.figure(figsize=(10, 5))
sns.lineplot(data=filtered_data, x='weekday', y='count', hue='season')
plt.title('Penyewaan Sepeda per Hari dalam Seminggu')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)


#Bar Chart - Penyewaan /bulan(month)
st.subheader('Penyewaan Sepeda per Bulan')
plt.figure(figsize=(10, 6))
monthly_data = filtered_data.groupby('month')['count'].sum().reset_index()
sns.barplot(data=monthly_data, x='month', y='count', palette='viridis')
plt.title('Total Penyewaan per Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.xlabel('Bulan')
st.pyplot(plt)

# Line Chart - Penyewaan /Tahun(year)
st.subheader('Tren Penyewaan Sepeda Berdasarkan Tahun')
plt.figure(figsize=(10, 6))
sns.lineplot(data=filtered_data, x='weekday', y='count', hue='year', marker='o', palette='coolwarm')
plt.title('Penyewaan per Hari dalam Seminggu Berdasarkan Tahun')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

# Scatter Plot - Hubungan Variabel
st.subheader('Hubungan Variabel dengan Total Penyewaan')
x_var = st.selectbox('Pilih Variabel X', ['temp', 'humidity', 'windspeed'], index=0)
y_var = st.selectbox('Pilih Variabel Y', ['count', 'casual', 'registered'], index=0)
plt.figure(figsize=(8, 6))
scatter = plt.scatter(filtered_data[x_var], filtered_data[y_var], c=filtered_data['temp'], cmap='coolwarm', alpha=0.7)
plt.colorbar(scatter, label='Suhu')
plt.title(f'{y_var.capitalize()} vs. {x_var.capitalize()}')
plt.xlabel(x_var.capitalize())
plt.ylabel(y_var.capitalize())
st.pyplot(plt)



# Count Plot - Penyewaan Berdasarkan Musim dan Cuaca
st.subheader('Distribusi Penyewaan Berdasarkan Musim dan Kondisi Cuaca')
plt.figure(figsize=(10, 6))
sns.countplot(data=filtered_data, x='season', hue='weathersit', palette='Set2')
plt.title('Distribusi Penyewaan')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

# Pie Chart - Hari kerja vs. libur
st.subheader('Proporsi Hari Kerja vs. Libur')
day_type_counts = filtered_data['workingday'].value_counts()
labels = ['Hari Kerja', 'Libur']
plt.figure(figsize=(5, 5))
plt.pie(day_type_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e'])
plt.title('Proporsi Hari Kerja vs. Libur')
st.pyplot(plt)

# Correlation heatmap
st.subheader('Korelasi Faktor Cuaca dengan Penyewaan')
plt.figure(figsize=(8, 6))
correlation = filtered_data[['temp', 'atemp', 'humidity', 'windspeed', 'count']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Heatmap Korelasi')
st.pyplot(plt)
