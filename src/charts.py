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

def create_loan_origination_trend_chart(loans_df):
    trend_df = (
        loans_df.groupby("origination_date", as_index=False)
        .size()
    )
    trend_df.columns = ["origination_date", "loan_count"]

    fig = px.line(
        trend_df,
        x="origination_date",
        y="loan_count",
        title="Loan Originations Over Time",
        markers=True,
    )

    fig.update_layout(
        xaxis_title="Origination Date",
        yaxis_title="Number of Loans",
    )

    return fig

def create_pd_lgd_scatter_chart(loans_df):
    fig = px.scatter(
        loans_df,
        x="pd",
        y="lgd",
        size="ead",
        color="product_type",
        hover_data=["loan_id", "region", "status"],
        title="PD vs LGD Risk Scatter",
        size_max=30,
    )

    fig.update_layout(
        xaxis_title="Probability of Default (PD)",
        yaxis_title="Loss Given Default (LGD)",
    )

    return fig


def create_vintage_npa_chart(loans_df):
    vintage_df = (
        loans_df.groupby("vintage", as_index=False)
        .agg(
            total_loans=("loan_id", "count"),
            npa_ratio=("npa_flag", "mean"),
            default_rate=("defaulted_flag", "mean"),
        )
        .sort_values("vintage")
    )

    vintage_df["npa_ratio_pct"] = vintage_df["npa_ratio"] * 100
    vintage_df["default_rate_pct"] = vintage_df["default_rate"] * 100

    fig = px.line(
        vintage_df,
        x="vintage",
        y="npa_ratio_pct",
        markers=True,
        title="Vintage Analysis: NPA Ratio by Origination Cohort",
    )

    fig.update_layout(
        xaxis_title="Vintage",
        yaxis_title="NPA Ratio (%)",
    )

    return fig

def create_income_distribution_chart(borrowers_df):
    fig = px.histogram(
        borrowers_df,
        x="monthly_income_npr",
        nbins=30,
        title="Borrower Income Distribution",
    )

    fig.update_layout(
        xaxis_title="Monthly Income (NPR)",
        yaxis_title="Number of Borrowers",
    )

    return fig


def create_credit_score_distribution_chart(borrowers_df):
    fig = px.histogram(
        borrowers_df,
        x="credit_score",
        nbins=30,
        title="Credit Score Distribution",
    )

    fig.update_layout(
        xaxis_title="Credit Score",
        yaxis_title="Number of Borrowers",
    )

    return fig


def create_employment_type_chart(borrowers_df):
    employment_df = (
        borrowers_df["employment_type"]
        .value_counts()
        .reset_index()
    )
    employment_df.columns = ["employment_type", "count"]

    fig = px.bar(
        employment_df,
        x="employment_type",
        y="count",
        color="employment_type",
        title="Borrowers by Employment Type",
        text="count",
    )

    fig.update_layout(
        xaxis_title="Employment Type",
        yaxis_title="Number of Borrowers",
        showlegend=False,
    )

    return fig


def create_region_borrower_chart(borrowers_df):
    region_df = (
        borrowers_df["region"]
        .value_counts()
        .reset_index()
    )
    region_df.columns = ["region", "count"]

    fig = px.bar(
        region_df,
        x="region",
        y="count",
        color="region",
        title="Borrowers by Region",
        text="count",
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Number of Borrowers",
        showlegend=False,
    )

    return fig

def create_npa_by_employment_chart(joined_df):
    summary = (
        joined_df.groupby("employment_type_borrower")
        .agg(
            total_loans=("loan_id", "count"),
            npa_loans=("npa_flag", "sum"),
        )
        .reset_index()
    )

    summary["npa_ratio"] = summary["npa_loans"] / summary["total_loans"]

    fig = px.bar(
        summary.sort_values("npa_ratio", ascending=False),
        x="employment_type_borrower",
        y="npa_ratio",
        color="employment_type_borrower",
        text="npa_ratio",
        title="NPA Ratio by Employment Type",
    )

    fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
    fig.update_layout(
        xaxis_title="Employment Type",
        yaxis_title="NPA Ratio",
        yaxis_tickformat=".0%",
        showlegend=False,
    )

    return fig


def create_expected_loss_by_borrower_region_chart(joined_df):
    summary = (
        joined_df.groupby("region_borrower")
        .agg(
            total_expected_loss_npr=("expected_loss_npr", "sum"),
        )
        .reset_index()
    )

    fig = px.bar(
        summary.sort_values("total_expected_loss_npr", ascending=True),
        x="total_expected_loss_npr",
        y="region_borrower",
        orientation="h",
        color="region_borrower",
        text="total_expected_loss_npr",
        title="Expected Loss by Borrower Region",
    )

    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(
        xaxis_title="Total Expected Loss (NPR)",
        yaxis_title="Borrower Region",
        showlegend=False,
    )

    return fig


def create_average_pd_by_education_chart(joined_df):
    summary = (
        joined_df.groupby("education_level_borrower")
        .agg(
            average_pd=("pd", "mean"),
        )
        .reset_index()
    )

    fig = px.bar(
        summary.sort_values("average_pd", ascending=False),
        x="education_level_borrower",
        y="average_pd",
        color="education_level_borrower",
        text="average_pd",
        title="Average PD by Education Level",
    )

    fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
    fig.update_layout(
        xaxis_title="Education Level",
        yaxis_title="Average PD",
        yaxis_tickformat=".0%",
        showlegend=False,
    )

    return fig