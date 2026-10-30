
import pandas as pd


def mask_name(name):
    if pd.isna(name):
        return name

    parts = str(name).split()

    masked_parts = []

    for part in parts:
        if len(part) <= 1:
            masked_parts.append(part)
        else:
            masked_parts.append(part[0] + "*" * (len(part) - 1))

    return " ".join(masked_parts)


def mask_email(email):
    if pd.isna(email):
        return email

    email = str(email)

    if "@" not in email:
        return "INVALID"

    username, domain = email.split("@", 1)

    if len(username) <= 1:
        masked_username = "*"
    else:
        masked_username = username[0] + "*" * (len(username) - 1)

    return masked_username + "@" + domain


def mask_phone(phone):
    if pd.isna(phone):
        return phone

    phone = str(phone)

    if len(phone) <= 4:
        return "*" * len(phone)

    return "*" * (len(phone) - 4) + phone[-4:]


def apply_masking(customers_df):
    masked_df = customers_df.copy()

    masked_df["full_name"] = masked_df["full_name"].apply(mask_name)
    masked_df["email"] = masked_df["email"].apply(mask_email)
    masked_df["phone"] = masked_df["phone"].apply(mask_phone)

    return masked_df
