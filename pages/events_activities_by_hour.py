
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
from modules.page_data_manager import PageDataManager

shared_user_activity_by_hour_db_path = f"{config.databases.shared_user_activity_by_hour.db_path}"
shared_user_activity_by_hour_table_name = f"{config.databases.shared_user_activity_by_hour.table_name}"



def show():
    PageDataManager.setup(shared_user_activity_by_hour_db_path,setup_data)
    activities_by_hour()

def setup_data():
        
    df_both = activities_by_hour_query()
    
    save_to_sqlite(df_both, f"{shared_user_activity_by_hour_db_path}", shared_user_activity_by_hour_table_name)
    

def activities_by_hour():
    st.title('User Activities by Hour')
    st.write('Explore the dynamics of user activities throughout the day and how these patterns shift between months.')
    st.write("""
    ### Overview and Steps:
    - **Data Retrieval**: Data concerning user activities logged each hour is extracted from a comprehensive database.
    - **Data Processing**: This raw data is processed to categorize activities by type, such as viewing products, adding items to carts, and making purchases, and then summarized by each hour of the day.
    - **Data Visualization**: Various visualizations are provided to illustrate the trends and differences in user activities:
        - **Hourly Activity Heatmaps**: Shows the concentration of different types of user activities throughout the day. Each activity type is normalized across the day for better comparability, highlighting peak hours.
        - **Event Type Distribution Charts**: These stacked bar charts compare the distribution of activity types between two months, showcasing how user behavior changes over time.
    - **User Interaction**: You can filter the visualizations by selecting specific activity types from a dropdown menu, focusing on particular aspects of user behavior.

    ### Select Event Type:
    Use the dropdown to filter activities by event type or view all activities to gain insights into specific or overall user engagements.
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
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(26, 16))  # Creating a subplot with two columns

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
    SELECT * FROM {shared_user_activity_by_hour_table_name}
    ORDER BY hour, event_type;
    """
    df = execute_query_to_df(shared_user_activity_by_hour_db_path,query)
    Logger.info(f"Dataframe shape: {df.shape[0]} rows, {df.shape[1]} columns")
    Logger.info('Df headers:')
    Logger.info(df.head())


    return df