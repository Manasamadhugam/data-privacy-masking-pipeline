
import pandas as pd
import hashlib


def mask_name(name):
    if pd.isna(name):
        return name

    parts = str(name).split()
    masked_parts = []

    for part in parts:
        if len(part) <= 1:
            masked_parts.append(part)
        else:
            masked_parts.append(
                part[0] + "*" * (len(part) - 1)
            )

    return " ".join(masked_parts)


def mask_email(email):
    if pd.isna(email):
        return email

    email = str(email).strip()

    if "@" not in email:
        return "INVALID"

    username, domain = email.split("@", 1)

    if not username or not domain:
        return "INVALID"

    if len(username) <= 1:
        masked_username = "*"
    else:
        masked_username = (
            username[0] + "*" * (len(username) - 1)
        )

    return masked_username + "@" + domain


def mask_phone(phone):
    if pd.isna(phone):
        return phone

    phone = str(phone).strip()

    if len(phone) <= 4:
        return "*" * len(phone)

    return "*" * (len(phone) - 4) + phone[-4:]


def tokenize_value(value):
    if pd.isna(value):
        return value

    value = str(value).strip()

    token = hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:12].upper()

    return "CUST_" + token


def apply_masking(customers_df, tokenization_enabled=False):
    masked_df = customers_df.copy()

    sensitive_columns = [
        "full_name",
        "email",
        "phone"
    ]

    for column in sensitive_columns:
        if column in masked_df.columns:

            if column == "full_name":
                masked_df[column] = masked_df[column].apply(
                    mask_name
                )

            elif column == "email":
                masked_df[column] = masked_df[column].apply(
                    mask_email
                )

            elif column == "phone":
                masked_df[column] = masked_df[column].apply(
                    mask_phone
                )

    if tokenization_enabled and "customer_id" in masked_df.columns:
        masked_df["customer_id_token"] = (
            masked_df["customer_id"].apply(tokenize_value)
        )

    return masked_df
