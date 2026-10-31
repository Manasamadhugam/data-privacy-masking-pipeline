
import pandas as pd


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


def validate_customers(customers_df):

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

    # Step 1: Normalize text columns
    text_columns = [
        "customer_id",
        "full_name",
        "email",
        "phone",
        "city"
    ]

    for column in text_columns:
        valid_customers[column] = (
            valid_customers[column].astype("string").str.strip()
        )

    # Step 2: Check missing and empty values
    required_columns = [
        "customer_id",
        "full_name",
        "email",
        "phone",
        "city",
        "date_of_birth"
    ]

    for column in required_columns:
        missing = (
            valid_customers[column].isna()
            | valid_customers[column].eq("")
        )

        for _, row in valid_customers[missing].iterrows():
            rejected.append({
                "record_id": row["customer_id"],
                "reason": f"Missing value in {column}"
            })

        valid_customers = valid_customers[~missing]

    # Step 3: Check duplicate customer IDs
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

    # Step 4: Check customer ID format
    valid_id = valid_customers["customer_id"].str.fullmatch(
        r"C\d{3,}",
        na=False
    )

    for _, row in valid_customers[~valid_id].iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Invalid customer ID format"
        })

    valid_customers = valid_customers[valid_id]

    # Step 5: Check email format
    email_pattern = r"^[\w.-]+@[\w.-]+\.\w+$"

    valid_email = valid_customers["email"].str.fullmatch(
        email_pattern,
        na=False
    )

    for _, row in valid_customers[~valid_email].iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Invalid email format"
        })

    valid_customers = valid_customers[valid_email]

    # Step 6: Check phone number
    valid_phone = valid_customers["phone"].str.fullmatch(
        r"\d{10}",
        na=False
    )

    for _, row in valid_customers[~valid_phone].iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Invalid phone number"
        })

    valid_customers = valid_customers[valid_phone]

    # Step 7: Check date of birth
    valid_dob = pd.to_datetime(
        valid_customers["date_of_birth"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    invalid_dob = (
        valid_dob.isna()
        | (valid_dob >= today)
    )

    for _, row in valid_customers[invalid_dob].iterrows():
        rejected.append({
            "record_id": row["customer_id"],
            "reason": "Invalid date of birth"
        })

    valid_customers = valid_customers[~invalid_dob]

    return valid_customers, rejected


def validate_orders(orders_df, valid_customer_ids):

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

    # Step 1: Normalize text columns
    for column in ["order_id", "customer_id", "order_date"]:
        valid_orders[column] = (
            valid_orders[column].astype("string").str.strip()
        )

    # Step 2: Check missing and empty values
    required_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "order_amount"
    ]

    for column in required_columns:
        missing = (
            valid_orders[column].isna()
            | valid_orders[column].eq("")
        )

        for _, row in valid_orders[missing].iterrows():
            rejected.append({
                "record_id": row["order_id"],
                "reason": f"Missing value in {column}"
            })

        valid_orders = valid_orders[~missing]

    # Step 3: Check duplicate order IDs
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

    # Step 4: Check order ID format
    valid_id = valid_orders["order_id"].str.fullmatch(
        r"O\d{3,}",
        na=False
    )

    for _, row in valid_orders[~valid_id].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Invalid order ID format"
        })

    valid_orders = valid_orders[valid_id]

    # Step 5: Check order amount
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

    # Step 6: Check customer relationship
    invalid_customer = ~valid_orders[
        "customer_id"
    ].isin(valid_customer_ids)

    for _, row in valid_orders[invalid_customer].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Customer ID does not exist"
        })

    valid_orders = valid_orders[~invalid_customer]

    # Step 7: Check order date
    valid_dates = pd.to_datetime(
        valid_orders["order_date"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    invalid_date = valid_dates.isna()

    for _, row in valid_orders[invalid_date].iterrows():
        rejected.append({
            "record_id": row["order_id"],
            "reason": "Invalid order date"
        })

    valid_orders = valid_orders[~invalid_date]

    return valid_orders, rejected
