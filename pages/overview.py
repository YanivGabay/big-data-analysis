# overview.py
import streamlit as st




def show():
  
    st.write("""
    ## Project Overview
    This dashboard provides a comprehensive analysis of ecommerce behavior through multiple interactive pages. Each page is designed to focus on specific aspects of ecommerce data ranging from individual brand performance to user engagement patterns across different times of the day.

    ## Pages Overview
    - **Brand Performance**: Analyzes sales performance across various brands, comparing metrics like total sales and average prices between October and November.
    - **User Activities by Hour**: Offers insights into user activities segmented by hour, which helps in understanding user engagement patterns throughout the day. interactive heatmap and bar chart for different event types.
    - **Static Graphs**: Displays static graphs for different metrics using an extracted sales_data database, which gives us aggregated information about the user total events,total purchases, and average price.
    - **Top Products by growth**: Using my favorite graph the bubble chart, we can see the top products in terms of sales,with a interactive slider to filter based on the growth of the product.
    - **User Retention**: Examines user retention rates by tracking user activity over time and identifying how long users stay engaged with the platform, get intersting metrics per month like average retention days, total users and average purchase frequency.

    
    
    """)

    st.markdown("---")
    st.write("## Detailed Page Descriptions")
    st.write("Navigate to each page from the sidebar to explore in-depth analyses and visualizations tailored to different aspects of ecommerce data.")
  
