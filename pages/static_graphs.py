from modules.create_visualization import show_aggregated_data
from modules.analyze_data import brand_performance_query
import streamlit as st
from modules.setup_runner import get_months
import plotly.graph_objects as go
import sqlite3
from modules.config_loader import config
import pandas as pd
import os

from utils.logger import Logger

def show():
    st.title('Static Graphs')
    st.write('This section provides static graphs for the aggregated sales data.')

   
