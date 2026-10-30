
import pandas as pd
import re


# Schema validation function
def check_required_columns(df, required_columns, dataset_name):

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{missing_columns}"
        )


# Validate customer records
def validate_customers(customers_df):

    # Step 1: Check required columns
    required_schema = [
        "customer_id",
        "full_name",
        "email",
        "phone",
        "date_of_birth",
        "city"
    ]

    check_required_columns(
        customers_df,
        required_schema,
        "Customers"
    )

    valid_customers = customers_df.copy()
    rejected = []

    # Step 2: Check duplicate customer IDs
    duplicate_ids = valid_customers[
        valid_customers.duplicated(
            subset=["customer_id"],
            keep="first"
        )
    ]

    for _, row in duplicate_ids.iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Duplicate customer ID"
        })

    valid_customers = valid_customers.drop_duplicates(
        subset=["customer_id"],
        keep="first"
    )

    # Step 3: Check missing values
    required_columns = [
        "customer_id",
        "full_name",
        "email",
        "phone",
        "city"
    ]

    for column in required_columns:
        missing = valid_customers[column].isna()

        for _, row in valid_customers[missing].iterrows():
            rejected.append({
                "record_id": row["customer_id"],
                "reason": f"Missing value in {column}"
            })

        valid_customers = valid_customers.dropna(
            subset=[column]
        )

    # Step 4: Check email format
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    valid_email = valid_customers["email"].astype(
        str
    ).str.match(email_pattern)

    for _, row in valid_customers[~valid_email].iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Invalid email format"
        })

    valid_customers = valid_customers[valid_email]

    return valid_customers, rejected


# Validate order records
def validate_orders(orders_df, valid_customer_ids):

    # Step 1: Check required columns
    required_schema = [
        "order_id",
        "customer_id",
        "order_date",
        "order_amount"
    ]

    check_required_columns(
        orders_df,
        required_schema,
        "Orders"
    )

    valid_orders = orders_df.copy()
    rejected = []

    # Step 2: Check duplicate order IDs
    duplicate_ids = valid_orders[
        valid_orders.duplicated(
            subset=["order_id"],
            keep="first"
        )
    ]

    for _, row in duplicate_ids.iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Duplicate order ID"
        })

    valid_orders = valid_orders.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    # Step 3: Check missing values
    required_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "order_amount"
    ]

    for column in required_columns:
        missing = valid_orders[column].isna()

        for _, row in valid_orders[missing].iterrows():
            rejected.append({
                "record_id": row["order_id"],
                "reason": f"Missing value in {column}"
            })

        valid_orders = valid_orders.dropna(
            subset=[column]
        )

    # Step 4: Check order amount
    valid_orders["order_amount"] = pd.to_numeric(
        valid_orders["order_amount"],
        errors="coerce"
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

    # Step 5: Check customer relationship
    invalid_customer = ~valid_orders[
        "customer_id"
    ].isin(valid_customer_ids)

    for _, row in valid_orders[invalid_customer].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Customer ID does not exist"
        })

    valid_orders = valid_orders[~invalid_customer]

    # Step 6: Check order date format
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


