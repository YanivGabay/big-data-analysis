import streamlit as st

import duckdb
from modules.sqlite_manager import execute_query_to_df
from modules.config_loader import config

class AggregateSalesResult:

    def __init__(self, db_path,aggregate_sales_table_name,month):
        self.db_path = db_path
   
        self.aggregate_sales_table_name = aggregate_sales_table_name
        self.month = month
        self.df = self.fetch_aggregated_data()

    def show(self):
        try:
  
            st.subheader(f'Sales Data for {self.month}')
            st.dataframe(self.df)
        except Exception as e:
            st.error(f"Failed to display data: {e}")
            raise e

    def fetch_aggregated_data(self):
        try:
            query = f"SELECT * FROM {self.aggregate_sales_table_name}"
            df = execute_query_to_df(self.db_path, query)
            return df
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
            raise e
     


   

