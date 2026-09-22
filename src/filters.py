def apply_filters(loans_df, selected_regions, selected_products, selected_statuses):
    filtered_df = loans_df.copy()

    if selected_regions:
        filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

    if selected_products:
        filtered_df = filtered_df[filtered_df["product_type"].isin(selected_products)]

    if selected_statuses:
        filtered_df = filtered_df[filtered_df["status"].isin(selected_statuses)]

    return filtered_df