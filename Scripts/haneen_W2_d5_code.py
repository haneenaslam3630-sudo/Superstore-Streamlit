import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Superstore Dashboard")
st.markdown("Interactive dashboard for Superstore sales analysis")



@st.cache_data(ttl=600)  
def load_data():
    return pd.read_csv(
        r"data/superstore_cleaned.csv",
        parse_dates=["order_date", "ship_date"]
    )

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

if st.button("refresh data"):
    st.cache_data.clear()  
    st.rerun()






with st.sidebar:

    st.header("Filters")

    selected_regions = st.multiselect(
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

filtered = df[
    (df["Region"].isin(selected_regions)) &
    (df["order_year"].isin(selected_years))
]

filtered = filtered[
    filtered["order_date"].dt.date.between(
        start_date,
        end_date
    )
]

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    "Download Filtered Data",
    data=csv_bytes,
    file_name="filtered_superstore.csv",
    mime="text/csv"
)


arr = pd.to_numeric(df["discount"], errors="coerce").dropna().to_numpy(dtype=float)
if arr.size > 0:
    per75 = np.percentile(arr, 75)
else:
    per75 = 0.0
high = df[pd.to_numeric(df["discount"], errors="coerce") > per75]

print(f"75th percentile of discount: {per75:.2f}")
print(f"Number of high discount records: {len(high)}")


    
sales_arr = pd.to_numeric(filtered["sales"], errors="coerce").dropna().to_numpy(dtype=float)
if sales_arr.size == 0:
        z = np.array([])
else:
        std = np.std(sales_arr)
        if std == 0:
            z = np.zeros_like(sales_arr)
        else:
            z = (sales_arr - np.mean(sales_arr)) / std
outliers = filtered.iloc[np.where(np.abs(z) > 2)[0]] if z.size > 0 else filtered.iloc[0:0]
print(f"outliers detected: {len(outliers)}")




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



st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered.groupby(
        filtered["order_date"].dt.to_period("M")
    )["sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)


st.subheader("Filtered Data")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)



csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    data=csv,
    file_name="filtered_superstore.csv",
    mime="text/csv"
)



tab1, tab2, tab3, tab4= st.tabs(
    ["📋 Overview", "📦 By Category", "🗺️ By Region", "🚨 Quality Alerts"]
)


with tab1:
    st.subheader("Filtered Data Preview")

    df["order_year"] = df["order_date"].dt.year
    df["month_period"] = df["order_date"].dt.strftime("%b")

    monthly_sales = (
    df.groupby(["order_year", "month_period"], as_index=False)["sales"]
      .sum()
    )

    fig = px.line(
    monthly_sales,
    x="month_period",
    y="sales",
    color="order_year",
    title="Monthly Sales Trend by Category"
    )
    st.plotly_chart(fig, use_container_width=True)


with tab2:
    st.subheader("Sales by Category")

    top10_subcat = (
    df.groupby("sub_category")["sales"]
      .sum()
      .nlargest(10)        
      .sort_values()         
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.barh(
    top10_subcat.index,
    top10_subcat.values,
    color="#3B82F6"

    )

  
    ax.bar_label(
    bars,
    fmt="${:,.0f}",
    padding=4,
    fontsize=8
    )

    ax.set_title("Top 10 Sub-Categories by Sales")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Sub-Category")

    st.pyplot(fig)
    plt.close(fig)

    fig = px.scatter(
    df,
    x="sales",
    y="profit",
    color="Category",         
    size="quantity",           
    hover_data=["sub_category"],
    title="Sales vs Profit by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

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


with tab3:

    st.subheader("Sales by Region")

    
    region_profit = (
    filtered.groupby("Region")["profit"]
      .sum()
      .reset_index()
    )

    fig = px.pie(
    region_profit,
    names="Region",
    values="profit",
    hole=0.4,
    title="Region Share of Total Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Quality Alerts")

    mean_margin = (filtered["profit"].sum() / filtered["sales"].sum()) * 100

    if mean_margin < 10:
         st.error(f"critical {mean_margin:.2f}% - urgent action needed!")
    elif mean_margin < 20:
        st.warning(f"moderate {mean_margin:.2f}% - improvement needed!")
    else:
        st.success(f"healthy {mean_margin:.2f}% - good performance!")


    st.info(f"75th percentile of discount: {per75:.2f}")
    if len(high) > 0:
        st.warning(f"Number of high discount records: {len(high)}")
    else:
        st.success("No high discount records found.")

    with st.expander("show raw data(first 50 rows)"):
        st.dataframe(filtered.head(50), use_container_width=True)


bar_sales = filtered.groupby("Category")["sales"].sum().sort_values(ascending=False)
fig_bar, ax = plt.subplots(figsize=(7, 4))
ax.barh(bar_sales.index.astype(str), bar_sales.to_numpy(dtype=float), color="#3B82F6")
ax.set_title("Sales by Category")
ax.set_xlabel("Sales ($)")
ax.set_ylabel("Category")
fig_bar.tight_layout()

monthly_sales_export = (
    filtered.groupby(filtered["order_date"].dt.to_period("M"))["sales"]
    .sum()
    .reset_index()
)
monthly_sales_export["order_month"] = monthly_sales_export["order_date"].astype(str)

fig_line = px.line(
    monthly_sales_export,
    x="order_month",
    y="sales",
    title="Monthly Sales Trend"
)

fig_scatter = px.scatter(
    filtered,
    x="sales",
    y="profit",
    color="Category",
    size="quantity",
    hover_data=["sub_category"],
    title="Sales vs Profit by Category"
)

fig_donut = px.pie(
    filtered.groupby("Region")["profit"].sum().reset_index(),
    names="Region",
    values="profit",
    hole=0.4,
    title="Region Share of Total Profit"
)

with st.form("export"):
    chart_type = st.selectbox(
        "Select chart to display",
        [
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Donut Chart"
        ]
    )

    submitted = st.form_submit_button("Generate Chart")

if submitted:
    if chart_type == "Bar Chart":
        st.pyplot(fig_bar)

    elif chart_type == "Line Chart":
        st.plotly_chart(fig_line, use_container_width=True)

    elif chart_type == "Scatter Plot":
        st.plotly_chart(fig_scatter, use_container_width=True)

    elif chart_type == "Donut Chart":
        st.plotly_chart(fig_donut, use_container_width=True)



    



st.markdown("---")

row_count = len(filtered)

min_year = filtered["order_year"].min()
max_year = filtered["order_year"].max()

st.caption(
    f"Showing {row_count:,} rows • "
    f"{min_year}–{max_year} • "
    f"Built by Haneen Aslam"
)