import logging
import sys
import plotly.express as px
import streamlit as st
from loader import *


st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

st_style = """
           <style>
           #MainMenu {visibility: hidden;}
           footer {visibility: hidden;}
           header {visibility: hidden;}
           div.block-container {padding-top:1rem;}
           .css-ysnqb2 e1g8pov64 {margin-top: -75px;}
           </style>
           """

st.markdown(st_style, 
            unsafe_allow_html=True)


total_due = db.get_total_due()


st.title("AdventureWorks Sales Dashboard")

# Create 3 columns for Sales, Profit, and Volume
col1, col2, col3 = st.columns(3)

# Display the metrics
with col1:
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 25px;">Total Sales: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:White; font-size: 20px;">{total_due}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)




if __name__ == "__main__":
    db.create_table_sales_per_day()
    db.insert_table_sales_per_day()
    # Configure logging
    format = '%(filename)s - %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        # filename=log_file_name,  # Save error log on file
        level=logging.ERROR,  # Set the logging level to INFO
        format=format,  # Set the logging format
        stream=sys.stdout  # Log to stdout
    )