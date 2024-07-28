from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-1.5-flash")

#func to load gemini pro model and get resp
def get_gemini_response(input,image):
    response=model.generate_content([input,image[0]])

    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError("No file uploaded.")


#initialize streamlit app
st.set_page_config(page_title="Food Nutrition App")
st.header("Food Nutrition App")


uploaded_file= st.file_uploader("Choose an Image of Dish....",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the Dish..")

input_prompt="""
                You are an expert in nutritionist where you need to see the food items from the image
                and calculate the total calories, also provide the details of every food items with calories intake
                is below forma      
                1. Item 1 - no of calories
                2. Item 2 - no of calories
                ----
                ----
            """

#if submit button clicked``
if submit:
    image_data=input_image_details(uploaded_file)
    resp=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is: ")
    st.write(resp)






