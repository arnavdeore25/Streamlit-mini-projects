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


# menu management

elif page == "Manage Menu":
    st.header("Manage Menu")
    menu_df = get_menu()

    st.subheader("Existing Menu Items")
    st.dataframe(menu_df, use_container_width=True, hide_index=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Add a Menu Item")
        with st.form("add_menu_form", clear_on_submit=True):
            #st.number_input("Item ID", min_value=1, step=1)
            new_name = st.text_input("Item Name")
            new_category = st.selectbox(
                "Category", ["Beverages", "Snacks", "Main Course", "Desserts", "Other"]
            )
            new_price = st.number_input("Price (₹)", min_value=0.0, step=5.0)
            new_stock = st.number_input("Initial Stock", min_value=0, step=1)
            add_clicked = st.form_submit_button("Add Item")

        if add_clicked:
            if not new_name.strip():
                st.error("Item name cannot be empty.")
            else:
                try:
                    with get_connection() as conn:
                        conn.execute(
                            "insert into menu (item_name, category, price, stock) "
                            "values (?, ?, ?, ?)",
                            (new_name.strip(), new_category, float(new_price), int(new_stock)),
                        )
                    st.success("Menu item added successfully.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("This item ID already exists or the supplied values are invalid.")
                except sqlite3.Error as error:
                    st.error(f"Database error: {error}")

    with right:
        st.subheader("Update Price or Stock")
        if not menu_df.empty:
            selected_update = st.selectbox(
                "Select item to update",
                menu_df["item_id"].tolist(),
                format_func=lambda x: f"{x} - {menu_df.loc[menu_df.item_id == x, 'item_name'].iloc[0]}",
            )
            current = menu_df[menu_df["item_id"] == selected_update].iloc[0]
            with st.form("update_menu_form"):
                updated_price = st.number_input(
                    "New Price (₹)", min_value=0.0, value=float(current["price"]), step=5.0
                )
                updated_stock = st.number_input(
                    "New Stock", min_value=0, value=int(current["stock"]), step=1
                )
                update_clicked = st.form_submit_button("Update Item")
            if update_clicked:
                try:
                    with get_connection() as conn:
                        conn.execute(
                            "update menu set price = ?, stock = ? where item_id = ?",
                            (float(updated_price), int(updated_stock), int(selected_update)),
                        )
                    st.success("Menu item updated.")
                    st.rerun()
                except sqlite3.Error as error:
                    st.error(f"Database error: {error}")

    st.divider()
    st.subheader("Delete a Menu Item")
    if not menu_df.empty:
        delete_id = st.selectbox(
            "Choose item to delete",
            menu_df["item_id"].tolist(),
            format_func=lambda x: f"{x} - {menu_df.loc[menu_df.item_id == x, 'item_name'].iloc[0]}",
            key="delete_item_select",
        )
        if st.button("Delete Selected Item", type="secondary"):
            try:
                with get_connection() as conn:
                    used = conn.execute(
                        "select count(*) from order_details where item_id = ?", (int(delete_id),)
                    ).fetchone()[0]
                    if used:
                        st.error("Cannot delete this item because it has associated order history.")
                    else:
                        conn.execute("delete from menu where item_id = ?", (int(delete_id),))
                        st.success("Menu item deleted.")
                        st.rerun()
            except sqlite3.Error as error:
                st.error(f"Database error: {error}")

#billing & order place

elif page == "Place Order":
    st.header("Place Customer Order")
    menu_df = get_menu()

    if menu_df.empty:
        st.warning("There are no menu items available.")
    else:
        customer_name = st.text_input("Customer Name")
        st.subheader("Select Items")

        available_items = menu_df[menu_df["stock"] > 0]
        if available_items.empty:
            st.warning("All menu items are currently out of stock.")
        else:
            for _, item in available_items.iterrows():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                col1.write(f"**{item['item_name']}**")
                col1.caption(f"{item['category']} · {money(item['price'])} · Stock: {item['stock']}")
                quantity = col2.number_input(
                    "Quantity",
                    min_value=0,
                    max_value=int(item["stock"]),
                    value=int(st.session_state.cart.get(int(item["item_id"]), 0)),
                    step=1,
                    key=f"qty_{int(item['item_id'])}",
                )
                if quantity > 0:
                    st.session_state.cart[int(item["item_id"])] = int(quantity)
                else:
                    st.session_state.cart.pop(int(item["item_id"]), None)
                col3.write(f"Subtotal: {money(float(item['price']) * quantity)}")
                col4.write("Available")

        cart_rows = []
        total = 0.0
        for item_id, quantity in st.session_state.cart.items():
            row = menu_df[menu_df["item_id"] == item_id]
            if not row.empty and quantity > 0:
                item = row.iloc[0]
                subtotal = float(item["price"]) * int(quantity)
                total += subtotal
                cart_rows.append(
                    {
                        "Item": item["item_name"],
                        "Quantity": int(quantity),
                        "Unit Price": float(item["price"]),
                        "Subtotal": subtotal,
                    }
                )

        st.subheader("Shopping Cart")
        if cart_rows:
            st.dataframe(pd.DataFrame(cart_rows), use_container_width=True, hide_index=True)
            discount_rate = get_discount_rate(total)
            discount_amount = total * discount_rate
            final_amount = total - discount_amount

            a, b, c = st.columns(3)
            a.metric("Total", money(total))
            b.metric(f"Discount ({discount_rate:.0%})", money(discount_amount))
            c.metric("Final Payable", money(final_amount))

            if st.button("Confirm Order", type="primary"):
                if not customer_name.strip():
                    st.error("Please enter the customer name.")
                else:
                    try:
                        # Order header, order details and stock changes are one transaction.
                        conn = get_connection()
                        try:
                            conn.execute("begin")
                            for item_id, quantity in st.session_state.cart.items():
                                stock_row = conn.execute(
                                    "select stock from menu where item_id = ?", (int(item_id),)
                                ).fetchone()
                                if stock_row is None or int(quantity) > stock_row[0]:
                                    raise ValueError("Insufficient stock. Please review the cart.")

                            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            cursor = conn.execute(
                                "insert into orders "
                                "(customer_name, order_date, total_amount, discount, final_amount, status) "
                                "values (?, ?, ?, ?, ?, ?)",
                                (
                                    customer_name.strip(),
                                    order_date,
                                    total,
                                    discount_amount,
                                    final_amount,
                                    "Completed",
                                ),
                            )
                            order_id = cursor.lastrowid

                            for item_id, quantity in st.session_state.cart.items():
                                item = conn.execute(
                                    "select price from menu where item_id = ?", (int(item_id),)
                                ).fetchone()
                                unit_price = float(item[0])
                                subtotal = unit_price * int(quantity)
                                conn.execute(
                                    "insert into order_details "
                                    "(order_id, item_id, quantity, unit_price, subtotal) "
                                    "values (?, ?, ?, ?, ?)",
                                    (order_id, int(item_id), int(quantity), unit_price, subtotal),
                                )
                                conn.execute(
                                    "update menu set stock = stock - ? "
                                    "where item_id = ? and stock >= ?",
                                    (int(quantity), int(item_id), int(quantity)),
                                )
                                if conn.execute("select changes()").fetchone()[0] != 1:
                                    raise ValueError("Stock changed during checkout. Please try again.")

                            conn.commit()
                        except Exception:
                            conn.rollback()
                            raise
                        finally:
                            conn.close()

                        st.session_state.cart = {}
                        st.success(f"Order #{order_id} placed successfully. Payable amount: {money(final_amount)}")
                        st.rerun()
                    except ValueError as error:
                        st.error(str(error))
                    except sqlite3.Error as error:
                        st.error(f"Could not complete the order: {error}")
        else:
            st.info("Your cart is empty.")

        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.rerun()


#order history and cancellation
elif page == "Order History":
    st.header("Order History")

    customer_filter = st.text_input("Filter by Customer Name")
    date_filter = st.date_input("Filter by Order Date", value=None)
    status_filter = st.selectbox("Filter by Status", ["All", "Completed", "Cancelled"])

    query = (
        "select order_id, customer_name, order_date, total_amount, discount, "
        "final_amount, status from orders where 1 = 1"
    )
    params = []
    if customer_filter.strip():
        query += " and customer_name like ?"
        params.append(f"%{customer_filter.strip()}%")
    if date_filter:
        query += " and date(order_date) = ?"
        params.append(date_filter.isoformat())
    if status_filter != "All":
        query += " and status = ?"
        params.append(status_filter)
    query += " order by order_id desc"

    orders_df = read_query(query, tuple(params))
    st.dataframe(orders_df, use_container_width=True, hide_index=True)

    if not orders_df.empty:
        st.subheader("View Order Details")
        chosen_order = st.selectbox("Select Order ID", orders_df["order_id"].tolist())
        details = read_query(
            "select m.item_name, od.quantity, od.unit_price, od.subtotal "
            "from order_details od join menu m on od.item_id = m.item_id "
            "where od.order_id = ?",
            (int(chosen_order),),
        )
        st.dataframe(details, use_container_width=True, hide_index=True)

        selected_status = orders_df.loc[
            orders_df["order_id"] == chosen_order, "status"
        ].iloc[0]
        if selected_status == "Completed":
            if st.button("Cancel Selected Order", type="secondary"):
                try:
                    conn = get_connection()
                    try:
                        conn.execute("begin")
                        status = conn.execute(
                            "select status from orders where order_id = ?", (int(chosen_order),)
                        ).fetchone()
                        if status is None or status[0] != "Completed":
                            raise ValueError("This order is already cancelled or does not exist.")

                        order_items = conn.execute(
                            "select item_id, quantity from order_details where order_id = ?",
                            (int(chosen_order),),
                        ).fetchall()
                        for item_id, quantity in order_items:
                            conn.execute(
                                "update menu set stock = stock + ? where item_id = ?",
                                (int(quantity), int(item_id)),
                            )
                        conn.execute(
                            "update orders set status = 'Cancelled' "
                            "where order_id = ? and status = 'Completed'",
                            (int(chosen_order),),
                        )
                        if conn.execute("select changes()").fetchone()[0] != 1:
                            raise ValueError("Cancellation could not be completed.")
                        conn.commit()
                    except Exception:
                        conn.rollback()
                        raise
                    finally:
                        conn.close()
                    st.success(f"Order #{chosen_order} cancelled and stock restored.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
                except sqlite3.Error as error:
                    st.error(f"Database error: {error}")


