\# System Architecture



\## Project: Data Privacy \& Masking Pipeline



\### 1. Overview



This project is a Python-based data pipeline that processes synthetic customer and order datasets, identifies sensitive information, validates records, masks personal data, and generates a privacy-safe analytics dataset.



\### 2. Pipeline Workflow



1\. \*\*Data Generation:\*\* Generate synthetic customer and order data.

2\. \*\*Data Ingestion:\*\* Load CSV datasets using Pandas.

3\. \*\*Data Profiling:\*\* Identify columns, data types, null values, unique values, and sensitive fields.

4\. \*\*Data Validation:\*\* Check duplicate records, missing values, invalid emails, order amounts, and customer references.

5\. \*\*Data Rejection:\*\* Store invalid records with rejection reasons.

6\. \*\*Data Masking:\*\* Mask customer names, email addresses, and phone numbers.

7\. \*\*Data Transformation:\*\* Calculate order count, total spending, and last order date.

8\. \*\*Data Output:\*\* Generate the analytics output CSV.

9\. \*\*Audit Logging:\*\* Record run ID, timestamps, record counts, execution time, and pipeline status.



\### 3. Technologies Used



\- Python

\- Pandas

\- NumPy

\- CSV

\- SQLite (planned for future enhancement)

\- Pytest

\- Git and GitHub



\### 4. Output Files



\- `analytics\_output.csv`

\- `rejected\_records.csv`

\- `data\_profile.csv`

\- `audit\_log.csv`



\### 5. Privacy Approach



The pipeline uses synthetic data and masks personally identifiable information (PII) before creating the analytics dataset. Date of birth is excluded from the final output.

