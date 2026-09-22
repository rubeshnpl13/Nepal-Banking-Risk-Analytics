import streamlit as st

from src.data_loader import load_borrowers_data
from src.borrower_analysis import calculate_borrower_kpis
from src.borrower_filters import apply_borrower_filters
from src.charts import (
    create_income_distribution_chart,
    create_credit_score_distribution_chart,
    create_employment_type_chart,
    create_region_borrower_chart,
)

st.set_page_config(
    page_title="Borrower Analytics",
    layout="wide",
)

st.title("Borrower Analytics")
st.write("Customer segmentation and borrower profile analysis.")

borrowers_df = load_borrowers_data()

st.sidebar.header("Borrower Filters")

region_options = sorted(borrowers_df["region"].dropna().unique().tolist())
employment_options = sorted(borrowers_df["employment_type"].dropna().unique().tolist())
education_options = sorted(borrowers_df["education_level"].dropna().unique().tolist())
delinquency_options = sorted(
    borrowers_df["existing_delinquency_flag"].astype(str).dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect("Select Region", options=region_options)
selected_employment_types = st.sidebar.multiselect("Select Employment Type", options=employment_options)
selected_education_levels = st.sidebar.multiselect("Select Education Level", options=education_options)
selected_delinquency_flags = st.sidebar.multiselect(
    "Select Existing Delinquency Flag",
    options=delinquency_options,
)

filtered_borrowers_df = apply_borrower_filters(
    borrowers_df,
    selected_regions,
    selected_employment_types,
    selected_education_levels,
    selected_delinquency_flags,
)

st.sidebar.write(f"Filtered borrowers: {len(filtered_borrowers_df):,}")

if filtered_borrowers_df.empty:
    st.warning("No borrower data available for the selected filters.")
else:
    kpis = calculate_borrower_kpis(filtered_borrowers_df)

    st.subheader("Borrower Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Borrowers", f"{kpis['total_borrowers']:,}")

    with col2:
        st.metric("Average Monthly Income", f"NPR {kpis['average_income']:,.0f}")

    with col3:
        st.metric("Average Credit Score", f"{kpis['average_credit_score']:.0f}")

    with col4:
        st.metric("Existing Delinquency Rate", f"{kpis['delinquency_rate']:.2%}")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(create_income_distribution_chart(filtered_borrowers_df), use_container_width=True)

    with chart_col2:
        st.plotly_chart(create_credit_score_distribution_chart(filtered_borrowers_df), use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.plotly_chart(create_employment_type_chart(filtered_borrowers_df), use_container_width=True)

    with chart_col4:
        st.plotly_chart(create_region_borrower_chart(filtered_borrowers_df), use_container_width=True)

    st.subheader("Borrower Records")
    st.dataframe(filtered_borrowers_df.head(50), use_container_width=True)