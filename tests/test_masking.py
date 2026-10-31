
import pandas as pd

from src.masking import (
    mask_name,
    mask_email,
    mask_phone,
    apply_masking,
    tokenize_value
)


def test_mask_name():
    assert mask_name("Rahul Kumar") == "R**** K****"


def test_mask_email():
    assert mask_email("rahul@example.com") == "r****@example.com"


def test_mask_phone():
    assert mask_phone("9000012345") == "******2345"


def test_apply_masking():
    customers = pd.DataFrame({
        "full_name": ["Rahul Kumar"],
        "email": ["rahul@example.com"],
        "phone": ["9000012345"]
    })

    masked = apply_masking(customers)

    assert masked.loc[0, "full_name"] == "R**** K****"
    assert masked.loc[0, "email"] == "r****@example.com"
    assert masked.loc[0, "phone"] == "******2345"


def test_tokenization_is_consistent():
    token1 = tokenize_value("C000001")
    token2 = tokenize_value("C000001")

    assert token1 == token2


def test_different_ids_generate_different_tokens():
    token1 = tokenize_value("C000001")
    token2 = tokenize_value("C000002")

    assert token1 != token2


def test_apply_masking_with_tokenization():
    customers = pd.DataFrame({
        "customer_id": ["C000001"],
        "full_name": ["Rahul Kumar"],
        "email": ["rahul@example.com"],
        "phone": ["9000012345"]
    })

    result = apply_masking(
        customers,
        tokenization_enabled=True
    )

    assert "customer_id_token" in result.columns
    assert result.loc[0, "customer_id_token"].startswith("CUST_")
    assert result.loc[0, "customer_id"] == "C000001"
