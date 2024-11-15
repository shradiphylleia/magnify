import streamlit as st
from PIL import Image
import os
import time
import re
import pandas as pd
from vizualization import plot_nutrient_composition, plot_nutrient_percentage
from report_download import generate_report
from threshold import load_rda_data, threshold


from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
rda_file = "data\dataRDA.xlsx"
rda_data = load_rda_data(rda_file)

generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 32,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-002",
  generation_config=generation_config,
)

st.title("magnify")
st.subheader("understanding food and nutrition")


#image uploading
option=st.radio("How would you like to upload the image?",["Local device","Capture now"])

if option=='Local device':
    uploaded_file = st.file_uploader("Upload from your device",type=['jpg','png'],help='Upload')
else:
    uploaded_file=st.camera_input("Take the picture",help="allow camera permissions")

matches=[]

with st.container():
  if uploaded_file is not None:
    st.image(uploaded_file)
    response = model.generate_content([
    Image.open(uploaded_file),
    "get the text from the image",
    "Image: what is the text in the image",
  ])
    st.header("Detected text is below:")
    st.write(response.text)
    extract_status=True
    pattern = r"([A-Za-z\s]+(?:[B][0-9]|C|D)?)\s*[-:]\s*([<]?[0-9\.]+)\s*([a-zA-Z/%]*)"
    matches = re.findall(pattern, response.text)

  
  else:
    st.write('We were not able to detect a file at the moment.Drag or capture file to get started')


target_keywords = {
    "Protein (PE ratio)": "Protein",
    "Calcium (mg/d)": "Calcium",
    "Magnesium (mg/d)": "Magnesium",
    "Iron (mg/d)": "Iron",
    "Zinc (mg/d)": "Zinc",
    "Iodine (µg/d)": "Iodine",
    "Niacin (mg/d)": "Niacin",
    "Vitamin B6 (mg/d)": "Vitamin B6",
    "Folate (µg/d)": "Folate",
    "Vitamin C (mg/d)": "Vitamin C",
    "Vitamin A (µg/d)": "Vitamin A",
    "Vitamin D (IU/d)": "Vitamin D"
}

data = {category: {} for category in target_keywords.keys()}
data["Other"] = {}

if uploaded_file:
  for match in matches:
      name, value, unit = match
      name = name.strip()

      try:
          value = float(value.replace("<", ""))
      except ValueError:
          pass

      found = False
      for category, keyword in target_keywords.items():
          if keyword in name:
              data[category] = {"value": value, "unit": unit}
              found = True
              break

      if not found:
          data["Other"][name] = {"value": value, "unit": unit}


  with st.container():
    st.header("Detected the given nutritional values")
    st.write(data)

  with st.container():
    plot_nutrient_composition(data)

  with st.container():
     plot_nutrient_percentage(data)
  
  with st.container():
     generate_report(data)

  with st.container():
  #  slider for age 
    st.header("RDA Analysis")
    age=st.select_slider(label='Select the category which fits you best',options=["Infants(0-6m)","Infants(7-12m)","1-3Y","4-6Y","7-9Y","10-12Y","13-15Y","16-18Y","18+","Pregnant","Lactation(0-6m)","Lactation(7-12)m"],value="18+")
    if age is not None:
       threshold(rda_data,age)
    else:
       st.write("No RDA data available for the selected age group.")




response=""
st.header("Chat and interact to get more insights")

if "messages" not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message['content'])

if prompt := st.chat_input("ask here"):
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
          st.markdown(prompt)

# Display assistant response in chat message container
if prompt is not None:
    with st.chat_message("assistant"):
      stream = model.generate_content(prompt)
      response = st.write(stream.text)
      st.session_state.messages.append({"role": "assistant", "content": response})
  