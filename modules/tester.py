
import duckdb



def test_data(db_path, table_name):
    try:
        con = duckdb.connect(db_path)
        count_rows(con, table_name)
        
        print_some_data(con, table_name)
        describe_table(con, table_name)

       
        check_categorical_data(con, table_name)
        count_missing_values(con, table_name)

        count_unique_products(con, table_name)
        
        print("Test completed. \n")
    finally:
        con.close()

def print_some_data(con, table_name):
    print_to(f"Printing some data from {table_name}...")
   
    query = f"SELECT * FROM {table_name} LIMIT 10"
    result = con.execute(query).fetchdf()
    print(result)
    


def describe_table(con,table_name):
    print_to(f"Describing table {table_name}...")
    result = con.execute(f"DESCRIBE {table_name}").fetchdf()
    print(result)



def print_to(string):
    print("-"*50)
    print(string)
    print("-"*50)


def check_categorical_data(con,table_name):
    print_to("Checking for unexpected values in the event type...")

    event_types = con.execute(f"SELECT DISTINCT event_type FROM {table_name} WHERE event_type IS NOT NULL").fetchall()
    print("Event Types:", event_types)
    # Similar checks can be done for 'category_code' and 'brand'

def count_rows(con,table_name):
    print_to(f"Counting rows in {table_name}...")
    result = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()
    print("Number of rows:", result[0][0])

def count_unique_products(con,table_name):
    print_to(f"Counting unique products in {table_name}...")
    result = con.execute(f"SELECT COUNT(DISTINCT product_id) FROM {table_name}").fetchall()
    print("Number of unique products:", result[0][0])



def count_missing_values(con, table_name):
    """
    Counts missing (NULL) values in each column of a specified table.
    
    Parameters:
    con (duckdb.DuckDBPyConnection): The connection to the DuckDB database.
    table_name (str): The name of the table to check for missing values.
    
    Returns:
    A dictionary with column names as keys and the count of missing values as values.
    """
    missing_counts = {}
    try:
        print_to(f"Counting missing values in {table_name}...")
        # Retrieve the list of columns from the table
        columns = con.execute(f"PRAGMA table_info({table_name});").fetchall()
        column_names = [column[1] for column in columns]  # column[1] is the name of the column

        # Count missing values for each column
        for column_name in column_names:
            result = con.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL;").fetchall()
            missing_counts[column_name] = result[0][0]  # result[0][0] is the count of NULL values

        print("Missing values per column:")
        for col, count in missing_counts.items():
            print(f"{col}: {count}")

    except Exception as e:
        print(f"Error counting missing values in {table_name}: {e}")
        raise e

    #return missing_counts
