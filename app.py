# import streamlit as st

# enable = st.checkbox("Enable camera")
# picture = st.camera_input("Take a picture", disabled=not enable)

# if picture:
#     st.image(picture)

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Uplaod an image",type=['jpg','png'],help='Upload')
if uploaded_file is not None:
    st.image(uploaded_file)

#backend logic here
#allow for imag to be caputred if user says so


