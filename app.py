import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SpendWise", layout="wide")
st.title("📊 SpendWise: Personal Finance Predictor")

# 1. Initialize an EMPTY storage (No default values)
if 'my_data' not in st.session_state:
    st.session_state.my_data = pd.DataFrame(columns=['Category', 'Amount'])

# 2. Sidebar for adding data
st.sidebar.header("Add New Expense")
add_cat = st.sidebar.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills"])
add_amt = st.sidebar.number_input("Amount", min_value=0, step=100)

if st.sidebar.button("Add Expense"):
    new_row = pd.DataFrame({'Category': [add_cat], 'Amount': [add_amt]})
    st.session_state.my_data = pd.concat([st.session_state.my_data, new_row], ignore_index=True)
    st.sidebar.success(f"Added ₹{add_amt}!")

# 3. Main Dashboard
st.write("### Expense Overview")

if st.session_state.my_data.empty:
    st.info("Your dashboard is currently empty. Add an expense in the sidebar to see the chart!")
else:
    # This chart ONLY appears once you add data
    fig = px.pie(st.session_state.my_data, values='Amount', names='Category', title="My Real-Time Spending")
    st.plotly_chart(fig, use_container_width=True)
    st.table(st.session_state.my_data)
    
