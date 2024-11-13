import pandas as pd
import streamlit as st

def load_rda_data(file_path):
    return pd.read_excel(file_path)

def check_thresholds(actual_data, rda_data, nutrients):
    threshold_results = {}
    for nutrient in nutrients:
        actual_value = actual_data.get(nutrient, {}).get("value", 0)
        rda_value = rda_data.get(nutrient, 0)

        if actual_value < rda_value:
            threshold_results[nutrient] = "Below RDA"
        elif actual_value > rda_value:
            threshold_results[nutrient] = "Above RDA"
        else:
            threshold_results[nutrient] = "Meets RDA"
        
        st.write(f"Comparing {nutrient}: Actual = {actual_value}, RDA = {rda_value}")


    return threshold_results
