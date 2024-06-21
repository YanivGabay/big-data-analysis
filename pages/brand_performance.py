from modules.analyze_data import brand_performance_query
import streamlit as st
import sqlite3
from modules.config_loader import config
import pandas as pd
from modules.sqlite_manager import save_to_sqlite
from utils.logger import Logger
import matplotlib.pyplot as plt

def show():
    brand_performance()

def brand_performance():
    st.title('Brand Performance')
    st.write('This section provides an overview of the brand performance per each month.')
    st.write("""
    ### Functionality Overview
    1. **Execute Brand Performance Query**: Retrieves data from the DuckDB database for both October and November.
    2. **Save Data to SQLite**: Saves the queried data into separate SQLite databases for October and November.
    3. **Load Top Brands**: Loads the top 25 brands based on total sales from the SQLite databases.
    4. **Display Data**: Displays the data in Streamlit using a DataFrame.
    5. **Create and Display Graphs**: Generates and displays bar charts for each month, showing both the total sales and the average price for each brand (with median lines).
    """)

    Logger.info('Executing Brand Performance Query')
    df_nov, df_oct = brand_performance_query()
    Logger.info('Brand Performance Query Executed')
    Logger.info('Trying to save data to SQLite')

    save_to_sqlite(df_oct, f"{config.queries_dbs.brands_performance.october}", config.queries_dbs.brands_performance.table_names.brands_performance_oct)
    save_to_sqlite(df_nov, f"{config.queries_dbs.brands_performance.november}", config.queries_dbs.brands_performance.table_names.brands_performance_nov)

    df_oct = load_top_brands(f"{config.queries_dbs.brands_performance.october}", config.queries_dbs.brands_performance.table_names.brands_performance_oct, 25)
    df_nov = load_top_brands(f"{config.queries_dbs.brands_performance.november}", config.queries_dbs.brands_performance.table_names.brands_performance_nov, 25)

    st.write('Brand Performance for October')
    st.dataframe(style_dataframe(df_oct))
    create_brand_performance_graph(df_oct, 'October', metric='total_sales')
    create_brand_performance_graph(df_oct, 'October', metric='average_price')

    st.write('Brand Performance for November')
    st.dataframe(style_dataframe(df_nov))
    create_brand_performance_graph(df_nov, 'November', metric='total_sales')
    create_brand_performance_graph(df_nov, 'November', metric='average_price')

def style_dataframe(df):
    styled_df = df.style.map(lambda val: 'color: red;' if val > df['total_sales'].mean() else 'color: black;', subset=['total_sales'])
    styled_df = styled_df.map(lambda val: 'color: blue;' if val > df['average_price'].mean() else 'color: black;', subset=['average_price'])
    return styled_df

def load_top_brands(sqlite_db_path, table_name, top=50):
    with sqlite3.connect(sqlite_db_path) as conn:
        query = f"""
        SELECT 
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
        df = pd.read_sql(query, conn)
        df.insert(0, 'Rank', range(1, 1 + len(df)))  # Add Rank column starting from 1
    return df

def create_brand_performance_graph(df, month, metric):
    plt.figure(figsize=(14, 7))
    
    if metric == 'total_sales':
        plt.bar(df['brand'], df['total_sales'] / 1e6, color='skyblue')  # Convert to millions
        median_value = df['total_sales'].median() / 1e6  # Convert to millions
        plt.axhline(y=median_value, color='r', linestyle='--', label=f'Median Total Sales: {median_value:.2f}M')
        plt.title(f'Total Sales for {month}')
        plt.ylabel('Total Sales (in millions)')
        
        # Add text labels on bars
        for index, value in enumerate(df['total_sales'] / 1e6):
            plt.text(index, value, f'{value:.2f}M', ha='center', va='bottom')
            
    elif metric == 'average_price':
        plt.bar(df['brand'], df['average_price'], color='lightgreen')
        median_value = df['average_price'].median()
        plt.axhline(y=median_value, color='b', linestyle='--', label=f'Median Avg Price: {median_value:.2f}')
        plt.title(f'Average Price for {month}')
        plt.ylabel('Average Price')
        
        # Add text labels on bars
        for index, value in enumerate(df['average_price']):
            plt.text(index, value, f'{value:.2f}', ha='center', va='bottom')

    plt.xlabel('Brand')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()