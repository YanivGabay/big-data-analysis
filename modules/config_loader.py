from dataclasses import dataclass
import json
from dataclasses import dataclass
{
    "data_paths": {
        "october": "db/2019-oct.duckdb",
        "november": "db/2019-nov.duckdb"
    },
    "table_names": {
        "raw_data": "raw_data",
        "sales_data": "sales_data",
        "aggregated_sales": "aggregated_sales"
    },
    "databases": {
        "brands_performance": {
            "october": {
                "db_path": "db/brands/2019-oct.db",
                "table_name": "brands_performance_oct"
            },
            "november": {
                "db_path": "db/brands/2019-nov.db",
                "table_name": "brands_performance_nov"
            }
        },
        "user_retention": {
            "october": {
                "db_path": "db/user_retention/2019-oct.db",
                "table_name": "user_retention_oct"
            },
            "november": {
                "db_path": "db/user_retention/2019-nov.db",
                "table_name": "user_retention_nov"
            }
        },
        "shared_user_activity_by_hour": {
            "db_path": "db/shared_user_activity_by_hour/2019-shared.db",
            "table_name": "shared_user_activity_by_hour_nov"
           
        }
    },
    "months": ["Oct", "Nov"]
}

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
            shared_user_activity_by_hour=SharedUserActivityByHour(**config_dict['databases']['shared_user_activity_by_hour'])
        ),
        months=config_dict['months']
    )


# Load the configuration once and use it across the application
config = load_config()
