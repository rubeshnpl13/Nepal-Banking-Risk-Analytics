import pandas as pd


LOANS_PATH = "datasets/nepal_synthetic_bank_loans.csv"
BORROWERS_PATH = "datasets/nepal_synthetic_borrowers.csv"
COMBINED_PATH = "datasets/nepal_synthetic_bank_dataset.csv"
SUMMARY_PATH = "datasets/dataset_summary.csv"


def load_loans_data():
    df = pd.read_csv(LOANS_PATH)
    df["origination_date"] = pd.to_datetime(df["origination_date"])
    df["maturity_date"] = pd.to_datetime(df["maturity_date"])
    return df


def load_borrowers_data():
    return pd.read_csv(BORROWERS_PATH)


def load_combined_data():
    return pd.read_csv(COMBINED_PATH)


def load_summary_data():
    return pd.read_csv(SUMMARY_PATH)