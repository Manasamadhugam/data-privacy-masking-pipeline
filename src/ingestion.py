
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_data():

    customers_file = DATA_DIR / "customers.csv"
    orders_file = DATA_DIR / "orders.csv"

    if not customers_file.exists():
        raise FileNotFoundError(
            f"Customers file not found: {customers_file}"
        )

    if not orders_file.exists():
        raise FileNotFoundError(
            f"Orders file not found: {orders_file}"
        )

    customers_df = pd.read_csv(
        customers_file,
        dtype={
            "customer_id": "string",
            "phone": "string"
        }
    )

    orders_df = pd.read_csv(
        orders_file,
        dtype={
            "order_id": "string",
            "customer_id": "string"
        }
    )

    print("Data loaded successfully!")

    print("\nCustomers Data:")
    print(customers_df.head())

    print("\nOrders Data:")
    print(orders_df.head())

    print("\nDataset Information:")
    print("Customers:", customers_df.shape)
    print("Orders:", orders_df.shape)

    return customers_df, orders_df


if __name__ == "__main__":
    load_data()
