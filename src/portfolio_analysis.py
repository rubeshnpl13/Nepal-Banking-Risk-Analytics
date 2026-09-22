def create_product_risk_summary(loans_df):
    summary_df = (
        loans_df.groupby("product_type", as_index=False)
        .agg(
            total_loans=("loan_id", "count"),
            total_balance_npr=("current_balance_npr", "sum"),
            total_ead_npr=("ead", "sum"),
            average_pd=("pd", "mean"),
            average_lgd=("lgd", "mean"),
            npa_ratio=("npa_flag", "mean"),
            default_rate=("defaulted_flag", "mean"),
            expected_loss_npr=("expected_loss_npr", "sum"),
        )
    )

    summary_df["npa_ratio"] = summary_df["npa_ratio"] * 100
    summary_df["default_rate"] = summary_df["default_rate"] * 100
    summary_df["average_pd"] = summary_df["average_pd"] * 100
    summary_df["average_lgd"] = summary_df["average_lgd"] * 100

    return summary_df.sort_values(by="expected_loss_npr", ascending=False)