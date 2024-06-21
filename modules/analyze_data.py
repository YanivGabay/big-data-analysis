import duckdb
import pandas as pd
import sqlite3


# at this point we have these tables in the duckdb databases:
# - config.table_names.raw_data
# - config.table_names.sales_data
# - config.table_names.aggregated_sales
# @config.json


def execute_query(db_path, query, params=None):
    """Executes a given SQL query on a specified DuckDB database."""
    try:
        con = duckdb.connect(database=db_path)
        if params:
            query = query.format(**params)  # Format query with additional parameters if provided
        df = con.execute(query).df()
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        con.close()


def execute_cross_db_query(db_path1, db_path2, query,params=None):
    try:
        con = duckdb.connect(database=db_path1)  # Connect to the primary database
        con.execute(f"ATTACH '{db_path2}' AS db2")  # Attach the second database as 'db2'
        
        query = query.format(**params) if params else query  # Format the query with additional parameters if provided
        df = con.execute(query).df()
        return df
    except Exception as e:
        print(f"Failed to execute cross-database query: {e}")
        raise
    finally:
        con.close()


def save_df_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str):
    """Saves a DataFrame to an SQLite database."""
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data saved to {db_path} in table {table_name}")
    except Exception as e:
        print(f"Failed to save data to SQLite: {e}")
        raise






