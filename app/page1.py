import logging
import sys
import plotly.express as px
import streamlit as st
import pandas as pd
from loader import *
from function.function import *



def app(option):
    # Part 1

    text = 'You can get information here about the market share of each category,\
        sales in each territory, and products in each region.'
    st.write_stream(write_stream_text(text, 0.1))

    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            by_category = db.get_sales_by_category(option)
            if by_category:
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
            else:
                st.warning('Data not available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col2:
        try:
            by_tretory = db.get_sales_by_territory(option)
            if by_tretory:
                df = pd.DataFrame(by_tretory, columns=['Territory', 'Category', option])
                fig = px.bar(df, x='Territory', y=option, color='Category', 
                            title='Sold Territory', 
                            labels={option: option, 'Category': 'Product Category'},
                            orientation='v',
                            text=option
                            )

                fig.update_layout(
                    xaxis_title="Territory",
                    yaxis_title=option,
                    barmode='stack',
                    coloraxis_colorbar=dict(
                        title="Product Territory"
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Data not available.')  
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    with col3:
        try:
            by_p_region = db.get_sales_by_p_region(option)
            if by_p_region:
                df = pd.DataFrame(by_p_region, columns=['Region', 'Category', option])
                fig = px.bar(df, x=option, y='Region', color='Category', 
                            title='Products Region',
                            labels={option: option, 'Category': 'Product Category'},
                            orientation='h', 
                            text=option)

                fig.update_layout(
                    xaxis_title=option,
                    yaxis_title="Region",
                    barmode='stack',
                    coloraxis_colorbar=dict(
                        title="Product Region"
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Data not available.')
        except Exception as err:
            st.warning('Data not available.')
            logging.error(err)

    year = db.get_years_from_sales_orders()
    
    year = ['All'] + [str(year[0]) for year in year]

    selected_year = st.selectbox('Select Year', 
                                 year, 
                                 key='year_selectbox_subcategory')

    subcategory_data = db.get_subcategory_sales(
        year=None if selected_year == 'All' else int(selected_year),
        option=option
    )

    if subcategory_data:
        df_subcategory = pd.DataFrame(subcategory_data, 
                                      columns=['Subcategory', 
                                               option])
        df_subcategory[option] = df_subcategory[option].astype(float)
        fig = px.bar(df_subcategory, x='Subcategory', 
                     y=option, 
                     title=f'Sales by Product Subcategory for {selected_year}')
        fig.update_layout(xaxis_title='Product Subcategory', 
                          yaxis_title='Total Sales', 
                          xaxis_tickangle=-45)

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


