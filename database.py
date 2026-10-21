# database.py
# B.D. function
from config import connection, cursor

def register_user(telegram_id, username):
    cursor.execute("""
        SELECT client_id
        FROM customers.customers
        WHERE telegram_id = %s
    """, (telegram_id,))

    user = cursor.fetchone()

    if user is None:
        cursor.execute("""
            INSERT INTO customers.customers(
                telegram_id,
                username
            )
            VALUES(%s,%s)
        """, (telegram_id, username))

        connection.commit()


def get_client_id(telegram_id):
    cursor.execute("""
        SELECT client_id
        FROM customers.customers
        WHERE telegram_id = %s
    """, (telegram_id,))

    result = cursor.fetchone()

    return result[0]


def get_products():
    cursor.execute("""
    SELECT
        product_id,
        product_name,
        price,
        photo
    FROM products.products
    ORDER BY product_id
    """)

    return cursor.fetchall()


def get_product_by_id(product_id):
    cursor.execute("""
        SELECT
            product_name,
            price,
            photo
        FROM products.products
        WHERE product_id = %s
    """, (product_id,))

    return cursor.fetchone()


def create_order(client_id):
    cursor.execute("""
        INSERT INTO orders.orders(client_id)
        VALUES(%s)
        RETURNING order_id
    """, (client_id,))

    order_id = cursor.fetchone()[0]
    connection.commit()

    return order_id


def add_product_to_order(order_id, product_id, quantity=1):
    cursor.execute("""
        INSERT INTO orders.order_items(
            order_id,
            product_id,
            quantity
        )
        VALUES(%s,%s,%s)
    """, (order_id, product_id, quantity))

    connection.commit()


# def decrease_stock(product_id):   а это уменьшение stock
#     cursor.execute("""             количество товара но
#         UPDATE products.products      в критерии это
#         SET stock = stock - 1           не входило
#         WHERE product_id = %s
#     """, (product_id,))           если можно то я схолкозю😁
#
#     connection.commit()


def complete_order(order_id):
    cursor.execute("""
        UPDATE orders.orders
        SET status='completed'
        WHERE order_id=%s
    """, (order_id,))

    connection.commit()
