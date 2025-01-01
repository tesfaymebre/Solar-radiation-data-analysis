import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
from datetime import datetime

# Page Config
st.set_page_config(page_title="Solar Radiation Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data_from_url():
    url = "https://drive.google.com/uc?id=1CkTd-KB1iMGE5KNENLZ3H8267rt9Pyid"
    data = pd.read_csv(url)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    return data

def load_data_from_file(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    return data

st.sidebar.header("Data Source")
data_source = st.sidebar.radio("Select Data Source", ("Sample Data", "Upload Data"))

if data_source == "Sample Data":
    data = load_data_from_url()
else:
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        data = load_data_from_file(uploaded_file)
    else:
        st.warning("Please upload a CSV file to proceed.")
        st.stop()

# Sidebar Options
st.sidebar.header("Filters")
show_data = st.sidebar.checkbox("Show Raw Data", value=False)

# Time Range Filter
start_date = st.sidebar.date_input("Start Date", value=data["Timestamp"].min().date())
end_date = st.sidebar.date_input("End Date", value=data["Timestamp"].max().date())
filtered_data = data[(data["Timestamp"] >= pd.Timestamp(start_date)) & (data["Timestamp"] <= pd.Timestamp(end_date))]

variables = st.sidebar.multiselect(
    "Select Variables for Analysis", 
    filtered_data.columns[1:], 
    default=["GHI", "DNI", "DHI", "Tamb"]
)

# Main Title
st.title("Enhanced Solar Radiation Dashboard")

# Display Raw Data
if show_data:
    st.subheader("Filtered Dataset Preview")
    st.dataframe(filtered_data.head())

# Line Plots
st.subheader("Time Series Analysis")
for var in variables:
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(x="Timestamp", y=var, data=filtered_data, ax=ax)
    ax.set_title(f"{var} Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel(var)
    st.pyplot(fig)

# Correlation Heatmap
st.subheader("Correlation Heatmap")
if len(variables) > 1:
    corr = filtered_data[variables].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.warning("Select at least two variables to display the correlation heatmap.")

# Wind Rose Visualization
st.subheader("Wind Rose")
fig = plt.figure(figsize=(8, 6))
ax = WindroseAxes.from_ax(fig=fig)
ax.bar(data["WD"], data["WS"], normed=True, opening=0.8, edgecolor="white", bins=np.arange(0, max(data['WS']) + 2, 2))
ax.set_legend(title='Wind Speed (m/s)', loc='upper left', bbox_to_anchor=(1, 1))
st.pyplot(fig)

# Z-Score Analysis
st.subheader("Z-Score Analysis")
numeric_columns = filtered_data.select_dtypes(include=["float", "int"]).columns
z_scores = (filtered_data[numeric_columns] - filtered_data[numeric_columns].mean()) / filtered_data[numeric_columns].std()
outliers = z_scores[(z_scores.abs() > 3).any(axis=1)]

st.write(f"Number of outliers detected: {len(outliers)}")
if not outliers.empty:
    st.dataframe(outliers)

# Bubble Chart
st.subheader("Bubble Chart")
x_var = st.selectbox("Select X-axis Variable", variables)
y_var = st.selectbox("Select Y-axis Variable", variables)
size_var = st.selectbox("Select Bubble Size Variable", variables)

if x_var and y_var and size_var:
    bubble_size = filtered_data[size_var] / filtered_data[size_var].max() * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        filtered_data[x_var], filtered_data[y_var], s=bubble_size, alpha=0.6, c=bubble_size, cmap="viridis", edgecolors="w"
    )
    plt.colorbar(scatter, ax=ax, label=size_var)
    ax.set_title(f"Bubble Chart: {x_var} vs {y_var} with {size_var} as Bubble Size")
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    st.pyplot(fig)
else:
    st.warning("Select variables for the bubble chart.")
