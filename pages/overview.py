# overview.py
import streamlit as st
import pandas as pd

from modules.config_loader import config
from modules.aggregate_sales_result import AggregateSalesResult
def show():
    st.title('Aggregated Sales Data')
  
    st.write("""
    ### Functionality Overview
    ##### 1. **Aggregate Sales Data**: Retrieves data from the DuckDB aggregated sales table for both October and November.
    ##### 2. **Display Data**: Displays the data in Streamlit using a DataFrame from a "result" class.

    """)
    aggregate_sales_oct = AggregateSalesResult(
    db_path=config.databases.aggregated_sales.october.db_path,
   
    aggregate_sales_table_name=config.table_names.aggregated_sales,
    month = 'October'
    )
    aggregate_sales_oct.show()

    aggregate_sales_nov = AggregateSalesResult(
    db_path=config.databases.aggregated_sales.november.db_path,

    aggregate_sales_table_name=config.table_names.aggregated_sales,
    month='November'
    )
    aggregate_sales_nov.show()
