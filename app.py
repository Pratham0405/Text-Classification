import streamlit as st
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

# Function to extract text from the URL
def extract_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from HTML
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return str(e)

# Function to analyze the text and calculate metrics
def analyze_text(text):
    # Calculate sentiment scores
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    
    # Calculate other metrics
    sentences = sent_tokenize(text)
    total_sentences = len(sentences)
    total_words = len(word_tokenize(text))
    words = [word for word in word_tokenize(text.lower()) if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    word_count = Counter(filtered_words)
    total_complex_words = sum(1 for word in word_count if word_count[word] > 2)
    avg_sentence_length = total_words / total_sentences
    percentage_complex_words = (total_complex_words / total_words) * 100

    # Calculate Fog index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Calculate average word length
    total_characters = sum(len(word) for word in filtered_words)
    avg_word_length = total_characters / total_words

    # Count personal pronouns
    personal_pronouns = ['i', 'me', 'my', 'mine', 'myself', 'you', 'your', 'yours', 'yourself', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'we', 'us', 'our', 'ours', 'ourselves', 'they', 'them', 'their', 'theirs', 'themselves']
    personal_pronoun_count = sum(word_count[pronoun] for pronoun in personal_pronouns if pronoun in word_count)

    # Calculate syllable count per word
    syllable_count_per_word = 0
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word.endswith(('es', 'ed')):
            word = word[:-2]
        elif word.endswith('e'):
            word = word[:-1]
        syllables = re.findall(r'[aeiou]+', word)
        syllable_count_per_word += max(1, len(syllables))

    return polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words, fog_index, avg_word_length, total_words, syllable_count_per_word, personal_pronoun_count

# Streamlit app
def main():
    st.title("Website Text Analysis App")
    st.write("Enter the URL of the website to analyze its text:")

    # Input URL
    url = st.text_input("URL")

    if st.button("Analyze"):
        if url:
            st.write(f"Analyzing text from {url}...")
            text = extract_text(url)
            if text:
                st.write("Text extracted from the website:")
                st.write(text)

                # Analyze text
                (polarity_score, subjectivity_score, avg_sentence_length, percentage_complex_words,
                fog_index, avg_word_length, total_words, syllable_count_per_word, personal_pronoun_count) = analyze_text(text)

                st.write("Analysis Results:")
                st.write(f"Polarity Score: {polarity_score}")
                st.write(f"Subjectivity Score: {subjectivity_score}")
                st.write(f"Average Sentence Length: {avg_sentence_length}")
                st.write(f"Percentage of Complex Words: {percentage_complex_words}")
                st.write(f"Fog Index: {fog_index}")
                st.write(f"Average Word Length: {avg_word_length}")
                st.write(f"Total Words: {total_words}")
                st.write(f"Syllable Count per Word: {syllable_count_per_word}")
                st.write(f"Personal Pronouns Count: {personal_pronoun_count}")

            else:
                st.write("Failed to extract text from the URL.")
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
