\# Design Trade-offs



\## Project: Data Privacy \& Masking Pipeline



\### 1. CSV vs Database



CSV files are used for input and output because they are simple, portable, and easy to inspect. SQLite or other relational databases can be added in a future version for structured storage.



\### 2. Pandas vs Other Processing Tools



Pandas is used because it provides convenient data cleaning, validation, transformation, aggregation, and CSV processing features. For very large datasets, distributed processing tools such as PySpark may be considered.



\### 3. Masking vs Data Deletion



Masking is used instead of deleting all customer information because analytical teams may still need limited customer details. Date of birth and original customer IDs are excluded from the analytics output to reduce exposure of sensitive information.



\### 4. Pseudonymization vs Reversible Tokenization



Deterministic SHA-256 hashing is used to generate pseudonymous customer identifiers. The same customer ID generates the same token, which supports consistent identification across pipeline runs.



A secure token vault or secret-key-based tokenization system is not implemented in the current version.



\### 5. Rejection vs Automatic Correction



Invalid records are rejected with clear reasons instead of silently changing potentially incorrect values. This improves data quality and traceability.



\### 6. Reproducibility vs Randomness



A fixed random seed is used to generate repeatable synthetic datasets. This makes testing, debugging, and performance comparison easier.



\### 7. Performance vs Simplicity



Pandas provides a simple and efficient solution for the current project scale. The pipeline successfully processed 300,000 input records in 2.89 seconds in one local execution. Distributed processing can be introduced if dataset size grows significantly.



\### 8. Data Reconciliation and Audit Logging



Record reconciliation verifies that input records are accounted for as valid or rejected records. Audit logging records execution details, record counts, pipeline status, and execution time.



\### 9. Limitations



\- The project currently uses synthetic datasets.

\- Masking is not encryption or irreversible anonymization.

\- SHA-256 pseudonymization does not use a secret key and is not reversible tokenization.

\- CSV files are used instead of a production database.

\- Authentication and role-based access control are not implemented.

\- The current implementation is a demonstration project, not a complete production-grade privacy solution.

