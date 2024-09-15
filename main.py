import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
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
    ('TotalDue', 'OrderQty', 'NetProfit')
)

by_category = db.get_sales_by_category(option)
by_tretory = db.get_sales_by_territory(option)
by_p_region = db.get_sales_by_p_region(option)


col1, col2, col3 = st.columns(3)
with col1:
    df = pd.DataFrame(by_category, columns=['Category', option])
    fig = px.pie(df, 
                names='Category', 
                values=option, 
                title='Total Products Sold by Category')

    fig.update_traces(pull=[0.02, 0.1, 0.01, 0.105],
                  textinfo='percent+label',
                  marker=dict(line=dict(color='white', width=2)))

    fig.update_layout(
        font=dict(size=16, color='#F39C12'),
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
    df1 = pd.DataFrame(online_sales_p, columns=['Flag', option])

    data2 = db.get_sales_by_reason_type(option)
    df2 = pd.DataFrame(data2, columns=['ReasonType', option])

    fig = make_subplots(rows=2, cols=1, specs=[[{'type':'domain'}], [{'type':'domain'}]])

    fig.add_trace(
        go.Pie(labels=df1['Flag'], values=df1[option], name='Online vs Offline', hole=0.5),
        row=1, col=1
    )
    fig.add_trace(
        go.Pie(labels=df2['ReasonType'], values=df2[option], name='ReasonType', hole=0.5),
        row=2, col=1
        
    )

    fig.update_layout(
        title_text="Online vs Offline Orders and ReasonType",
        annotations=[dict(text='Online vs Offline', x=0.5, y=1.15, font_size=14, showarrow=False, xref='paper', yref='paper'),
                    dict(text='ReasonType', x=0.5, y=0.5, font_size=14, showarrow=False, xref='paper', yref='paper')]
    )

    st.plotly_chart(fig)

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

col1, col2 = st.columns(2)


with col1:
    locations = db.get_locations()
    categories = db.get_categories()

    selected_location = st.selectbox('Select Location', ['All'] + locations)
    selected_category = st.selectbox('Select Category', ['All'] + categories)

    financial_data = db.get_financial_breakdown(location=selected_location, category=selected_category)

    if financial_data:
        total_revenue, production_cost, delivery_cost, net_profit = financial_data

        if not any([total_revenue, production_cost, delivery_cost, net_profit]):
            st.warning('No data found for the selected parameters.')
        else:
            total_revenue = float(total_revenue or 0)
            production_cost = float(production_cost or 0)
            delivery_cost = float(delivery_cost or 0)
            net_profit = float(net_profit or 0)
            other_expenses = 0.0

            labels = ['Production Costs', 'Delivery Costs', 'Other Expenses', 'Net Profit']
            values = [production_cost, delivery_cost, other_expenses, net_profit]

            values = [v if v > 0 else 0 for v in values]

            total = sum(values)

            if total == 0:
                st.warning('No financial data available for the selected parameters.')
            else:
                df = pd.DataFrame({
                    'Labels': labels,
                    'Values': values
                })

                fig = px.pie(df,
                            names='Labels', 
                            values='Values', 
                            title='Financial Breakdown', hole=0.4)
                fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
                            textinfo='percent+label',
                            marker=dict(line=dict(color='white', width=2)))
                st.plotly_chart(fig)
    else:
        st.error('An error occurred while retrieving data.')

with col2:
    data = db.get_map(option)
    if not data:
        st.error('An error occurred while retrieving data.')
        st.stop()

    df = pd.DataFrame(data, columns=['city', 'Longitude', 'Latitude', 'value'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    df = df.dropna(subset=['Longitude', 'Latitude', 'value'])

    if option == 'NetProfit':
        df['ProfitType'] = df['value'].apply(lambda x: 'Profit' if x > 0 else 'Loss')
        df['abs_value'] = df['value'].abs()

        if df.empty:
            st.warning('No financial data available for the selected parameters.')
            st.stop()

        fig = px.scatter_mapbox(df,
                                lat="Latitude", 
                                lon="Longitude",
                                hover_name='city',
                                hover_data={'value': True, 'ProfitType': True},
                                size='abs_value', 
                                color='ProfitType', 
                                size_max=40,
                                zoom=3, 
                                height=550)
    else:
        df = df[df['value'] > 0]

        if df.empty:
            st.warning('No financial data available for the selected parameters.')
            st.stop()

        fig = px.scatter_mapbox(df,
                                lat="Latitude", 
                                lon="Longitude",
                                hover_name='city',
                                hover_data={'value': True},
                                size='value', 
                                color='value', 
                                color_continuous_scale=px.colors.cyclical.IceFire,
                                size_max=40,
                                zoom=3, 
                                height=550)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)


col1, col2, col3 = st.columns(3)

with col1:
    metric_option = st.selectbox('Select Metric', ['Total Revenue', 'Number of Orders'], key='metric_selectbox')
with col2:
    selected_location = st.selectbox('Select Location', ['All'] + locations, key='location_selectbox')
with col3:
    selected_category = st.selectbox('Select Product Category', ['All'] + categories, key='category_selectbox')

col1, col2, col3 = st.columns(3)
with col1:

    if metric_option == 'Total Revenue':
        metric = 'TotalRevenue'
    else:
        metric = 'OrderCount'

    shipmethod_data = db.get_shipmethod_distribution(
        metric=metric,
        location=selected_location,
        category=selected_category
    )

    if shipmethod_data:
        if metric == 'TotalRevenue':
            df = pd.DataFrame(shipmethod_data, columns=['ShipMethod', 'TotalRevenue'])
            df['TotalRevenue'] = df['TotalRevenue'].astype(float)
            values_column = 'TotalRevenue'
            title = 'Total Revenue by Ship Method'
        else:
            df = pd.DataFrame(shipmethod_data, columns=['ShipMethod', 'OrderCount'])
            df['OrderCount'] = df['OrderCount'].astype(int)
            values_column = 'OrderCount'
            title = 'Number of Orders by Ship Method'

        fig = px.pie(df, names='ShipMethod', values=values_column, title=title, hole=0.4)
        fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
                        textinfo='percent+label',
                        marker=dict(line=dict(color='white', width=2)))

        st.plotly_chart(fig)
    else:
        st.warning('No data available to display the Ship Method distribution.')




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