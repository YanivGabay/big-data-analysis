# overview.py
import streamlit as st
import pandas as pd
from modules.create_visualization import show_aggregated_data
from modules.config_loader import config

def show():
    st.title('Overview')
    st.write('Some general information about the data and the dashboard.')

    show_aggregated_data(config.months)
  
