import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
load_dotenv()
import json


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model=genai.GenerativeModel("gemini-pro")
    resp=model.generate_content(input)
    return resp.text

def pdf_to_text(pdf_file):
    reader=pdf.PdfReader(pdf_file)
    text=""
    for p in range(len(reader.pages)):
        p=reader.pages[p]
        text+=str(p.extract_text())
    return text




input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

st.title("ATS Checker")
st.text("Get ATS Score")
jd=st.text_area("Paste JD for the role")
pdf_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload Resume")
submit=st.button("Submit")

if submit:
    if pdf_file is not None:
        text=pdf_to_text(pdf_file)
        resp=get_gemini_response(input_prompt)
        st.subheader(resp)

