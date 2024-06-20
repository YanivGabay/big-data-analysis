import streamlit as st
from modules.loader import load_data
from modules.tester import test_data
from modules.loader import process_multiple_months
from modules.processor import aggregate_sales, process_data


months = ['Oct', 'Nov']
csv_file_path = 'data/2019-{month}.csv'
data_base_path = 'db/2019-{month}.duckdb'
table_name = 'raw_data'

def setup_runner():
    
      with st.spinner('Loading data... Please wait...'):
            # Load data into DuckDB from CSV
            print("Loading data...")
            process_multiple_months(months)

         
            for month in months:
                # Test data
                print(f"Testing data for {month}...")
                db_path = data_base_path.format(month=month.lower())
                test_data(db_path, table_name)


                # Process data
                print(f"Processing data for {month}...")
                db_path = data_base_path.format(month=month.lower())
                process_data(db_path, table_name, 'sales_data')
                aggregate_sales(db_path, table_name)
         
        
            for month in months:
               
            