from dataclasses import dataclass
import json

@dataclass
class BrandPerformanceTableNames:
    brands_performance_oct: str
    brands_performance_nov: str

@dataclass
class UserRetentionTableNames:
    user_retention_oct: str
    user_retention_nov: str

@dataclass
class BrandDatabases:
    october: str
    november: str
    table_names: BrandPerformanceTableNames

@dataclass
class UserRetentionDatabases:
    october: str
    november: str
    table_names: UserRetentionTableNames

@dataclass
class QueriesDbs:
    brands_performance: BrandDatabases
    user_retention: UserRetentionDatabases

@dataclass
class DatabaseConfig:
    october: str
    november: str

@dataclass
class TableNames:
    raw_data: str
    sales_data: str
    aggregated_sales: str

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
        
        # Brand Performance
        brand_performance_table_names = BrandPerformanceTableNames(**config_dict['queries_dbs']['brands_performance']['table_names'])
        brands_performance_dict = {k: v for k, v in config_dict['queries_dbs']['brands_performance'].items() if k != 'table_names'}
        brands_performance_dbs = BrandDatabases(**brands_performance_dict, table_names=brand_performance_table_names)
        
        # User Retention
        user_retention_table_names = UserRetentionTableNames(**config_dict['queries_dbs']['user_retention']['table_names'])
        user_retention_dict = {k: v for k, v in config_dict['queries_dbs']['user_retention'].items() if k != 'table_names'}
        user_retention_dbs = UserRetentionDatabases(**user_retention_dict, table_names=user_retention_table_names)
        
        queries_dbs = QueriesDbs(brands_performance=brands_performance_dbs, user_retention=user_retention_dbs)
        
        months = config_dict['months']

        return Config(data_paths=data_paths, table_names=table_names, queries_dbs=queries_dbs, months=months)

# Load the configuration once and use it across the application
config = load_config()
