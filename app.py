import streamlit as st
from PIL import Image
import os
import time
import re
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

 
import google.generativeai as genai
GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def progress():
  progress_text = "Operation in progress. Please wait."
  my_bar = st.progress(0, text=progress_text)

  for percent_complete in range(100):
      time.sleep(0.01)
      my_bar.progress(percent_complete + 1, text=progress_text)
  
  my_bar.empty()

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
st.subheader("understanding medical labels")

#image uploading
option=st.radio("How would you like to upload the image?",["Local device","Capture now"])

if option=='Local device':
    # progress()
    uploaded_file = st.file_uploader("Upload from your device",type=['jpg','png'],help='Upload')
else:
    # progress()
    uploaded_file=st.camera_input("Take the picture",help="allow camera permissions")


extract_status=False

if uploaded_file is not None:
  st.image(uploaded_file)
  response = model.generate_content([
  Image.open(uploaded_file),
  "get the text from the image",
  "Image: what is the text in the image",
])

  st.header("Detected text is below:")
  progress()
  st.write(response.text)
  extract_status=True

  ingredient_pattern = r"([A-Za-z\s]+(?:\s[IP]+)?)\s*[\.\-]+\s*([0-9\.]+)%\s?w/v"

  text =response.text
  matches = re.findall(ingredient_pattern, text)
  print(matches)

  with st.container():
    st.subheader("Detected ingredients:")
    ingredients = [entry[0].strip() for entry in matches]
    concentrations = [float(entry[1]) for entry in matches]

# Display the data
st.write("Ingredients and Concentrations:")
st.table(matches)

fig, ax = plt.subplots()
# Bar chart
ax.barh(ingredients, concentrations, color='#208FD4')
# Labels and title
ax.set_xlabel('Concentration (%)')
ax.set_title('Concentration of Ingredients in the Medicine')

st.pyplot(fig)


if(extract_status==True):
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
  


# need a main page explaining stuf
#need to add other regex to make it more efficient