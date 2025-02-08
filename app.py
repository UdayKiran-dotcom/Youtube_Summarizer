import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for the summarizer
prompt = """You are a YouTube Video Summarizer tasked with providing an in-depth analysis of a video's content. Your goal is to generate a comprehensive summary that captures the main points, key arguments, and supporting details within a 750-word limit. Please thoroughly analyze the transcript text provided and offer a detailed summary, ensuring to cover all relevant aspects of the video: """

# Function to extract transcript from YouTube
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " "
        for i in transcript_text:
            transcript += " " + i['text']

        return transcript

    except Exception as e:
        raise e

# Function to generate content using Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit App UI
st.title("📹 YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter the YouTube Video URL:")

# Validate YouTube link
if youtube_link and "watch?v=" not in youtube_link:
    st.error("❌ Please enter a valid YouTube URL.")

# Display thumbnail
if youtube_link and "watch?v=" in youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

# Button to get detailed notes
if st.button("Get Detailed Notes"):
    with st.spinner("⏳ Fetching transcript and generating notes..."):
        try:
            transcript_text = extract_transcript_details(youtube_link)

            if transcript_text:
                summary = generate_gemini_content(transcript_text, prompt)
                st.markdown("## 📝 Detailed Notes:")
                st.write(summary)

                # Download button for notes
                st.download_button("📥 Download Notes", summary, file_name="youtube_notes.txt")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")

st.markdown("---")
