
from src.reconciliation import reconcile_records


def test_successful_reconciliation():
    assert reconcile_records(100, 90, 10) is True


def test_failed_reconciliation():
    assert reconcile_records(100, 90, 5) is False


def test_no_rejected_records():
    assert reconcile_records(100, 100, 0) is True


def test_all_records_rejected():
    assert reconcile_records(100, 0, 100) is True


def test_empty_dataset():
    assert reconcile_records(0, 0, 0) is True
