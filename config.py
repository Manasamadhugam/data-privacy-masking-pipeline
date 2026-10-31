from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
REPORT_DIR = PROJECT_ROOT / "reports"

INPUT_FILE = DATA_DIR / "customers.csv"
OUTPUT_FILE = DATA_DIR / "analytics_output.csv"
REJECT_FILE = DATA_DIR / "rejected_records.csv"

RANDOM_SEED = 42

MASKING_ENABLED = True
TOKENIZATION_ENABLED = True