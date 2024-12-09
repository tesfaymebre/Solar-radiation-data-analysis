# Solar Radiation Data Analysis

This repository contains notebooks and scripts for analyzing solar radiation data. The goal is to understand patterns, trends, and anomalies in solar radiation measurements.

## Project Structure

- `data/`: Contains raw and processed data files.
- `notebooks/`: Jupyter notebooks for data analysis and visualization.
- `scripts/`: Python scripts for data processing and analysis.
- `results/`: Output files and visualizations generated from the analysis.

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/tesfaymebre/Solar-radiation-data-analysis.git
   ```
2. Navigate to the project directory:
   ```sh
   cd solar-radiation-data-analysis
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. Start Jupyter Notebook:
   ```sh
   jupyter notebook
   ```
2. Open and run the notebooks in the `notebooks/` directory to perform the analysis.

## Dataset Overview

### Solar Radiation Measurement Data

The data for this project is extracted and aggregated from Solar Radiation Measurement Data. Each row in the data contains values for solar radiation, air temperature, relative humidity, barometric pressure, precipitation, wind speed, and wind direction, cleaned and soiled radiance sensor (soiling measurement), and cleaning events.

#### Data Structure

- `Timestamp (yyyy-mm-dd hh:mm)`: Date and time of each observation.
- `GHI (W/m²)`: Global Horizontal Irradiance, the total solar radiation received per square meter on a horizontal surface.
- `DNI (W/m²)`: Direct Normal Irradiance, the amount of solar radiation received per square meter on a surface perpendicular to the rays of the sun.
- `DHI (W/m²)`: Diffuse Horizontal Irradiance, solar radiation received per square meter on a horizontal surface that does not arrive on a direct path from the sun.
- `ModA (W/m²)`: Measurements from a module or sensor (A), similar to irradiance.
- `ModB (W/m²)`: Measurements from a module or sensor (B), similar to irradiance.
- `Tamb (°C)`: Ambient Temperature in degrees Celsius.
- `RH (%)`: Relative Humidity as a percentage of moisture in the air.
- `WS (m/s)`: Wind Speed in meters per second.
- `WSgust (m/s)`: Maximum Wind Gust Speed in meters per second.
- `WSstdev (m/s)`: Standard Deviation of Wind Speed, indicating variability.
- `WD (°N (to east))`: Wind Direction in degrees from north.
- `WDstdev`: Standard Deviation of Wind Direction, showing directional variability.
- `BP (hPa)`: Barometric Pressure in hectopascals.
- `Cleaning (1 or 0)`: Signifying whether cleaning (possibly of the modules or sensors) occurred.
- `Precipitation (mm/min)`: Precipitation rate measured in millimeters per minute.
- `TModA (°C)`: Temperature of Module A in degrees Celsius.
- `TModB (°C)`: Temperature of Module B in degrees Celsius.
- `Comments`: This column is designed for any additional notes.

## Exploratory Data Analysis (EDA)

### Summary Statistics

Calculate the mean, median, standard deviation, and other statistical measures for each numeric column to understand data distribution.

### Data Quality Check

Look for missing values, outliers, or incorrect entries (e.g., negative values where only positive should exist), especially in columns like GHI, DNI, and DHI. Check for outliers, especially in sensor readings (ModA, ModB) and wind speed data (WS, WSgust).

### Time Series Analysis

Plot bar charts or line charts of GHI, DNI, DHI, and Tamb over time to observe patterns by month, trends throughout the day, or anomalies, such as peaks in solar irradiance or temperature fluctuations. Evaluate the impact of cleaning (using the 'Cleaning' column) on the sensor readings (ModA, ModB) over time.

### Correlation Analysis

Use correlation matrices or pair plots to visualize the correlations between solar radiation components (GHI, DNI, DHI) and temperature measures (TModA, TModB). Investigate the relationship between wind conditions (WS, WSgust, WD) and solar irradiance using scatter matrices.

### Wind Analysis

Use radial bar plots or wind roses to identify trends and significant wind events by showing the distribution of wind speed and direction, along with how variable the wind direction tends to be.

### Temperature Analysis

Examine how relative humidity (RH) might influence temperature readings and solar radiation.

### Histograms

Create histograms for variables like GHI, DNI, DHI, WS, and temperatures to visualize the frequency distribution of these variables.

### Z-Score Analysis

Calculate Z-scores to flag data points that are significantly different from the mean.

### Bubble Charts

Explore complex relationships between variables, such as GHI vs. Tamb vs. WS, with bubble size representing an additional variable like RH or BP (Barometric Pressure).

### Data Cleaning

Based on the initial analysis, clean the dataset by handling anomalies and missing values, especially in columns like Comments which appear entirely null.
