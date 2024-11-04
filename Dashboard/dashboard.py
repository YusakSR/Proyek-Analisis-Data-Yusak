# prompt: Buatlah Dashboard Sederhana Menggunakan Streamlit dari data all_df_full dan tampilkan semua visualisasi data yang kita punya serta mempunyai side bar yang menunjuukan tanggal penggunaan sepeda terbanyak

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy as sp
from scipy.stats import ttest_ind

# Load the dataset
all_df_full = pd.read_csv("all_data_full.csv")

# Convert 'dteday_daily' to datetime
all_df_full['dteday_daily'] = pd.to_datetime(all_df_full['dteday_daily'])

# Create season and weather mappings
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain', 4: 'Heavy Rain'}

# Sidebar
st.sidebar.header("Proyek Analisis Yusak SR")
selected_date = st.sidebar.date_input("Select a Date", min_value=all_df_full['dteday_daily'].min(), max_value=all_df_full['dteday_daily'].max(), value = all_df_full['dteday_daily'].mode()[0])
# Main Dashboard
st.title("Bike Sharing Dashboard")


# Display the selected date on the main page
st.write(f"Selected Date: {selected_date}")


# Display the top 10 rows of the dataframe.
st.subheader("Data Preview")
st.write(all_df_full.head(10))


# Visualization 1: Heatmap of Average Hourly Bike Usage by Season and Weather Condition
st.subheader("Average Hourly Bike Usage by Season and Weather Condition")

season_weather_usage = all_df_full.groupby(['season_daily', 'weathersit_daily'])['cnt_hourly'].mean().reset_index()
season_weather_usage.columns = ['Season', 'Weather Condition', 'Average Hourly Count']
season_weather_usage['Season'] = season_weather_usage['Season'].map(season_mapping)
season_weather_usage['Weather Condition'] = season_weather_usage['Weather Condition'].map(weather_mapping)
season_weather_pivot = season_weather_usage.pivot(index="Season", columns="Weather Condition", values="Average Hourly Count")


fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(season_weather_pivot, annot=True, cmap="YlGnBu", fmt=".1f", ax=ax, cbar_kws={'label': 'Average Hourly Bike Usage'})
ax.set_title('Heatmap of Average Hourly Bike Usage by Season and Weather Condition')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Season')
st.pyplot(fig)



# Visualization 2: Bike Usage by Season and Weather
st.subheader("Bike Usage Distribution by Season and Weather")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

season_weather_df = all_df_full[['season_daily', 'weathersit_daily', 'cnt_daily']].dropna()
sns.boxplot(x='season_daily', y='cnt_daily', data=season_weather_df, ax=axes[0])
axes[0].set_title('Bike Usage by Season')

sns.boxplot(x='weathersit_daily', y='cnt_daily', data=season_weather_df, ax=axes[1])
axes[1].set_title('Bike Usage by Weather Condition')
st.pyplot(fig)


# Visualization 3: Distribution of Bike Usage: Weekday vs Weekend
st.subheader("Distribution of Bike Usage: Weekday vs Weekend")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=all_df_full, x='workingday_hourly', y='cnt_hourly', ax=ax)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Weekend', 'Weekday'])
ax.set_title('Distribution of Bike Usage: Weekday vs Weekend')
st.pyplot(fig)


#Visualization 4: Hourly Bike Usage Pattern: Weekday vs Weekend

st.subheader("Hourly Bike Usage Pattern: Weekday vs Weekend")

fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(x='hr', y='cnt_hourly', hue='workingday_hourly', data=all_df_full, ax = ax)
ax.set_title('Hourly Bike Usage Pattern: Weekday vs Weekend')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Bike Usage')
st.pyplot(fig)

#Visualization 5: Trend of Daily Bike Usage
st.subheader("Trend of Daily Bike Usage")

fig, ax = plt.subplots(figsize=(10, 6))

all_df_full.groupby('dteday_daily')['cnt_daily'].mean().plot(ax=ax)
ax.set_title('Trend of Daily Bike Usage')
plt.xlabel('Date')
plt.ylabel('Average Bike Usage')
st.pyplot(fig)

# Visualization 6: Average Bike Usage by Season and Weather (Barplot)
st.subheader("Average Bike Usage by Season and Weather (Barplot)")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=season_weather_usage, x='Season', y='Average Hourly Count', hue='Weather Condition', ax=ax)
st.pyplot(fig)

#Pisahkan data ke dalam hari kerja dan akhir pekan

workingday_usage = all_df_full[all_df_full['workingday_hourly'] == 1]['cnt_hourly']
weekend_usage = all_df_full[all_df_full['workingday_hourly'] == 0]['cnt_hourly']

#Melakukan uji independen t-test
t_stat, p_val = ttest_ind(workingday_usage.dropna(), weekend_usage.dropna(), equal_var=False)

#Menampilkan Hasil Tes
st.text("Hasil Uji Test independen t-test")
t_stat, p_val

st.caption('Copyright © Yusak Stainly Ritonga 2024')