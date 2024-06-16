from modules.loader import load_data, check_data
from modules.processor import process_data
from modules.analyzer import analyze_data
from modules.visualizer import create_visualization

def main():
    # Define the paths and parameters
    csv_file_path = 'data/large_file.csv'
    db_path = 'db/my_database.duckdb'
    table_name = 'my_table'

    # Load data into DuckDB from CSV
    print("Loading data...")
    load_data(csv_file_path, db_path, table_name)

    # Process data
    print("Processing data...")
    process_data(db_path, table_name)

    # Analyze data
    print("Analyzing data...")
    query = "SELECT * FROM processed_data LIMIT 10"  # Modify query as needed
    analysis_results = analyze_data(db_path, query)

    # Visualize data
    print("Visualizing results...")
    create_visualization(analysis_results)

    # Optionally, display check data (for debugging)
    print("Checking loaded data...")
    print(check_data(db_path, table_name))

if __name__ == '__main__':
    main()
