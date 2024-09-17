import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from loader import *
from function.function import *

st.set_page_config(page_title="AdventureWorks Dashboard",
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
person_count = db.get_total_person()
product_count = db.get_total_product()

st.header(':blue[AdventureWorks] Dashboard')
# Header
col1, col2, col3, col4, col5 = st.columns(5)

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

with col4:
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 15px;">User Count: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:red; font-size: 20px;">{abbreviate_number(person_count)}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)

with col5:
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 15px;">Product Count: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:red; font-size: 20px;">{abbreviate_number(product_count)}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)


text = """
### **Metric Descriptions**

In this section, you can select various metrics to analyze. Each metric has the following meaning:

- **TotalDue**: **Total Amount Due**  
  The total amount that the customer is required to pay for the order. This includes the cost of the products, tax, and freight charges.

- **OrderQty**: **Order Quantity**  
  The total number of products ordered. This metric indicates how many units were purchased in the order.

- **LineTotal**: **Line Total**  
  The total amount for each order line. This value is calculated by multiplying the unit price by the quantity ordered (UnitPrice × OrderQty).

- **NetProfit**: **Net Profit**  
  The difference between revenue and expenses. This metric shows the net profit the company makes from the sale of products.

- **UnitPrice**: **Unit Price**  
  The price for a single unit of the product. This metric represents the retail or wholesale price of the product.

- **TaxAmt**: **Tax Amount**  
  The amount of tax calculated for the order. This amount is added to the total due.

- **Freight**: **Freight Charge**  
  The cost associated with shipping or delivering the product to the customer. This amount is also added to the total due.

- **SubTotal**: **Subtotal**  
  The total amount of the products before tax and freight charges. This amount represents the original cost of the products ordered.

---

**Note:** The charts and reports will update based on the metric you select, allowing you to analyze sales performance from different perspectives.
"""


show_description = st.checkbox('Show Description', key='show_description')

if show_description:
    st.markdown(text)

st.markdown("######  :blue[***This will affect the overall dashboard.***]")
option = st.selectbox(
    'Choice:',
    ('TotalDue', 'OrderQty', 'LineTotal', 'NetProfit', 'UnitPrice', 'TaxAmt', 'Freight', 'SubTotal')
)

if "nav" not in st.session_state:
    st.session_state["nav"] = "1"

col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])

with col1:
    if st.button("Home"):
        st.session_state["nav"] = "1"
with col2:
    if st.button("Page 1"):
        st.session_state["nav"] = "2"
with col3:
    if st.button("Page 2"):
        st.session_state["nav"] = "3"
with col4:
    if st.button("Page 3"):
        st.session_state["nav"] = "4"
with col5:
    if st.button("Page 4"):
        st.session_state["nav"] = "5"
with col6:
    if st.button("Model"):
        st.session_state["nav"] = "m"

selected_page = st.session_state["nav"]

if selected_page == "1":
    from app.page1 import app
    app(option=option)
elif selected_page == "2":
    from app.page2 import app
    app(option=option)
elif selected_page == "3":
    from app.page3 import app
    app(option=option)
elif selected_page == "4":
    from app.page4 import app
    app(option=option)
elif selected_page == "5":
    from app.page5 import app
    app(option=option)
elif selected_page == "m":
    from app.model import app
    app()

# # Part 1

# text = 'You can get information here about the market share of each category,\
#     sales in each territory, and products in each region.'
# st.write_stream(write_stream_text(text, 0.1))

# col1, col2, col3 = st.columns(3)
# with col1:
#     try:
#         by_category = db.get_sales_by_category(option)
#         if by_category:
#             df = pd.DataFrame(by_category, columns=['Category', option])
#             fig = px.pie(df, 
#                         names='Category', 
#                         values=option, 
#                         title='Total Products Sold by Category')

#             fig.update_traces(pull=[0.02, 0.1, 0.01, 0.105],
#                         textinfo='percent+label',
#                         marker=dict(line=dict(color='white', width=2)))

