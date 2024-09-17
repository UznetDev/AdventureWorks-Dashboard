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


