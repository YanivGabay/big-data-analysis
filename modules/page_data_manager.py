

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
    
    
    def get_state(page_name):
        if f'{page_name}_data' not in st.session_state:
            Logger.info(f"Setting up {page_name} data...")
            return False
        return True
    