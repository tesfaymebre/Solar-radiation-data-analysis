import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from windrose import WindroseAxes

def univariate_plot(df, column, title, xlabel, ylabel, color):
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column], kde=True, bins=30, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def bivariate_plot(data, pairs, titles, xlabel,ylabel, n_cols=2):
    n_rows = (len(pairs) + n_cols - 1) // n_cols  # Calculate number of rows needed
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 8, n_rows * 6))  # Adjust figure size
    axes = axes.flatten()
    
    for i, (x_var, y_var) in enumerate(pairs):
        sns.scatterplot(x=x_var, y=y_var, data=data, alpha=0.6, ax=axes[i])
        axes[i].set_title(f'{titles[i]} - {x_var} vs {y_var}')
        axes[i].set_xlabel(xlabel[i])
        axes[i].set_ylabel(y_var[i])
        axes[i].grid()
    
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.show()

def bivariate_plot2(df, columns, title):
    sns.pairplot(df[columns], diag_kind='kde')
    plt.suptitle(title, y=1.02)
    plt.show()

def time_series_line_plot(df, columns, time_column, title, xlabel, ylabel):
    # Aggregate data by time_column and calculate the mean of each column
    df = df.groupby(time_column)[columns].mean().reset_index()
    
    # Convert month numbers to month names if time_column is "Month"
    if time_column == "Month":
        df[time_column] = df[time_column].apply(lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1])

    plt.figure(figsize=(15, 8))
    
    for column in columns:
        sns.lineplot(x=time_column, y=column, data=df, label=column)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.show()

def time_series_bar_plot(df, columns, time_column, title, xlabel, ylabel, colors=None):
    # Aggregate data by time_column and calculate the mean of each column
    df = df.groupby(time_column)[columns].mean().reset_index()
    
    # Convert month numbers to month names if time_column is "Month"
    if time_column == "Month":
        df[time_column] = df[time_column].apply(lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1])
    
    plt.figure(figsize=(14, 7))
    
    if colors is None:
        colors = plt.cm.tab10(np.linspace(0, 1, len(columns)))

    bar_width = 0.2  # Width of each bar
    time_values = np.arange(len(df[time_column]))  # Unique time values (x-axis positions)
    
    # Plot each column
    for i, column in enumerate(columns):
        plt.bar(time_values + i * bar_width, df[column], color=colors[i], width=bar_width, label=column)
    
    # Customize x-axis ticks and labels
    plt.xticks(time_values + bar_width * (len(columns) - 1) / 2, df[time_column])
    
    # Add titles and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_histogram(df, columns, bins=30, color='#669bbc', kde=False, n_cols=3):
    n_rows = (len(columns) + n_cols - 1) // n_cols  # Calculate number of rows needed
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))  # Adjust figure size
    axes = axes.flatten()
    
    for i, column in enumerate(columns):
        axes[i].hist(df[column], bins=bins, color=color, edgecolor='black', density=kde)
        axes[i].set_title(f'{column} over time')
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('Frequency')
        axes[i].grid(axis='y')
    
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.show()

# correlation matrix
def plot_correlation_matrix(df,columns):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[columns].corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=2)
    plt.title('Correlation Matrix')
    plt.show()

def plot_outlier_detection(df, numerical_cols):
    """
    Detects outliers using box plots for numerical columns and displays them in 3 columns.
    """
    # Number of rows needed
    n_cols = 3
    n_rows = (len(numerical_cols) + n_cols - 1) // n_cols  # Calculate number of rows needed
    # Create subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))  # Adjust figure size
    # Flatten axes array in case of multiple rows and columns
    axes = axes.flatten()
    # Loop through the numerical columns and plot each boxplot
    for i, col in enumerate(numerical_cols):
        sns.boxplot(x=df[col].dropna(), ax=axes[i])
        axes[i].set_title(f'Box Plot for {col}')
    # Remove empty subplots if any
    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    plt.show()

def plot_outliers(df, columns, title, orient='h', palette='set2'):
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df[columns], orient=orient)
    plt.title(title)
    plt.show()


def plot_wind_rose(data, ws_col='WS', wd_col='WD', title='Wind Rose'):
    plt.figure(figsize=(10, 8))
    ax = WindroseAxes.from_ax()
    ax.bar(data[wd_col], data[ws_col], normed=True, opening=0.8, edgecolor='white', bins=np.arange(0, max(data[ws_col]), 2))
    ax.set_legend(title='Wind Speed (m/s)', loc='upper left', bbox_to_anchor=(1, 1))
    plt.title(title)
    plt.show()

def create_radial_bar_plot(wind_stats):
    angles = np.linspace(0, 2 * np.pi, len(wind_stats), endpoint=False).tolist()
    angles += angles[:1]
    wind_speeds = wind_stats.values.tolist()
    wind_speeds += wind_speeds[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
    ax.fill(angles, wind_speeds, color='blue', alpha=0.3)
    ax.plot(angles, wind_speeds, color='blue')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(wind_stats.index)
    plt.title("Radial Bar Plot: Wind Speed by Compass Direction")
    plt.show()

def create_bubble_chart(data, x_var, y_var, size_var, color_var, title, xlabel, ylabel):
    """
    Create a bubble chart with the given parameters.

    Parameters:
    data (pd.DataFrame): The dataset to plot.
    x_var (str): The column name for the x-axis.
    y_var (str): The column name for the y-axis.
    size_var (str): The column name for the bubble size.
    color_var (str): The column name for the bubble color.
    title (str): The title of the plot.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.
    """
    # Normalize bubble size for better scaling
    bubble_size = data[size_var] / data[size_var].max() * 100

    # Create a scatter plot with bubble size
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(data[x_var], data[y_var], s=bubble_size, c=data[color_var], alpha=0.6, cmap='viridis', edgecolors="w")
    plt.colorbar(scatter, label=color_var)
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()