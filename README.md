
# Ecommerce Big Data Analysis

## Yaniv Gabay 205745615

## Project Overview

This project focuses on analyzing ecommerce behavior data from a multi-categ
ory store. The dataset is sourced from Kaggle and includes user interactions over the month of October and November 2019.

## Dataset

The dataset used in this project can be found on Kaggle:
[ecommerce behavior data from multi-category store](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/data?select=2019-Oct.csv)

### How to Read the Data

- `event_time`: The time when the event happened.
- `event_type`: Actions (view, cart, purchase) performed by users.
- `product_id`: ID of the product.
- `category_code`: Category of the product.
- `brand`: Brand of the product.
- `price`: Price of the product.
- `user_id`: ID of the user.
- `user_session`: Session ID of the user interaction.

## Requirements

@requirements.txt

```bash
pip install -r requirements.txt
```

if you have some admin problems
you can use :

```bash
pip install -r requirements.txt --user
```

## Installation

To set up the project environment:

```bash
pip install -r requirements.txt
```

## Running the Project

If you want to download the csv and use this program please update to True in main.py:
@main.py / line 14

```python
LOAD_FROM_CSV = False  # Set to False to skip loading data from CSV files
```
If you want to show some basic test data on the console please update to True in main.py:
@main.py / line 15

```python
TEST_DUCKDB = False  # Set to True to test DuckDB queries
```

if you want console output please update to True in main.py:

```python
Logger.set_console_output(False)  # Set to True to enable console output
```

To run the the program:

```bash
streamlit run main.py
```

## Project Structure

- `.gitignore` (standard Python `.gitignore` file)
- `config.json` (configuration file for database paths and table names)
- `main.py` (main script to run the Streamlit app)
- `README.md` (this file)
- `requirements.txt` (list of Python dependencies)
- `TODO.md` (task list for the project)
- `.streamlit/`
- `e_commerce_uml.drawio` (UML diagram of the project)
  - `config.toml` (Streamlit configuration file)
- `data/` (directory containing the dataset CSV files)
  - `2019-Nov.csv`
  - `2019-Oct.csv`
- `db/` (directory containing the SQLite databases + DuckDB files)
  - `2019-nov.duckdb`
  - `2019-oct.duckdb`
  - `aggregated_sales/`
    - `2019-nov.db`
    - `2019-oct.db`
  - `brands/`
    - `2019-nov.db`
    - `2019-oct.db`
  - `sales_data/`
    - `2019-nov.db`
    - `2019-oct.db`
  - `shared_user_activity_by_hour/`
    - `2019-shared.db`
  - `spark/`
    - `ecommerce_data_spark.db`
  - `top_products/`
    - `2019-top-products.db`
  - `user_retention/`
    - `2019-nov.db`
    - `2019-oct.db`
- `db_limited_50(same dbs with limiting 50 rows)/`
  - `aggregated_sales/`
    - `2019-nov.db`
    - `2019-oct.db`
  - `brands/`
    - `2019-nov.db`
    - `2019-oct.db`
  - `sales_data/`
    - `2019-nov.db`
    - `2019-oct.db`
  - `shared_user_activity_by_hour/`
    - `2019-shared.db`
  - `spark/`
    - `ecommerce_data_spark.db`
  - `top_products/`
    - `2019-top-products.db`
  - `user_retention/`
    - `2019-nov.db`
    - `2019-oct.db`
- `modules/` (directory containing Python modules)
  - `aggregate_sales_result.py`
  - `analyze_data.py`
  - `config_loader.py`
  - `loader.py`
  - `page_data_manager.py`
  - `processor.py`
  - `setup_runner.py`
  - `sqlite_manager.py`
  - `tester.py`
  - `__init__.py`
- `pages/` (directory containing Streamlit pages)
  - `brand_performance.py`
  - `events_activities_by_hour.py`
  - `faker_spark_stats.py`
  - `overview.py`
  - `static_graphs.py`
  - `top_prods.py`
  - `user_retention.py`
- `Part-c/` (directory containing Part-c files)
  - `e_commerce_spark.ipynb`
  - `Graphdb.md`
  - `graph_db_query.md`
  - `image-1.png`
  - `image.png`
- `utils/` (directory containing utility scripts)
  - `db_minimizer.py`
  - `logger.py`


# Functional Modules Overview

## Configuration Loader (`config_loader.py`)

