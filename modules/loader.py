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

def load_data(csv_file_path, db_path, table_name='raw_data', auto_detect=True):
    """
    Loads data from a CSV file into DuckDB, checking if the table already exists.
    """
    try:
        with duckdb.connect(database=db_path) as con:
            if not table_exists(con, table_name):
                query = f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file_path}')" if auto_detect else f"CREATE TABLE {table_name} AS SELECT * FROM read_csv('{csv_file_path}')"
                con.execute(query)
                print(f"Table {table_name} created and data loaded into {db_path}.")
            else:
                print(f"Table {table_name} already exists in {db_path}. No data loaded.")
    except Exception as e:
        print(f"Failed to load data from {csv_file_path} to {db_path}: {e}")
        raise e

def process_multiple_months(months):
    """
    Processes multiple months and loads data into separate DuckDB instances.
    """
    base_csv_path = 'data/2019-{month}.csv'
    base_db_path = 'db/2019-{month}.duckdb'
    table_name = 'raw_data'

    for month in months:
        csv_file_path = base_csv_path.format(month=month)
        db_path = base_db_path.format(month=month.lower())
        print(f"Processing month: {month}")
        load_data(csv_file_path, db_path, table_name)