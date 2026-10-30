
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_data():
    customers_file = DATA_DIR / "customers.csv"
    orders_file = DATA_DIR / "orders.csv"

    customers_df = pd.read_csv(customers_file)
    orders_df = pd.read_csv(orders_file)

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
