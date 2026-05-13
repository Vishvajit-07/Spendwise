import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="SpendWise", layout="wide")
st.title("📊 SpendWise: Monthly Expense Tracker")

# --- DATABASE LOGIC ---
DATA_FILE = "expenses.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE)
        data['Date'] = pd.to_datetime(data['Date'])
        return data
    return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

df = load_data()

# --- SIDEBAR: DAILY ENTRY ---
st.sidebar.header("📝 Log Daily Expense")
add_date = st.sidebar.date_input("Transaction Date")
add_cat = st.sidebar.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills", "Other"])
add_amt = st.sidebar.number_input("Amount (₹)", min_value=0, step=10)

if st.sidebar.button("Save Entry"):
    new_entry = pd.DataFrame([[pd.to_datetime(add_date), add_cat, add_amt]], columns=['Date', 'Category', 'Amount'])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success(f"Logged: ₹{add_amt}")
    st.rerun()

# --- MAIN DASHBOARD: MONTHLY FILTER ---
if df.empty:
    st.info("No data yet. Use the sidebar to add an expense!")
else:
    # 1. Create a Month-Year selector
    df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
    unique_months = df['Month_Year'].unique()
    
    selected_month = st.selectbox("Select Month to View Dashboard", unique_months)

    # 2. Filter data for that month ONLY
    month_df = df[df['Month_Year'] == selected_month].copy()
    total_spent = month_df['Amount'].sum()

    st.write(f"### Expense Analysis for {selected_month}")
    st.metric("Total Monthly Spending", f"₹{total_spent:,.2f}")

    # 3. Monthly Pie Chart
    fig = px.pie(month_df, values='Amount', names='Category', title=f"Spending Distribution ({selected_month})")
    st.plotly_chart(fig, use_container_width=True)

    # 4. Monthly Table (Daily breakdown)
    st.write(f"#### Detailed Transactions: {selected_month}")
    month_df['Date'] = month_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(month_df[['Date', 'Category', 'Amount']].sort_values(by='Date'), use_container_width=True, hide_index=True)
    

