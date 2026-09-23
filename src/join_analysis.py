import pandas as pd


def create_joined_loan_borrower_data(loans_df, borrowers_df):
    joined_df = pd.merge(
        loans_df,
        borrowers_df,
        on="borrower_id",
        how="left",
        validate="many_to_one",
        suffixes=("_loan", "_borrower"),
    )
    return joined_df


def npa_ratio_by_employment_type(joined_df):
    summary = (
        joined_df.groupby("employment_type_borrower")
        .agg(
            total_loans=("loan_id", "count"),
            npa_loans=("npa_flag", "sum"),
        )
        .reset_index()
    )

    summary["npa_ratio"] = summary["npa_loans"] / summary["total_loans"]
    summary = summary.sort_values("npa_ratio", ascending=False)

    return summary


def expected_loss_by_region(joined_df):
    summary = (
        joined_df.groupby("region_borrower")
        .agg(
            total_expected_loss_npr=("expected_loss_npr", "sum"),
            total_loans=("loan_id", "count"),
        )
        .reset_index()
    )

    summary = summary.sort_values("total_expected_loss_npr", ascending=False)
    return summary


def average_pd_by_education_level(joined_df):
    summary = (
        joined_df.groupby("education_level_borrower")
        .agg(
            average_pd=("pd", "mean"),
            total_loans=("loan_id", "count"),
        )
        .reset_index()
    )

    summary = summary.sort_values("average_pd", ascending=False)
    return summary