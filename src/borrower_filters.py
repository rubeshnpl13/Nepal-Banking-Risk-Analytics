def apply_borrower_filters(
    borrowers_df,
    selected_regions,
    selected_employment_types,
    selected_education_levels,
    selected_delinquency_flags,
):
    filtered_df = borrowers_df.copy()

    if selected_regions:
        filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

    if selected_employment_types:
        filtered_df = filtered_df[filtered_df["employment_type"].isin(selected_employment_types)]

    if selected_education_levels:
        filtered_df = filtered_df[filtered_df["education_level"].isin(selected_education_levels)]

    if selected_delinquency_flags:
        filtered_df = filtered_df[
            filtered_df["existing_delinquency_flag"].astype(str).isin(selected_delinquency_flags)
        ]

    return filtered_df