import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Personal Expense Tracker")
st.caption(r"C:\Users\h1n2e\OneDrive\Desktop\project_4.1\data\Expense.csv")

uploaded_file = st.file_uploader(
    "Upload your expenses CSV",
    type=["csv"]
)

if uploaded_file is None:

    st.info("No file uploaded — showing sample data.")

    data = {
        "Date": [
            "2024-01-05",
            "2024-01-12",
            "2024-02-01",
            "2024-02-14",
            "2024-03-08"
        ],
        "Category": [
            "Food",
            "Transport",
            "Food",
            "Entertainment",
            "Bills"
        ],
        "Amount": [
            850,
            220,
            1100,
            550,
            2500
        ],
        "Description": [
            "Groceries",
            "Bus pass",
            "Restaurant",
            "Cinema",
            "Electricity"
        ]
    }

    df = pd.DataFrame(data)

else:
    df = pd.read_csv(uploaded_file)

df["Date"] = pd.to_datetime(df["Date"])

st.subheader("Filters")

start_date = df["Date"].min().date()
end_date = df["Date"].max().date()

date_range = st.date_input(
    "Date range",
    value=(start_date, end_date)
)

if len(date_range) == 2:
    start, end = date_range
else:
    start = start_date
    end = end_date

categories = sorted(df["Category"].unique())

selected_categories = st.multiselect(
    "Category",
    options=categories,
    default=categories
)

minimum_amount = st.slider(
    "Minimum amount (₹)",
    min_value=0,
    max_value=int(df["Amount"].max()),
    value=0
)

filtered_df = df[
    (df["Date"].dt.date >= start) &
    (df["Date"].dt.date <= end) &
    (df["Category"].isin(selected_categories)) &
    (df["Amount"] >= minimum_amount)
]

total_spent = filtered_df["Amount"].sum()
transactions = len(filtered_df)
largest_expense = filtered_df["Amount"].max()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Spent",
        f"₹{total_spent:,.0f}"
    )

with col2:
    st.metric(
        "Transactions",
        transactions
    )

with col3:
    st.metric(
        "Largest Expense",
        f"₹{largest_expense:,.0f}"
    )

st.subheader("Filtered Expenses")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)