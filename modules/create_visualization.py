import streamlit as st

import duckdb



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
        
