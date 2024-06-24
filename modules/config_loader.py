from dataclasses import dataclass
import json
from dataclasses import dataclass

@dataclass
class DatabasePaths:
    october: str
    november: str

@dataclass
class TableNames:
    raw_data: str
    sales_data: str
    aggregated_sales: str

@dataclass
class DatabaseDetails:
    db_path: str
    table_name: str

@dataclass
class BrandPerformance:
    october: DatabaseDetails
    november: DatabaseDetails

@dataclass
class TopProds:
    db_path: str
    table_name: str

@dataclass
class UserRetention:
    october: DatabaseDetails
    november: DatabaseDetails

@dataclass
class SharedUserActivityByHour:
    db_path: str
    table_name: str

@dataclass
class Databases:
    brands_performance: BrandPerformance
    user_retention: UserRetention
    shared_user_activity_by_hour: SharedUserActivityByHour
    top_products: TopProds

@dataclass
class Config:
    data_paths: DatabasePaths
    table_names: TableNames
    databases: Databases
    months: list




def load_config(config_path: str = 'config.json') -> Config:
    with open(config_path, 'r') as file:
        config_dict = json.load(file)
    return Config(
        data_paths=DatabasePaths(**config_dict['data_paths']),
        table_names=TableNames(**config_dict['table_names']),
        databases=Databases(
            brands_performance=BrandPerformance(
                october=DatabaseDetails(**config_dict['databases']['brands_performance']['october']),
                november=DatabaseDetails(**config_dict['databases']['brands_performance']['november'])
            ),
            user_retention=UserRetention(
                october=DatabaseDetails(**config_dict['databases']['user_retention']['october']),
                november=DatabaseDetails(**config_dict['databases']['user_retention']['november'])
            ),
            shared_user_activity_by_hour=SharedUserActivityByHour(**config_dict['databases']['shared_user_activity_by_hour']),
            top_products=TopProds(**config_dict['databases']['top_products'])
        ),
        months=config_dict['months']
    )


# Load the configuration once and use it across the application
config = load_config()
