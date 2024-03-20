import streamlit as st
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import re

# Function to get text content from URL
def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from HTML
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return str(e)

# Function to analyze text
def analyze_text(text):
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    # Add more analysis as needed

    return polarity_score, subjectivity_score

# Streamlit app
def main():
    st.title("Website Text Analysis App")
    st.write("Enter the URL of the website to analyze its text:")

    # Input URL
    url = st.text_input("URL")

    if st.button("Analyze"):
        if url:
            st.write(f"Analyzing text from {url}...")
            text = get_text_from_url(url)
            if text:
                st.write("Text extracted from the website:")
                st.write(text)

                # Analyze text
      
