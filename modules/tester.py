
import duckdb
import streamlit as st
from utils.logger import Logger


def test_data(db_path, table_name, month):
    """
    Perform a series of data integrity checks and visualizations on a specified table for a given month.

    Parameters:
    db_path (str): Path to the database file.
    table_name (str): Name of the table to test.
    month (str): Month for which the data is being tested, used for display purposes.
    """
    try:
        Logger.info(f"Testing data for {month}: {table_name}...")
        con = duckdb.connect(db_path)
        st.write(f"#### Testing data for {month}: {table_name}")
        count_rows(con, table_name)
        print_some_data(con, table_name)
        describe_table(con, table_name)
        check_categorical_data(con, table_name)
        count_missing_values(con, table_name)
        count_unique_products(con, table_name)
        Logger.info(f"Data testing for {month}: {table_name} complete.")
    finally:
        con.close()


def print_some_data(con, table_name):
    """Prints the first 10 rows of the specified table."""
    Logger.info(f"Displaying sample data from {table_name}...")
    query = f"SELECT * FROM {table_name} LIMIT 10"
    result = con.execute(query).fetchdf()
    st.dataframe(result)


def describe_table(con,table_name):
    Logger.info(f"Describing table {table_name}...")
    st.write(f"**Describing table {table_name}:**")
    result = con.execute(f"DESCRIBE {table_name}").fetchdf()
    Logger.info(result)
    st.dataframe(result)





def describe_table(con, table_name):
    """Displays the schema of the specified table."""
    Logger.info(f"Describing schema of {table_name}...")
    result = con.execute(f"DESCRIBE {table_name}").fetchdf()
    st.dataframe(result)

def check_categorical_data(con, table_name):
    """Checks and displays distinct categories within the 'event_type' column."""
    Logger.info("Checking distinct event types...")
    event_types = con.execute(f"SELECT DISTINCT event_type FROM {table_name}").fetchall()
    st.write("**Distinct Event Types:**", event_types)

def count_rows(con, table_name):
    """Counts and displays the number of rows in the specified table."""
    Logger.info(f"Counting rows in {table_name}...")
    result = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()
    st.write("**Number of rows:**", result[0][0])

def count_unique_products(con, table_name):
    """Counts and displays the number of unique products in the specified table."""
    Logger.info(f"Counting unique products in {table_name}...")
    result = con.execute(f"SELECT COUNT(DISTINCT product_id) FROM {table_name}").fetchall()
    st.write("**Number of unique products:**", result[0][0])



def count_missing_values(con, table_name):
    """
    Counts missing (NULL) values in each column of a specified table.
    
    Parameters:
    con (duckdb.DuckDBPyConnection): The connection to the DuckDB database.
    table_name (str): The name of the table to check for missing values.
    
    """
    try:
        Logger.info(f"Counting missing values in {table_name}...")
        st.write(f"**Counting missing values in {table_name}...**")

        # Retrieve the list of columns from the table
        columns = con.execute(f"PRAGMA table_info({table_name});").fetchall()
        column_names = [column[1] for column in columns]  # column[1] is the name of the column

        # Construct a query to count NULLs across all columns in one go
        count_query = ", ".join([f"COUNT(CASE WHEN {col} IS NULL THEN 1 END) AS {col}_nulls" for col in column_names])
        full_query = f"SELECT {count_query} FROM {table_name};"

        # Execute the query
        result = con.execute(full_query).fetchdf()

      
        st.dataframe(result)

    except Exception as e:
        Logger.error(f"Error counting missing values in {table_name}: {e}")
        raise e

