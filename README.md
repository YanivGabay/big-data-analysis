
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

This project aims to understand brand performance within the ecommerce platform. Here are the key questions addressed through our analysis:

1. **Brand Performance Comparison**: How do different brands perform month-over-month in terms of sales and customer purchases?

2. **Seasonal Impact on Brands**: How do brand sales compare between the months of October and November?

3. **Brand Popularity**: Which brands are the most popular among users?

4. **User Engagement and Behavior Analysis**: this will explore a couple of things:
   - session duration
   - session frequency
   - num of purchaes per user
   - avg spending per session

## Requirements

@requirements.txt

```bash
pip install -r requirements.txt
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


