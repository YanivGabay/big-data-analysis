from modules.analyze_data import brand_performance_query
import streamlit as st
import sqlite3
from modules.config_loader import config
import pandas as pd
from modules.sqlite_manager import save_to_sqlite
from utils.logger import Logger
import matplotlib.pyplot as plt
from modules.sqlite_manager import execute_query_to_df
TOP = 50

october_db_path = f"{config.databases.brands_performance.october.db_path}"
november_db_path = f"{config.databases.brands_performance.november.db_path}"
october_table_name = f"{config.databases.brands_performance.october.table_name}"
november_table_name = f"{config.databases.brands_performance.november.table_name}"

def show():
    setup_brand_data()
    brand_performance()

def setup_brand_data():
    """
    This function is called to set up brand data. It processes data only once per session.
    """
    if 'brand_data_prep' not in st.session_state:
        Logger.info("Setting up brand data...")
   
        setup_data()  
        Logger.info("Brand data setup completed.")
        st.session_state['brand_data_prep'] = True  # Mark data as prepared

def setup_data():
   
    Logger.info('Executing Brand Performance Query')
    df_nov, df_oct = brand_performance_query()
    Logger.info(f"October data: {df_oct.shape[0]} rows, {df_oct.shape[1]} columns")
    Logger.info(f"November data: {df_nov.shape[0]} rows, {df_nov.shape[1]} columns")
    Logger.info('Df headers:')
    Logger.info(df_oct.head())
    Logger.info(df_nov.head())
    Logger.info('Brand Performance Query Executed')
    Logger.info('Trying to save data to SQLite')

    save_to_sqlite(df_oct, f"{october_db_path}",
                   october_table_name)
    save_to_sqlite(df_nov, f"{november_db_path}", 
                  november_table_name)
   

def brand_performance():
    Logger.info('Displaying Brand Performance')
    st.title('Brand Performance')
    st.write('This section provides an overview of the brand performance per each month.')
    st.write("""
    ### Functionality Overview
    1. **Execute Brand Performance Query**: Retrieves data from the DuckDB database for both October and November.
    2. **Save Data to SQLite**: Saves the queried data into separate SQLite databases for October and November.
    3. **Load Top Brands**: Loads the top @TOP brands based on total sales from the SQLite databases.
    4. **Display Data**: Displays the data in Streamlit using a DataFrame.
    5. **Create and Display Graphs**: Generates and displays bar charts for each month, showing both the total sales and the average price for each brand (with median lines).
    """)
     # Slider for user input
    top_brands = st.slider('Select how many top brands to display:', min_value=10, max_value=100, value=25, step=5)


    df_oct = load_top_brands(f"{october_db_path}", october_table_name, top_brands)
    df_nov = load_top_brands(f"{november_db_path}", november_table_name, top_brands)



    st.write('### Brand Performance for October')
    display_dataframe_with_legend(df_oct)
    create_brand_performance_graph(df_oct, 'October', metric='total_sales')
    create_brand_performance_graph(df_oct, 'October', metric='average_price')
  
    st.write('### Brand Performance for November')
   # st.dataframe(style_dataframe(df_nov))
    display_dataframe_with_legend(df_nov)
    create_brand_performance_graph(df_nov, 'November', metric='total_sales')
    create_brand_performance_graph(df_nov, 'November', metric='average_price')
    

def style_dataframe(df):
    Logger.info("DataFrame head for styling:")
    Logger.info(df.head())

    try:
    
        Logger.info("Styling DataFrame...")
        median_total_sales = df['total_sales'].median()
        median_average_price = df['average_price'].median()

        # Styling for 'total_sales' and 'average_price'
        styled_df = df.style.apply(
            lambda x: ['background-color: red' if v > median_total_sales else 'background-color: transparent' for v in x],
            subset=['total_sales']
        ).apply(
            lambda x: ['background-color: cyan' if v > median_average_price else 'background-color: transparent' for v in x],
            subset=['average_price']
        ).set_caption("Red: Total Sales above median ||| Blue: Average Price above median")

        return styled_df

    except Exception as e:
        Logger.error(f"Error styling DataFrame: {str(e)}")
        raise


def display_dataframe_with_legend(df):

  
    try:
        st.write('#### Red: Total Sales above median; Cyan: Average Price above median')
        styled_df = style_dataframe(df)
        st.dataframe(styled_df)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")




def load_top_brands(sqlite_db_path, table_name, top=TOP):
    Logger.info(f"Loading top {top} brands from {sqlite_db_path}...")
    Logger.info(f"Table name: {table_name}")

    query = f"""
                SELECT
                    ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS Rank,
                    brand,
                    total_sales,
                    total_purchases,
                    average_price
                FROM
                    {table_name}
                ORDER BY
                    total_sales DESC
                LIMIT
                    {top};
                """
    df = execute_query_to_df(sqlite_db_path, query)
    Logger.info(f"Successfully queried from {sqlite_db_path} the top {top} brands.")
    return df


def create_brand_performance_graph(df, month, metric):
    plt.figure(figsize=(14, 7))
    Logger.info(f"Creating brand performance graph for {month}...")
    if metric == 'total_sales':
        # Convert total sales to millions for easier readability
        sales_in_millions = df['total_sales'] / 1e6
        median_value = sales_in_millions.median()
        colors = ['red' if x > median_value else 'skyblue' for x in sales_in_millions]

        bars = plt.bar(df['brand'], sales_in_millions, color=colors)
        plt.axhline(y=median_value, color='r', linestyle='--', label=f'Median Total Sales: {median_value:.2f}M')
        plt.title(f'Total Sales for {month}')
        plt.ylabel('Total Sales (in millions)')
        
        # Add text labels on bars
        for bar, value in zip(bars, sales_in_millions):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}M', ha='center', va='bottom')
            
    elif metric == 'average_price':
        median_value = df['average_price'].median()
        colors = ['blue' if x > median_value else 'lightgreen' for x in df['average_price']]

        bars = plt.bar(df['brand'], df['average_price'], color=colors)
        plt.axhline(y=median_value, color='b', linestyle='--', label=f'Median Avg Price: {median_value:.2f}')
        plt.title(f'Average Price for {month}')
        plt.ylabel('Average Price')
        
        # Add text labels on bars
        for bar, value in zip(bars, df['average_price']):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom')

    plt.xlabel('Brand')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()
