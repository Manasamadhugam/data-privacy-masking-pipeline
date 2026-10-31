# System Architecture

## Project: Data Privacy & Masking Pipeline

### 1. Overview

This project is a Python-based data engineering pipeline that processes synthetic customer and order datasets, identifies sensitive information, validates records, masks personal data, generates deterministic customer ID pseudonyms, and produces a privacy-aware analytics dataset.

### 2. Pipeline Workflow

1. **Data Generation:** Generate synthetic customer and order datasets.
2. **Data Ingestion:** Load CSV datasets using Pandas.
3. **Data Profiling:** Identify columns, data types, null values, unique values, and dataset information.
4. **Data Validation:** Check duplicate records, missing values, invalid emails, order amounts, dates, and customer references.
5. **Data Rejection:** Separate invalid records and store rejection reasons.
6. **Data Reconciliation:** Verify input, valid, and rejected record counts.
7. **Data Masking:** Mask customer names, email addresses, and phone numbers.
8. **Pseudonymization:** Generate deterministic SHA-256-based customer ID tokens.
9. **Data Transformation:** Calculate order count, total spending, and last order date.
10. **Data Output:** Generate the minimized analytics output CSV without original customer IDs or dates of birth.
11. **Audit Logging:** Record run ID, timestamps, record counts, execution time, and pipeline status.

### 3. Technologies Used

- Python 3.11
- Pandas
- NumPy
- CSV
- Pytest
- Anaconda
- Git and GitHub

### 4. Output Files

- `analytics_output.csv` – Masked and pseudonymized analytics dataset.
- `rejected_records.csv` – Invalid records and rejection reasons.
- `data_profile.csv` – Data profiling report.
- `audit_log.csv` – Pipeline execution audit history.

### 5. Privacy Approach

The pipeline uses synthetic data and applies privacy techniques before creating the analytics dataset.

- Customer names are partially masked.
- Email usernames are masked.
- Phone numbers are masked except for the last four digits.
- Customer IDs are pseudonymized using deterministic SHA-256 hashing.
- Date of birth and original customer IDs are excluded from the final analytics output.

**Limitation:** SHA-256 pseudonymization is not reversible tokenization. The current implementation does not use a secret key or secure token vault.

### 6. Data Quality and Reliability

- Validates customer and order records.
- Identifies duplicate, missing, and invalid records.
- Separates rejected records for review.
- Reconciles input, valid, and rejected record counts.
- Maintains audit logs for pipeline execution monitoring.
- Uses automated tests to verify pipeline components.

### 7. Future Enhancements

- Secure secret-key-based tokenization.
- Reversible token vault with access controls.
- Database integration.
- Cloud storage integration.
- Pipeline scheduling and orchestration.