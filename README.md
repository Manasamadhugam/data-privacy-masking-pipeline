
# Data Privacy & Masking Pipeline

## 1. Project Overview

The Data Privacy & Masking Pipeline is a Python-based Data Engineering project designed to protect sensitive customer information.

The pipeline generates synthetic customer and order data, validates records, identifies data quality issues, masks sensitive fields, and creates a minimized analytical dataset.

## 2. Business Problem

Organizations collect sensitive customer information such as names, email addresses, phone numbers, and dates of birth.

Sharing original personal information with analytical teams can create privacy risks.

This project uses data masking to protect sensitive customer information while creating a minimized dataset for analytics.

## 3. Objectives

- Generate reproducible synthetic customer and order datasets.
- Ingest source data using Python and Pandas.
- Perform data profiling and validation.
- Identify duplicate, null, and invalid records.
- Mask sensitive customer information.
- Create a minimized analytical dataset.
- Store rejected records for review.
- Maintain audit logs with execution details.
- Measure pipeline execution time.
- Test the pipeline using automated test cases.

## 4. Technologies Used

- Python 3.11
- Pandas
- NumPy
- Pytest
- Git and GitHub
- Anaconda
- CSV for data storage

## 5. Project Structure

```text
data-privacy-masking-pipeline/
│
├── data/
├── docs/
├── logs/
├── reports/
├── src/
├── tests/
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## 6. Pipeline Workflow

1. Generate synthetic customer and order datasets.
2. Load source CSV files into the pipeline.
3. Perform data profiling.
4. Validate customer and order records.
5. Identify duplicate and invalid records.
6. Separate rejected records.
7. Mask sensitive customer information.
8. Aggregate order data for analytics.
9. Generate the minimized analytical dataset.
10. Save audit logs and execution metrics.
11. Run automated tests.

## 7. Expected Outputs

- Generated customer dataset (`customers.csv`)
- Generated order dataset (`orders.csv`)
- Privacy-safe analytical dataset (`analytics_output.csv`)
- Rejected records report (`rejected_records.csv`)
- Data profiling report (`data_profile.csv`)
- Pipeline audit log (`audit_log.csv`)

## 8. Installation

Clone the repository:

```bash
git clone https://github.com/Manasamadhugam/data-privacy-masking-pipeline.git
cd data-privacy-masking-pipeline
```

Create and activate the Python environment:

```bash
conda create -n privacy_env python=3.11 -y
conda activate privacy_env
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 9. Execution

Generate synthetic datasets:

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

## 10. Data Privacy

This project uses synthetic data for demonstration purposes. Sensitive customer information is masked before publishing the analytical dataset.

## 11. Future Enhancements

- Tokenization of sensitive customer information.
- SQLite database integration.
- Cloud storage integration.
- API-based data ingestion.
- Advanced data quality monitoring.
- Pipeline scheduling and orchestration.
- Dashboard for pipeline metrics.

