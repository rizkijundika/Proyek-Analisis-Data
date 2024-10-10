import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the data
main_data_df = pd.read_csv("main_data.csv")
main_data_df['order_purchase_timestamp'] = pd.to_datetime(main_data_df['order_purchase_timestamp'])

# Sidebar for navigation
st.sidebar.title("E-commerce Dashboard")
page = st.sidebar.selectbox("Select Visualization", ["Top Products Sold Each Year", "States with the Most and Least Orders"])

# Top Products Sold Each Year
if page == "Top Products Sold Each Year":
    st.title("Top Products Sold Each Year")

    # Extract year from 'order_purchase_timestamp'
    main_data_df['order_year'] = main_data_df['order_purchase_timestamp'].dt.year

    # Group by year and product category to get sales summary
    yearly_sales_summary = main_data_df.groupby(['order_year', 'product_category_name_english']).agg(
        total_sales=('order_item_id', 'count'),
        total_revenue=('price', 'sum')
    ).reset_index()

    yearly_sales_summary = yearly_sales_summary.sort_values(by=['order_year', 'total_sales'], ascending=[True, False])
    top_products_per_year = yearly_sales_summary.groupby('order_year').head(5)

    # Visualization for top products sold each year
    st.write("**Top Products Sold Each Year**")
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(data=top_products_per_year, x='order_year', y='total_sales', hue='product_category_name_english', palette='Set2', ax=ax)
    ax.set_title("Top Products Sold Each Year", fontsize=18)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Total Sales", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

# States with the Most and Least Orders
elif page == "States with the Most and Least Orders":
    st.title("States with the Most and Least Orders")

    if 'customer_state' not in main_data_df.columns:
        st.write("Column 'customer_state' not found.")
    else:
        sales_by_state = main_data_df.groupby('customer_state').agg(
            total_orders=('order_id', 'count'),
            total_price=('price', 'sum'),
            total_freight=('freight_value', 'sum')
        ).reset_index()

        sales_by_state['total_revenue'] = sales_by_state['total_price'] + sales_by_state['total_freight']
        sales_by_state = sales_by_state.sort_values(by='total_orders', ascending=False)

        top_5_states = sales_by_state.head(5)
        bottom_5_states = sales_by_state.tail(5)

        # Visualization for states with the most orders
        st.write("**Top 5 States with the Most Orders**")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_5_states, y='customer_state', x='total_orders', palette='viridis', ax=ax)
        ax.set_title("Top 5 States with the Most Orders", fontsize=20, fontweight='bold')
        ax.set_xlabel("Number of Orders", fontsize=14)
        ax.set_ylabel("State", fontsize=14)
        ax.grid(axis='x', linestyle='--', alpha=0.6)
        st.pyplot(fig)

        # Visualization for states with the least orders
        st.write("**Top 5 States with the Least Orders**")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=bottom_5_states, y='customer_state', x='total_orders', palette='magma', ax=ax)
        ax.set_title("Top 5 States with the Least Orders", fontsize=20, fontweight='bold')
        ax.set_xlabel("Number of Orders", fontsize=14)
        ax.set_ylabel("State", fontsize=14)
        ax.grid(axis='x', linestyle='--', alpha=0.6)
        st.pyplot(fig)
