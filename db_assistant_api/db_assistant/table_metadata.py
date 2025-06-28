"""Static placeholder for table & column metadata.
Replace with dynamic discovery from Trino/Iceberg as needed."""

from __future__ import annotations

TABLES_MD = """
orders (order_id INT, order_date DATE, customer_id INT, region STRING, amount DOUBLE)
customers (customer_id INT, customer_name STRING, region STRING)
"""
