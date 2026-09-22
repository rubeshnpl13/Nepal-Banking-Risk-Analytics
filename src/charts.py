import plotly.express as px


def create_loan_product_chart(loans_df):
    product_counts = (
        loans_df["product_type"]
        .value_counts()
        .reset_index()
    )
    product_counts.columns = ["product_type", "loan_count"]

    fig = px.bar(
        product_counts,
        x="product_type",
        y="loan_count",
        color="product_type",
        title="Loan Portfolio by Product Type",
        text="loan_count",
    )

    fig.update_layout(
        xaxis_title="Product Type",
        yaxis_title="Number of Loans",
        showlegend=False,
    )

    return fig


def create_delinquency_chart(loans_df):
    status_counts = (
        loans_df["status"]
        .value_counts()
        .reset_index()
    )
    status_counts.columns = ["status", "count"]

    fig = px.pie(
        status_counts,
        names="status",
        values="count",
        title="Loan Delinquency Status Distribution",
        hole=0.4,
    )

    return fig


def create_npa_by_region_chart(loans_df):
    npa_region = (
        loans_df.groupby("region", as_index=False)["npa_flag"]
        .mean()
    )

    npa_region["npa_ratio_pct"] = npa_region["npa_flag"] * 100

    fig = px.bar(
        npa_region,
        x="region",
        y="npa_ratio_pct",
        color="region",
        title="NPA Ratio by Region",
        text="npa_ratio_pct",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="NPA Ratio (%)",
        showlegend=False,
    )

    return fig