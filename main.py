
import pandas as pd
import time

from src.profiling import profile_data
from config import MASKING_ENABLED
from src.ingestion import load_data
from src.validation import validate_customers, validate_orders
from src.masking import apply_masking
from src.audit import start_audit, finish_audit


def main():
    start_time = time.perf_counter()
    audit_info = start_audit()

    input_records = 0
    output_records = 0
    rejected_records = 0

    try:
        # Step 1: Load data
        customers_df, orders_df = load_data()

        # Step 2: Profile source data
        profile_data(customers_df, orders_df)

        input_records = len(customers_df) + len(orders_df)

        # Step 3: Validate customers
        valid_customers, customer_rejected = validate_customers(
            customers_df
        )

        # Step 4: Validate orders
        valid_orders, order_rejected = validate_orders(
            orders_df,
            valid_customers["customer_id"]
        )

        # Step 5: Mask sensitive information
        if MASKING_ENABLED:
            masked_customers = apply_masking(valid_customers)
        else:
            masked_customers = valid_customers.copy()

        # Step 6: Calculate order summary
        order_summary = (
            valid_orders.groupby("customer_id")
            .agg(
                order_count=("order_id", "count"),
                total_spend=("order_amount", "sum"),
                last_order_date=("order_date", "max")
            )
            .reset_index()
        )

        # Step 7: Create analytics dataset
        analytics_df = masked_customers.drop(
            columns=["date_of_birth"]
        ).merge(
            order_summary,
            on="customer_id",
            how="left"
        )

        analytics_df["order_count"] = (
            analytics_df["order_count"].fillna(0).astype(int)
        )

        analytics_df["total_spend"] = (
            analytics_df["total_spend"].fillna(0).round(2)
        )

        # Step 8: Save analytics output
        analytics_df.to_csv(
            "data/analytics_output.csv",
            index=False
        )

        # Step 9: Save rejected records
        all_rejected = customer_rejected + order_rejected
        rejected_records = len(all_rejected)

        rejected_df = pd.DataFrame(
            all_rejected,
            columns=["record_id", "reason"]
        )

        rejected_df.to_csv(
            "data/rejected_records.csv",
            index=False
        )

        output_records = len(analytics_df)

        # Step 10: Calculate execution time
        end_time = time.perf_counter()
        execution_time = round(end_time - start_time, 2)

        # Step 11: Save audit log with execution time
        finish_audit(
            audit_info,
            input_records,
            output_records,
            rejected_records,
            status="SUCCESS",
            duration_seconds=execution_time
        )

        # Step 12: Display pipeline results
        print("\n--- Pipeline Results ---")
        print("Input records:", input_records)
        print("Output records:", output_records)
        print("Rejected records:", rejected_records)
        print("Execution time:", execution_time, "seconds")
        print("Pipeline completed successfully!")

    except Exception as error:
        finish_audit(
            audit_info,
            input_records,
            output_records,
            rejected_records,
            status="FAILED",
            failure_reason=str(error)
        )
        raise


if __name__ == "__main__":
    main()
