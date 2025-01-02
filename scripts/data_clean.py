import numpy as np
import pandas as pd

def clean_data(data, critical_columns):
    """
    Cleans and preprocesses the dataset.
    
    Steps:
    - Drop duplicates
    - Handle missing values
    - Treat outliers
    """
    print("Starting data cleaning...")
    
    # Step 1: Drop duplicates
    data = data.drop_duplicates()

    # Step 2: Handle missing critical data (e.g., unique identifiers)
    data = data.dropna(subset=critical_columns, how='any')

    # Step 3: Fill missing values for numeric columns with the column mean
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean(numeric_only=True))

    # Step 4: Fill missing non-critical categorical columns with a default value
    categorical_columns = data.select_dtypes(include=['object']).columns
    data[categorical_columns] = data[categorical_columns].fillna("unknown")

    print("Missing value handling completed.")
    
    # Step 5: Treat outliers
    for column in numeric_columns:
        data[column] = treat_outliers_with_mean(data[column])
    
    print("Outlier treatment completed.")
    print("Data cleaning finished.")
    return data

def treat_outliers_with_mean(column):
    """
    Detects and replaces outliers in a given column using the IQR method.

    Args:
        column: The column containing the data to be cleaned.

    Returns:
        The cleaned column with outliers replaced by the column mean.
    """
    Q1 = column.quantile(0.25)  # 25th percentile
    Q3 = column.quantile(0.75)  # 75th percentile
    IQR = Q3 - Q1  # Interquartile range

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Replace outliers with the mean
    column_mean = column.mean()
    return np.where((column < lower_bound) | (column > upper_bound), column_mean, column)

def replace_negative_values(df, columns):
        for col in columns:
            df[col] = df[col].apply(lambda x: max(x, 0))
        return df

def normalize_wind_direction(data, column='WD'):
    compass_labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    data['WD_compass'] = pd.cut(data[column], bins=np.linspace(0, 360, 9), labels=compass_labels, include_lowest=True)
    return data

def calculate_mean_wind_speed(data, group_by_column='WD_compass', target_column='WS'):
    wind_stats = data.groupby(group_by_column)[target_column].mean()
    return wind_stats

def calculate_z_scores(df, numeric_columns):
    """
    Calculate Z-scores for numeric columns in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The input dataframe.
    numeric_columns (list): List of numeric columns to calculate Z-scores for.
    
    Returns:
    pd.DataFrame: DataFrame containing Z-scores for the numeric columns.
    """
    z_scores = pd.DataFrame()
    for col in numeric_columns:
        z_scores[col] = (df[col] - df[col].mean()) / df[col].std()
    return z_scores

def flag_outliers(z_scores, threshold=3):
    """
    Flag outliers based on Z-scores.
    
    Parameters:
    z_scores (pd.DataFrame): DataFrame containing Z-scores.
    threshold (float): Z-score threshold to flag outliers.
    
    Returns:
    pd.DataFrame: DataFrame containing outliers.
    """
    outliers = z_scores[(z_scores.abs() > threshold).any(axis=1)]
    return outliers