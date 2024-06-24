import duckdb
import pandas as pd
import sqlite3
from modules.config_loader import config

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


    


def brand_performance_query():
    query = """
    SELECT
        brand,
        SUM(price) AS total_sales,
        COUNT(*) AS total_purchases,
        AVG(price) AS average_price
    FROM
        {table_name}
    
    WHERE 
        event_type = 'purchase' AND
        brand IS NOT NULL
    GROUP BY
        brand

    ORDER BY
       total_sales DESC
  
    """
    df_nov = execute_query(config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    df_oct = execute_query(config.data_paths.october, query, params={'table_name': config.table_names.raw_data})

    return df_nov, df_oct

def user_retention_query():
    query = """
    WITH First_Last_Activities AS (
        SELECT
            user_id,
            MIN(event_time) AS first_activity,
            MAX(event_time) AS last_activity,
            COUNT(*) AS total_events,
            SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchase_count
        FROM {table_name}
        GROUP BY user_id
    ),
    Retention_Analysis AS (
        SELECT
            user_id,
            DATEDIFF('days', first_activity, last_activity) AS retention_days, 
            purchase_count
        FROM First_Last_Activities
    )
    SELECT
        AVG(retention_days) AS avg_retention_days,
        COUNT(*) AS total_users,
        AVG(purchase_count) AS avg_purchase_frequency
    FROM Retention_Analysis
    WHERE retention_days > 0;

    """
    df_nov = execute_query(config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    df_oct = execute_query(config.data_paths.october, query, params={'table_name': config.table_names.raw_data})

    return df_nov, df_oct


