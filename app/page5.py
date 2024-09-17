import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from loader import *
from function.function import *



def app(option):
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
                fig = px.pie(df, names='Color', values=option, title=title, hole=0.4)
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
                    df_vendor = pd.DataFrame(vendor_category_data, columns=['VendorName', 'CategoryName', 'MetricValue'])
                    df_vendor['MetricValue'] = df_vendor['MetricValue'].astype(float)
                    values_column = 'MetricValue'
                    title = f"{option} by Vendor and Category for {selected_year}"

                    fig_vendor = px.bar(df_vendor, x='VendorName', y=values_column, color='CategoryName', title=title)
                    fig_vendor.update_layout(
                        xaxis_title='Vendor',
                        yaxis_title=option,
                        xaxis_tickangle=-45,
                        barmode='stack'
                    )
                    st.plotly_chart(fig_vendor)
                else:
                    st.warning('No data available to display the Vendor purchases with category breakdown.')
            else:
                vendor_data = db.get_vendor_purchases(
                    option=option,
                    year=None if selected_year == 'All' else int(selected_year)
                )

                if vendor_data:
                    df_vendor = pd.DataFrame(vendor_data, columns=['VendorName', 'MetricValue'])
                    df_vendor['MetricValue'] = df_vendor['MetricValue'].astype(float)
                    values_column = 'MetricValue'
                    title = f"{option} by Vendor for {selected_year}"

                    fig_vendor = px.bar(df_vendor, x='VendorName', y=values_column, title=title)
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


