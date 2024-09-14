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


col1, col2, col3 = st.columns(3)

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
by_tretory = db.get_sales_by_territory(option)
by_p_region = db.get_sales_by_p_region(option)


col1, col2, col3 = st.columns(3)
with col1:
    df = pd.DataFrame(by_category, columns=['Category', 'Total Sold'])
    fig = px.pie(df, names='Category', values='Total Sold', title='Total Products Sold by Category')

    fig.update_traces(pull=[0.02, 0.1, 0.01, 0.105],
                  textinfo='percent+label',
                  marker=dict(line=dict(color='white', width=2)))

    fig.update_layout(
        showlegend=True, 
        title_font_size=20,
        title_x=0.5,
        margin=dict(t=30, b=0, l=0, r=0),
    )
    st.plotly_chart(fig)

with col2:
    df = pd.DataFrame(by_tretory, columns=['Territory', 'Category', 'Total Sold'])
    fig = px.bar(df, x='Territory', y='Total Sold', color='Category', 
                title='Sold Category', 
                labels={'Total Sold': 'Total Sold', 'Category': 'Product Category'},
                orientation='v', 
                text='Total Sold')

    fig.update_layout(
        xaxis_title="Territory",
        yaxis_title="Total Sold",
        barmode='stack',
        coloraxis_colorbar=dict(
            title="Product Category"
        )
    )
    st.plotly_chart(fig, use_container_width=True)




with col3:
    df = pd.DataFrame(by_p_region, columns=['Region', 'Category', 'Total Sold'])
    fig = px.bar(df, x='Total Sold', y='Region', color='Category', 
                title='Products Category', 
                labels={'Total Sold': 'Total Sold', 'Category': 'Product Category'},
                orientation='h', 
                text='Total Sold')

    fig.update_layout(
        xaxis_title="Total Sold",
        yaxis_title="Region",
        barmode='stack',
        coloraxis_colorbar=dict(
            title="Product Category"
        )
    )
    st.plotly_chart(fig, use_container_width=True)



by_month = db.get_sales_by_c_month(option)
by_day = db.get_sales_by_c_day(option)
by_year = db.get_sales_by_c_year(option)
online_sales_p = db.get_online_persentage(option)

col, col1, col2, col3 = st.columns(4)

with col:
    text = '<p style="font-family:sans-serif; color:yellow; font-size: 20px;">Online Sales Persentage!</p>'
    st.markdown(text, unsafe_allow_html=True)
    st.write(make_donut(online_sales_p, f'Online Sales by {option}'))

with col1:
    df = pd.DataFrame(by_month, columns=['Month', 'Category', option])
            
    df['data'] = normalize_data(df[option])

    fig = px.line(df, x='Month', y=option, color='Category',
                          title='Product Category Sales by Month',
                          hover_data={option: True})
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df = pd.DataFrame(by_day, columns=['Day', 'Category', option])

    df['data'] = normalize_data(df[option])

    fig = px.line(df, x='Day', y=option, color='Category',
                title='Product Category Sales by Day',
                hover_data={option: True})

    fig.update_layout(yaxis_type="log",
                    title={'text': 'Product Category Sales by Day (Log Scale)',
                            'x':0.5, 'xanchor': 'center'})

    st.plotly_chart(fig, use_container_width=True)

with col3:
    df = pd.DataFrame(by_year, columns=['Year', 'ProductCategory', 'Total Sold'])

    fig = px.bar(df, x='Year', y='Total Sold', color='ProductCategory', 
                title='Total Products Sold by Year and Product Category', 
                labels={'Total Sold': 'Total Sold', 'ProductCategory': 'Product Category'},
                orientation='v', 
                text='Total Sold')
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Sold",
        barmode='stack', 
        coloraxis_colorbar=dict(
            title="Product Category"
        )
    )
    st.plotly_chart(fig)


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