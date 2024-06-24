
# Ecommerce Big Data Analysis

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

## Project Structure


```
Ecommerce_Big_Data_Analysis/
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/            # Contains the datasets
│   ├── 2019-Nov.csv - 
│   └── 2019-Oct.csv - 
├── db/         # Contains the SQLite and Duckdb databases
│   ├── 2019-nov.duckdb
│   ├── 2019-oct.duckdb
│   ├── aggregated_sales/
│   ├── brands/
│   ├── sales_data/
│   ├── shared_user_activity_by_hour/
│   ├── top_products/
│   └── user_retention/
├── modules/  
│   ├── __init__.py
│   ├── aggregate_sales_result.py
│   ├── analyze_data.py
│   ├── config_loader.py
│   ├── loader.py
│   ├── processor.py
│   ├── setup_runner.py
│   ├── sqlite_manager.py
│   └── tester.py
    └── page_data_manager.py
├── pages/      # Contains the Streamlit pages
│   ├── brand_performance.py
│   ├── events_activities_by_hour.py
│   ├── overview.py
│   ├── static_graphs.py
│   ├── top_prods.py
│   └── user_retention.py
├── utils/      
│   └── logger.py
├── config.json      # Contains the configuration settings, filepaths etc.
├── main.py
├── README.md
├── requirements.txt

```

## Analytical Queries on Brands




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

To run the main analysis:

```bash
streamlit run main.py
```


