import streamlit as st

import duckdb
from modules.analyze_data import execute_query
from modules.config_loader import config

class AggregateSalesResult:

    def __init__(self, db_path, table_name, aggregate_sales_table_name,month):
        self.db_path = db_path
        self.table_name = table_name
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
            df = execute_query(self.db_path, query)
            return df
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
            raise e
     


   

