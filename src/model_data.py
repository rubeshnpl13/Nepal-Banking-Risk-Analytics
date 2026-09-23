def create_default_model_dataset(joined_df):
    model_df = joined_df.copy()

    selected_columns = [
        "loan_id",
        "borrower_id",
        "defaulted_flag",
        "age_borrower",
        "gender_borrower",
        "marital_status_borrower",
        "education_level_borrower",
        "employment_type_borrower",
        "region_borrower",
        "sector_borrower",
        "monthly_income_npr_borrower",
        "credit_score_borrower",
        "dependents",
        "home_owner",
        "product_type",
        "loan_amount_npr",
        "interest_rate_pct",
        "term_months",
        "collateral_type",
    ]

    model_df = model_df[selected_columns].copy()

    model_df = model_df.dropna(subset=["defaulted_flag"])

    return model_df