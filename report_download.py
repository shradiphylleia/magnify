import pandas as pd
import streamlit as st

def generate_report(information):
    # Convert data to DataFrame and export as CSV
    report_df = pd.DataFrame.from_dict(information, orient="index")
    report_csv = report_df.to_csv().encode("utf-8")
    st.download_button(
        label="Download Nutrient Report",
        data=report_csv,
        file_name="nutrient_report.csv",
        mime="text/csv"
    )
