
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"


SENSITIVE_FIELDS = [
    "full_name",
    "email",
    "phone",
    "date_of_birth"
]


def profile_data(customers_df, orders_df):

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        "customers": customers_df,
        "orders": orders_df
    }

    profile_results = []

    for dataset_name, df in datasets.items():

        for column in df.columns:

            profile_results.append({
                "dataset": dataset_name,
                "column_name": column,
                "data_type": str(df[column].dtype),
                "total_records": len(df),
                "null_count": int(df[column].isna().sum()),
                "unique_count": int(df[column].nunique()),
                "sensitive_field": column in SENSITIVE_FIELDS
            })

    profile_df = pd.DataFrame(profile_results)

    profile_df.to_csv(
        REPORT_DIR / "data_profile.csv",
        index=False
    )

    print("Data profiling completed!")
    print("Profile report saved in reports/data_profile.csv")

    return profile_df
