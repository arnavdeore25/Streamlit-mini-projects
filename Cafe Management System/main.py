import sqlite3


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

DB_NAME = "cafe.db"

INITIAL_MENU = [
    ("Cappuccino", "Beverages", 120.0, 30),
    ("Cold Coffee", "Beverages", 150.0, 25),
    ("Veg Sandwich", "Snacks", 100.0, 20),
    ("French Fries", "Snacks", 90.0, 35),
    ("Chicken Burger", "Main Course", 180.0, 15),
    ("White Sauce Pasta", "Main Course", 220.0, 20),
    ("Chocolate Brownie", "Desserts", 130.0, 12),
    ("Ice Cream", "Desserts", 80.0, 25),
]

def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.execute("pragma foreign_keys = on;")
    return conn

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            create table if not exists menu (
                item_id integer primary key autoincrement,
                item_name text not null,
                category text not null,
                price real not null check(price >= 0),
                stock integer not null check(stock >= 0)
            )
        """)
        conn.execute("""
            create table if not exists orders (
                order_id integer primary key autoincrement,
                customer_name text not null,
                order_date text not null,
                total_amount real not null,
                discount real not null,
                final_amount real not null,
                status text not null check(status in ('Completed', 'Cancelled'))
            )
        """)
        conn.execute("""
            create table if not exists order_details (
                detail_id integer primary key autoincrement,
                order_id integer not null,
                item_id integer not null,
                quantity integer not null check(quantity > 0),
                unit_price real not null,
                subtotal real not null,
                foreign key(order_id) references orders(order_id),
                foreign key(item_id) references menu(item_id)
            )
        """)
        count = conn.execute("select count(*) from menu").fetchone()[0]
        if count == 0:
            conn.executemany(
                "insert into menu (item_name, category, price, stock) values (?, ?, ?, ?)",
                INITIAL_MENU,
            )

def read_query(query, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def get_menu():
    return read_query("select item_id, item_name, category, price, stock from menu order by item_id")


def get_stock_status(stock):
    if stock == 0:
        return "Out of Stock"
    if stock <= 5:
        return "Critical Stock"
    if stock <= 10:
        return "Low Stock"
    return "Sufficient Stock"


def get_discount_rate(total):
    if total >= 1500:
        return 0.15
    if total >= 1000:
        return 0.10
    if total >= 500:
        return 0.05
    return 0.0


def money(value):
    return f"₹{value:,.2f}"

#page config

st.set_page_config(
    page_title="Cafe Management System",
    page_icon="☕",
    layout="wide",
)

initialize_database()

if "cart" not in st.session_state:
    st.session_state.cart = {}

st.title("☕ Smart Café Management System")
st.caption("Manage menu items, customer orders, inventory and café sales.")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Manage Menu",
        "Place Order",
        "Order History",
        "Inventory Management",
        "Sales Reports",
    ],
)

#dashboard
if page == "Dashboard":
    st.header("Dashboard")
    menu_df = get_menu()
    order_df = read_query("select * from orders")

    completed = order_df[order_df["status"] == "Completed"] if not order_df.empty else order_df
    revenue = float(completed["final_amount"].sum()) if not completed.empty else 0.0
    completed_count = len(completed)
    average_order = revenue / completed_count if completed_count else 0.0
    low_stock_count = int(menu_df["stock"].between(1, 10).sum()) if not menu_df.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Net Revenue", money(revenue))
    c2.metric("Completed Orders", completed_count)
    c3.metric("Average Order Value", money(average_order))
    c4.metric("Low / Critical Stock Items", low_stock_count)

    st.subheader("Current Menu")
    st.dataframe(menu_df, use_container_width=True, hide_index=True)

    if not order_df.empty:
        st.subheader("Recent Orders")
        recent = read_query(
            "select order_id, customer_name, order_date, final_amount, status "
            "from orders order by order_id desc limit 5"
        )
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("No orders have been placed yet.")

