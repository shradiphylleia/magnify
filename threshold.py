import pandas as pd
import streamlit as st


def load_rda_data(file_path):
    return pd.read_excel(file_path)

def threshold(rda_data,age):
    rda_age_group_data = rda_data[rda_data['Age'] == age]
    st.write(rda_age_group_data)