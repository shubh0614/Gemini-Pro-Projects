from dotenv import load_dotenv
load_dotenv()     #Loading all env var
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model=genai.GenerativeModel("gemini-1.5-flash")

#func to load gemini pro model and get resp
def get_gemini_response(input,image):
    if input!="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)

    return response.text

#initializing streamlit
st.set_page_config(page_title="Image Analyser App")
st.header("End-To-End LLM App")

input=st.text_input("Input: ", key="input")

uploaded_file= st.file_uploader("Choose an Image.... ", type=["jpeg","jpg","png"])
image=""
#If error occurs when uploading image use "streamlit run vision_app.py --server.enableXsrfProtection false"
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image",use_column_width=True)


submit=st.button("Tell me about Image")

#when submit button is clicked
if submit:
    response=get_gemini_response(input,image)
    st.subheader("The Response is: ")
    st.write(response)




