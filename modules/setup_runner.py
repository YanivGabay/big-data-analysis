import streamlit as st

from modules.loader import process_multiple_months
from modules.config_loader import config

from modules.tester import test_data


def setup_runner(load_from_csv: bool = False, test_duckdb: bool = False):
    progress = st.progress(0)
    status_message = st.empty()
    total_steps = len(config.get_months()) * 3  # Example: each month has 3 steps
    current_step = 0

    try:
        for month in config.get_months():
            # Process multiple months (assuming this might involve loading the data)
            
            status_message.markdown(f"Loading data for {month}...")
            if load_from_csv:
                process_multiple_months([month])  # Make sure this only processes the given month
            current_step += 1
            progress.progress(current_step / total_steps)

            current_step += 1
            progress.progress(current_step / total_steps)
            if test_duckdb:
                # Test DuckDB queries (if enabled)
                status_message.markdown(f"Testing DuckDB for {month}...")
                test_data(config.get_data_base_path(month),config.table_names.raw_data,month)
            current_step += 1
            progress.progress(current_step / total_steps)

        status_message.empty()
        progress.empty()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise e

if __name__ == '__main__':
    setup_runner()
