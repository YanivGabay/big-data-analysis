from modules.create_visualization import show_aggregated_data

import streamlit as st
from modules.setup_runner import get_months

def show():
    st.title('Static Graphs')
    st.write('This section provides static graphs for the aggregated sales data.')

    show_aggregated_data(get_months())

