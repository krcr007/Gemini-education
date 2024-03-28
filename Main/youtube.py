import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

api = "AIzaSyAxPJTpSHwA2Ng-rZ7FPXyUuhXc8Jgs_nE"
genai.configure(api_key=api)

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and Detailed notes on the topic every topic should be explained section by section such that anyone would learn from that topic and score full marks in the exam """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
            transcript+=" " +i["text"]
        return transcript


    except Exception as e:
        raise e

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text1 = extract_transcript_details(youtube_link)

    if transcript_text1:
        summary = generate_gemini_content(transcript_text1, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)