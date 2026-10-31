import random
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

RANDOM_SEED = 42


def generate_data(number_of_customers=1000):
    if number_of_customers <= 0:
        raise ValueError("Number of customers must be greater than zero")

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    DATA_DIR.mkdir(exist_ok=True)

    first_names = [
        "Rahul", "Priya", "Anita", "Kiran", "Vijay",
        "Sneha", "Arjun", "Divya", "Ravi", "Meena"
    ]

    last_names = [
        "Sharma", "Reddy", "Kumar", "Rao", "Patel",
        "Singh", "Gupta", "Verma", "Naidu", "Das"
    ]

    cities = [
        "Hyderabad", "Warangal", "Karimnagar",
        "Nizamabad", "Khammam"
    ]

    customers = []

    for i in range(1, number_of_customers + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)

        customers.append({
            "customer_id": f"C{i:06d}",
            "full_name": f"{first} {last}",
            "email": f"customer{i}@example.com",
            "phone": f"9{i:09d}",
            "date_of_birth": (
                f"{random.randint(1970, 2002)}-"
                f"{random.randint(1, 12):02d}-"
                f"{random.randint(1, 28):02d}"
            ),
            "city": random.choice(cities)
        })

    customers_df = pd.DataFrame(customers)

    orders = []

    for i in range(1, number_of_customers * 2 + 1):
        customer_number = random.randint(1, number_of_customers)

        orders.append({
            "order_id": f"O{i:06d}",
            "customer_id": f"C{customer_number:06d}",
            "order_date": (
                f"2026-{random.randint(1, 12):02d}-"
                f"{random.randint(1, 28):02d}"
            ),
            "order_amount": round(random.uniform(100, 10000), 2)
        })

    orders_df = pd.DataFrame(orders)

    customers_df.to_csv(DATA_DIR / "customers.csv", index=False)
    orders_df.to_csv(DATA_DIR / "orders.csv", index=False)

    print("Synthetic data generated successfully!")
    print("Customers:", len(customers_df))
    print("Orders:", len(orders_df))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--customers",
        type=int,
        default=1000,
        help="Number of synthetic customers to generate"
    )

    args = parser.parse_args()
    generate_data(args.customers)