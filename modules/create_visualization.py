import streamlit as st
from pages import overview, interactive, static_graphs
import duckdb

def start_visualization():
    # This function will start the visualization

    st.sidebar.title('Navigation')
    choice = st.sidebar.selectbox('Choose a page:', ['Overview', 'Interactive Graphs', 'Static Graphs'])

    if choice == 'Overview':
        overview.show()
    elif choice == 'Interactive Graphs':
        interactive.show()
    elif choice == 'Static Graphs':
        static_graphs.show()



def fetch_aggregated_data(db_path):
    try:
        con = duckdb.connect(db_path)
        result = con.execute("SELECT * FROM aggregated_sales").df()
        return result
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        raise e
    finally:
        con.close()


def show_aggregated_data(months):
    st.title('Aggregated Sales Data')
    for month in months:
        try:
            db_path = f'db/2019-{month.lower()}.duckdb'
            data = fetch_aggregated_data(db_path)
            st.subheader(f'Sales Data for {month.capitalize()}')
            st.dataframe(data)
        except Exception as e:
            st.error(f"Failed to load data for {month.capitalize()}: {e}")
            raise e
        
