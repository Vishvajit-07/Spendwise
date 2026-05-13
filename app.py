import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="SpendWise", layout="wide")
st.title("📊 SpendWise: Permanent Tracker")

# --- DATABASE LOGIC ---
DATA_FILE = "expenses.csv"

# Function to load data from the CSV file
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

# Load the current data
df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Log Daily Expense")
# 1. Added Date Wise Input
add_date = st.sidebar.date_input("Select Date")
add_cat = st.sidebar.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills", "Other"])
add_amt = st.sidebar.number_input("Amount (₹)", min_value=0, step=50)

if st.sidebar.button("Save Permanently"):
    # Create new entry
    new_entry = pd.DataFrame([[add_date, add_cat, add_amt]], columns=['Date', 'Category', 'Amount'])
    # Combine with old data
    df = pd.concat([df, new_entry], ignore_index=True)
    # Save back to CSV file
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success(f"Saved for {add_date}!")
    st.rerun()

# --- DASHBOARD ---
st.write("### Expense Overview")

if df.empty:
    st.info("No data found. Add your first expense in the sidebar!")
else:
    # Show Date-wise table
    st.write("#### Detailed Transaction Table")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

    # Pie Chart based on Categories
    fig = px.pie(df, values='Amount', names='Category', title="Total Spending by Category")
    st.plotly_chart(fig, use_container_width=True)