- **Purpose**: Manages the loading of configuration settings from `config.json`. This includes database paths, table names, and other crucial settings that need to be dynamically loaded across different modules.
- **Functionality**: Provides a central point for managing configurations which helps in maintaining and updating paths and settings in one place rather than hardcoding them across scripts.

## Data Loader (`loader.py`)

- **Purpose**: Responsible for loading data into the system, either from flat files (CSV) into duckdb.

## Data Processor (`processor.py`)

- **Purpose**: Creates the aggregated_sales,sales_data databases per month.
- **Functionality**: first query:
  
```sql
    SELECT 
        COUNT(*) AS total_events,
        SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
        SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS total_cart_additions,
        SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS total_views,
        AVG(price) AS average_price
    FROM {input_table_name}
    WHERE price IS NOT NULL;
```

second query:

```sql
    SELECT 
        user_id, 
        COUNT(*) AS total_events, 
        SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
        AVG(price) AS average_price
    FROM {input_table_name}
    WHERE price IS NOT NULL
    GROUP BY user_id;
```

## Data Analyzer (`analyze_data.py`)

- **Purpose**: Contain the "Main" queries, to be used in the more complex visualizations.
- **Functionality**: Can do two types of excutes, one as a single db, and the other as a multiple db, using attach. those queries are done on the "big" duck db files, and are saved if not already found as small sqlite databases.

## Data Tester (`tester.py`)

- **Purpose**: Some basic tests and information to check if the data is being loaded correctly.
- **Functionality**: runs some basic queries to check if the data is being loaded correctly, what missing values are there, and some basic information about the data.

## SQLite Manager (`sqlite_manager.py`)

- **Purpose**: Manages the SQLite database queries, and help convert df recieved from the duckdb to sqlite.

## Setup Runner (`setup_runner.py`)

- **Purpose**: Manages the setup of the databases, and the first loading of the data if created from scratch from the csv files.

## Aggregate Sales Result (`aggregate_sales_result.py`)

- **Purpose**: Class to manage and print the results of the aggregate sales query.

## Page Data Manager (`page_data_manager.py`)

- **Purpose**: Manages data specifically formatted for presentation on Streamlit pages.
- **Functionality**: Check for each page, if its "mini" sqlite database is already created, if not, create it, and then load the data to be used in the page.

## "Main" Analytical Queries 

The following are the main analytical queries used in the project, each one has its own function in the `analyze_data.py` module.
Those are the queries that are used as the base for the visualizations in the Streamlit pages.

```python

def top_prod_compare_query():
    query = """
        WITH OctoberSales AS (
        SELECT 
            product_id,
            COUNT(*) AS sales_count_oct,
            SUM(price) AS total_sales_oct
        FROM {table_name}
        WHERE event_type = 'purchase'
        GROUP BY product_id
        ),
        NovemberSales AS (
        SELECT 
            product_id,
            COUNT(*) AS sales_count_nov,
            SUM(price) AS total_sales_nov
        FROM db2.{table_name}
        WHERE event_type = 'purchase'
        GROUP BY product_id
        ),
        CombinedSales AS (
        SELECT
            o.product_id,
            COALESCE(o.sales_count_oct, 0) AS sales_count_oct,
            COALESCE(o.total_sales_oct, 0) AS total_sales_oct,
            COALESCE(n.sales_count_nov, 0) AS sales_count_nov,
            COALESCE(n.total_sales_nov, 0) AS total_sales_nov,
            (COALESCE(o.total_sales_oct, 0) + COALESCE(n.total_sales_nov, 0)) AS total_sales
        FROM OctoberSales o
        FULL OUTER JOIN NovemberSales n ON o.product_id = n.product_id
        )
        SELECT 
        product_id,
        sales_count_oct,
        total_sales_oct,
        sales_count_nov,
        total_sales_nov,
        total_sales
        FROM CombinedSales
        ORDER BY total_sales DESC
        

    """
    df_both = execute_cross_db_query(config.data_paths.october, config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    return df_both
```


