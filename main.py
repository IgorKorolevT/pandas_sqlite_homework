import sqlite3
import pandas as pd
import os


DATA_PATH = os.path.join("data", "shop.sqlite")


conn = sqlite3.connect(DATA_PATH)

products = pd.read_sql("SELECT * FROM products", conn)
sales = pd.read_sql("SELECT * FROM sales", conn)

print(products.head())
print(sales.head())


conn.close()