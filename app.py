import streamlit as st
from src.data_loader import (
    load_loans_data,
    load_borrowers_data,
    load_combined_data,
    load_summary_data,
)
#check git and github
st.set_page_config(page_title="Nepal Banking Risk Analytics Dashboard", layout="wide")

st.title("Nepal Banking Risk Analytics Dashboard")
st.write("Dataset loading test")

loans_df = load_loans_data()
borrowers_df = load_borrowers_data()
combined_df = load_combined_data()
summary_df = load_summary_data()

st.subheader("Loans Data")
st.dataframe(loans_df.head())

st.subheader("Borrowers Data")
st.dataframe(borrowers_df.head())

st.subheader("Combined Data")
st.dataframe(combined_df.head())

st.subheader("Summary Data")
st.dataframe(summary_df)