import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title for your app
st.title('Data Visualization App')

# Load data from CSV
@st.cache  # This decorator caches the data to prevent reloading on every interaction.
def load_data(file_path):
    data = pd.read_csv(file_path, parse_dates=['DateColumn'], dayfirst=True)  # Adjust 'DateColumn' to your date column name
    return data

# Assuming your CSV is named 'data.csv' and is in the same directory as your app.py
df = load_data('data/interim/data.csv')

# Creating a line chart
st.subheader('Line Chart of Numerical Data Over Time')

# Select the numerical column to plot
# This lets the user select a column if there are multiple numerical columns available
numerical_column = st.selectbox('Select the column to visualize:', df.select_dtypes(include=['float', 'int']).columns)

# Create the plot
fig, ax = plt.subplots()
ax.plot(df['DateColumn'], df[numerical_column])  # Adjust 'DateColumn' to your date column name
ax.set_xlabel('Time')
ax.set_ylabel(numerical_column)
ax.set_title(f'Time Series Plot of {numerical_column}')

# Display the plot
st.pyplot(fig)
