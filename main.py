
from pages import overview, interactive, static_graphs
import streamlit as st

from modules.setup_runner import setup_runner

st.set_page_config(page_title='Data Analysis Dashboard', layout='wide')
def main():
  
   
    try:
      
        # Setup sidebar for navigation
        st.sidebar.title('Navigation')
        choice = st.sidebar.selectbox('Choose a page:', ['Overview', 'Interactive Graphs', 'Static Graphs'])

        # Load and process data only once and not reload on navigation change
        if 'data_loaded' not in st.session_state:
            with st.spinner('Setting up data...'):
                setup_runner()
                st.session_state['data_loaded'] = True  # Mark as loaded
                st.success('Data has been loaded and processed successfully.')

        # Show aggregated data on a dedicated page or under a condition
        if choice == 'Overview':
            overview.show()
        elif choice == 'Interactive Graphs':
            interactive.show()
        elif choice == 'Static Graphs':
            static_graphs.show()

  
        
  

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
