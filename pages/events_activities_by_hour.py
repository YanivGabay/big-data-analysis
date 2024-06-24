
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
import numpy as np
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
    event_type = st.selectbox('Select an Event Type:', ['All'] + sorted(df['event_type'].unique()))
    df = df if event_type == 'All' else df[df['event_type'] == event_type]
    st.dataframe(df)
    plot_activities_by_hour(df)
    plot_event_type_distribution(df)


def plot_event_type_distribution(df):
    st.title('Distribution of Event Types by Hour')
    st.write('This section visualizes the distribution of different event types by hour for October and November.')
    custom_colors_oct = ['#FFE9D0', '#FFFED3', '#BBE9FF']
    custom_colors_nov = ['#FFC0CB', '#FFDAB9', '#FFD700']
    # Prepare data for plotting
    pivot_oct = df.pivot_table(index='hour', columns='event_type', values='event_count_oct', aggfunc='sum').fillna(0)
    pivot_nov = df.pivot_table(index='hour', columns='event_type', values='event_count_nov', aggfunc='sum').fillna(0)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 12), sharey=True)

    # Stacked bar for October
    pivot_oct.plot(kind='bar', stacked=True, ax=ax1, color=custom_colors_oct)
    ax1.set_title('Hourly Distribution of Event Types in October')
    ax1.set_ylabel('Count of Events')
    ax1.set_xlabel('Hour of Day')
    # Adding text labels for October
    for container in ax1.containers:
        ax1.bar_label(container, label_type='center', fmt='%.0f')

    # Stacked bar for November
    pivot_nov.plot(kind='bar', stacked=True, ax=ax2, color=custom_colors_nov)
    ax2.set_title('Hourly Distribution of Event Types in November')
    ax2.set_ylabel('Count of Events')
    ax2.set_xlabel('Hour of Day')
    # Adding text labels for November
    for container in ax2.containers:
        ax2.bar_label(container, label_type='center', fmt='%.0f')

    plt.tight_layout()
    st.pyplot(fig)



def plot_activities_by_hour(df):
    st.title('User Activities by Hour')
    st.write('This section provides an overview of user activities by hour across two months: October and November.')

    # Pivot the DataFrame for each month
    heatmap_data_oct = df.pivot(index='event_type', columns='hour', values='event_count_oct').fillna(0)
    heatmap_data_nov = df.pivot(index='event_type', columns='hour', values='event_count_nov').fillna(0)

    # Normalize each event type independently
    heatmap_data_oct_normalized = heatmap_data_oct.div(heatmap_data_oct.max(axis=1), axis=0)
    heatmap_data_nov_normalized = heatmap_data_nov.div(heatmap_data_nov.max(axis=1), axis=0)

    # Create the heatmaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))  # Creating a subplot with two columns

    # Heatmap for October
    sns.heatmap(heatmap_data_oct_normalized, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5, ax=ax1)
    ax1.set_title('Hourly Distribution of User Activities in October (Normalized)')
    ax1.set_ylabel('Event Type')
    ax1.set_xlabel('Hour of Day')

    # Heatmap for November
    sns.heatmap(heatmap_data_nov_normalized, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5, ax=ax2)
    ax2.set_title('Hourly Distribution of User Activities in November (Normalized)')
    ax2.set_ylabel('Event Type')
    ax2.set_xlabel('Hour of Day')

    plt.tight_layout()  # Adjust layout to make room for plot titles etc.
    st.pyplot(fig)  # Display the plot in Streamlit


def get_activities_by_hour():
    query = f"""
    SELECT * FROM {config.databases.shared_user_activity_by_hour.table_name}
    ORDER BY hour, event_type;
    """
    df = execute_query_to_df(config.databases.shared_user_activity_by_hour.db_path,query)
    Logger.info(f"Dataframe shape: {df.shape[0]} rows, {df.shape[1]} columns")
    Logger.info('Df headers:')
    Logger.info(df.head())


    return df