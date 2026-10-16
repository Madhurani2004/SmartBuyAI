import sqlite3

DATABASE_NAME = "smartbuy.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            order_id TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_cost REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_purchase_order(order):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO purchase_orders
        (order_id, quantity, unit_price, total_cost, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            order["order_id"],
            order["quantity"],
            order["unit_price"],
            order["total_cost"],
            order["status"],
        ),
    )

    connection.commit()
    connection.close()


def get_purchase_order(order_id):
    connection = get_connection()

    order = connection.execute(
        "SELECT * FROM purchase_orders WHERE order_id = ?",
        (order_id,),
    ).fetchone()

    connection.close()

    return dict(order) if order else None
