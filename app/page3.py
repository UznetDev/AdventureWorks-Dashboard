import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from loader import *
from function.function import *



def app(option):
    # Page 3

    text = 'In this view, you can see what percentage of the total sales price is taken by each cost. \
        You can select the product type and the country. Additionally, \
        a map shows the locations where the products were sold.'
    st.write_stream(write_stream_text(text, 0.1))

    col1, col2 = st.columns(2)

    with col1:
        try:
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
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col2:
        try:
            data = db.get_map(option)
            if not data:
                st.error('An error occurred while retrieving data.')
            else:
                df = pd.DataFrame(data, columns=['city', 'Longitude', 'Latitude', 'value'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')

                df = df.dropna(subset=['Longitude', 'Latitude', 'value'])

                if option == 'NetProfit':
                    df['ProfitType'] = df['value'].apply(lambda x: 'Profit' if x > 0 else 'Loss')
                    df['abs_value'] = df['value'].abs()

                    if df.empty:
                        st.warning('No financial data available for the selected parameters.')

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
                                            height=618)

                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

                st.plotly_chart(fig, use_container_width=True)

        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)


    with col1:
        years = db.get_years_from_sales_orders()
        years = ['All'] + [str(year[0]) for year in years]

        selected_year = st.selectbox('Select Year', years, key='year_selectbox_store')

        store_limit = st.number_input('Select number of top stores to display', min_value=1, max_value=100, value=20, step=1)

        show_category_breakdown = st.checkbox('Show Category Breakdown', key='category_breakdown_checkbox')

        if show_category_breakdown:
            store_category_data = db.get_top_sales_stores_with_categories(
                year=None if selected_year == 'All' else int(selected_year),
                limit=store_limit,
                option=option
            )

            if store_category_data:
                df_store_category = pd.DataFrame(store_category_data, columns=['StoreName', 'CategoryName', option])
                df_store_category[option] = df_store_category[option].astype(float)

                fig = px.bar(df_store_category, x=option, y='StoreName', color='CategoryName', 
                            title=f'Top {store_limit} Stores by Sales with Category Breakdown for {selected_year}', 
                            orientation='h')
                fig.update_layout(xaxis_title='Total Sales', 
                                  yaxis_title='Store Name', 
                                  barmode='stack')

                st.plotly_chart(fig)
            else:
                st.warning('No data available for the selected year.')
        else:
            top_stores = db.get_top_sales_stores(
                year=None if selected_year == 'All' else int(selected_year),
                limit=store_limit
            )
            if top_stores:
                df_stores = pd.DataFrame(top_stores, columns=['StoreName', option])
                df_stores[option] = df_stores[option].astype(float)

                fig = px.bar(df_stores, y='StoreName', x=option, title=f'Top {store_limit} Stores by Sales for {selected_year}', orientation='h')
                fig.update_layout(xaxis_title='Total Sales', yaxis_title='Store Name', yaxis_categoryorder='total ascending')

                st.plotly_chart(fig)
            else:
                st.warning('No data available for the selected year.')

    with col2:
        years = db.get_years_from_sales_orders()
        years = ['All'] + [str(year[0]) for year in years]

        selected_year = st.selectbox('Select Year', years, key='year_selectbox_customers')

        customer_limit = st.number_input('Select number of top customers to display', min_value=1, max_value=100, value=20, step=1)

        show_category_breakdown = st.checkbox('Show Category Breakdown', key='category_breakdown_checkbox_customers')

        if show_category_breakdown:
            customer_category_data = db.get_top_customers_with_categories(
                year=None if selected_year == 'All' else int(selected_year),
                limit=customer_limit
            )

            if customer_category_data:
                df_customer_category = pd.DataFrame(customer_category_data, columns=['FirstName', 'LastName', 'CategoryName', option])
                df_customer_category[option] = df_customer_category[option].astype(float)

                df_customer_category['CustomerName'] = df_customer_category['FirstName'] + " " + df_customer_category['LastName']

                fig = px.bar(df_customer_category, x=option, y='CustomerName', color='CategoryName', 
                            title=f'Top {customer_limit} Customers by Sales with Category Breakdown for {selected_year}', 
                            orientation='h')

                fig.update_layout(xaxis_title='Total Sales', yaxis_title='Customer Name', barmode='stack')

                st.plotly_chart(fig)
            else:
                st.warning('No data available for the selected year.')
        else:
            top_customers = db.get_top_customers(
                year=None if selected_year == 'All' else int(selected_year),
                limit=customer_limit,
                option=option
            )

            if top_customers:
                df = pd.DataFrame(top_customers, columns=['name', option])
                df[option] = df[option].astype(float)


                fig = px.bar(df, 
                             y='name',
                             x=option, 
                             title=f'Top {customer_limit} Customers by Sales for {selected_year}', orientation='h')

                st.plotly_chart(fig)
            else:
                st.warning('No data available for the selected year.')



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
    app()


