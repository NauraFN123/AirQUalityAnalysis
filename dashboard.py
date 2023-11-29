import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#MENYIAPKAN DATAFRAME----------


def create_year_highest_Polutant_df(df):
    year_highest_Polutant_df = df.groupby(by=["year"]).agg({
        "PM10":"mean",
        "PM2.5":"mean",
        "NO2":"mean"
    }).sort_values(by="year", ascending=True).reset_index()

    return year_highest_Polutant_df

def create_air_in2016_df(df):
    air_in2016_df = df[df["year"] == 2016]
    
    return air_in2016_df


def create_highest_2016pm10_df(df):
    highest_2016pm10_df = df.groupby(by=["station","year"]).PM10.mean().sort_values(ascending=False).reset_index()
    
    return highest_2016pm10_df

def create_highest_2016pm25_df(df):
    highest_2016pm25_df = df.groupby(by=["station","year"])["PM2.5"].mean().sort_values(ascending=False).reset_index()

    return highest_2016pm25_df

def create_highest_2016NO2_df(df):
    highest_2016NO2_df = df.groupby(by=["station","year"]).NO2.mean().sort_values(ascending=False).reset_index()

    return highest_2016NO2_df

def create_polutantmonth2016_df(df):
    polutantmonth2016_df = df.resample(rule='M', on='date').agg({
        "PM10":"mean",
        "PM2.5":"mean",
        "NO2":"mean"
    })
    polutantmonth2016_df.index = polutantmonth2016_df.index.strftime('%Y/%m') #mengubah format date menjadi nama bulan
    
    polutantmonth2016_df = polutantmonth2016_df.reset_index()

    return polutantmonth2016_df

all_city_df = pd.read_csv("all_data.csv")
datetime_columns = ["date"]
all_city_df.sort_values(by=["year", "date"], inplace=True)
all_city_df.reset_index(inplace=True)

for column in datetime_columns:
    all_city_df[column] = pd.to_datetime(all_city_df[column])

min_date = all_city_df["date"].min()
max_date = all_city_df["date"].max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    year_columns= ["year"]

    year_select = all_city_df["year"].unique()
    year_input = st.selectbox(
        'Tahun',
        (year_select),
        index=None,
        placeholder="Pilih tahun"
    )
    st.write('You selected:', year_input)

main_df=all_city_df[(all_city_df["year"]==year_input)
                    ]
main_df2 = all_city_df[(all_city_df["date"]>= str(start_date)) & 
                (all_city_df["date"] <= str(end_date))]
year_highest_Polutant_df=create_year_highest_Polutant_df(main_df)
air_in2016_df=create_air_in2016_df(main_df)
highest_2016pm10_df=create_highest_2016pm10_df(main_df)
highest_2016pm25_df=create_highest_2016pm25_df(main_df)
highest_2016NO2_df=create_highest_2016NO2_df(main_df)
polutantmonth2016_df=create_polutantmonth2016_df(main_df2)
#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Air Quality Dashboard')


polutant_PM10_per_year = year_highest_Polutant_df.PM10.mean()
st.metric("Rata-rata Polutan PM10 Per Tahun "+str(year_input)+": ", value=polutant_PM10_per_year)
st.subheader('Tingkat Polutan per Tahun')
#menampilkan grafik PM10, PM2.5, dan NO2 per tahun

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 7))
 
sns.barplot(y="PM10", x="year", data=year_highest_Polutant_df.sort_values(by="PM10", ascending=False), color="#72BCD4", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("PM10", loc="center", fontsize=18)
ax[0].tick_params(axis ='both', labelsize=12)
 
sns.barplot(y="PM2.5", x="year", data=year_highest_Polutant_df.sort_values(by="PM2.5", ascending=False), color="#72BCD4", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("PM2.5", loc="center", fontsize=18)
ax[1].tick_params(axis='both', labelsize=12)
 
sns.barplot(y="NO2", x="year", data=year_highest_Polutant_df.sort_values(by="NO2", ascending=False), color="#72BCD4", ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("NO2", loc="center", fontsize=18)
ax[2].tick_params(axis='both', labelsize=12)
 
plt.suptitle("Tingkat rata-rata polutan per tahun ", fontsize=20)
plt.show()

st.pyplot(fig)

#menampilkan grafik PM10, PM2.5, dan NO2 pada tahun 2016
min([], default="EMPTY")
st.subheader("Tingkat rata-rata polutan per Daerah")
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(20, 20))
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(y="PM10", x="station", data=highest_2016pm10_df.sort_values(by="PM10", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("PM10", loc="center", fontsize=18)
ax[0].tick_params(axis ='both', labelsize=12)
 
sns.barplot(y="PM2.5", x="station", data=highest_2016pm25_df.sort_values(by="PM2.5", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("station")
ax[1].set_title("PM2.5", loc="center", fontsize=18)
ax[1].tick_params(axis='both', labelsize=12)
 
sns.barplot(y="NO2", x="station", data=highest_2016NO2_df.sort_values(by="NO2", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("NO2", loc="center", fontsize=18)
ax[2].tick_params(axis='both', labelsize=12)
plt.show()
st.pyplot(fig)

st.subheader("Tingkat rata-rata polutan per periode "+str(min_date)+" s/d "+ str(max_date))

col1, col2, col3 = st.columns(3)
with col1:
    polutantPM10_months = round(polutantmonth2016_df.PM10.mean(), 4)
    st.metric("Rata-rata Polutan PM10", value=polutantPM10_months)

with col2:
    polutantPM25_months = round(polutantmonth2016_df["PM2.5"].mean(), 4)
    st.metric("Rata-rata Polutan PM2.5", value=polutantPM25_months)

with col3:
    polutantNO2_months = round(polutantmonth2016_df.NO2.mean(), 4)
    st.metric("Rata-rata Polutan NO2", value=polutantNO2_months)



st.subheader("Tingkat rata-rata polutan per Bulan")

fig, ax= plt.subplots(figsize=(20, 6)) 
plt.plot(polutantmonth2016_df["date"], polutantmonth2016_df["PM10"], marker='o', linewidth=2, color="#72BCD4",label="PM10")
plt.plot(polutantmonth2016_df["date"], polutantmonth2016_df["PM2.5"], marker='o', linewidth=2, color="red", label="PM2.5")
plt.plot(polutantmonth2016_df["date"], polutantmonth2016_df["NO2"], marker='o', linewidth=2, color="orange", label="NO2")
#plt.locator_params(integer=True)
plt.title("Rata-rata tingkat polutan tahun 2016 (per bulan)", loc="center", fontsize=20) 
plt.xticks(fontsize=15, rotation=90) 
plt.yticks(fontsize=15) 
plt.legend()
plt.show()
st.pyplot(fig)

