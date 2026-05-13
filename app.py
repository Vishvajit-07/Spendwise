import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="SpendWise Pro", layout="wide", page_icon="💰")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 40px; color: #00d4ff; }
    </style>
    """, unsafe_index=True)

st.title("🛡️ SpendWise: Professional Finance Suite")

# --- DATA ENGINE ---
DATA_FILE = "expenses.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE)
        data['Date'] = pd.to_datetime(data['Date'])
        return data
    return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

df = load_data()

# --- SIDEBAR (Pro Inputs) ---
with st.sidebar:
    st.header("📥 Data Entry")
    add_date = st.date_input("Transaction Date")
    add_cat = st.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills", "Health", "Entertainment"])
    add_amt = st.number_input("Amount (₹)", min_value=0, step=10)
    
    if st.button("Add Transaction", use_container_width=True):
        new_entry = pd.DataFrame([[pd.to_datetime(add_date), add_cat, add_amt]], columns=['Date', 'Category', 'Amount'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Transaction Secured!")
        st.rerun()
    
    st.divider()
    monthly_budget = st.slider("Set Monthly Budget (₹)", 1000, 50000, 15000)

# --- MAIN DASHBOARD ---
if df.empty:
    st.info("Welcome! Please log your first transaction in the sidebar to begin.")
else:
    df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
    selected_month = st.selectbox("📅 Select Billing Cycle", df['Month_Year'].unique())
    
    month_df = df[df['Month_Year'] == selected_month].copy()
    total_spent = month_df['Amount'].sum()
    remaining = monthly_budget - total_spent

    # 1. Metric Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₹{total_spent:,.2f}")
    col2.metric("Budget Remaining", f"₹{remaining:,.2f}", delta=f"{ (remaining/monthly_budget)*100:.1f}%")
    col3.metric("Daily Avg", f"₹{ (total_spent/30):,.2f}")

    # 2. Budget Progress Bar
    progress = min(total_spent / monthly_budget, 1.0)
    st.write(f"**Budget Utilization: {progress*100:.1f}%**")
    st.progress(progress)

    st.divider()

    # 3. Charts Row
    c1, c2 = st.columns(2)
    
    with c1:
        fig_pie = px.pie(month_df, values='Amount', names='Category', hole=0.5, 
                         title="Spending by Sector", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        daily_sum = month_df.groupby('Date')['Amount'].sum().reset_index()
        fig_line = px.line(daily_sum, x='Date', y='Amount', title="Daily Spending Trend", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    # 4. Data Table & Download
    st.write("### 📑 Transaction History")
    st.dataframe(month_df[['Date', 'Category', 'Amount']].sort_values(by='Date'), use_container_width=True, hide_index=True)
    
    csv = month_df.to_csv(index=False).encode('utf-8')
    st.download_button("📩 Download Monthly Report (CSV)", data=csv, file_name=f"Spendwise_{selected_month}.csv", mime='text/csv')
    
