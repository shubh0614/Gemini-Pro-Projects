from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import sqlite3
import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#func to load Gemini model
def get_gemini_resp(ques,prompt):
    model=genai.GenerativeModel('gemini-pro')
    resp= model.generate_content([prompt,ques])
    return resp.text

#func to retrieve query from db
def read_sql_query(query,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(query)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt= """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """


st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_resp(question,prompt)
    st.subheader("Generated Query is: ")
    st.write(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is: ")
    for row in response:
        print(row)
        st.write(row)
