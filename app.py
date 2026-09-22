import streamlit as st

from src.data_loader import load_loans_data
from src.kpi_calculations import calculate_portfolio_kpis


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
    st.metric(
        label="Total Loans",
        value=f"{kpis['total_loans']:,}",
    )

with col2:
    st.metric(
        label="Outstanding Balance",
        value=f"NPR {kpis['total_outstanding_balance']:,.0f}",
    )

with col3:
    st.metric(
        label="NPA Ratio",
        value=f"{kpis['npa_ratio']:.2%}",
    )

with col4:
    st.metric(
        label="Default Rate",
        value=f"{kpis['default_rate']:.2%}",
    )


st.subheader("Expected Loss and Credit Risk")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        label="Total EAD",
        value=f"NPR {kpis['total_ead']:,.0f}",
    )

with col6:
    st.metric(
        label="Expected Loss",
        value=f"NPR {kpis['total_expected_loss']:,.0f}",
    )

with col7:
    st.metric(
        label="Average PD",
        value=f"{kpis['average_pd']:.2%}",
    )

with col8:
    st.metric(
        label="Average LGD",
        value=f"{kpis['average_lgd']:.2%}",
    )

st.write(kpis)