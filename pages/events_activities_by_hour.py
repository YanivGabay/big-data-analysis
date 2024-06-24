
from modules.analyze_data import activities_by_hour_query
import streamlit as st

import plotly.graph_objects as go
import sqlite3
from modules.config_loader import config
import pandas as pd
import os
from modules.sqlite_manager import save_to_sqlite
from modules.sqlite_manager import execute_query_to_df
from utils.logger import Logger
import matplotlib.pyplot as plt
import seaborn as sns

def show():
    setup_user_ret()
    activities_by_hour()

def setup_user_ret():
    """
    This function is called to set up activities by hour. It processes data only once per session.
    """
    if 'activities_by_hour_data' not in st.session_state:
        Logger.info("Setting up activities by hour...")
   
        setup_data()  
        Logger.info("activities by hour setup completed.")
        st.session_state['activities_by_hour_data'] = True  # Mark data as prepared
    

def setup_data():
   
    Logger.info('Executing activities_by_hour_query Query')
    df_both = activities_by_hour_query()
    Logger.info('Trying to save data to SQLite')

    save_to_sqlite(df_both, f"{config.databases.shared_user_activity_by_hour.db_path}", config.databases.shared_user_activity_by_hour.table_name)

def activities_by_hour():
    st.title('User Activities by Hour')
    st.write('This section provides an overview of user activities by hour.')
    st.write("""
    ### Functionality Overview
    1. **Execute User Activities by Hour Query**: Retrieves data from the minified sqlite database.
    
            
    """)
    df = get_activities_by_hour()
    plot_activities_by_hour(df)

    
def plot_activities_by_hour(df):
    st.title('User Activities by Hour')
    st.write('This section provides an overview of user activities by hour across two months: October and November.')

    # Pivot the DataFrame for each month
    heatmap_data_oct = df.pivot(index='event_type', columns='hour', values='event_count_oct').fillna(0)
    heatmap_data_nov = df.pivot(index='event_type', columns='hour', values='event_count_nov').fillna(0)

    # Create the heatmaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))  # Creating a subplot with two columns

    # Heatmap for October
    sns.heatmap(heatmap_data_oct, annot=True, fmt=".0f", cmap='coolwarm', linewidths=.5, ax=ax1)
    ax1.set_title('Hourly Distribution of User Activities in October')
    ax1.set_ylabel('Event Type')
    ax1.set_xlabel('Hour of Day')

    # Heatmap for November
    sns.heatmap(heatmap_data_nov, annot=True, fmt=".0f", cmap='coolwarm', linewidths=.5, ax=ax2)
    ax2.set_title('Hourly Distribution of User Activities in November')
    ax2.set_ylabel('Event Type')
    ax2.set_xlabel('Hour of Day')

    plt.tight_layout()  # Adjust layout to make room for plot titles etc.
    st.pyplot(fig)  # Display the plot in Streamlit


def get_activities_by_hour():
    query = f"""
    SELECT * FROM {config.databases.shared_user_activity_by_hour.table_name}
    """
    df = execute_query_to_df(config.databases.shared_user_activity_by_hour.db_path,query)
    Logger.info(f"Dataframe shape: {df.shape[0]} rows, {df.shape[1]} columns")
    Logger.info('Df headers:')
    Logger.info(df.head())


    return df