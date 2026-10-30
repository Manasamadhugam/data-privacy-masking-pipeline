import pandas as pd
import pytest

from src.validation import validate_customers, validate_orders


def sample_customers():
    return pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "full_name": ["Rahul Kumar", "Priya Sharma"],
        "email": ["rahul@example.com", "priya@example.com"],
        "phone": ["9000012345", "9000067890"],
        "date_of_birth": ["1995-01-10", "1998-05-15"],
        "city": ["Hyderabad", "Warangal"]
    })


def sample_orders():
    return pd.DataFrame({
        "order_id": ["O001", "O002"],
        "customer_id": ["C001", "C002"],
        "order_date": ["2026-01-10", "2026-02-15"],
        "order_amount": [500, 1000]
    })


def test_valid_customers():
    valid, rejected = validate_customers(sample_customers())
    assert len(valid) == 2
    assert len(rejected) == 0


def test_duplicate_customer_ids():
    customers = sample_customers()
    customers = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)

    valid, rejected = validate_customers(customers)
    assert len(valid) == 2
    assert len(rejected) == 1


def test_missing_customer_value():
    customers = sample_customers()
    customers.loc[0, "email"] = None

    valid, rejected = validate_customers(customers)
    assert len(valid) == 1
    assert len(rejected) == 1


def test_invalid_email():
    customers = sample_customers()
    customers.loc[0, "email"] = "invalid-email"

    valid, rejected = validate_customers(customers)
    assert len(valid) == 1
    assert len(rejected) == 1


def test_negative_order_amount():
    orders = sample_orders()
    orders.loc[0, "order_amount"] = -500

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 1
    assert len(rejected) == 1


def test_invalid_customer_reference():
    orders = sample_orders()
    orders.loc[0, "customer_id"] = "C999"

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 1
    assert len(rejected) == 1


def test_empty_customer_data():
    customers = sample_customers().iloc[0:0]

    valid, rejected = validate_customers(customers)
    assert len(valid) == 0
    assert len(rejected) == 0


import pandas as pd
import pytest

from src.validation import validate_customers, validate_orders


# Sample customer data
def sample_customers():
    return pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "full_name": ["Rahul Kumar", "Priya Sharma"],
        "email": ["rahul@example.com", "priya@example.com"],
        "phone": ["9000012345", "9000067890"],
        "date_of_birth": ["1995-01-10", "1998-05-15"],
        "city": ["Hyderabad", "Warangal"]
    })


# Sample order data
def sample_orders():
    return pd.DataFrame({
        "order_id": ["O001", "O002"],
        "customer_id": ["C001", "C002"],
        "order_date": ["2026-01-10", "2026-02-15"],
        "order_amount": [500, 1000]
    })


# Customer validation tests

def test_valid_customers():
    valid, rejected = validate_customers(sample_customers())
    assert len(valid) == 2
    assert len(rejected) == 0


def test_duplicate_customer_ids():
    customers = sample_customers()
    customers = pd.concat(
        [customers, customers.iloc[[0]]],
        ignore_index=True
    )

    valid, rejected = validate_customers(customers)
    assert len(valid) == 2
    assert len(rejected) == 1


def test_missing_customer_value():
    customers = sample_customers()
    customers.loc[0, "email"] = None

    valid, rejected = validate_customers(customers)
    assert len(valid) == 1
    assert len(rejected) == 1


def test_invalid_email():
    customers = sample_customers()
    customers.loc[0, "email"] = "invalid-email"

    valid, rejected = validate_customers(customers)
    assert len(valid) == 1
    assert len(rejected) == 1


def test_empty_customer_data():
    customers = sample_customers().iloc[0:0]

    valid, rejected = validate_customers(customers)
    assert len(valid) == 0
    assert len(rejected) == 0


# Order validation tests

def test_negative_order_amount():
    orders = sample_orders()
    orders.loc[0, "order_amount"] = -500

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 1
    assert len(rejected) == 1


def test_zero_order_amount():
    orders = sample_orders()
    orders.loc[0, "order_amount"] = 0

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 1
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "Invalid or non-positive order amount"


def test_invalid_customer_reference():
    orders = sample_orders()
    orders.loc[0, "customer_id"] = "C999"

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 1
    assert len(rejected) == 1


def test_duplicate_order_ids():
    orders = sample_orders()
    orders = pd.concat(
        [orders, orders.iloc[[0]]],
        ignore_index=True
    )

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 2
    assert len(rejected) == 1


def test_invalid_order_date():
    orders = sample_orders()
    orders.loc[0, "order_date"] = "invalid-date"

    valid, rejected = validate_orders(orders, ["C001", "C002"])
    assert len(valid) == 1
    assert len(rejected) == 1


# Schema validation tests

def test_missing_customer_column():
    customers = sample_customers().drop(columns=["email"])

    with pytest.raises(ValueError, match="missing required columns"):
        validate_customers(customers)


def test_missing_order_column():
    orders = sample_orders().drop(columns=["order_amount"])

    with pytest.raises(ValueError, match="missing required columns"):
        validate_orders(orders, ["C001", "C002"])
