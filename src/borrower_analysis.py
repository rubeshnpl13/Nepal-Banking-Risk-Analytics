def calculate_borrower_kpis(borrowers_df):
    total_borrowers = len(borrowers_df)
    average_income = borrowers_df["monthly_income_npr"].mean()
    average_credit_score = borrowers_df["credit_score"].mean()
    delinquency_rate = borrowers_df["existing_delinquency_flag"].mean()

    return {
        "total_borrowers": total_borrowers,
        "average_income": average_income,
        "average_credit_score": average_credit_score,
        "delinquency_rate": delinquency_rate,
    }