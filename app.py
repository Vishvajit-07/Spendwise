import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="SpendWise", layout="wide")
st.title("📊 SpendWise: Personal Finance Predictor")

# Sidebar for adding data
st.sidebar.header("Add New Expense")
add_date = st.sidebar.date_input("Date")
add_cat = st.sidebar.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills"])
add_amt = st.sidebar.number_input("Amount", min_value=0)

if st.sidebar.button("Add Expense"):
    st.sidebar.success(f"Added ₹{add_amt} to {add_cat}")

# Main Dashboard
st.write("### Expense Overview")
st.info("This is your live capstone project dashboard. Once you upload data, charts will appear here!")

# Sample Chart (to show it works)
chart_data = pd.DataFrame({
    'Category': ["Food", "Transport", "Rent", "Shopping", "Bills"],
    'Amount': [2000, 1500, 5000, 3000, 1200]
})
fig = px.pie(chart_data, values='Amount', names='Category', title="Sample Spending Distribution")
st.plotly_chart(fig)
