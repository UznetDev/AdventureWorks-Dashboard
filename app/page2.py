import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from loader import *
from function.function import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def app(option):
    # Part 2

    text = 'You can view the share of online and offline customers,\
        the ReasonType, as well as daily, monthly, and yearly sales, categorized by product.'
    st.write_stream(write_stream_text(text, 0.1))

    col, col1, col2, col3 = st.columns(4)

    with col:
        try:
            online_sales_p = db.get_online_percentage(option=option)
            if online_sales_p:
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
            else:
                st.warning('Data not available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col1:
        try:
            by_day = db.get_sales_by_day_with_category(option=option)
            if by_day:
                df = pd.DataFrame(by_day, columns=['Day', 'Category', option])

                df['data'] = normalize_data(df, option, 1, 10, response=True)

                fig = px.line(df, x='Day', y=option, color='Category',
                            title='Product Sales by Day',
                            hover_data={option: True})

                fig.update_layout(yaxis_type="log",
                                title={'text': 'Product Sales by Day',
                                        'x':0.5, 'xanchor': 'center'})

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Data not available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col2:
        try:
            by_month = db.get_sales_by_month_with_category(option=option)
            if by_month:
                df = pd.DataFrame(by_month, columns=['Month', 'Category', option])
                        
                df['data'] = normalize_data(df, option, 1, 10, response=True)

                fig = px.line(df, x='Month', y=option, color='Category',
                                    title='Product Sales by Month',
                                    hover_data={option: True},
                                    )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Data not available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col3:
        try:
            by_year = db.get_sales_by_year(option=option)
            if by_year:
                df = pd.DataFrame(by_year, columns=['Year', 'ProductCategory', option])

                fig = px.bar(df, x='Year', y=option, color='ProductCategory', 
                            title='Total Sold by Year', 
                            labels={option: option, 'ProductCategory': 'Product Category'},
                            orientation='v', 
                            text=option)
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Total Sold",
                    barmode='stack', 
                    coloraxis_colorbar=dict(
                        title="Product Category"
                    )
                )
                st.plotly_chart(fig)
            else:
                st.warning('Data not available.') 
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)



 # Page 5
    col1, col2 = st.columns(2)
    with col1:
        try:
            locations = db.get_locations()
            categories = db.get_categories()
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                years = db.get_years_from_purchase_orders()
                years = ['All'] + [str(year[0]) for year in years]
                selected_year = st.selectbox('Select Year', years, key='year_selectbox_color')
            with s_col2:
                selected_location = st.selectbox('Select Location', ['All'] + locations, key='location_selectbox_color')
                selected_category = st.selectbox('Select Category', ['All'] + categories, key='category_selectbox_color')


            color_data = db.get_color_distribution(
                option=option,
                location=selected_location,
                category=selected_category,
                year=None if selected_year == 'All' else int(selected_year)
            )

            if color_data:
                df = pd.DataFrame(color_data, columns=['Color', option])
                df[option] = df[option].astype(float)
                title = f'{option} by Product Color for {selected_year}'
                fig = px.pie(df, names='Color',
                             values=option, 
                             title=title, 
                             hole=0.4)
                fig.update_traces(pull=[0.04, 0.06, 0.08, 0.1],
                                textinfo='percent+label',
                                marker=dict(line=dict(color='white', width=2)))

                st.plotly_chart(fig)
            else:
                st.warning('No data available to display the Product Color distribution.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col2:
        try:
            years = db.get_years_from_purchase_orders()
            years = ['All'] + [str(year[0]) for year in years]
            selected_year = st.selectbox('Select Year', years, key='year_selectbox_vendor')

            show_category_breakdown = st.checkbox('Show Category Breakdown', key='category_breakdown_checkbox')

            if show_category_breakdown:
                vendor_category_data = db.get_vendor_purchases_by_category(
                    option=option,
                    year=None if selected_year == 'All' else int(selected_year)
                )

                if vendor_category_data:
                    df = pd.DataFrame(vendor_category_data, columns=['VendorName', 
                                                                    'CategoryName', 
                                                                    option])
                    df[option] = df[option].astype(float)
                    title = f"{option} by Vendor and Category for {selected_year}"

                    fig = px.bar(df, 
                                x='VendorName', 
                                y=option,
                                color='CategoryName', 
                                title=title)
                    st.plotly_chart(fig)
                else:
                    st.warning('No data available to display the Vendor purchases with category breakdown.')
            else:
                vendor_data = db.get_vendor_purchases(
                    option=option,
                    year=None if selected_year == 'All' else int(selected_year)
                )

                if vendor_data:
                    df_vendor = pd.DataFrame(vendor_data, columns=['VendorName', option])
                    df_vendor[option] = df_vendor[option].astype(float)
                    values_column = option
                    title = f"{option} by Vendor for {selected_year}"

                    fig_vendor = px.bar(df_vendor, 
                                        x='VendorName', 
                                        y=values_column, 
                                        color=option,
                                        title=title)
                    fig_vendor.update_layout(
                        xaxis_title='Vendor',
                        yaxis_title=option,
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_vendor)
                else:
                    st.warning('No data available to display the Vendor purchases.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)






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