#             fig.update_layout(
#                 font=dict(size=16, color='#F39C12'),
#                 showlegend=True, 
#                 title_font_size=20,
#                 title_x=0.5,
#                 margin=dict(t=30, b=0, l=0, r=0),
#             )
#             st.plotly_chart(fig)
#         else:
#             st.warning('Data not available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col2:
#     try:
#         by_tretory = db.get_sales_by_territory(option)
#         if by_tretory:
#             df = pd.DataFrame(by_tretory, columns=['Territory', 'Category', option])
#             fig = px.bar(df, x='Territory', y=option, color='Category', 
#                         title='Sold Territory', 
#                         labels={option: option, 'Category': 'Product Category'},
#                         orientation='v',
#                         text=option
#                         )

#             fig.update_layout(
#                 xaxis_title="Territory",
#                 yaxis_title="Total Sold",
#                 barmode='stack',
#                 coloraxis_colorbar=dict(
#                     title="Product Territory"
#                 )
#             )
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning('Data not available.')  
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col3:
#     try:
#         by_p_region = db.get_sales_by_p_region(option)
#         if by_p_region:
#             df = pd.DataFrame(by_p_region, columns=['Region', 'Category', option])
#             fig = px.bar(df, x=option, y='Region', color='Category', 
#                         title='Products Region',
#                         labels={option: option, 'Category': 'Product Category'},
#                         orientation='h', 
#                         text=option)

