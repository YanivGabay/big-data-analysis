
import pandas as pd
import sqlite3
import os
from utils.logger import Logger


def save_to_sqlite(df, db_path, table_name):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure directory exists
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        Logger.info(f"Data saved to SQLite database at {db_path}")
    except Exception as e:
        Logger.error(f"Error saving data to SQLite database: {str(e)}")