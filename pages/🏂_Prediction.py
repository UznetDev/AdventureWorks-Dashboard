import joblib
import plotly.express as px
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from loader import *
from function.function import *
from datetime import datetime



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


model = joblib.load('model.pkl')

current_date = datetime.now().date()
current_year = current_date.year
current_day = current_date.day


st.title("Sales TotalDue Prediction")


col1, col2, col3 = st.columns(3)

with col1:
    SalesOrderID = st.number_input('SalesOrderID')
    OnlineOrderFlag = st.selectbox('OnlineOrderFlag', [0, 1])
    SalesOrderNumber = st.number_input('SalesOrderNumber', min_value=1)
    PurchaseOrderNumber = st.number_input('PurchaseOrderNumber', min_value=1)
with col2:
    LineTotal = st.number_input('LineTotal', value=0.0)
    StandardCost = st.number_input('StandardCost', value=0.0)
    ListPrice = st.number_input('ListPrice', value=0.0)
    CustomerID = st.number_input('CustomerID')
    AccountNumber = st.number_input('AccountNumber')

with col3:
    OrderDate_Day = st.number_input('OrderDate_Day', min_value=1, max_value=31, value=current_day)
    OrderDate_Year = st.number_input('OrderDate_Year', min_value=2000, max_value=2025, value=current_year)

    DueDate_Day = st.number_input('DueDate_Day', min_value=1, max_value=31, value=current_day)
    DueDate_Year = st.number_input('DueDate_Year', min_value=2000, max_value=2025, value=current_year)

    ShipDate_Day = st.number_input('ShipDate_Day', min_value=1, max_value=31, value=current_day)
    ShipDate_Year = st.number_input('ShipDate_Year', min_value=2000, max_value=2025, value=current_year)


if st.button('Predict TotalDue'):
    if not all([SalesOrderID, SalesOrderNumber, PurchaseOrderNumber, CustomerID, AccountNumber]):
        st.error("Please fill in all the required fields!")
    else:
        input_data = pd.DataFrame({
            'SalesOrderID': [SalesOrderID],
            'OnlineOrderFlag': [OnlineOrderFlag],
            'SalesOrderNumber': [SalesOrderNumber],
            'PurchaseOrderNumber': [PurchaseOrderNumber],
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
            'ShipDate_Year': [ShipDate_Year]
        })

        prediction = model.predict(input_data)
        st.write(f'Predicted TotalDue: {prediction[0]:.2f}')