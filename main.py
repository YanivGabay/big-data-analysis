
from pages import overview,  static_graphs , brand_performance , user_retention, events_activities_by_hour, top_prods
import streamlit as st

from modules.setup_runner import setup_runner
from utils.logger import Logger
st.set_page_config(page_title='Data Analysis Dashboard', layout='wide')


### If you only have the sql files, both of them need to be FALSE
### If you have the csv files, LOAD_FROM_CSV needs to be TRUE
### If you want to test some basic info, TEST_DUCKDB needs to be TRUE and Logger.set_console_output(True)

LOAD_FROM_CSV = False  # Set to False to skip loading data from CSV files
TEST_DUCKDB = False  # Set to True to test DuckDB queries

def main():
    """
    This function serves as the entry point for the application.
    It sets up the sidebar for navigation and handles the different page choices.
    It also loads and processes data only once and not reloads on navigation change.
    """

    #### i reccomend to use True to see command line outputs
    #### your choice

    Logger.set_console_output(False)
    try:
        # Setup sidebar for navigation
        st.sidebar.title('Navigation')
        choice = st.sidebar.selectbox(
            'Choose a page:',
            ['Overview', 'Static Graphs', 'Brand Performance',
             'User Retention', 'User Activities by Hour', 'Top Products'])

        container = st.container(border=True)
        # Load and process data only once and not reload on navigation change
        if 'data_loaded' not in st.session_state:
            with st.spinner('Setting up data...'):
                setup_runner(LOAD_FROM_CSV, TEST_DUCKDB)
                st.session_state['data_loaded'] = True  # Mark as loaded
                container.success('Data has been loaded and processed successfully.')

        # Show aggregated data on a dedicated page or under a condition
        if choice == 'Overview':
            overview.show()

        elif choice == 'Static Graphs':
            static_graphs.show()
        elif choice == 'Brand Performance':
            brand_performance.show()
        elif choice == 'User Retention':
            user_retention.show()
        elif choice == 'User Activities by Hour':
            events_activities_by_hour.show()
        elif choice == 'Top Products':
            top_prods.show()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
