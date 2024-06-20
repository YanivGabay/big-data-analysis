from modules.loader import load_data
from modules.tester import test_data
from modules.loader import process_multiple_months
from modules.processor import aggregate_sales, process_data
from pages import overview, interactive, static_graphs
import streamlit as st
from modules.create_visualization import start_visualization,show_aggregated_data

st.set_page_config(page_title='Data Analysis Dashboard', layout='wide')

def main():
    # Define the paths and parameters
    months = ['Oct', 'Nov']
    csv_file_path = 'data/2019-{month}.csv'

    data_base_path = 'db/2019-{month}.duckdb'

    table_name = 'raw_data'

    try:
      
            st.success("Data has been loaded, tested, and processed successfully.")
            start_visualization()
            show_aggregated_data(months)


       
        
  

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
