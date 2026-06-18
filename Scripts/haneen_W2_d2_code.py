import streamlit as st
import pandas as pd

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Load Data
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        r"C:\Users\h1n2e\OneDrive\Desktop\project_4.1\data\superstore_cleaned.csv",
        parse_dates=["order_date", "ship_date"]
    )

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# --------------------------------
# Page Title
# --------------------------------
st.title("📊 Superstore Dashboard")
st.markdown("Interactive dashboard for Superstore sales analysis")

# =========================
# SIDEBAR FILTERS
# =========================

with st.sidebar:

    st.header("Filters")

    selected_Regions = st.multiselect(
        "Region",
        options=sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

    selected_years = st.multiselect(
        "Year",
        options=sorted(df["order_year"].unique()),
        default=sorted(df["order_year"].unique())
    )

    start_date = st.date_input(
        "Start Date",
        value=df["order_date"].min().date()
    )

    end_date = st.date_input(
        "End Date",
        value=df["order_date"].max().date()
    )

# =========================
# APPLY FILTERS
# =========================

filtered = df[
    (df["Region"].isin(selected_Regions)) &
    (df["order_year"].isin(selected_years))
]

filtered = filtered[
    filtered["order_date"].dt.date.between(
        start_date,
        end_date
    )
]

# =========================
# KPI ROW
# =========================

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"${filtered['sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${filtered['profit'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Average Discount",
        f"{filtered['discount'].mean():.1%}"
    )

# =========================
# CHARTS
# =========================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Sales by Category")

    category_sales = (
        filtered.groupby("Category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

with col2:

    st.subheader("Profit by Category")

    category_profit = (
        filtered.groupby("Category")["profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_profit)

# =========================
# SALES TREND
# =========================

st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered.groupby(
        filtered["order_date"].dt.to_period("M")
    )["sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)

# =========================
# DATA TABLE
# =========================

st.subheader("Filtered Data")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# =========================
# DOWNLOAD BUTTON
# =========================

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    data=csv,
    file_name="filtered_superstore.csv",
    mime="text/csv"
)

# =========================
# TASK 5 - TABS
# =========================

tab1, tab2, tab3 = st.tabs(
    ["📋 Overview", "📦 By Category", "🗺️ By Region"]
)

# Overview Tab
with tab1:
    st.subheader("Filtered Data Preview")

    st.dataframe(
        filtered.head(20),
        use_container_width=True,
        hide_index=True
    )
    st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered.set_index("order_date")
    .resample("ME")["sales"]
    .sum()
)

st.line_chart(monthly_sales)

# By Category Tab
with tab2:
    st.subheader("Sales by Category")

    category_sales = (
        filtered.groupby("Category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)
    st.subheader("Sub-Category Breakdown")

    subcategory_summary = (
        filtered.groupby("sub_category")
        .agg(
            Total_Sales=("sales", "sum"),
            Total_Profit=("profit", "sum")
        )
        .sort_values(
            by="Total_Sales",
            ascending=False
        )
    )

    st.dataframe(
        subcategory_summary.style.format("${:,.0f}"),
        use_container_width=True
    )

# By Region Tab
with tab3:

    st.subheader("Sales by Region")

    Region_sales = (
        filtered.groupby("Region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.area_chart(Region_sales)

   


# =========================
# TASK 6 - FOOTER CAPTION
# =========================

st.markdown("---")

row_count = len(filtered)

min_year = filtered["order_year"].min()
max_year = filtered["order_year"].max()

st.caption(
    f"Showing {row_count:,} rows • "
    f"{min_year}–{max_year} • "
    f"Built by Haneen Aslam"
)