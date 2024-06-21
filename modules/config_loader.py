from dataclasses import dataclass
import json

# Define your data class for the queries' database paths
@dataclass
class BrandPerformanceTableNames:
    brands_performance_oct: str
    brands_performance_nov: str

@dataclass
class BrandDatabases:
    october: str
    november: str
    table_names: BrandPerformanceTableNames

# Define your data class for all queries' databases
@dataclass
class QueriesDbs:
    brands_performance: BrandDatabases

# Define your data classes for other configurations
@dataclass
class DatabaseConfig:
    october: str
    november: str

@dataclass
class TableNames:
    raw_data: str
    sales_data: str
    aggregated_sales: str

# Define a top-level configuration data class that includes everything
@dataclass
class Config:
    data_paths: DatabaseConfig
    table_names: TableNames
    queries_dbs: QueriesDbs
    months: list

def load_config(config_path: str = 'config.json') -> Config:
    with open(config_path, 'r') as file:
        config_dict = json.load(file)
        
        data_paths = DatabaseConfig(**config_dict['data_paths'])
        table_names = TableNames(**config_dict['table_names'])
        
        # Extract table names separately
        brand_performance_table_names = BrandPerformanceTableNames(**config_dict['queries_dbs']['brands_performance']['table_names'])
        
        # Exclude table names from the dictionary before passing it to BrandDatabases
        brands_performance_dict = {k: v for k, v in config_dict['queries_dbs']['brands_performance'].items() if k != 'table_names'}
        brands_performance_dbs = BrandDatabases(**brands_performance_dict, table_names=brand_performance_table_names)
        
        queries_dbs = QueriesDbs(brands_performance=brands_performance_dbs)
        
        months = config_dict['months']

        return Config(data_paths=data_paths, table_names=table_names, queries_dbs=queries_dbs, months=months)

# Load the configuration once and use it across the application
config = load_config()
