

from utils.logger import Logger
import os
import streamlit as st
import sqlite3



class PageDataManager:
    
    def check_db_exists(db_path):

        if(os.path.exists(db_path)):
            Logger.info('Data already exists, skipping setup')
            return True
        return False
    
    
    def get_state(state_name):
        if f'{state_name}_data' not in st.session_state:
            Logger.info(f"Setting up {state_name} data...")
            return False
        return True
    
    def setup(db_path_as_state,setup_data_func):
        if PageDataManager.get_state(db_path_as_state):
            return
        if PageDataManager.check_db_exists(db_path_as_state):
            return
        
        setup_data_func()
        st.session_state[f'{db_path_as_state}_data'] = True
        Logger.info(f"{db_path_as_state} data setup completed.")