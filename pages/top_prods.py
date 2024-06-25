from modules.analyze_data import top_prod_compare_query
import streamlit as st
import sqlite3
from modules.config_loader import config
import pandas as pd
from modules.sqlite_manager import save_to_sqlite
from utils.logger import Logger
import matplotlib.pyplot as plt
from modules.sqlite_manager import execute_query_to_df
import plotly.express as px
from modules.page_data_manager import PageDataManager

october_db_path = f"{config.databases.top_products.db_path}"
november_db_path = f"{config.databases.top_products.db_path}"

top_prods_table_name = f"{config.databases.top_products.table_name}"
top_prods_db_path = f"{config.databases.top_products.db_path}"


colors = ['sunset', 'magenta', 'blues', 'teal', 'sunsetdark']

def show():
    PageDataManager.setup(top_prods_db_path,setup_data)
    top_prods()


def setup_data():
        
       Logger.info('Executing')

       df = top_prod_compare_query()

       Logger.info('Trying to save data to SQLite')
       save_to_sqlite(df, top_prods_db_path,top_prods_table_name )
       Logger.info('Data saved to SQLite')

def top_prods():
    Logger.info('Displaying Top selling Products')
    st.title('Top Products Performance Analysis')
    st.write('This section provides a dynamic and interactive overview of top products based on sales performance across two distinct months: October and November.')

    # Detailed explanation of what the user is seeing and how to interact with the data
    st.write("""
        ### Chart Overview
        - **Interactive Elements**: Use the sliders below to customize the data presented:
          - **Number of Products**: Select how many top products to display based on total sales.
          - **Percentage Increase Threshold**: Set a minimum sales increase percentage to highlight products with significant month-to-month sales growth.
        - **Visualization Details**:
          - **Bubbles**: Each bubble represents a product.
          - **Size**: The size of each bubble indicates the total sales value of the product across both months—larger bubbles denote higher sales (price x total sales count).
          - **Color Intensity**: Darker bubbles signify higher total sales, providing a visual cue to quickly identify top-performing products.
          - **Position**: The horizontal (X-axis) position shows sales count in October, and the vertical (Y-axis) position shows sales count in November.
        - **Data Points**:
          - **Hover Data**: Hover over any bubble to see detailed information about the product’s October sales count, November sales count, total sales, and percentage increase in sales formatted for easy reading.

        ### How to Interpret
        - **Assess Product Performance**: Quickly assess which products are the best performers both in terms of total sales and sales growth.
        - **Identify Trends**: Look for trends such as products that have significant increases in sales from October to November, as indicated by their movement from left to right.

        ### Interactive Controls
        - **Top Products Slider**: Adjust to increase or decrease the number of top selling products displayed.
        - **Percentage Increase Slider**: Move to set the threshold for highlighting products with significant sales growth.
    """)
    top_brands = st.slider('Select how many top selling products to display:', min_value=10, max_value=100, value=25, step=5)
    percent_increase = st.slider('Select the minimum percentage increase to highlight:', min_value=0, max_value=100, value=50, step=5)
    select_color_palette = st.selectbox('Select Color Palette', colors)  
    Logger.info(f"Top products to display: {top_brands}, Minimum percentage increase to highlight: {percent_increase}%,Choosen Color Pallete: {select_color_palette}")
    df = load_top_prods(top_brands)
    
    plot_top_brands(df,percent_increase,select_color_palette)
    st.dataframe(df)

def plot_top_brands(df, percent_increase,select_color_pallete):
    Logger.info(f"Plotting top brands, threshold for significant increase: {percent_increase}%")
    
    # Filter the DataFrame to include only the rows with significant increases
    filtered_df = df[df['percent_increase'] > percent_increase]
    
    fig = px.scatter(
        filtered_df,
        x='sales_count_oct',
        y='sales_count_nov',
        size='total_sales',  # Bubble size based on total sales
        color='percent_increase',  # Bubble color also based on total sales for additional visual differentiation
        hover_name='product_id',  # Shows product_id on hover for clarity
        color_continuous_scale=select_color_pallete,
        hover_data={
            'total_sales': ':,',  # Add total sales with comma as thousands separator
            'sales_count_oct': ':,',  # Add sales count in October with comma as thousands separator
            'sales_count_nov': ':,',  # Add sales count in November with comma as thousands separator
            'percent_increase': ':.2f%'  # Add percentage increase with 2 decimal places
        },
        size_max=60,  # Maximum bubble size
        title='Comparative Sales Analysis for Top Products',
        labels={
            'sales_count_oct': 'Sales Count in October',
            'sales_count_nov': 'Sales Count in November',
            'percent_increase': 'Percent Increase %'
        }
    )

    fig.update_layout(
        coloraxis_colorbar=dict(title='Percent Increase %'),
        xaxis_title='Sales Count in October',
        yaxis_title='Sales Count in November',
        title_font=dict(size=24, family='Arial', color='Black'),
        font=dict(size=14),
        annotations=[
            dict(
                x=0.5,
                y=-1.15,
                showarrow=False,
                text="Bubble size represents total sales; color intensity increase percentage from October to November",
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14)
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)


def load_top_prods(top):
 
    query = f"""
        SELECT 
            total_sales,
            product_id,
            sales_count_oct,
            total_sales_oct,
            sales_count_nov,
            total_sales_nov,
           
             -- Calculate the percentage increase from October to November
            CASE 
                WHEN sales_count_oct > 0 THEN
                    (sales_count_nov - sales_count_oct) * 100.0 / sales_count_oct
                ELSE
                    0  -- Handle cases where October sales are 0 to avoid division by zero
            END AS percent_increase
        FROM {top_prods_table_name}
        ORDER BY total_sales DESC
        LIMIT {top}
        """
    df = execute_query_to_df(top_prods_db_path, query)
    return df