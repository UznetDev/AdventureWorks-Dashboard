import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from loader import *
from function.function import *


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
total_profit = db.get_total_profit()
sales_count = db.get_sales_count()

st.title("AdventureWorks Sales Dashboard")

# Create 3 columns for Sales, Profit, and Volume
col1, col2, col3 = st.columns(3)

# Display the metrics
with col1:
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 15px;">Total Due: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:red; font-size: 20px;">{abbreviate_number(total_due)}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)

with col2:
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 15px;">Total Profit: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:red; font-size: 20px;">{abbreviate_number(total_profit)}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)

with col3:
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 15px;">Sales Count: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:red; font-size: 20px;">{abbreviate_number(sales_count)}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)








option = st.selectbox(
    'Tanlang: Total Sales (TotalDue) yoki Order Quantity (OrderQty)',
    ('TotalDue', 'OrderQty')
)

by_category = db.get_sales_by_category(option)
by_tretory = db.get_sales_by_tretory(option)
by_p_region = db.get_sales_by_p_region(option)
by_month = db.get_sales_by_p_month(option)

col1, col2, col3 = st.columns(3)
with col1:
    df = pd.DataFrame(by_category, columns=['Category', 'Total Sold'])
    fig = px.pie(df, names='Category', values='Total Sold', title='Total Products Sold by Category')
    st.plotly_chart(fig)

with col2:
    df = pd.DataFrame(by_tretory, columns=['Territory', 'Total Sold'])
    fig = px.bar(df, x='Territory', y='Total Sold', 
                color='Total Sold', 
                color_continuous_scale=['yellow', 'red'], 
                title='Total Products Sold by Territory')

    fig.update_layout(
        xaxis_title="Territory",
        yaxis_title="Total Sold",
        coloraxis_colorbar=dict(
            title="Total Sold"
        )
    )
    st.plotly_chart(fig)

with col3:
    df = pd.DataFrame(by_p_region, columns=['Total Sold', 'Region'])
    fig = px.bar(df,  x='Region', y='Total Sold', 
             color='Total Sold', 
             orientation='h',
             title='Total Products Sold by Person and Region')

    fig.update_layout(
        xaxis_title="Total Sold",
        yaxis_title="Product",
        coloraxis_colorbar=dict(
            title="Region"
        )
    )

    st.plotly_chart(fig, use_container_width=True)




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