```python
def activities_by_hour_query():
    query = """
    WITH hourly_activity_oct AS (
        SELECT 
            strftime('%H', event_time) AS hour,
            event_type,
            COUNT(*) AS event_count
        FROM {table_name}
        WHERE CAST(event_time AS DATE) BETWEEN '2019-10-01' AND '2019-10-31'
        GROUP BY strftime('%H', event_time), event_type
    ),
    hourly_activity_nov AS (
        SELECT 
            strftime('%H', event_time) AS hour,
            event_type,
            COUNT(*) AS event_count
        FROM db2.{table_name}  -- Use the alias for the November database
        WHERE CAST(event_time AS DATE) BETWEEN '2019-11-01' AND '2019-11-30'
        GROUP BY strftime('%H', event_time), event_type
    )
    SELECT 
        COALESCE(hourly_activity_oct.hour, hourly_activity_nov.hour) AS hour,
        COALESCE(hourly_activity_oct.event_type, hourly_activity_nov.event_type) AS event_type,
        COALESCE(hourly_activity_oct.event_count, 0) AS event_count_oct,
        COALESCE(hourly_activity_nov.event_count, 0) AS event_count_nov
    FROM 
        hourly_activity_oct
        FULL OUTER JOIN 
        hourly_activity_nov
        ON 
        hourly_activity_oct.hour = hourly_activity_nov.hour 
        AND hourly_activity_oct.event_type = hourly_activity_nov.event_type;
    """
    df_both = execute_cross_db_query(config.data_paths.october, config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    return df_both
```

```python
def brand_performance_query():
    query = """
    SELECT
        brand,
        SUM(price) AS total_sales,
        COUNT(*) AS total_purchases,
        AVG(price) AS average_price
    FROM
        {table_name}
    
    WHERE 
        event_type = 'purchase' AND
        brand IS NOT NULL
    GROUP BY
        brand

    ORDER BY
       total_sales DESC
  
    """
    df_nov = execute_query(config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    df_oct = execute_query(config.data_paths.october, query, params={'table_name': config.table_names.raw_data})

    return df_nov, df_oct
```

```python
def user_retention_query():
    query = """
    WITH First_Last_Activities AS (
        SELECT
            user_id,
            MIN(event_time) AS first_activity,
            MAX(event_time) AS last_activity,
            COUNT(*) AS total_events,
            SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchase_count
        FROM {table_name}
        GROUP BY user_id
    ),
    Retention_Analysis AS (
        SELECT
            user_id,
            DATEDIFF('days', first_activity, last_activity) AS retention_days, 
            purchase_count
        FROM First_Last_Activities
    )
    SELECT
        AVG(retention_days) AS avg_retention_days,
        COUNT(*) AS total_users,
        AVG(purchase_count) AS avg_purchase_frequency
    FROM Retention_Analysis
    WHERE retention_days > 0;

    """
    df_nov = execute_query(config.data_paths.november, query, params={'table_name': config.table_names.raw_data})
    df_oct = execute_query(config.data_paths.october, query, params={'table_name': config.table_names.raw_data})

    return df_nov, df_oct
```

### From the google collab notebook using spark

```python
# Window function query for Spark SQL
rolling_sales_summary_query = """
WITH DailySales AS (
    SELECT
        category_code,
        DATE(event_time) AS event_date,
        COUNT(*) AS daily_sales
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY category_code, DATE(event_time)
), AvgSales AS (
    SELECT
        category_code,
        event_date,
        daily_sales,
        AVG(daily_sales) OVER (PARTITION BY category_code ORDER BY event_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_last_7_days
    FROM DailySales
)
SELECT
    category_code,
    event_date,
    daily_sales,
    avg_last_7_days,
    (daily_sales - avg_last_7_days) AS diff_from_avg
FROM AvgSales
ORDER BY event_date, category_code;
"""

# Execute the query
sales_summary = spark.sql(rolling_sales_summary_query)
sales_summary.show()

# Optionally, convert to Pandas DataFrame for visualization
sales_summary_pd = sales_summary.toPandas()
```

## Streamlit Pages

The project includes the following Streamlit pages:
`brand_performance.py`
`events_activities_by_hour.py`
`overview.py`
`static_graphs.py`
`top_prods.py`
`user_retention.py`
`faker_spark_stats.py`

Each page is responsible for visualizing specific data insights and trends from the specified small sqlite database.

## Database Minimizer (`db_minimizer.py`)

we were asked to create a script that will minimize the size of the SQLite databases by limiting the number of rows in each table.

- **Purpose**: Minimizes the size of the SQLite databases by limiting the number of rows in each table.
- **Functionality**: The script walks through a specified source directory, finds all SQLite database files, and creates new database files in a target directory with a limited number of rows for each table.

## Part-c

- **Purpose**: Contains the Google Collab notebook using spark, and aswell the graphdb scheme.
- **Functionality**: The Google Collab notebook uses faker to create some data equivalent to the one we have, and then uses spark to analyze it, we save the processed data to a sqlite database, and then we can use it in the designated streamlit page.

