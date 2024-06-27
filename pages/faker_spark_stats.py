from modules.page_data_manager import PageDataManager
import streamlit as st
from utils.logger import Logger
from modules.sqlite_manager import execute_query_to_df
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

db_path = f"ecommerce_data_spark.db"
db_full_path = f"db/spark/{db_path}"
max_rows = 50
table_name = 'sales_summary'

def show():
    PageDataManager.setup(db_full_path, setup_data)
    


    st.write("""
             
    ## Using Apache Spark, PySpark in Google Colab, we used faker to generate fake data based on the schema of the original data.
             
- `event_time`: The time when the event happened.
- `event_type`: Actions (view, cart, purchase) performed by users.
- `product_id`: ID of the product.
- `category_code`: Category of the product.
- `brand`: Brand of the product.
- `price`: Price of the product.
- `user_id`: ID of the user.
- `user_session`: Session ID of the user interaction.
             
Spark "fake" data schema:
             
schema = T.StructType([
    T.StructField("user_id", T.IntegerType(), True),
    T.StructField("product_id", T.IntegerType(), True),
    T.StructField("event_type", T.StringType(), True),
    T.StructField("price", T.IntegerType(), True),
    T.StructField("event_time", T.TimestampType(), True),
    T.StructField("category_code", T.StringType(), True),
    T.StructField("brand", T.StringType(), True),
    T.StructField("user_session", T.StringType(), True)
])
The only difference is we had two dataset per month, October and November, while
             In our fake data we generate:  fake.date_time_this_year(),  # event_time
             so basicly till today.
          
             
             """)

    faker_spark_stats()


def faker_spark_stats():
    st.title('Fake Data Analysis')
    st.write('This section provides a dynamic and interactive overview of the data generated using Faker and Spark.')

    non_query_graphs(load_fake_spark_query(db_full_path,table_name))

def setup_data():
    
    st.write("""Problem, the SQLite from Spark database is not available you should get it from the 
             Google Colab notebook, where we generated the fake data , and download it at the end of the script""")
    
    raise Exception(f"SQLite database not found at {db_full_path}")
    
def non_query_graphs(df):
    cumulative_sales_by_categ(df)
    area_chart(df)
    

def cumulative_sales_by_categ(df):
    query = f"""
SELECT
    category_code,
    strftime('%Y-%m', event_date) AS month,
    SUM(daily_sales) AS monthly_sales,
    SUM(SUM(daily_sales)) OVER (PARTITION BY category_code ORDER BY strftime('%Y-%m', event_date)) AS cumulative_sales
FROM {table_name}
GROUP BY category_code, month
ORDER BY month, category_code;



"""
    df = execute_query_to_df(db_full_path, query)
    st.write('### Cumulative Sales by Category (Monthly)')
    plot_cumulative_sales_by_categ(df)
   

   
def plot_cumulative_sales_by_categ(df):
    plt.figure(figsize=(10, 5))
    for category, group in df.groupby('category_code'):
        plt.plot(group['month'], group['cumulative_sales'], label=f'Category {category}')
    plt.title('Cumulative Sales by Category (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Cumulative Sales')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())  # Use plt.gcf() to get the current figure in Streamlit
    plt.close()
    
def area_chart(df):
    st.write('### Area Chart')

    query = f"""
    SELECT
    category_code,
    strftime('%Y-%m', event_date) AS month,
    SUM(daily_sales) AS monthly_sales
FROM {table_name}
GROUP BY category_code, month
ORDER BY month, category_code;
"""
    df = execute_query_to_df(db_full_path, query)
    plot_area_chart(df)

def plot_area_chart(df):
   
    df_pivot = df.pivot(index='month', columns='category_code', values='monthly_sales').fillna(0)
    df_pivot.plot(kind='area', stacked=True, figsize=(10, 5))
    plt.title('Stacked Area Chart of Monthly Sales by Category')
    plt.xlabel('Month')
    plt.ylabel('Monthly Sales')
    plt.xticks(rotation=45)
    plt.legend(title='Category')
    st.pyplot(plt.gcf())  # Use plt.gcf() to get the current figure in Streamlit
    plt.close()


def load_fake_spark_query(sqlite_db_path,table_name):

    query = f"""
   SELECT
        category_code,
        event_date,
        daily_sales,
        avg_last_7_days,
        (daily_sales - avg_last_7_days) AS diff_from_avg
    FROM {table_name}
    ORDER BY event_date, category_code;
  
    """
    df = execute_query_to_df(sqlite_db_path, query)
    st.write(f"Loaded {len(df)} rows from {table_name} table.")
    st.dataframe(df.head(max_rows))

    return df
  
    