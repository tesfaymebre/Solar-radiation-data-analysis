import pandas as pd
import numpy as np

def check_missing_values(data):
    """
    Check for missing values in the DataFrame and provide a detailed report as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with columns 'Column', 'Missing Count', 'Missing Percentage'
    """
    missing_count = data.isnull().sum()
    missing_percentage = (data.isnull().mean() * 100)
    
    # Create a DataFrame for the report
    report_df = pd.DataFrame({
        'Column': missing_count.index,
        'Missing Count': missing_count.values,
        'Missing Percentage': missing_percentage.values
    })
    
    return report_df

def check_data_types(data, expected_types):
    """
    Check if the columns in the DataFrame have the expected data types.
    Args:
        expected_types (dict): A dictionary with column names as keys and expected data types as values.
    Returns:
        pd.DataFrame: A DataFrame with columns 'Column', 'Actual Data Type', 'Expected Data Type', and 'Match'.
    """
    results = []
    for col, dtype in expected_types.items():
        actual_dtype =  data[col].dtype
        dtype= data[col].dtype
        match = pd.api.types.is_dtype_equal(actual_dtype, dtype)
        results.append({
            'Column': col,
            'Actual Data Type': actual_dtype,
            'Expected Data Type': dtype,
            'Match': match
        })
    return pd.DataFrame(results)


def check_duplicates(data):
    """
    Check for duplicate rows in the DataFrame and provide a summary.

    Returns:
        str: A message indicating whether duplicates are present or not.
    """
    has_duplicates =  data.duplicated().any()
    if has_duplicates:
        return "Duplicate rows found in the DataFrame."
    else:
        return "No duplicate rows found in the DataFrame."
    
def check_negative_values(data):
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    negative_values = data[numeric_cols].lt(0).sum()
    return negative_values

def detect_outliers_iqr(df, columns):
    outlier_summary = {}
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_summary[col] = len(outliers)
    return outlier_summary