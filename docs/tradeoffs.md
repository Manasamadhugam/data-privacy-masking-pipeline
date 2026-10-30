\# Design Trade-offs



\## Project: Data Privacy \& Masking Pipeline



\### 1. CSV vs Database



CSV files are used for input and output because they are simple, portable, and easy to inspect. SQLite can be added in a future version for structured storage.



\### 2. Pandas vs Other Processing Tools



Pandas is used because it provides convenient data cleaning, validation, transformation, and CSV processing features. For very large datasets, distributed tools such as PySpark may be considered.



\### 3. Masking vs Data Deletion



Masking is used instead of deleting all customer information because analytical teams may still need limited customer details. Date of birth is removed from the analytics output because it is not required for the current analysis.



\### 4. Rejection vs Automatic Correction



Invalid records are rejected with clear reasons instead of silently changing potentially incorrect values. This improves data quality and traceability.



\### 5. Reproducibility vs Randomness



A fixed random seed is used to generate repeatable synthetic datasets. This makes testing and debugging easier.



\### 6. Performance vs Simplicity



Pandas provides a simple solution for the current project scale. Distributed processing can be introduced if dataset size grows significantly.



\### 7. Limitations



\- The project currently uses synthetic datasets.

\- Masking is not encryption or irreversible anonymization.

\- CSV files are used instead of a production database.

\- Authentication and role-based access control are not implemented.

