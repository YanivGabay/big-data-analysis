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
class AggregateSales:
    october: DatabaseDetails
    november: DatabaseDetails

@dataclass
class UserAggSales:
    october: DatabaseDetails
    november: DatabaseDetails

@dataclass
class Databases:
    brands_performance: BrandPerformance
    user_retention: UserRetention
    shared_user_activity_by_hour: SharedUserActivityByHour
    top_products: TopProds
    aggregated_sales: AggregateSales
    sales_data: UserAggSales

@dataclass
class Config:
    data_paths: DatabasePaths
    table_names: TableNames
    databases: Databases
    months: list

    def get_sales_data_table_name():
        return config.table_names.sales_data

    def get_aggregate_sales_table_name():
        return config.table_names.aggregated_sales

    def get_data_base_path(month):
        return config.data_paths.october if month == 'Oct' else config.data_paths.november

    def get_sales_data_path(month):
        return config.databases.sales_data.october.db_path if month == 'Oct' else config.databases.sales_data.november.db_path

    def get_agg_data_path(month):
        return config.databases.aggregated_sales.october.db_path if month == 'Oct' else config.databases.aggregated_sales.november.db_path

    def get_months(self):
        return self.months



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
            top_products=TopProds(**config_dict['databases']['top_products']),
            aggregated_sales=AggregateSales(
                october=DatabaseDetails(**config_dict['databases']['aggregated_sales']['october']),
                november=DatabaseDetails(**config_dict['databases']['aggregated_sales']['november'])
            ),
            sales_data=UserAggSales(
                october=DatabaseDetails(**config_dict['databases']['sales_data']['october']),
                november=DatabaseDetails(**config_dict['databases']['sales_data']['november'])
            )

        ),
        months=config_dict['months']
    )


# Load the configuration once and use it across the application
config = load_config()