#             fig.update_layout(
#                 xaxis_title="Total Sold",
#                 yaxis_title="Region",
#                 barmode='stack',
#                 coloraxis_colorbar=dict(
#                     title="Product Region"
#                 )
#             )
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning('Data not available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)


# # Part 2

# text = 'You can view the share of online and offline customers,\
#     the ReasonType, as well as daily, monthly, and yearly sales, categorized by product.'
# st.write_stream(write_stream_text(text, 0.1))

# col, col1, col2, col3 = st.columns(4)

# with col:
#     try:
#         online_sales_p = db.get_online_percentage(option=option)
#         if online_sales_p:
#             df1 = pd.DataFrame(online_sales_p, columns=['Flag', option])

#             data2 = db.get_sales_by_reason_type(option)
#             df2 = pd.DataFrame(data2, columns=['ReasonType', option])

#             fig = make_subplots(rows=2, cols=1, specs=[[{'type':'domain'}], [{'type':'domain'}]])

#             fig.add_trace(
#                 go.Pie(labels=df1['Flag'], values=df1[option], name='Online vs Offline', hole=0.5),
#                 row=1, col=1
#             )
#             fig.add_trace(
#                 go.Pie(labels=df2['ReasonType'], values=df2[option], name='ReasonType', hole=0.5),
#                 row=2, col=1
                
#             )

#             fig.update_layout(
#                 title_text="Online vs Offline Orders and ReasonType",
#                 annotations=[dict(text='Online vs Offline', x=0.5, y=1.15, font_size=14, showarrow=False, xref='paper', yref='paper'),
#                             dict(text='ReasonType', x=0.5, y=0.5, font_size=14, showarrow=False, xref='paper', yref='paper')]
#             )

#             st.plotly_chart(fig)
#         else:
#             st.warning('Data not available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col1:
#     try:
#         by_day = db.get_sales_by_day_with_category(option=option)
#         if by_day:
#             df = pd.DataFrame(by_day, columns=['Day', 'Category', option])

#             df['data'] = normalize_data(df, option, 1, 10, response=True)

#             fig = px.line(df, x='Day', y=option, color='Category',
#                         title='Product Sales by Day',
#                         hover_data={option: True})

#             fig.update_layout(yaxis_type="log",
#                             title={'text': 'Product Sales by Day',
#                                     'x':0.5, 'xanchor': 'center'})

#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning('Data not available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col2:
#     try:
#         by_month = db.get_sales_by_month_with_category(option=option)
#         if by_month:
#             df = pd.DataFrame(by_month, columns=['Month', 'Category', option])
                    
#             df['data'] = normalize_data(df, option, 1, 10, response=True)

#             fig = px.line(df, x='Month', y=option, color='Category',
#                                 title='Product Sales by Month',
#                                 hover_data={option: True},
#                                 )
            
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning('Data not available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col3:
#     try:
#         by_year = db.get_sales_by_year(option=option)
#         if by_year:
#             df = pd.DataFrame(by_year, columns=['Year', 'ProductCategory', option])

#             fig = px.bar(df, x='Year', y=option, color='ProductCategory', 
#                         title='Total Sold by Year', 
#                         labels={option: option, 'ProductCategory': 'Product Category'},
#                         orientation='v', 
#                         text=option)
#             fig.update_layout(
#                 xaxis_title="Year",
#                 yaxis_title="Total Sold",
#                 barmode='stack', 
#                 coloraxis_colorbar=dict(
#                     title="Product Category"
#                 )
#             )
#             st.plotly_chart(fig)
#         else:
#            st.warning('Data not available.') 
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)


# # Page 3

# text = 'In this view, you can see what percentage of the total sales price is taken by each cost. \
#     You can select the product type and the country. Additionally, \
#     a map shows the locations where the products were sold.'
# st.write_stream(write_stream_text(text, 0.1))

# col1, col2 = st.columns(2)

# with col1:
#     try:
#         locations = db.get_locations()
#         categories = db.get_categories()

#         selected_location = st.selectbox('Select Location', ['All'] + locations)
#         selected_category = st.selectbox('Select Category', ['All'] + categories)

#         financial_data = db.get_financial_breakdown(location=selected_location, category=selected_category)

#         if financial_data:
#             total_revenue, production_cost, delivery_cost, net_profit = financial_data

#             if not any([total_revenue, production_cost, delivery_cost, net_profit]):
#                 st.warning('No data found for the selected parameters.')
#             else:
#                 total_revenue = float(total_revenue or 0)
#                 production_cost = float(production_cost or 0)
#                 delivery_cost = float(delivery_cost or 0)
#                 net_profit = float(net_profit or 0)
#                 other_expenses = 0.0

#                 labels = ['Production Costs', 'Delivery Costs', 'Other Expenses', 'Net Profit']
#                 values = [production_cost, delivery_cost, other_expenses, net_profit]

#                 values = [v if v > 0 else 0 for v in values]

#                 total = sum(values)

#                 if total == 0:
#                     st.warning('No financial data available for the selected parameters.')
#                 else:
#                     df = pd.DataFrame({
#                         'Labels': labels,
#                         'Values': values
#                     })

#                     fig = px.pie(df,
#                                 names='Labels', 
#                                 values='Values', 
#                                 title='Financial Breakdown', hole=0.4)
#                     fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
#                                 textinfo='percent+label',
#                                 marker=dict(line=dict(color='white', width=2)))
#                     st.plotly_chart(fig)
#         else:
#             st.error('An error occurred while retrieving data.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col2:
#     try:
#         data = db.get_map(option)
#         if not data:
#             st.error('An error occurred while retrieving data.')
#         else:
#             df = pd.DataFrame(data, columns=['city', 'Longitude', 'Latitude', 'value'])
#             df['value'] = pd.to_numeric(df['value'], errors='coerce')

#             df = df.dropna(subset=['Longitude', 'Latitude', 'value'])

#             if option == 'NetProfit':
#                 df['ProfitType'] = df['value'].apply(lambda x: 'Profit' if x > 0 else 'Loss')
#                 df['abs_value'] = df['value'].abs()

#                 if df.empty:
#                     st.warning('No financial data available for the selected parameters.')

#                 fig = px.scatter_mapbox(df,
#                                         lat="Latitude", 
#                                         lon="Longitude",
#                                         hover_name='city',
#                                         hover_data={'value': True, 'ProfitType': True},
#                                         size='abs_value', 
#                                         color='ProfitType', 
#                                         size_max=40,
#                                         zoom=3, 
#                                         height=550)
#             else:
#                 df = df[df['value'] > 0]

#                 if df.empty:
#                     st.warning('No financial data available for the selected parameters.')

#                 fig = px.scatter_mapbox(df,
#                                         lat="Latitude", 
#                                         lon="Longitude",
#                                         hover_name='city',
#                                         hover_data={'value': True},
#                                         size='value', 
#                                         color='value', 
#                                         color_continuous_scale=px.colors.cyclical.IceFire,
#                                         size_max=40,
#                                         zoom=3, 
#                                         height=550)

#             fig.update_layout(mapbox_style="open-street-map")
#             fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#             st.plotly_chart(fig, use_container_width=True)

#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)


# # Page 4
# text = 'In this view,\
#     you can see the share of product metrics and the sales for each day,\
#     month, and year. Use the filters to refine the data.'
# st.write_stream(write_stream_text(text, 0.1))

# locations = db.get_locations()
# categories = db.get_categories()

# col1, col2, col3, col4 = st.columns(4)

# with col2:
#     chart_type = st.selectbox('Select Chart Type', ['Bar Chart', 'Line Chart'], key='chart_type')
# with col3:
#     selected_category = st.selectbox('Select Product Category', ['All'] + categories, key='category_selectbox')
# with col4:
#     selected_location = st.selectbox('Select Location', ['All'] + locations, key='location_sales_selectbox')

# sales_data_day = db.get_sales_by_day(option=option, 
#                                      location=selected_location, 
#                                      category=selected_category)

# with col1:
#     try:
#         shipmethod_data = db.get_shipmethod_distribution(
#             option=option,
#             location=selected_location,
#             category=selected_category
#         )
#         if shipmethod_data:
#             df = pd.DataFrame(shipmethod_data, columns=['ShipMethod', option])
#             df[option] = df[option].astype(float)
#             values_column = option
#             title = f'{option} by Ship Method'
#             fig = px.pie(df, names='ShipMethod', values=values_column, title=title, hole=0.4)
#             fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
#                             textinfo='percent+label',
#                             marker=dict(line=dict(color='white', width=2)))

#             st.plotly_chart(fig)
#         else:
#             st.warning('No data available to display the Ship Method distribution.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col2:
#     try:
#         if selected_category == 'All':
#             sales_data_day = db.get_sales_by_day_with_category(option=option,
#                                                             location=selected_location)
#             if sales_data_day:
#                 df_day = pd.DataFrame(sales_data_day, columns=['Day', 'Category', option])
#                 df_day['Day'] = df_day['Day'].astype(str)

#                 df_day = normalize_data(df_day, option, 1, 10)

#                 if chart_type == 'Bar Chart':
#                     fig_day = px.bar(df_day, x='Day', y='NormalizedSales', color='Category',
#                                     title='Total Sales by Day', barmode='stack',
#                                     hover_data={option: True, 'NormalizedSales': False})
#                 else:
#                     fig_day = px.line(df_day, x='Day', y='NormalizedSales', color='Category',
#                                     title='Total Sales by Day',
#                                     hover_data={option: True, 'NormalizedSales': False})

#                 st.plotly_chart(fig_day)
#             else:
#                 st.warning('No daily sales data available.')
#         else:
#             if sales_data_day:
#                 df_day = pd.DataFrame(sales_data_day, columns=['Day', option])
#                 df_day['Day'] = df_day['Day'].astype(str)

#                 df_day = normalize_data(df_day, option, 1, 10)

#                 if chart_type == 'Bar Chart':
#                     fig_day = px.bar(df_day, x='Day', y='NormalizedSales',
#                                     title=f'Total Sales by Day for {selected_category}',
#                                     hover_data={option: True, 'NormalizedSales': False})
#                 else:
#                     fig_day = px.line(df_day, x='Day', y='NormalizedSales',
#                                     title=f'Total Sales by Day for {selected_category}',
#                                     hover_data={option: True, 'NormalizedSales': False})

#                 st.plotly_chart(fig_day)
#             else:
#                 st.warning('No daily sales data available.')

#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col3:
#     try:
#         if selected_category == 'All':
#             sales_data_month = db.get_sales_by_month_with_category(option=option,
#                                                                 location=selected_location)
#             if sales_data_month:
#                 df_month = pd.DataFrame(sales_data_month, columns=['Month', 'Category', option])
#                 df_month['Month'] = df_month['Month'].astype(str)

#                 df_month = normalize_data(df_month, option, 1, 10)

#                 if chart_type == 'Bar Chart':
#                     fig_month = px.bar(df_month, x='Month', y='NormalizedSales', color='Category',
#                                     title='Total Sales by Month', barmode='stack',
#                                     hover_data={option: True, 'NormalizedSales': False})
#                 else:
#                     fig_month = px.line(df_month, x='Month', y='NormalizedSales', color='Category',
#                                         title='Total Sales by Month',
#                                         hover_data={option: True, 'NormalizedSales': False})

#                 st.plotly_chart(fig_month)
#             else:
#                 st.warning('No monthly sales data available.')
#         else:
#             sales_data_month = db.get_sales_by_month(option=option,location=selected_location, category=selected_category)
#             if sales_data_month:
#                 df_month = pd.DataFrame(sales_data_month, columns=['Month', option])
#                 df_month['Month'] = df_month['Month'].astype(str)

#                 df_month = normalize_data(df_month, option, 1, 10)

#                 if chart_type == 'Bar Chart':
#                     fig_month = px.bar(df_month, x='Month', y='NormalizedSales',
#                                     title=f'Total Sales by Month for {selected_category}',
#                                     hover_data={option: True, 'NormalizedSales': False})
#                 else:
#                     fig_month = px.line(df_month, x='Month', y='NormalizedSales',
#                                         title=f'Total Sales by Month for {selected_category}',
#                                         hover_data={option: True, 'NormalizedSales': False})

#                 st.plotly_chart(fig_month)
#             else:
#                 st.warning('No monthly sales data available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col4:
#     try:
#         if selected_category == 'All':
#             sales_data_year = db.get_sales_by_year_with_category(option=option,location=selected_location)
#             if sales_data_year:
#                 df_year = pd.DataFrame(sales_data_year, columns=['Year', 'Category', option])
#                 df_year['Year'] = df_year['Year'].astype(str)

#                 df_year = normalize_data(df_year, option, 1, 10)

#                 if chart_type == 'Bar Chart':
#                     fig_year = px.bar(df_year, x='Year', y='NormalizedSales', color='Category',
#                                     title='Total Sales by Year', barmode='stack',
#                                     hover_data={option: True, 'NormalizedSales': False})
#                 else:
#                     fig_year = px.line(df_year, x='Year', y='NormalizedSales', color='Category',
#                                     title='Total Sales by Year',
#                                     hover_data={option: True, 'NormalizedSales': False})

#                 st.plotly_chart(fig_year)
#             else:
#                 st.warning('No yearly sales data available.')
#         else:
#             sales_data_year = db.get_sales_by_year(option=option, location=selected_location, category=selected_category)
#             if sales_data_year:
#                 df_year = pd.DataFrame(sales_data_year, columns=['Year', option])
#                 df_year['Year'] = df_year['Year'].astype(str)

#                 df_year = normalize_data(df_year, option, 1, 10)

#                 if chart_type == 'Bar Chart':
#                     fig_year = px.bar(df_year, x='Year', y='NormalizedSales',
#                                     title=f'Total Sales by Year for {selected_category}',
#                                     hover_data={option: True, 'NormalizedSales': False})
#                 else:
#                     fig_year = px.line(df_year, x='Year', y='NormalizedSales',
#                                     title=f'Total Sales by Year for {selected_category}',
#                                     hover_data={option: True, 'NormalizedSales': False})

#                 st.plotly_chart(fig_year)
#             else:
#                 st.warning('No yearly sales data available.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)


# # Page 5
# col1, col2 = st.columns(2)
# with col1:
#     try:
#         s_col1, s_col2 = st.columns(2)
#         with s_col1:
#             years = db.get_years_from_purchase_orders()
#             years = ['All'] + [str(year[0]) for year in years]
#             selected_year = st.selectbox('Select Year', years, key='year_selectbox_color')
#         with s_col2:
#             selected_location = st.selectbox('Select Location', ['All'] + locations, key='location_selectbox_color')
#             selected_category = st.selectbox('Select Category', ['All'] + categories, key='category_selectbox_color')


#         color_data = db.get_color_distribution(
#             option=option,
#             location=selected_location,
#             category=selected_category,
#             year=None if selected_year == 'All' else int(selected_year)
#         )

#         if color_data:
#             df = pd.DataFrame(color_data, columns=['Color', option])
#             df[option] = df[option].astype(float)
#             title = f'{option} by Product Color for {selected_year}'
#             fig = px.pie(df, names='Color', values=option, title=title, hole=0.4)
#             fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
#                               textinfo='percent+label',
#                               marker=dict(line=dict(color='white', width=2)))

#             st.plotly_chart(fig)
#         else:
#             st.warning('No data available to display the Product Color distribution.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)

# with col2:
#     try:
#         years = db.get_years_from_purchase_orders()
#         years = ['All'] + [str(year[0]) for year in years]
#         selected_year = st.selectbox('Select Year', years, key='year_selectbox_vendor')

#         show_category_breakdown = st.checkbox('Show Category Breakdown', key='category_breakdown_checkbox')

#         if show_category_breakdown:
#             vendor_category_data = db.get_vendor_purchases_by_category(
#                 option=option,
#                 year=None if selected_year == 'All' else int(selected_year)
#             )

#             if vendor_category_data:
#                 df_vendor = pd.DataFrame(vendor_category_data, columns=['VendorName', 'CategoryName', 'MetricValue'])
#                 df_vendor['MetricValue'] = df_vendor['MetricValue'].astype(float)
#                 values_column = 'MetricValue'
#                 title = f"{option} by Vendor and Category for {selected_year}"

#                 fig_vendor = px.bar(df_vendor, x='VendorName', y=values_column, color='CategoryName', title=title)
#                 fig_vendor.update_layout(
#                     xaxis_title='Vendor',
#                     yaxis_title=option,
#                     xaxis_tickangle=-45,
#                     barmode='stack'
#                 )
#                 st.plotly_chart(fig_vendor)
#             else:
#                 st.warning('No data available to display the Vendor purchases with category breakdown.')
#         else:
#             vendor_data = db.get_vendor_purchases(
#                 option=option,
#                 year=None if selected_year == 'All' else int(selected_year)
#             )

#             if vendor_data:
#                 df_vendor = pd.DataFrame(vendor_data, columns=['VendorName', 'MetricValue'])
#                 df_vendor['MetricValue'] = df_vendor['MetricValue'].astype(float)
#                 values_column = 'MetricValue'
#                 title = f"{option} by Vendor for {selected_year}"

#                 fig_vendor = px.bar(df_vendor, x='VendorName', y=values_column, title=title)
#                 fig_vendor.update_layout(
#                     xaxis_title='Vendor',
#                     yaxis_title=option,
#                     xaxis_tickangle=-45
#                 )
#                 st.plotly_chart(fig_vendor)
#             else:
#                 st.warning('No data available to display the Vendor purchases.')
#     except Exception as err:
#         st.warning('Data not available.')
#         logging.error(err)



footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 255, 0.1);  /* Very transparent blue */
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #FFFFFF;  /* White text color */
    }
    .footer a {
        color: #FFD700;  /* Golden link color */
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="footer">
        <p>AdventureWorks Dashboard | Data Source: AdventureWorks Database | © 2024 UZNetDev <a href="https://github.com/UznetDev/AdventureWorks-Dashboard.git" target="_blank">GitHub</a></p>
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)


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



