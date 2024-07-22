from dotenv import load_dotenv
load_dotenv()     #Loading all env var
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



model=genai.GenerativeModel("gemini-pro")

#func to load gemini pro model and get resp
def get_gemini_response(ques):
    response=model.generate_content(ques)
    return response.text


#initializing streamlit
st.set_page_config(page_title="Q&A App")
st.header("End-To-End LLM App")

input=st.text_input("Input: ", key="input")
submit=st.button("Ask the question")


#when submit button is clicked
if submit:
    response=get_gemini_response(input)
    st.subheader("The Response is: ")
    st.write(response)


