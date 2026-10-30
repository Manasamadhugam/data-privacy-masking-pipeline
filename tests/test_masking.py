import pandas as pd

from src.masking import mask_name, mask_email, mask_phone, apply_masking


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