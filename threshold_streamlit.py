import streamlit as st
import pandas as pd
import glob
import os

st.title("Threshold Achievement Year by Country")

def find_years(input_csv, threshold):
    df = pd.read_csv(input_csv)
    years = df.columns[1:]  # Exclude 'Country'
    result = []
    for idx, row in df.iterrows():
        country = row.iloc[0]
        vals = row.iloc[1:]
        try:
            year_idx = next(i for i, v in enumerate(vals) if pd.to_numeric(v, errors='coerce') >= threshold)
            year = years[year_idx]
        except StopIteration:
            year = None
        result.append({"Country": country, "Year": year})
    out_df = pd.DataFrame(result)
    out_df = out_df[out_df['Year'].notna()]
    return out_df

threshold = st.number_input("Set threshold value", min_value=0.0, max_value=100.0, value=80.0, step=0.1)

# List all CSV files in DATACSV automatically
import os

data_folder = "DATACSV"
if not os.path.exists(data_folder):
    st.error(f"Data folder '{data_folder}' does not exist.")
    st.stop()

csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
st.write(f"Files in {data_folder}:", csv_files)

if not csv_files:
    st.warning(f"No CSV files found in '{data_folder}'. Please upload data files.")
    st.stop()

input_csvs = [os.path.join(data_folder, f) for f in csv_files]
selected_csv = st.selectbox("Select a data file:", input_csvs)

if selected_csv:
    try:
        df = find_years(selected_csv, threshold)
        st.write(f"### Year each country achieved the threshold ({threshold}%) in {selected_csv}:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to load or process '{selected_csv}': {e}")

    # Optionally: search/filter by country
    country = st.text_input("Search for a country:")
    if 'df' in locals() and country:
        filtered = df[df['Country'].str.contains(country, case=False, na=False)]
        st.dataframe(filtered)
