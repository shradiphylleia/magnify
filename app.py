# import streamlit as st

# enable = st.checkbox("Enable camera")
# picture = st.camera_input("Take a picture", disabled=not enable)

# if picture:
#     st.image(picture)

import streamlit as st
from PIL import Image
import os
import time
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


st.text_input(label="enter to get more info on the medication info",help='enter text for further context')