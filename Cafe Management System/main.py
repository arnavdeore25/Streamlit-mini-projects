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
