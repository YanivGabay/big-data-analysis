import streamlit as st
from modules.loader import load_data
from modules.tester import test_data
from modules.loader import process_multiple_months
from modules.processor import aggregate_sales, process_data
from modules.config_loader import config

def get_sales_data_table_name():
    return config.table_names.sales_data

def get_aggregate_sales_table_name():
    return config.table_names.aggregated_sales

def get_data_base_path(month):
    return config.data_paths.october if month == 'Oct' else config.data_paths.november

def get_months():
    return config.months

def setup_runner():
    progress = st.progress(0)
    status_message = st.empty()
    total_steps = len(get_months()) * 3  # Example: each month has 3 steps
    current_step = 0

    try:
        for month in get_months():
            # Process multiple months (assuming this might involve loading the data)
            status_message.markdown(f"Loading data for {month}...")
            process_multiple_months([month])  # Make sure this only processes the given month
            current_step += 1
            progress.progress(current_step / total_steps)

            # Test data
            status_message.markdown(f"Testing data for {month}...")
            db_path = get_data_base_path(month)
            test_data(db_path, config.table_names.raw_data,month)
            current_step += 1
            progress.progress(current_step / total_steps)

            # Process data
            status_message.markdown(f"Processing data for {month}...")
            process_data(db_path, config.table_names.raw_data, get_sales_data_table_name())
            aggregate_sales(db_path, config.table_names.raw_data, get_aggregate_sales_table_name())
            current_step += 1
            progress.progress(current_step / total_steps)

        status_message.empty()
        progress.empty()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise e

if __name__ == '__main__':
    setup_runner()
