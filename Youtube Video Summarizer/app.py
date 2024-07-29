import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    resp=model.generate_content(prompt+transcript_text)
    return resp.text

def extract_transcript(yt_url):
    try:
        vid_id=yt_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(vid_id)
        
        t_text=""
        for i in transcript_text:
            t_text+=" "+i["text"]
        return t_text

    except Exception as e:
        raise e

prompt="""You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 500 words. Please provide the summary of the text given here:  """


st.title("Youtube Video Transcript Summarizer")
yt_link=st.text_input("Enter Youtube Video Link:")

if yt_link:
    vid_id=((yt_link.split("=")[1]).split("=")[0]).split("&")[0]
    st.image(f"http://img.youtube.com/vi/{vid_id}/0.jpg", use_column_width=True)

if st.button("Get Transcript Summary"):
    transcript_text=extract_transcript(yt_link)
    if transcript_text:
        resp=generate_gemini_content(transcript_text,prompt)
        st.write("Summary of Video is :\n"  + resp)