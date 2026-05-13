import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="SpendWise Pro", layout="wide", page_icon="💰")

# Fixed the error shown in 1000024086.jpg
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] { font-size: 35px; color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SpendWise: Professional Suite")

DATA_FILE = "expenses.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE)
        data['Date'] = pd.to_datetime(data['Date'])
        return data
    return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📥 Data Entry")
    add_date = st.date_input("Date")
    add_cat = st.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills", "Health", "Other"])
    add_amt = st.number_input("Amount (₹)", min_value=0, step=10)
    
    if st.button("Save Transaction", use_container_width=True):
        new_entry = pd.DataFrame([[pd.to_datetime(add_date), add_cat, add_amt]], columns=['Date', 'Category', 'Amount'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.rerun()
    
    st.divider()
    budget = st.number_input("Monthly Budget", value=10000)

# --- DASHBOARD ---
if df.empty:
    st.info("Log your first transaction to see the dashboard!")
else:
    df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
    selected_month = st.selectbox("Select Month", df['Month_Year'].unique())
    
    m_df = df[df['Month_Year'] == selected_month].copy()
    total = m_df['Amount'].sum()

    # Metrics
    c1, c2 = st.columns(2)
    c1.metric("Total Spent", f"₹{total:,.2f}")
    c2.metric("Budget Left", f"₹{budget - total:,.2f}")

    # Charts
    st.divider()
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_pie = px.pie(m_df, values='Amount', names='Category', hole=0.5, title="Spending by Category")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        daily = m_df.groupby('Date')['Amount'].sum().reset_index()
        fig_line = px.line(daily, x='Date', y='Amount', title="Daily Trend", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    # Data Table
    st.write("### 📑 History")
    m_df['Date'] = m_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(m_df[['Date', 'Category', 'Amount']].sort_values(by='Date'), use_container_width=True, hide_index=True)
    
    
