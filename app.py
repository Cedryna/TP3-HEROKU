import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import os
import glob

# Custom imports
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data, calculate_daily_average

logging.basicConfig(level=logging.INFO)

LAG_N_DAYS: int = 7

os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

st.title("Data Visualization App")

@st.cache(ttl=15 * 60)
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    daily_avg = main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data, daily_avg

df, daily_avg = load_data(LAG_N_DAYS)

# Assigning colors to each day of the week
colors = px.colors.qualitative.Set3

# Ordering days of the week from Monday to Friday
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

st.subheader("Line Chart of Numerical Data Over Time")
numerical_column = col_donnees
fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)

st.subheader("Average Consumption per Day of the Week")

# Sorting data by day of the week and reindexing
daily_avg = daily_avg.set_index('day_of_week').reindex(days_order).reset_index()

# Create a bar chart for daily average consumption with custom colors
fig_bar = px.bar(daily_avg, x='day_of_week', y=col_donnees, title='Moyenne de la consommation par jour de la semaine',
                 color='day_of_week', color_discrete_sequence=colors)
st.plotly_chart(fig_bar)
