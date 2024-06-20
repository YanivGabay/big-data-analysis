from modules.loader import load_data
from modules.tester import test_data
from modules.loader import process_multiple_months
from modules.processor import aggregate_sales, process_data

def main():
    # Define the paths and parameters
    months = ['Oct', 'Nov']
    csv_file_path = 'data/2019-{month}.csv'

    data_base_path = 'db/2019-{month}.duckdb'

    table_name = 'raw_data'

    try:
        # Load data into DuckDB from CSV
        print("Loading data...")
        process_multiple_months(months)

        # Test data
        for month in months:
            print(f"Testing data for {month}...")
            db_path = data_base_path.format(month=month.lower())
            test_data(db_path, table_name)
  
        # Process data
       
        for month in months:
            print(f"Processing data for {month}...")
            db_path = data_base_path.format(month=month.lower())
            process_data(db_path, table_name, 'sales_data')
            aggregate_sales(db_path, table_name)
        
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
