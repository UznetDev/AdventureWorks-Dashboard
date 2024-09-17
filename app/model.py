import streamlit as st
import pandas as pd
import logging
import sys
import joblib
from loader import *
from datetime import datetime


def app():
    model = joblib.load('model.pkl')


    colors = db.get_color()
    categories = db.get_categories()
    ship_methods = db.get_ship_method()

    current_date = datetime.now().date()
    current_year = current_date.year
    current_day = current_date.day


    st.title("Sales TotalDue Prediction")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        SalesOrderID = 0 #st.number_input('SalesOrderID', min_value=1)
        OnlineOrderFlag = st.selectbox('OnlineOrderFlag', [0, 1])
        SalesOrderNumber = 0 #st.number_input('SalesOrderNumber', min_value=1)
        PurchaseOrderNumber = 0 #st.number_input('PurchaseOrderNumber', min_value=1)
        OrderQty = st.number_input('OrderQty', min_value=1, value=1)
        AccountNumber = st.number_input('AccountNumber', min_value=1)
        CustomerID = st.number_input('CustomerID', min_value=1)

    with col2:
        LineTotal = st.number_input('LineTotal', value=0.0)
        StandardCost = st.number_input('StandardCost', value=0.0)
        ListPrice = st.number_input('ListPrice', value=0.0)

    with col3:
        Color = st.selectbox('Color', options=colors)
        CategoryName = st.selectbox('CategoryName', options=categories)
        ShipMethodName = st.selectbox('ShipMethodName', options=ship_methods)

    with col4:
        OrderDate = st.date_input('Order Date', current_date)
        DueDate = st.date_input('Due Date', current_date)
        ShipDate = st.date_input('Ship Date', current_date)


    OrderDate_Day = OrderDate.day
    OrderDate_Year = OrderDate.year
    DueDate_Day = DueDate.day
    DueDate_Year = DueDate.year
    ShipDate_Day = ShipDate.day
    ShipDate_Year = ShipDate.year


    input_data = pd.DataFrame({
        'SalesOrderID': [SalesOrderID],
        'OnlineOrderFlag': [OnlineOrderFlag],
        'SalesOrderNumber': [SalesOrderNumber],
        'PurchaseOrderNumber': [PurchaseOrderNumber],
        'OrderQty': [OrderQty],
        'LineTotal': [LineTotal],
        'StandardCost': [StandardCost],
        'ListPrice': [ListPrice],
        'CustomerID': [CustomerID],
        'AccountNumber': [AccountNumber],
        'OrderDate_Day': [OrderDate_Day],
        'OrderDate_Year': [OrderDate_Year],
        'DueDate_Day': [DueDate_Day],
        'DueDate_Year': [DueDate_Year],
        'ShipDate_Day': [ShipDate_Day],
        'ShipDate_Year': [ShipDate_Year],
        'Color': [Color],
        'CategoryName': [CategoryName],
        'ShipMethodName': [ShipMethodName],
        'DueDate': [DueDate],
        'ShipDate': [ShipDate],
        'OrderDate': [OrderDate]
    })
    with col2:
        if st.button('Predict TotalDue'):
            prediction = model.predict(input_data)
            with col3:
                st.write(f'Predicted TotalDue: {prediction[0]:.2f}')


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