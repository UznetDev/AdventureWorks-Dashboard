import logging
import sys
import streamlit as st
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
total_line = db.get_total_line()

st.header(':blue[AdventureWorks] Dashboard')
# Header
col1, col2, col3, col4, col5, col6 = st.columns(6)

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
    text1 = '<p style="font-family:sans-serif; color:White; font-size: 15px;">Total Line: 📖 </p>'
    text2 = f'<p style="font-family:sans-serif; color:red; font-size: 20px;">{abbreviate_number(total_line)}</p>'
    st.markdown(text1, unsafe_allow_html=True)
    st.markdown(text2, unsafe_allow_html=True)

with col6:
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

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

with col1:
    if st.button("Page 1"):
        st.session_state["nav"] = "1"
with col2:
    if st.button("Page 2"):
        st.session_state["nav"] = "2"
with col3:
    if st.button("Page 3"):
        st.session_state["nav"] = "3"
with col4:
    if st.button("Page 4"):
        st.session_state["nav"] = "4"
with col5:
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
    from app.page5 import app
    app(option=option)
elif selected_page == "m":
    from app.model import app
    app()



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



