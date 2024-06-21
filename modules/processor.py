import duckdb
from utils.logger import Logger


def process_data(db_path, input_table_name, output_table_name):
    try:
        Logger.section_header(f"Processing data in {db_path}...")
        with duckdb.connect(database=db_path) as con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {output_table_name} AS
                SELECT 
                    user_id, 
                    COUNT(*) AS total_events, 
                    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
                    AVG(price) AS average_price
                FROM {input_table_name}
                WHERE price IS NOT NULL
                GROUP BY user_id;
            """)
            Logger.info(f"Data has been processed and stored in {output_table_name}.")
           
            print_table_info(con, output_table_name)
    except Exception as e:
        print(f"Error processing data in {db_path}: {e}")
        raise e

def aggregate_sales(db_path, input_table_name,output_table_name):
    try:
        with duckdb.connect(database=db_path) as con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {output_table_name} AS
                SELECT 
                    COUNT(*) AS total_events,
                    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
                    SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS total_cart_additions,
                    SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS total_views,
                    AVG(price) AS average_price
                FROM {input_table_name}
                WHERE price IS NOT NULL;
            """)
            print("Sales and event data aggregated and stored.")
            print_table_info(con, output_table_name)
    except Exception as e:
        print(f"Error aggregating sales data in {db_path}: {e}")
        raise e
import duckdb
import pandas as pd

def print_table_info(con, table_name):
    """
    Prints basic information about a table, focusing on aggregated data, using pandas DataFrame for better presentation.
    
    Parameters:
    con (duckdb.DuckDBPyConnection): Active database connection.
    table_name (str): The name of the table to describe.
    """
    try:
        # Get total row count
        row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Table '{table_name}' contains {row_count} rows.")

        # Print sample data using DataFrame if the table is not empty
        if row_count > 0:
            df = con.execute(f"SELECT * FROM {table_name} LIMIT 5").df()  # Fetching first 5 rows into a DataFrame
            Logger.section_header(f"Sample data from table '{table_name}':")
            print(df)
    except Exception as e:
        print(f"Error retrieving table info for {table_name}: {e}")
        raise e