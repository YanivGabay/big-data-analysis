import os
import sqlite3
import pandas as pd

def limit_db_rows(source_dir, target_dir, max_rows=50):
    # Ensure the target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Traverse the source directory and its subdirectories
    for subdir, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".db"):  # Process only database files
                source_path = os.path.join(subdir, file)
                # Create a corresponding structure in the target directory
                relative_path = os.path.relpath(subdir, source_dir)
                target_subdir = os.path.join(target_dir, relative_path)
                if not os.path.exists(target_subdir):
                    os.makedirs(target_subdir)
                target_path = os.path.join(target_subdir, file)

                # Connect to the source database
                conn_src = sqlite3.connect(source_path)
                cursor_src = conn_src.cursor()

                # Retrieve all table names from the source database
                cursor_src.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor_src.fetchall()

                # Connect to the target database (creates new if not existing)
                conn_target = sqlite3.connect(target_path)

                # For each table, read up to max_rows rows and write to the target database
                for table_name, in tables:
                    df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT {max_rows}", conn_src)
                    df.to_sql(table_name, conn_target, if_exists='replace', index=False)

                # Close both connections
                conn_src.close()
                conn_target.close()

                print(f"Processed {file} with limited rows into {target_path}")

# Example usage
source_directory = 'db/'
target_directory = 'db_limited_50/'
limit_db_rows(source_directory, target_directory)
