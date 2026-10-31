# Data Privacy & Masking Pipeline

## 1. Project Overview

The Data Privacy & Masking Pipeline is a Python-based Data Engineering project designed to protect sensitive customer information while preparing data for analytics.

The pipeline generates synthetic customer and order datasets, performs data ingestion, profiling, validation, masking, deterministic pseudonymization, reconciliation, and audit logging.

It produces a privacy-aware analytical dataset without exposing original customer IDs or dates of birth.

## 2. Business Problem

Organizations collect sensitive customer information such as names, email addresses, phone numbers, and dates of birth.

Sharing original personal information with analytical teams can create privacy risks.

This project addresses the problem by masking sensitive fields, generating pseudonymous customer identifiers, validating data quality, and creating a minimized analytical dataset.

## 3. Project Objectives

- Generate reproducible synthetic customer and order datasets.
- Ingest source data using Python and Pandas.
- Perform data profiling and validation.
- Identify duplicate, null, and invalid records.
- Mask sensitive customer information.
- Generate deterministic customer ID tokens.
- Reconcile input, valid, and rejected records.
- Quarantine rejected records for review.
- Create a minimized analytical dataset.
- Maintain audit logs with execution details.
- Measure pipeline execution time.
- Validate functionality using automated tests.

## 4. Technologies Used

- Python 3.11
- Pandas
- Pytest
- Anaconda
- Git and GitHub
- CSV for data storage

## 5. Project Structure

data-privacy-masking-pipeline/
│
├── data/
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── tradeoffs.md
│
├── logs/
├── reports/
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── ingestion.py
│   ├── profiling.py
│   ├── validation.py
│   ├── masking.py
│   ├── reconciliation.py
│   └── audit.py
│
├── tests/
│   ├── test_masking.py
│   ├── test_reconciliation.py
│   └── test_validation.py
│
├── config.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
## 6. Pipeline Workflow

1. Generate synthetic customer and order datasets.
2. Load source CSV files.
3. Perform data profiling.
4. Validate customer and order records.
5. Identify duplicate, null, and invalid records.
6. Separate rejected records.
7. Reconcile input, valid, and rejected record counts.
8. Mask sensitive customer information.
9. Generate deterministic customer ID tokens.
10. Aggregate order information for analytics.
11. Generate the minimized analytical dataset.
12. Save audit logs and execution metrics.
13. Run automated tests.

## 7. Privacy and Masking

The pipeline applies the following privacy techniques:

| Field | Privacy technique |
|---|---|
| Customer name | Partial masking |
| Email | Username masking |
| Phone | All digits except last four masked |
| Customer ID | Deterministic SHA-256-based pseudonym |
| Date of birth | Excluded from analytics output |

The customer ID token is generated using SHA-256 hashing. The same input ID produces the same token.

**Limitation:** This implementation provides deterministic pseudonymization, not reversible tokenization or a secure token vault. It does not use a secret key.

## 8. Configuration

Pipeline settings are maintained in `config.py`.

- `MASKING_ENABLED`: Enables or disables masking.
- `TOKENIZATION_ENABLED`: Enables or disables customer ID token generation.
- `RANDOM_SEED`: Controls reproducible synthetic data generation.

## 9. Expected Outputs

| Output file | Description |
|---|---|
| customers.csv | Synthetic customer records |
| orders.csv | Synthetic order records |
| analytics_output.csv | Masked and tokenized analytics dataset |
| rejected_records.csv | Invalid and rejected records |
| data_profile.csv | Data profiling report |
| audit_log.csv | Pipeline execution audit history |

## 10. Installation

Clone the repository:

```bash
git clone https://github.com/Manasamadhugam/data-privacy-masking-pipeline.git
cd data-privacy-masking-pipeline
```

Create and activate the environment:

```bash
conda create -n privacy_env python=3.11 -y
conda activate privacy_env
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 11. Execution

Generate 100,000 synthetic customer records and corresponding order records:

```bash
python src/generate_data.py --customers 100000
```

Run the pipeline:

```bash
python main.py
```

Run automated tests:

```bash
python -m pytest -v
```

## 12. Performance Results

One successful local execution processed:

| Metric | Result |
|---|---:|
| Customer records | 100,000 |
| Order records | 200,000 |
| Total input records | 300,000 |
| Analytics output records | 100,000 |
| Rejected records | 0 |
| Execution time |2.89 seconds |

Performance may vary depending on the machine and execution environment.

## 13. Testing

The project includes automated tests for:

- Customer and order validation.
- Duplicate records.
- Missing values and columns.
- Invalid email addresses.
- Negative and zero order amounts.
- Invalid customer references.
- Invalid order dates.
- Record reconciliation.
- Masking functions.

The existing test suite has passed **24 tests**.

## 14. Documentation

Additional project documentation is available in the `docs/` directory:

- `architecture.md` – Pipeline architecture and workflow.
- `data_dictionary.md` – Dataset fields and descriptions.
- `tradeoffs.md` – Design decisions and limitations.

## 15. Future Enhancements

- Secure, secret-key-based tokenization.
- Reversible token vault with access controls.
- SQLite or relational database integration.
- Cloud storage integration.
- API-based data ingestion.
- Advanced data quality monitoring.
- Pipeline scheduling and orchestration.
- Dashboard for pipeline metrics.

## 16. Data Privacy Disclaimer

This project uses synthetic data for demonstration and learning purposes. The generated analytical output is designed to reduce exposure of personal information. The current hashing implementation should not be treated as a complete production-grade privacy solution.
