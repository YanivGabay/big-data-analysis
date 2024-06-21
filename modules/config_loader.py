from dataclasses import dataclass
import json

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

def load_config(config_path: str = 'config.json') -> Config:
    with open(config_path, 'r') as file:
        config_dict = json.load(file)
        data_paths = DatabaseConfig(**config_dict['data_paths'])
        table_names = TableNames(**config_dict['table_names'])
        return Config(data_paths=data_paths, table_names=table_names)

# Load the configuration once and use it across the application
config = load_config()