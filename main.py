
import pandas as pd
import time

from config import (
    MASKING_ENABLED,
    TOKENIZATION_ENABLED,
    OUTPUT_FILE,
    REJECT_FILE
)

from src.ingestion import load_data
from src.profiling import profile_data
from src.validation import validate_customers, validate_orders
from src.masking import apply_masking, tokenize_value
from src.reconciliation import reconcile_records
from src.audit import start_audit, finish_audit


def main():

    start_time = time.perf_counter()
    audit_info = start_audit()

    input_records = 0
    output_records = 0
    rejected_records = 0

    try:
        # Step 1: Load source data
        customers_df, orders_df = load_data()

        # Step 2: Profile source data
        profile_data(customers_df, orders_df)

        # Step 3: Count input records
        customer_input = len(customers_df)
        order_input = len(orders_df)

        input_records = customer_input + order_input

        # Step 4: Validate customers
        valid_customers, customer_rejected = validate_customers(
            customers_df
        )

        # Step 5: Validate orders
        valid_orders, order_rejected = validate_orders(
            orders_df,
            valid_customers["customer_id"]
        )

        # Step 6: Calculate valid and rejected counts
        customer_valid_count = len(valid_customers)
        customer_rejected_count = len(customer_rejected)

        order_valid_count = len(valid_orders)
        order_rejected_count = len(order_rejected)

        # Step 7: Reconcile customers
        customer_reconciliation = reconcile_records(
            customer_input,
            customer_valid_count,
            customer_rejected_count
        )

        # Step 8: Reconcile orders
        order_reconciliation = reconcile_records(
            order_input,
            order_valid_count,
            order_rejected_count
        )

        # Step 9: Verify reconciliation
        if not customer_reconciliation or not order_reconciliation:
            raise ValueError("Data reconciliation failed")

        # Step 10: Create order summary using original IDs
        order_summary = (
            valid_orders.groupby("customer_id")
            .agg(
                order_count=("order_id", "count"),
                total_spend=("order_amount", "sum"),
                last_order_date=("order_date", "max")
            )
            .reset_index()
        )

        # Step 11: Apply masking and tokenization
        if MASKING_ENABLED:
            masked_customers = apply_masking(
                valid_customers,
                tokenization_enabled=TOKENIZATION_ENABLED
            )
        else:
            masked_customers = valid_customers.copy()

        # Step 12: Merge using original customer IDs
        analytics_df = masked_customers.merge(
            order_summary,
            on="customer_id",
            how="left"
        )

        # Step 13: Remove sensitive and original ID columns
        analytics_df = analytics_df.drop(
            columns=["date_of_birth"],
            errors="ignore"
        )

        if TOKENIZATION_ENABLED and MASKING_ENABLED:
            analytics_df = analytics_df.drop(
                columns=["customer_id"],
                errors="ignore"
            )

        # Step 14: Fill missing order summary values
        analytics_df["order_count"] = (
            analytics_df["order_count"]
            .fillna(0)
            .astype(int)
        )

        analytics_df["total_spend"] = (
            analytics_df["total_spend"]
            .fillna(0)
            .round(2)
        )

        # Step 15: Save analytics output
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        analytics_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        # Step 16: Save rejected records
        all_rejected = customer_rejected + order_rejected
        rejected_records = len(all_rejected)

        rejected_df = pd.DataFrame(
            all_rejected,
            columns=["record_id", "reason"]
        )

        REJECT_FILE.parent.mkdir(parents=True, exist_ok=True)

        rejected_df.to_csv(
            REJECT_FILE,
            index=False
        )

        output_records = len(analytics_df)

        # Step 17: Calculate execution time
        execution_time = round(
            time.perf_counter() - start_time,
            2
        )

        # Step 18: Save audit log
        finish_audit(
            audit_info,
            input_records,
            output_records,
            rejected_records,
            status="SUCCESS",
            duration_seconds=execution_time
        )

        # Step 19: Display customer reconciliation
        print("\n--- Customer Reconciliation ---")
        print("Input customers:", customer_input)
        print("Valid customers:", customer_valid_count)
        print("Rejected customers:", customer_rejected_count)
        print("Reconciliation:", customer_reconciliation)

        # Step 20: Display order reconciliation
        print("\n--- Order Reconciliation ---")
        print("Input orders:", order_input)
        print("Valid orders:", order_valid_count)
        print("Rejected orders:", order_rejected_count)
        print("Reconciliation:", order_reconciliation)

        # Step 21: Display pipeline results
        print("\n--- Pipeline Results ---")
        print("Total input records:", input_records)
        print("Analytics output records:", output_records)
        print("Total rejected records:", rejected_records)
        print("Execution time:", execution_time, "seconds")

        print("\nPipeline completed successfully!")

    except Exception as error:

        execution_time = round(
            time.perf_counter() - start_time,
            2
        )

        finish_audit(
            audit_info,
            input_records,
            output_records,
            rejected_records,
            status="FAILED",
            failure_reason=str(error),
            duration_seconds=execution_time
        )

        raise


if __name__ == "__main__":
    main()
