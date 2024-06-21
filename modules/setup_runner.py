import streamlit as st
from modules.loader import load_data
from modules.tester import test_data
from modules.loader import process_multiple_months
from modules.processor import aggregate_sales, process_data
from modules.config_loader import config

months = ['Oct', 'Nov']
csv_file_path = 'data/2019-{month}.csv'
data_base_path = 'db/2019-{month}.duckdb'

table_name = 'raw_data'
sales_data_table_name = 'sales_data'
aggregate_sales_table_name = 'aggregated_sales'

def get_sales_data_table_name():
    return sales_data_table_name

def get_aggregate_sales_table_name():
    return aggregate_sales_table_name

def get_data_base_path():
    return data_base_path

def get_months():
    return months

def setup_runner():
    progress = st.progress(0)
    status_message = st.empty()
    total_steps = len(months) * 3  # Example: each month has 3 steps
    current_step = 0

    try:
        for month in months:
            # Process multiple months (assuming this might involve loading the data)
            status_message.markdown(f"Loading data for {month}...")
            process_multiple_months([month])  # Make sure this only processes the given month
            current_step += 1
            progress.progress(current_step / total_steps)

            # Test data
            status_message.markdown(f"Testing data for {month}...")
            db_path = data_base_path.format(month=month.lower())
            test_data(db_path, table_name)
            current_step += 1
            progress.progress(current_step / total_steps)

            # Process data
            status_message.markdown(f"Processing data for {month}...")
            process_data(db_path, table_name,config.table_names.sales_data )
            aggregate_sales(db_path, table_name, config.table_names.aggregated_sales)
            current_step += 1
            progress.progress(current_step / total_steps)

        
        status_message.empty()
        progress.empty()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise e
          
               
            