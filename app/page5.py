import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from loader import *
from function.function import *



def app(option):

        # Page 4
    text = 'In this view,\
        you can see the share of product metrics and the sales for each day,\
        month, and year. Use the filters to refine the data.'
    st.write_stream(write_stream_text(text, 0.1))

    locations = db.get_locations()
    categories = db.get_categories()

    col1, col2, col3, col4 = st.columns(4)

    with col2:
        chart_type = st.selectbox('Select Chart Type', ['Bar Chart', 'Line Chart'], key='chart_type')
    with col3:
        selected_category = st.selectbox('Select Product Category', ['All'] + categories, key='category_selectbox')
    with col4:
        selected_location = st.selectbox('Select Location', ['All'] + locations, key='location_sales_selectbox')

    sales_data_day = db.get_sales_by_day(option=option, 
                                        location=selected_location, 
                                        category=selected_category)

    with col1:
        try:
            shipmethod_data = db.get_shipmethod_distribution(
                option=option,
                location=selected_location,
                category=selected_category
            )
            if shipmethod_data:
                df = pd.DataFrame(shipmethod_data, columns=['ShipMethod', option])
                df[option] = df[option].astype(float)
                values_column = option
                title = f'{option} by Ship Method'
                fig = px.pie(df, names='ShipMethod', values=values_column, title=title, hole=0.4)
                fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
                                textinfo='percent+label',
                                marker=dict(line=dict(color='white', width=2)))

                st.plotly_chart(fig)
            else:
                st.warning('No data available to display the Ship Method distribution.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col2:
        try:
            if selected_category == 'All':
                sales_data_day = db.get_sales_by_day_with_category(option=option,
                                                                location=selected_location)
                if sales_data_day:
                    df_day = pd.DataFrame(sales_data_day, columns=['Day', 'Category', option])
                    df_day['Day'] = df_day['Day'].astype(str)

                    df_day = normalize_data(df_day, option, 1, 10)

                    if chart_type == 'Bar Chart':
                        fig_day = px.bar(df_day, x='Day', y='NormalizedSales', color='Category',
                                        title='Total Sales by Day', barmode='stack',
                                        hover_data={option: True, 'NormalizedSales': False})
                    else:
                        fig_day = px.line(df_day, x='Day', y='NormalizedSales', color='Category',
                                        title='Total Sales by Day',
                                        hover_data={option: True, 'NormalizedSales': False})

                    st.plotly_chart(fig_day)
                else:
                    st.warning('No daily sales data available.')
            else:
                if sales_data_day:
                    df_day = pd.DataFrame(sales_data_day, columns=['Day', option])
                    df_day['Day'] = df_day['Day'].astype(str)

                    df_day = normalize_data(df_day, option, 1, 10)

                    if chart_type == 'Bar Chart':
                        fig_day = px.bar(df_day, x='Day', y='NormalizedSales',
                                        title=f'Total Sales by Day for {selected_category}',
                                        hover_data={option: True, 'NormalizedSales': False})
                    else:
                        fig_day = px.line(df_day, x='Day', y='NormalizedSales',
                                        title=f'Total Sales by Day for {selected_category}',
                                        hover_data={option: True, 'NormalizedSales': False})

                    st.plotly_chart(fig_day)
                else:
                    st.warning('No daily sales data available.')

        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col3:
        try:
            if selected_category == 'All':
                sales_data_month = db.get_sales_by_month_with_category(option=option,
                                                                    location=selected_location)
                if sales_data_month:
                    df_month = pd.DataFrame(sales_data_month, columns=['Month', 'Category', option])
                    df_month['Month'] = df_month['Month'].astype(str)

                    df_month = normalize_data(df_month, option, 1, 10)

                    if chart_type == 'Bar Chart':
                        fig_month = px.bar(df_month, x='Month', y='NormalizedSales', color='Category',
                                        title='Total Sales by Month', barmode='stack',
                                        hover_data={option: True, 'NormalizedSales': False})
                    else:
                        fig_month = px.line(df_month, x='Month', y='NormalizedSales', color='Category',
                                            title='Total Sales by Month',
                                            hover_data={option: True, 'NormalizedSales': False})

                    st.plotly_chart(fig_month)
                else:
                    st.warning('No monthly sales data available.')
            else:
                sales_data_month = db.get_sales_by_month(option=option,location=selected_location, category=selected_category)
                if sales_data_month:
                    df_month = pd.DataFrame(sales_data_month, columns=['Month', option])
                    df_month['Month'] = df_month['Month'].astype(str)

                    df_month = normalize_data(df_month, option, 1, 10)

                    if chart_type == 'Bar Chart':
                        fig_month = px.bar(df_month, x='Month', y='NormalizedSales',
                                        title=f'Total Sales by Month for {selected_category}',
                                        hover_data={option: True, 'NormalizedSales': False})
                    else:
                        fig_month = px.line(df_month, x='Month', y='NormalizedSales',
                                            title=f'Total Sales by Month for {selected_category}',
                                            hover_data={option: True, 'NormalizedSales': False})

                    st.plotly_chart(fig_month)
                else:
                    st.warning('No monthly sales data available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col4:
        try:
            if selected_category == 'All':
                sales_data_year = db.get_sales_by_year_with_category(option=option,location=selected_location)
                if sales_data_year:
                    df_year = pd.DataFrame(sales_data_year, columns=['Year', 'Category', option])
                    df_year['Year'] = df_year['Year'].astype(str)

                    df_year = normalize_data(df_year, option, 1, 10)

                    if chart_type == 'Bar Chart':
                        fig_year = px.bar(df_year, x='Year', y='NormalizedSales', color='Category',
                                        title='Total Sales by Year', barmode='stack',
                                        hover_data={option: True, 'NormalizedSales': False})
                    else:
                        fig_year = px.line(df_year, x='Year', y='NormalizedSales', color='Category',
                                        title='Total Sales by Year',
                                        hover_data={option: True, 'NormalizedSales': False})

                    st.plotly_chart(fig_year)
                else:
                    st.warning('No yearly sales data available.')
            else:
                sales_data_year = db.get_sales_by_year(option=option, location=selected_location, category=selected_category)
                if sales_data_year:
                    df_year = pd.DataFrame(sales_data_year, columns=['Year', option])
                    df_year['Year'] = df_year['Year'].astype(str)

                    df_year = normalize_data(df_year, option, 1, 10)

                    if chart_type == 'Bar Chart':
                        fig_year = px.bar(df_year, x='Year', y='NormalizedSales',
                                        title=f'Total Sales by Year for {selected_category}',
                                        hover_data={option: True, 'NormalizedSales': False})
                    else:
                        fig_year = px.line(df_year, x='Year', y='NormalizedSales',
                                        title=f'Total Sales by Year for {selected_category}',
                                        hover_data={option: True, 'NormalizedSales': False})

                    st.plotly_chart(fig_year)
                else:
                    st.warning('No yearly sales data available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)




    # # Page 5
    # col1, col2 = st.columns(2)
    # with col1:
    #     try:
    #         locations = db.get_locations()
    #         categories = db.get_categories()
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
    #             fig = px.pie(df, names='Color',
    #                          values=option, 
    #                          title=title, 
    #                          hole=0.4)
    #             fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
    #                             textinfo='percent+label',
    #                             marker=dict(line=dict(color='white', width=2)))

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
    #                 df = pd.DataFrame(vendor_category_data, columns=['VendorName', 
    #                                                                 'CategoryName', 
    #                                                                 option])
    #                 df[option] = df[option].astype(float)
    #                 title = f"{option} by Vendor and Category for {selected_year}"

    #                 fig = px.bar(df, 
    #                             x='VendorName', 
    #                             y=option,
    #                             color='CategoryName', 
    #                             title=title)
    #                 st.plotly_chart(fig)
    #             else:
    #                 st.warning('No data available to display the Vendor purchases with category breakdown.')
    #         else:
    #             vendor_data = db.get_vendor_purchases(
    #                 option=option,
    #                 year=None if selected_year == 'All' else int(selected_year)
    #             )

    #             if vendor_data:
    #                 df_vendor = pd.DataFrame(vendor_data, columns=['VendorName', option])
    #                 df_vendor[option] = df_vendor[option].astype(float)
    #                 values_column = option
    #                 title = f"{option} by Vendor for {selected_year}"

    #                 fig_vendor = px.bar(df_vendor, 
    #                                     x='VendorName', 
    #                                     y=values_column, 
    #                                     color=option,
    #                                     title=title)
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


