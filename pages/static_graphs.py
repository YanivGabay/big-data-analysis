from modules.create_visualization import show_aggregated_data
from modules.analyze_data import brand_performance_query
import streamlit as st
from modules.setup_runner import get_months
import plotly.graph_objects as go
import sqlite3
from modules.config_loader import config
import pandas as pd
import os

from utils.logger import Logger

def show():
    st.title('Static Graphs')
    st.write('This section provides static graphs for the aggregated sales data.')

    show_aggregated_data(get_months())
    brand_performance()


def brand_performance():
    st.title('Brand Performance')
    st.write('This section provides an overview of the brand performance per each month.')

    Logger.info('Executing Brand Performance Query')
    df_nov, df_oct = brand_performance_query()
    Logger.info('Brand Performance Query Executed')
    Logger.info('trying to save data to sqlite')
    
    save_to_sqlite(df_oct, f"{config.queries_dbs.brands_performance.october}", config.queries_dbs.brands_performance.table_names.brands_performance_oct)
    save_to_sqlite(df_nov, f"{config.queries_dbs.brands_performance.november}", config.queries_dbs.brands_performance.table_names.brands_performance_nov)

    df_oct = load_top_brands(f"{config.queries_dbs.brands_performance.october}",config.queries_dbs.brands_performance.table_names.brands_performance_oct,25)
    df_nov = load_top_brands(f"{config.queries_dbs.brands_performance.november}",config.queries_dbs.brands_performance.table_names.brands_performance_nov,25)



    st.write('Brand Performance for October')
    st.write(df_oct)
    fig_oct = create_brand_performance_graph(df_oct)
    st.plotly_chart(fig_oct)

    st.write('Brand Performance for November')
    st.write(df_nov)
    fig_nov = create_brand_performance_graph(df_nov)
    st.plotly_chart(fig_nov)
 

def save_to_sqlite(df, db_path, table_name):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure directory exists
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        Logger.info(f"Data saved to SQLite database at {db_path}")
    except Exception as e:
        Logger.error(f"Error saving data to SQLite database: {str(e)}")


def load_top_brands(sqlite_db_path,table_name,top=50):
    with sqlite3.connect(sqlite_db_path) as conn:
        query = f"""
        SELECT * FROM {table_name}
        ORDER BY total_sales DESC
        LIMIT {top};
        """
        df = pd.read_sql(query, conn)
    return df

def create_brand_performance_graph(df):
    # Create a bar chart with Plotly
    fig = go.Figure(data=[
        go.Bar(name='Total Sales', x=df['brand'], y=df['total_sales'], yaxis='y', offsetgroup=1),
        go.Bar(name='Average Price', x=df['brand'], y=df['average_price'], yaxis='y2', offsetgroup=2)
    ])

    # Here we add a secondary y-axis for the average price
    fig.update_layout(
        title='Brand Performance: Total Sales and Average Price',
        xaxis=dict(title='Brand'),
        yaxis=dict(title='Total Sales', side='left', showgrid=False),
        yaxis2=dict(title='Average Price', side='right', overlaying='y', showgrid=False, range=[0, max(df['average_price']) * 1.2]),
        legend=dict(x=0.01, y=0.99, bordercolor='Black', borderwidth=1)
    )

    # Show the figure
    return fig