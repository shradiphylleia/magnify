import matplotlib.pyplot as plt
import streamlit as st

def plot_nutrient_composition(data):
    nutrients = []
    values = []

    for key, info in data.items():
        if key == "Other":
            for sub_key, sub_info in info.items():
                unit = sub_info.get("unit", "")
                value = sub_info.get("value", 0)
                
                if unit == "mg":
                    value /= 1000
                elif unit == "mcg":
                    value /= 1_000_000
                elif unit == "%" or unit=='kcal':
                    continue   
                nutrients.append(sub_key)
                values.append(value)
        else:
            unit = info.get("unit", "")
            value = info.get("value", 0)
            if unit == "mg":
                value /= 1000
            elif unit == "mcg":
                value /= 1_000_000
            elif unit == "%":
                continue 
            else: 
                continue
            nutrients.append(key)
            values.append(value)

    fig, ax = plt.subplots(figsize=(10, 15))
    ax.barh(nutrients, values, color="#231DBD")
    ax.set_xlabel("Amount (g)")
    ax.set_title("Nutrient Composition per 100g")
    ax.invert_yaxis()  

    st.pyplot(fig)


def plot_nutrient_percentage(data):
    percent_nutrients = []
    percent_values = []

    for key, info in data.items():
        if key == 'Other':  
            for sub_key, sub_info in info.items():
                unit = sub_info.get("unit", "")
                value = sub_info.get("value", 0)
                if unit == "%":
                    percent_nutrients.append(sub_key)
                    percent_values.append(value)
        else:
            unit = info.get("unit", "")
            value = info.get("value", 0)
            if unit == "%":
                percent_nutrients.append(key)
                percent_values.append(value)

    if not percent_nutrients or not percent_values:
        st.write("No percentage-based nutrient data available to display.")
        return

    fig, ax = plt.subplots(figsize=(8, len(percent_nutrients) * 0.5))
    ax.barh(percent_nutrients, percent_values, color="#4CAF50")
    ax.set_xlabel("Percentage (%)")
    ax.set_title("Nutrient Composition by Percentage")

    st.pyplot(fig)



    # slider to filter nutirent percentage
    # added details on hover with altair
    # comparison with rda
