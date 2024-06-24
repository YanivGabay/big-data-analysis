import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
from modules.sqlite_manager import execute_query_to_df
from modules.config_loader import config


# You can call these functions within your main app function
def show():
    st.title('User Activity Analysis')
    df_oct, df_nov = setup_data()
    for df in [df_oct, df_nov]:
            plot_total_events_distribution( df)
            show_price_statistics( df)
            plot_purchase_proportion( df)



def setup_data():

    df_oct, df_nov = load_user_data()
    return df_oct, df_nov

def load_user_data():
    table_name_oct = config.databases.sales_data.october.table_name
    table_name_nov = config.databases.sales_data.november.table_name
    
    query = """SELECT user_id
                ,total_events
                ,total_purchases
                ,average_price

            FROM {}"""
    
    df_oct = execute_query_to_df(config.databases.sales_data.october.db_path, query.format(table_name_oct))
    df_nov = execute_query_to_df(config.databases.sales_data.november.db_path, query.format(table_name_nov))
    
    return df_oct, df_nov
    

# Function to plot the distribution of total events
def plot_total_events_distribution(df):
 
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_events'], bins=30, kde=True)
    plt.title('Distribution of Total Events per User')
    plt.xlabel('Total Events')
    plt.ylabel('Number of Users')
    st.pyplot(plt)

# Function to show summary statistics of average prices
def show_price_statistics(df):

    st.write('### Summary Statistics for Average Prices')
    st.write(df['average_price'].describe())

# Function to plot the proportion of users with purchases
def plot_purchase_proportion(df):

    purchase_counts = df['total_purchases'].apply(lambda x: 'Purchased' if x > 0 else 'No Purchase').value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(purchase_counts, labels=purchase_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Proportion of Users Making Purchases')
    st.pyplot(plt)



# Assuming you call this show() function at some point in your Streamlit script
