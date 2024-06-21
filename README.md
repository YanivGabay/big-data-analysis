
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
big_data_project/
├── data/
├── db/
├── modules/
│   ├── __init__.py
│   ├── loader.py         # For loading data into the system
│   ├── processor.py      # For processing and preparing data
│   ├── analyzer.py       # For performing data analysis
│   ├── tester.py         # For testing data quality and integrity
│   └── visualizer.py     # For creating visualizations
├── utils/
│   ├── __init__.py
│   └── logger.py         # Utility for logging events
├── main.py               # Main script to run analyses
└── requirements.txt      # Required Python packages
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


