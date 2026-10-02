"""Gera sales.db (SQLite) com dados sinteticos de um varejo ficticio.

Cria 3 tabelas: products, customers, orders. Todos os dados sao gerados com
Faker (nenhum dado real). Rode este script antes de build_report.py.

Uso:
    python src/generate_db.py
"""
import os
import random
import sqlite3

from faker import Faker

DB_PATH = os.path.join(os.path.dirname(__file__), "sales.db")
SEED = 42
N_PRODUCTS = 20
N_CUSTOMERS = 60
N_ORDERS = 400

CATEGORIES = ["Eletronicos", "Casa", "Moda", "Esporte", "Beleza", "Livros"]


def build_schema(conn):
    conn.executescript(
        """
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
            product_id INTEGER NOT NULL REFERENCES products(product_id),
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total REAL NOT NULL
        );
        """
    )


def generate(conn, fake: Faker):
    products = []
    for i in range(1, N_PRODUCTS + 1):
        category = random.choice(CATEGORIES)
        products.append((i, f"{category} {fake.unique.word().capitalize()}", category, round(random.uniform(15, 800), 2)))
    conn.executemany("INSERT INTO products VALUES (?,?,?,?)", products)

    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        customers.append((i, fake.name(), fake.unique.email(), fake.city()))
    conn.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)

    orders = []
    for i in range(1, N_ORDERS + 1):
        customer_id = random.randint(1, N_CUSTOMERS)
        product_id = random.randint(1, N_PRODUCTS)
        price = products[product_id - 1][3]
        quantity = random.randint(1, 5)
        order_date = fake.date_between(start_date="-180d", end_date="today").isoformat()
        total = round(price * quantity, 2)
        orders.append((i, customer_id, product_id, quantity, order_date, total))
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)


def main():
    random.seed(SEED)
    fake = Faker("pt_BR")
    Faker.seed(SEED)

    conn = sqlite3.connect(DB_PATH)
    try:
        build_schema(conn)
        generate(conn, fake)
        conn.commit()
    finally:
        conn.close()

    print(f"Banco gerado em {DB_PATH} ({N_PRODUCTS} produtos, {N_CUSTOMERS} clientes, {N_ORDERS} pedidos).")


if __name__ == "__main__":
    main()
