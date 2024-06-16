from modules.loader import load_data


def main():
    # Define the paths and parameters
    csv_file_path = 'data/large_file.csv'
    db_path = 'db/my_database.duckdb'
    table_name = 'raw_data'

    try:
        # Load data into DuckDB from CSV
        print("Loading data...")
        load_data(csv_file_path, db_path, table_name, auto_detect=True)  # Assuming auto_detect feature

        # Process data
        print("Processing data...")
        processed_table_name = 'processed_data'  # Define processed table name
        process_data(db_path, table_name, processed_table_name)

        # Analyze data
        print("Analyzing data...")
        query = "SELECT * FROM processed_data LIMIT 10"  
        analysis_results = analyze_data(db_path, query)

        # Visualize data
        print("Visualizing results...")
        create_visualization(analysis_results)

       
        print("Checking loaded data...")
        if check_data(db_path, table_name):  # Check if the raw table exists
            print("Data check passed: Table exists.")
        else:
            print("Data check failed: Table does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
