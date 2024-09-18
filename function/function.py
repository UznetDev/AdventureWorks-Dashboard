import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import time


def abbreviate_number(num):
    """
    Given a large number, this function converts it to an abbreviated format using K (thousands), M (millions), 
    B (billions), and T (trillions) as shorthand notations. 
    It handles both positive and negative numbers. If the input is not a number, it returns the input as is.

    Args:
        num (int or float): The number to be abbreviated.

    Returns:
        str: The abbreviated version of the input number.

    Example:
        abbreviate_number(1500)  # Returns "1.5K"
    """
    try:
        num = int(num)
        if abs(num) < 1000:
            return str(num)
        elif abs(num) < 1000000:
            return f"{num / 1000:.1f}K"
        elif abs(num) < 1000000000:
            return f"{num / 1000000:.1f}M"
        elif abs(num) < 1000000000000:
            return f"{num / 1000000000:.1f}B"
        else:
            return f"{num / 1000000000000:.1f}T"
    except:
        return num
    

def normalize_data(df, value_column, start=-1, end=1, new_column=None, response=False):
    """
    Normalizes the data in a specific column of a Pandas DataFrame between a given range [start, end].
    If `response` is True, the function will return the normalized data as a Pandas Series without altering the DataFrame. 
    Otherwise, it adds a new column to the DataFrame with normalized values.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to normalize.
        value_column (str): The column name whose values need to be normalized.
        start (float, optional): The lower bound of the normalized range. Default is -1.
        end (float, optional): The upper bound of the normalized range. Default is 1.
        new_column (str, optional): The name of the new column to store normalized values. Default is 'NormalizedSales'.
        response (bool, optional): Whether to return the normalized series instead of modifying the DataFrame. Default is False.

    Returns:
        pd.DataFrame or pd.Series: The DataFrame with a new normalized column, or a Series if `response=True`.

    Example:
        df = pd.DataFrame({'Sales': [100, 200, 300]})
        normalize_data(df, 'Sales')  # Adds a 'NormalizedSales' column to the DataFrame
    """
    min_value = df[value_column].min()
    max_value = df[value_column].max()

    if new_column is None:
        new_column = 'NormalizedSales'
        
    if max_value != min_value:
        if response:
            return start + (df[value_column] - min_value) / (max_value - min_value) * (end - start)
        df[new_column] = start + (df[value_column] - min_value) / (max_value - min_value) * (end - start)
    else:
        if response:
            return start
        df[new_column] = start
    
    return df


def write_stream_text(text, sped=0.02):
    """
    Simulates the typing of a string word by word, where each word appears with a delay.
    Useful for creating a dynamic, typing-like effect in applications such as Streamlit.

    Args:
        text (str): The input string to be displayed with a typing effect.
        sped (float, optional): The time delay (in seconds) between each word being displayed. Default is 0.02 seconds.

    Yields:
        str: The next word of the input string to be displayed.

    Example:
        # In a Streamlit application:
        for word in write_stream_text("Hello, this is a typing effect!", sped=0.1):
            st.write(word)
    """
    for word in text.split(" "):
        yield word + " "
        time.sleep(sped)
