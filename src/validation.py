

import pandas as pd
import re


def validate_customers(customers_df):
    valid_customers = customers_df.copy()
    rejected = []

    # Check duplicate customer IDs
    duplicate_ids = valid_customers[
        valid_customers.duplicated(subset=["customer_id"], keep="first")
    ]

    for _, row in duplicate_ids.iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Duplicate customer ID"
        })

    valid_customers = valid_customers.drop_duplicates(
        subset=["customer_id"], keep="first"
    )

    # Check missing values
    required_columns = ["customer_id", "full_name", "email", "phone", "city"]

    for column in required_columns:
        missing = valid_customers[column].isna()

        for _, row in valid_customers[missing].iterrows():
            rejected.append({
                "record_id": row["customer_id"],
                "reason": f"Missing value in {column}"
            })

        valid_customers = valid_customers.dropna(subset=[column])

    # Check email format
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    valid_email = valid_customers["email"].astype(str).str.match(email_pattern)

    for _, row in valid_customers[~valid_email].iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Invalid email format"
        })

    valid_customers = valid_customers[valid_email]

    return valid_customers, rejected


def validate_orders(orders_df, valid_customer_ids):
    valid_orders = orders_df.copy()
    rejected = []

    # Check duplicate order IDs
    duplicate_ids = valid_orders[
        valid_orders.duplicated(subset=["order_id"], keep="first")
    ]

    for _, row in duplicate_ids.iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Duplicate order ID"
        })

    valid_orders = valid_orders.drop_duplicates(
        subset=["order_id"], keep="first"
    )

    # Check missing values
    required_columns = ["order_id", "customer_id", "order_date", "order_amount"]

    for column in required_columns:
        missing = valid_orders[column].isna()

        for _, row in valid_orders[missing].iterrows():
            rejected.append({
                "record_id": row["order_id"],
                "reason": f"Missing value in {column}"
            })

        valid_orders = valid_orders.dropna(subset=[column])

    # Check negative order amounts
    valid_orders["order_amount"] = pd.to_numeric(
        valid_orders["order_amount"], errors="coerce"
    )

    invalid_amount = (
        valid_orders["order_amount"].isna()
        | (valid_orders["order_amount"] <= 0)
    )

    for _, row in valid_orders[invalid_amount].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Invalid or non-positive order amount"
        })

    valid_orders = valid_orders[~invalid_amount]

    # Check customer relationship
    invalid_customer = ~valid_orders["customer_id"].isin(valid_customer_ids)

    for _, row in valid_orders[invalid_customer].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Customer ID does not exist"
        })

    valid_orders = valid_orders[~invalid_customer]

    # Check order date format
    valid_dates = pd.to_datetime(
        valid_orders["order_date"],
        format="%Y-%m-%d",
        errors="coerce"
    ).notna()
    for _, row in valid_orders[~valid_dates].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Invalid order date"
        })

    valid_orders = valid_orders[valid_dates]

    return valid_orders, rejected
