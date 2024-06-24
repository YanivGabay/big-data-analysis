import duckdb
import pandas as pd
import sqlite3
from modules.config_loader import config
from utils.logger import Logger
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
        Logger.info(f"Executing cross-database query on {db_path1} and {db_path2}")
        con = duckdb.connect(database=db_path1)  # Connect to the primary database
        con.execute(f"ATTACH '{db_path2}' AS db2")  # Attach the second database as 'db2'
        
        query = query.format(**params) if params else query  # Format the query with additional parameters if provided
        df = con.execute(query).df()
        Logger.info("Cross-database query executed successfully.")
        con.execute("DETACH db2")  # Detach the second database
        return df
    except Exception as e:
        print(f"Failed to execute cross-database query: {e}")
        raise
    finally:
        con.close()

def top_prod_compare_query():
    query = """
        WITH OctoberSales AS (
        SELECT 
            product_id,
            COUNT(*) AS sales_count_oct,
            SUM(price) AS total_sales_oct
        FROM {table_name}
        WHERE event_type = 'purchase'
        GROUP BY product_id
        ),
        NovemberSales AS (
        SELECT 
            product_id,
            COUNT(*) AS sales_count_nov,
            SUM(price) AS total_sales_nov
        FROM db2.{table_name}
        WHERE event_type = 'purchase'
        GROUP BY product_id
        ),
        CombinedSales AS (
        SELECT
            o.product_id,
            COALESCE(o.sales_count_oct, 0) AS sales_count_oct,
            COALESCE(o.total_sales_oct, 0) AS total_sales_oct,
            COALESCE(n.sales_count_nov, 0) AS sales_count_nov,
            COALESCE(n.total_sales_nov, 0) AS total_sales_nov,
            (COALESCE(o.total_sales_oct, 0) + COALESCE(n.total_sales_nov, 0)) AS total_sales
        FROM OctoberSales o
        FULL OUTER JOIN NovemberSales n ON o.product_id = n.product_id
        )
        SELECT 
        product_id,
        sales_count_oct,
        total_sales_oct,
        sales_count_nov,
        total_sales_nov,
        total_sales
        FROM CombinedSales
        ORDER BY total_sales DESC
        LIMIT 100;

    """
    df_both = execute_cross_db_query(config.data_paths.october, config.data_paths.november, query, params={'table_name_oct': config.table_names.raw_data, 'table_name_nov': config.table_names.raw_data})
    return df_both

def activities_by_hour_query():
    query = """
    WITH hourly_activity_oct AS (
        SELECT 
            strftime('%H', event_time) AS hour,
            event_type,
            COUNT(*) AS event_count
        FROM {table_name}
        WHERE CAST(event_time AS DATE) BETWEEN '2019-10-01' AND '2019-10-31'
        GROUP BY strftime('%H', event_time), event_type
    ),
    hourly_activity_nov AS (
        SELECT 
            strftime('%H', event_time) AS hour,
            event_type,
            COUNT(*) AS event_count
        FROM db2.{table_name}  -- Use the alias for the November database
        WHERE CAST(event_time AS DATE) BETWEEN '2019-11-01' AND '2019-11-30'
        GROUP BY strftime('%H', event_time), event_type
    )
    SELECT 
        COALESCE(hourly_activity_oct.hour, hourly_activity_nov.hour) AS hour,
        COALESCE(hourly_activity_oct.event_type, hourly_activity_nov.event_type) AS event_type,
        COALESCE(hourly_activity_oct.event_count, 0) AS event_count_oct,
        COALESCE(hourly_activity_nov.event_count, 0) AS event_count_nov
    FROM 
        hourly_activity_oct
        FULL OUTER JOIN 
        hourly_activity_nov
        ON 
        hourly_activity_oct.hour = hourly_activity_nov.hour 
        AND hourly_activity_oct.event_type = hourly_activity_nov.event_type;
    """
    df_both = execute_cross_db_query(config.data_paths.october, config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    return df_both

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


