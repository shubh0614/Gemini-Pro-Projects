from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#func to load Gemini pro model and get response
model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(ques):
    resp=chat.send_message(ques,stream=True)
    return resp


#initialize streamlit app
st.set_page_config(page_title="Q&A ChatBot")
st.header("Q&A ChatBot")

#initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input = st.text_input("Input: ",key="input")
submit=st.button("Ask the Question")

if submit and input:
    resp=get_gemini_response(input)
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is")
    for chunk in resp:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("ChatBot",chunk.text))

st.subheader("The Chat History is: ")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")