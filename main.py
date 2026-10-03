import sqlite3
import pandas as pd
import os

DATA_PATH = os.path.join("data", "shop.sqlite")
OUTPUT_PATH = os.path.join("output", "shop_analysis.sqlite")

conn = sqlite3.connect(DATA_PATH)

products = pd.read_sql("SELECT * FROM products", conn)
sales = pd.read_sql("SELECT * FROM sales", conn)

print(products.head())
print(sales.head())

conn.close()

products_renamed = products.rename(columns={"id": "product_id"})
merged = sales.merge(products_renamed, on="product_id", how="inner")
merged["total"] = merged["quantity"] * merged["price"]

product_statistics = (
    merged.groupby("product_id", as_index=False)
    .agg(
        name=("name", "first"),
        category=("category", "first"),
        quantity_sold=("quantity", "sum"),
        total_sales=("total", "sum"),
    )
    .drop(columns=["product_id"])
)
print(product_statistics.head())
print()

category_statistics = (
    merged.groupby("category", as_index=False)
    .agg(
        operations=("id", "count"),
        units_sold=("quantity", "sum"),
        total_sales=("total", "sum"),
        avg_sale=("total", "mean"),
    )
)

print(category_statistics)
print()

top_products = (
    product_statistics
    .nlargest(5, "quantity_sold")
    [["name", "category", "quantity_sold", "total_sales"]]
    .reset_index(drop=True)
)

print(top_products)

os.makedirs("output", exist_ok=True)

out_conn = sqlite3.connect(OUTPUT_PATH)
product_statistics.to_sql("product_statistics", out_conn, if_exists="replace", index=False)
category_statistics.to_sql("category_statistics", out_conn, if_exists="replace", index=False)
top_products.to_sql("top_products", out_conn, if_exists="replace", index=False)

out_conn.close()
