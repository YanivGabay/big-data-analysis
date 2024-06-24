from modules.analyze_data import top_prod_compare_query
import streamlit as st
import sqlite3
from modules.config_loader import config
import pandas as pd
from modules.sqlite_manager import save_to_sqlite
from utils.logger import Logger
import matplotlib.pyplot as plt
from modules.sqlite_manager import execute_query_to_df


october_db_path = f"{config.databases.top_products.db_path}"
november_db_path = f"{config.databases.top_products.db_path}"

top_prods_table_name = f"{config.databases.top_products.table_name}"
top_prods_db_path = f"{config.databases.top_products.db_path}"




def show():
    setup_top_prods()
    #top_prods()


def setup_top_prods():
    """
    This function is called to set up brand data. It processes data only once per session.
    """
    if 'user_retention_data' not in st.session_state:
        Logger.info("Setting up brand data...")
       
        setup_data()  
        Logger.info("Brand data setup completed.")
        st.session_state['user_retention_data'] = True  # Mark data as prepared

def setup_data():
        
       Logger.info('Executing')

       df = top_prod_compare_query()

       Logger.info('Trying to save data to SQLite')
       save_to_sqlite(df, top_prods_db_path,top_prods_table_name )
       Logger.info('Data saved to SQLite')

def top_prods():
    Logger.info('Displaying Top Prods')
    st.title('Top Prods')
    st.write('This section provides an overview of top prods.')
    st.write("""
    ### Functionality Overview
    1. **Execute Top Prods Query**: Retrieves data from the minified sqlite database.
    
            
    """)
    top_brands = st.slider('Select how many top brands to display:', min_value=10, max_value=100, value=25, step=5)

    df = get_top_prods(top_brands)
    event_type = st.selectbox('Select an Event Type:', ['All'] + sorted(df['event_type'].unique()))
    df = df if event_type == 'All' else df[df['event_type'] == event_type]

def get_top_prods():
    query = """
    f"SELECT * 
            FROM {top_prods_table_name}"
            """
    df = execute_query_to_df(top_prods_db_path, query)
    return df