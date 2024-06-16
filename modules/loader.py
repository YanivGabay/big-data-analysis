import duckdb

def table_exists(con, table_name):
    """
    Check if a table exists in the DuckDB database.
    Parameters:
    con (duckdb.DuckDBPyConnection): The connection to the database.
    table_name (str): The name of the table to check.
    Returns:
    bool: True if the table exists, False otherwise.
    """
    try:
        result = con.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');").fetchall()
        return result[0][0]
    except Exception as e:
        print(f"Error checking if table exists: {e}")
        return False  # Assume table doesn't exist if there's an error

def load_data(csv_file_path, db_path='db/my_database.duckdb', table_name='raw_data', auto_detect=True, delimiter=',', header=True):
    """
    Loads data from a CSV file into DuckDB, checking if the table already exists.
    Parameters:
    csv_file_path (str): The file path of the CSV to load.
    db_path (str): The DuckDB database file path.
    table_name (str): The name of the table to create from the CSV data.
    auto_detect (bool): Whether to use auto-detection for CSV format.
    delimiter (str): The column delimiter (used if auto_detect is False).
    header (bool): Indicates if the first row in CSV is a header (used if auto_detect is False).
    """
    try:
        with duckdb.connect(database=db_path) as con:
            if not table_exists(con, table_name):
                if auto_detect:
                    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file_path}')")
                else:
                    con.execute(f"""
                        CREATE TABLE {table_name} AS 
                        SELECT * 
                        FROM read_csv('{csv_file_path}', delimiter='{delimiter}', header={header})
                    """)
                print(f"Table {table_name} created and data loaded.")
            else:
                print(f"Table {table_name} already exists. No data loaded.")
    except Exception as e:
        print(f"Failed to load data: {e}")
        raise e
