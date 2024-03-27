import streamlit as st
import pandas as pd

# import matplotlib.pyplot as plt
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data
import logging
import os
import glob

logging.basicConfig(level=logging.INFO)


LAG_N_DAYS: int = 7

# * INIT REPO FOR DATA
os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

# * remove outdated json files
for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

# plt.switch_backend("TkAgg")

# Title for your app
st.title("Data Visualization App")


# Load data from CSV
@st.cache_data(
    ttl=15 * 60
)  # This decorator caches the data to prevent reloading on every interaction.
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(
        fic_export_data, parse_dates=[col_date]
    )  # Adjust 'DateColumn' to your date column name*
    return data


# Assuming your CSV is named 'data.csv' and is in the same directory as your app.py
df = load_data(LAG_N_DAYS)

# Creating a line chart
st.subheader("Line Chart of Numerical Data Over Time")

# Select the numerical column to plot
# This lets the user select a column if there are multiple numerical columns available
# numerical_column = st.selectbox('Select the column to visualize:', df.select_dtypes(include=['float', 'int']).columns)
numerical_column = col_donnees

# ! Matplotlib - Create the plot
# fig, ax = plt.subplots()
# ax.plot(df[col_date], df[numerical_column])  # Adjust 'DateColumn' to your date column name
# ax.set_xlabel('Time')
# ax.set_ylabel(numerical_column)
# ax.set_title(f'Time Series Plot of {numerical_column}')
# # Display the plot
# st.pyplot(fig)

# ! Plotly
# Create interactive line chart using Plotly
fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)












import streamlit as st
import pandas as pd
import plotly.express as px

# Suppose col_date is your date column and col_donnees is your consumption data column.
# Ensure they are named appropriately as they appear in your CSV.

# Function to load data
@st.cache  # This decorator caches the data to prevent reloading on every interaction.
def load_data():
    data = pd.read_csv('your_data.csv', parse_dates=[col_date])
    return data

# Load data
df = load_data()

# Process data to find the mean consumption per day of the week
# First ensure the date column is in datetime format
df[col_date] = pd.to_datetime(df[col_date])

# Then extract the day of the week from the date column
df['day_of_week'] = df[col_date].dt.day_name()

# Now group by day of the week and calculate the mean consumption
df_mean = df.groupby('day_of_week')[col_donnees].mean().reset_index()

# Sort the days in the order you want them to appear on the plot
sorter = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_mean['day_of_week'] = pd.Categorical(df_mean['day_of_week'], categories=sorter, ordered=True)
df_mean = df_mean.sort_values('day_of_week')

# Create the plot using Plotly Express
fig = px.bar(df_mean, x='day_of_week', y=col_donnees, title='Average Consumption by Day of the Week')

# Show the plot in Streamlit
st.plotly_chart(fig)
