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

SalesOrderID = st.text_input('SalesOrderID')
OnlineOrderFlag = st.selectbox('OnlineOrderFlag', [0, 1])
SalesOrderNumber = st.text_input('SalesOrderNumber')
PurchaseOrderNumber = st.text_input('PurchaseOrderNumber')
OrderQty = st.number_input('OrderQty', min_value=1, value=1)
LineTotal = st.number_input('LineTotal', value=0.0)
StandardCost = st.number_input('StandardCost', value=0.0)
ListPrice = st.number_input('ListPrice', value=0.0)
CustomerID = st.text_input('CustomerID')
AccountNumber = st.text_input('AccountNumber')

OrderDate_Day = st.number_input('OrderDate_Day', min_value=1, max_value=31, value=current_day)  # Hozirgi kun
OrderDate_Year = st.number_input('OrderDate_Year', min_value=2000, max_value=2025, value=current_year)  # Hozirgi yil

DueDate_Day = st.number_input('DueDate_Day', min_value=1, max_value=31, value=current_day)  # Hozirgi kun
DueDate_Year = st.number_input('DueDate_Year', min_value=2000, max_value=2025, value=current_year)  # Hozirgi yil

ShipDate_Day = st.number_input('ShipDate_Day', min_value=1, max_value=31, value=current_day)  # Hozirgi kun
ShipDate_Year = st.number_input('ShipDate_Year', min_value=2000, max_value=2025, value=current_year)  # Hozirgi yil

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

# Model bilan prognoz qilish
if st.button('Predict TotalDue'):
    prediction = model.predict(input_data)
    st.write(f'Predicted TotalDue: {prediction[0]:.2f}')