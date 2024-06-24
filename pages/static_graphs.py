import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
from modules.sqlite_manager import execute_query_to_df
from modules.config_loader import config
from modules.aggregate_sales_result import AggregateSalesResult
def load_user_data():
    table_name = config.table_names.sales_data
    query = f"SELECT user_id, total_events, total_purchases, average_price FROM {table_name}"
    df_oct = execute_query_to_df(config.databases.sales_data.october.db_path, query)
    df_nov = execute_query_to_df(config.databases.sales_data.november.db_path, query)
    return df_oct, df_nov

def show():
    st.title('User Activity Analysis')
    df_oct, df_nov = load_user_data()

    with st.expander("October Data Analysis"):
        aggregate_sales_oct = AggregateSalesResult(
        db_path=config.databases.aggregated_sales.october.db_path,
    
        aggregate_sales_table_name=config.table_names.aggregated_sales,
        month = 'October'
        )
        aggregate_sales_oct.show()
        show_summary(df_oct['average_price'], "Average Price", "October")
        plot_purchases(df_oct['total_purchases'], "Purchases", "October")
        
        plot_box(df_nov['total_events'], "Total Events in October")
        plot_aggregated_bar(df_nov['total_events'], "Total Events in October")
        plot_density(df_oct['total_events'], "Total Events", "October")

    with st.expander("November Data Analysis"):
        aggregate_sales_nov = AggregateSalesResult(
        db_path=config.databases.aggregated_sales.november.db_path,

        aggregate_sales_table_name=config.table_names.aggregated_sales,
        month='November'
    )
        aggregate_sales_nov.show()
        show_summary(df_nov['average_price'], "Average Price", "November")
        plot_purchases(df_nov['total_purchases'], "Purchases", "November")
        plot_box(df_nov['total_events'], "Total Events in November")
        plot_aggregated_bar(df_nov['total_events'], "Total Events in November")
        plot_density(df_nov['total_events'], "Total Events", "November")


def plot_box(data, title):
    plt.figure(figsize=(10, 4))
    sns.boxplot(x=data)
    plt.title(f'Box Plot of {title}')
    st.pyplot(plt)

def plot_aggregated_bar(data, title):

    # Binning data
    bins = pd.cut(data, [1, 2, 3, 4, 5, 10, 20, 40, 80, 500, 5000, np.inf], right=False)
    bin_counts = bins.value_counts().sort_index()

    plt.figure(figsize=(12, 6))  # Adjusted figure size
    
    barplot = sns.barplot(x=bin_counts.index.categories, y=bin_counts.values, edgecolor='black', linewidth=1.5, hue=bin_counts.index.categories, palette='viridis')
    barplot.set_xticks(range(len(bin_counts)))  # Set ticks to match the number of bins
    barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45, ha='right')  # Rotate labels for better visibility

    plt.title(f'Aggregated Bar Chart of {title}')
    plt.xlabel('Event Bins')
    plt.ylabel('Number of Users')
    st.pyplot(plt) 


def plot_distribution(data, metric, month):
    plt.figure(figsize=(10, 4))
    log_data = np.log(data + 1)  # Adding 1 to avoid log(0)
    sns.histplot(log_data, kde=True, bins=50)  # Log transform to manage skewness
    plt.title(f'Log-Transformed Distribution of {metric} in {month}')
    plt.xlabel(f'Log of {metric}')
    plt.ylabel('Frequency')
    st.pyplot(plt)
    st.write(f"### The log transformation helps in reducing skewness and bringing the data of {metric.lower()} onto a similar scale for better visual interpretation.")

def show_summary(data, metric, month):
    st.write(f'### Summary Statistics for {metric} in {month}')
    st.write(data.describe())
    st.write(f"### This table provides basic descriptive statistics such as mean, median, and standard deviation for {metric.lower()} which helps in understanding the central tendency and dispersion of {metric.lower()}.")



def plot_density(data, metric, month):
    plt.figure(figsize=(10, 4))
    sns.kdeplot(data, bw_adjust=0.10)  # You can adjust the bandwidth to control smoothness
    plt.title(f'Density Plot of {metric} in {month}')
    plt.xlabel(f'{metric}')
    plt.ylabel('Density')
    st.pyplot(plt)
    st.write(f"### This density plot provides a smooth estimate of the distribution of {metric.lower()} across users in {month}. It helps identify the data concentration and spread without the skewness that often comes with raw data visualization.")



def plot_purchases(data, metric, month):
    purchases = data.apply(lambda x: 'Purchased' if x > 0 else 'No Purchase').value_counts(normalize=True)
    plt.figure(figsize=(7, 4))
    plt.pie(purchases, labels=purchases.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'Proportion of Users Making {metric} in {month}')
    st.pyplot(plt)
    st.write("### This pie chart illustrates the proportion of users who have made purchases compared to those who have not, providing insights into user buying behavior during the month.")
