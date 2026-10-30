
import csv
import uuid
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

AUDIT_FILE = LOG_DIR / "audit_log.csv"


def start_audit():
    LOG_DIR.mkdir(exist_ok=True)

    run_id = str(uuid.uuid4())
    start_time = datetime.now().isoformat(timespec="seconds")

    return {
        "run_id": run_id,
        "start_time": start_time
    }


def finish_audit(
    audit_info,
    input_records,
    output_records,
    rejected_records,
    status="SUCCESS",
    failure_reason="",
    duration_seconds=""
):

    end_time = datetime.now().isoformat(timespec="seconds")

    fieldnames = [
        "run_id",
        "start_time",
        "end_time",
        "input_records",
        "output_records",
        "rejected_records",
        "duration_seconds",
        "status",
        "failure_reason"
    ]

    # Preserve previous audit records and update an older CSV header
    old_rows = []

    if AUDIT_FILE.exists():
        with open(AUDIT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            old_rows = list(reader)

    with open(AUDIT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in old_rows:
            writer.writerow(row)

        writer.writerow({
            "run_id": audit_info["run_id"],
            "start_time": audit_info["start_time"],
            "end_time": end_time,
            "input_records": input_records,
            "output_records": output_records,
            "rejected_records": rejected_records,
            "duration_seconds": duration_seconds,
            "status": status,
            "failure_reason": failure_reason
        })

    print("Audit log saved successfully!")
