import streamlit as st
import pandas as pd
import glob
import os

st.title("Threshold Achievement Year by Country")

# Find all the threshold output CSVs
csv_files = glob.glob("*_threshold_years_80.csv")

if not csv_files:
    st.warning("No threshold results found. Please run the calculation script first.")
else:
    selected_csv = st.selectbox("Select a threshold results file:", csv_files)
    df = pd.read_csv(selected_csv)
    st.write(f"### Year each country achieved the threshold ({selected_csv}):")
    st.dataframe(df)

    # Optionally: search/filter by country
    country = st.text_input("Search for a country:")
    if country:
        filtered = df[df['Country'].str.contains(country, case=False, na=False)]
        st.dataframe(filtered)
