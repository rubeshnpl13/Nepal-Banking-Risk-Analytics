import streamlit as st

from src.model_data import create_default_model_dataset
from src.data_loader import load_loans_data
from src.kpi_calculations import calculate_portfolio_kpis
from src.charts import (
    create_loan_product_chart,
    create_delinquency_chart,
    create_npa_by_region_chart,
    create_loan_origination_trend_chart,
    create_pd_lgd_scatter_chart,
    create_vintage_npa_chart,
    create_npa_by_employment_chart,
    create_expected_loss_by_borrower_region_chart,
    create_average_pd_by_education_chart,
)

from src.data_loader import load_loans_data, load_borrowers_data
from src.join_analysis import (
    create_joined_loan_borrower_data,
    npa_ratio_by_employment_type,
    expected_loss_by_region,
    average_pd_by_education_level,
)

from src.filters import apply_filters
from src.portfolio_analysis import create_product_risk_summary
from src.export_utils import convert_df_to_csv

st.set_page_config(
    page_title="Nepal Banking Risk Analytics Dashboard",
    layout="wide",
)

st.title("Nepal Banking Risk Analytics Dashboard")
st.write("Credit risk overview of the synthetic Nepal loan portfolio.")

loans_df = load_loans_data()
borrowers_df = load_borrowers_data()
joined_df = create_joined_loan_borrower_data(loans_df, borrowers_df)
model_df = create_default_model_dataset(joined_df)
st.subheader("Default Model Dataset Preview")
st.write(f"Model dataset shape: {model_df.shape}")
st.dataframe(model_df.head(20), use_container_width=True)

st.subheader("Default Target Distribution")
st.write(model_df["defaulted_flag"].value_counts())
st.write(model_df["defaulted_flag"].value_counts(normalize=True))
# st.subheader("Join Debug")
# st.write(joined_df.columns.tolist())
# st.dataframe(joined_df.head(5), use_container_width=True)

st.sidebar.header("Portfolio Filters")

region_options = sorted(loans_df["region"].dropna().unique().tolist())
product_options = sorted(loans_df["product_type"].dropna().unique().tolist())
status_options = sorted(loans_df["status"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect("Select Region", options=region_options)
selected_products = st.sidebar.multiselect("Select Product Type", options=product_options)
selected_statuses = st.sidebar.multiselect("Select Loan Status", options=status_options)

filtered_loans_df = apply_filters(
    loans_df,
    selected_regions,
    selected_products,
    selected_statuses,
)

csv_data = convert_df_to_csv(filtered_loans_df)

st.sidebar.write(f"Filtered records: {len(filtered_loans_df):,}")

st.sidebar.markdown("---")
st.sidebar.subheader("Export Data")

st.sidebar.download_button(
    label="Download Filtered Loans CSV",
    data=csv_data,
    file_name="filtered_loans_data.csv",
    mime="text/csv",
)


#csv_data = convert_df_to_csv(filtered_loans_df)
kpis = calculate_portfolio_kpis(filtered_loans_df)

st.subheader("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Loans", f"{kpis['total_loans']:,}")

with col2:
    st.metric("Outstanding Balance", f"NPR {kpis['total_outstanding_balance']:,.0f}")

with col3:
    st.metric("NPA Ratio", f"{kpis['npa_ratio']:.2%}")

with col4:
    st.metric("Default Rate", f"{kpis['default_rate']:.2%}")

st.subheader("Expected Loss and Credit Risk")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Total EAD", f"NPR {kpis['total_ead']:,.0f}")

with col6:
    st.metric("Expected Loss", f"NPR {kpis['total_expected_loss']:,.0f}")

with col7:
    st.metric("Average PD", f"{kpis['average_pd']:.2%}")

with col8:
    st.metric("Average LGD", f"{kpis['average_lgd']:.2%}")

tab1, tab2 = st.tabs(["Dashboard Charts", "Portfolio Details"])

with tab1:
    st.subheader("Portfolio Charts")

    if filtered_loans_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        fig_product = create_loan_product_chart(filtered_loans_df)
        fig_delinquency = create_delinquency_chart(filtered_loans_df)
        fig_npa_region = create_npa_by_region_chart(filtered_loans_df)
        fig_trend = create_loan_origination_trend_chart(filtered_loans_df)
        fig_pd_lgd = create_pd_lgd_scatter_chart(filtered_loans_df)
        fig_vintage = create_vintage_npa_chart(filtered_loans_df)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(fig_product, use_container_width=True)

        with chart_col2:
            st.plotly_chart(fig_delinquency, use_container_width=True)

        st.plotly_chart(fig_npa_region, use_container_width=True)
        st.plotly_chart(fig_trend, use_container_width=True)

        risk_col1, risk_col2 = st.columns(2)

        with risk_col1:
            st.plotly_chart(fig_pd_lgd, use_container_width=True)

        with risk_col2:
            st.plotly_chart(fig_vintage, use_container_width=True)

with tab2:
    st.subheader("Risk Segmentation by Product")

    product_summary_df = create_product_risk_summary(filtered_loans_df)
    st.dataframe(product_summary_df, use_container_width=True)

    st.subheader("Filtered Loan Records")
    st.dataframe(filtered_loans_df.head(50), use_container_width=True)

#borrower-loan join analysis this for table
# st.subheader("Borrower-Loan Joined Analysis")
#
# joined_col1, joined_col2, joined_col3 = st.columns(3)
#
# with joined_col1:
#     st.markdown("### NPA Ratio by Employment Type")
#     st.dataframe(npa_ratio_by_employment_type(joined_df), use_container_width=True)
#
# with joined_col2:
#     st.markdown("### Expected Loss by Borrower Region")
#     st.dataframe(expected_loss_by_region(joined_df), use_container_width=True)
#
# with joined_col3:
#     st.markdown("### Average PD by Education Level")
#     st.dataframe(average_pd_by_education_level(joined_df), use_container_width=True)

# borrower-loan join analysis for the chart as well as table

st.subheader("Borrower-Loan Joined Analysis")

joined_chart_col1, joined_chart_col2 = st.columns(2)

with joined_chart_col1:
    st.plotly_chart(create_npa_by_employment_chart(joined_df), use_container_width=True)

with joined_chart_col2:
    st.plotly_chart(create_expected_loss_by_borrower_region_chart(joined_df), use_container_width=True)

st.plotly_chart(create_average_pd_by_education_chart(joined_df), use_container_width=True)

st.subheader("Joined Analysis Tables")

joined_col1, joined_col2, joined_col3 = st.columns(3)

with joined_col1:
    st.markdown("### NPA Ratio by Employment Type")
    st.dataframe(npa_ratio_by_employment_type(joined_df), use_container_width=True)

with joined_col2:
    st.markdown("### Expected Loss by Borrower Region")
    st.dataframe(expected_loss_by_region(joined_df), use_container_width=True)

with joined_col3:
    st.markdown("### Average PD by Education Level")
    st.dataframe(average_pd_by_education_level(joined_df), use_container_width=True)