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

plt.style.use('ggplot')
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
```python             
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
```
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
    avg_daily_sales_per_category(df)

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
    st.write("""
    This chart shows the cumulative sales by category on a monthly basis. It helps to understand the overall growth
    of sales over time for each category. The x-axis represents the months, and the y-axis represents the cumulative sales.
    """)

    selected_categories = st.multiselect('Select categories to display (Cumulative Sales)', df['category_code'].unique(), default=df['category_code'].unique(), key='cumulative_sales_multiselect')
    plot_cumulative_sales_by_categ(df[df['category_code'].isin(selected_categories)])


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
    st.write("""
    This chart shows the monthly sales by category using a stacked area chart. It allows you to see the contribution
    of each category to the total sales over time. The x-axis represents the months, and the y-axis represents the sales.
    """)
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
    selected_categories = st.multiselect('Select categories to display (Area Chart)', df['category_code'].unique(), default=df['category_code'].unique(), key='area_chart_multiselect')
    plot_area_chart(df[df['category_code'].isin(selected_categories)])



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



def avg_daily_sales_per_category(df):
    query = f"""
    SELECT
        category_code,
        strftime('%Y-%m', event_date) AS month,
        AVG(daily_sales) AS avg_daily_sales
    FROM {table_name}
    GROUP BY category_code, month
    ORDER BY month, category_code;
    """
    df = execute_query_to_df(db_full_path, query)
    st.write('### Average Daily Sales by Category (Monthly)')
    st.write("""
    This chart shows the average daily sales by category on a monthly basis. It helps to understand the sales trends
    over time for each category. The x-axis represents the months, and the y-axis represents the average daily sales.
    """)

    selected_categories = st.multiselect('Select categories to display (Average Daily Sales)', df['category_code'].unique(), default=df['category_code'].unique(), key='avg_daily_sales_multiselect')
    plot_avg_daily_sales_per_category(df[df['category_code'].isin(selected_categories)])


def plot_avg_daily_sales_per_category(df):
    plt.figure(figsize=(10, 5))
    for category, group in df.groupby('category_code'):
        sns.lineplot(data=group, x='month', y='avg_daily_sales', label=f'Category {category}')
    plt.title('Average Daily Sales by Category (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Average Daily Sales')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
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
  
    