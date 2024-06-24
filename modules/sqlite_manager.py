
import pandas as pd
import sqlite3
import os
from utils.logger import Logger


def save_to_sqlite(df, db_path, table_name):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure directory exists
    try:
        # if exists: 'fail’, ‘replace’, ‘append
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists='fail', index=False)
       
        Logger.info(f"Data saved to SQLite database at {db_path}")
    except ValueError as e:
        Logger.error(f"Error saving data to SQLite database: {str(e)}")
    except Exception as e:
        Logger.error(f"Error saving data to SQLite database: {str(e)}")
 

def execute_query_to_df(db_path, query):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql(query, conn)
        Logger.info(f"Query executed successfully on {db_path}")
        return df   
    except Exception as e:
        Logger.error(f"Error executing query on {db_path}: {str(e)}")
        return None
    finally:
        conn.close()