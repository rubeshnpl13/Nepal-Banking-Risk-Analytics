import streamlit as st

from src.data_loader import load_loans_data
from src.kpi_calculations import calculate_portfolio_kpis
from src.charts import (
    create_loan_product_chart,
    create_delinquency_chart,
    create_npa_by_region_chart,
)


st.set_page_config(
    page_title="Nepal Banking Risk Analytics Dashboard",
    layout="wide",
)

st.title("Nepal Banking Risk Analytics Dashboard")
st.write("Credit risk overview of the synthetic Nepal loan portfolio.")

loans_df = load_loans_data()
kpis = calculate_portfolio_kpis(loans_df)

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

st.subheader("Portfolio Charts")

fig_product = create_loan_product_chart(loans_df)
fig_delinquency = create_delinquency_chart(loans_df)
fig_npa_region = create_npa_by_region_chart(loans_df)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.plotly_chart(fig_product, use_container_width=True)

with chart_col2:
    st.plotly_chart(fig_delinquency, use_container_width=True)

st.plotly_chart(fig_npa_region, use_container_width=True)