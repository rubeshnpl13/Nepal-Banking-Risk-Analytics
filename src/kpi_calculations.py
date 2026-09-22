def calculate_portfolio_kpis(loans_df):
    total_loans = len(loans_df)

    total_outstanding_balance = loans_df["current_balance_npr"].sum()

    total_ead = loans_df["ead"].sum()

    total_npa_loans = loans_df["npa_flag"].sum()

    npa_ratio = total_npa_loans / total_loans if total_loans > 0 else 0

    default_rate = loans_df["defaulted_flag"].mean()

    total_expected_loss = loans_df["expected_loss_npr"].sum()

    average_pd = loans_df["pd"].mean()

    average_lgd = loans_df["lgd"].mean()

    return {
        "total_loans": total_loans,
        "total_outstanding_balance": total_outstanding_balance,
        "total_ead": total_ead,
        "total_npa_loans": total_npa_loans,
        "npa_ratio": npa_ratio,
        "default_rate": default_rate,
        "total_expected_loss": total_expected_loss,
        "average_pd": average_pd,
        "average_lgd": average_lgd,
    }