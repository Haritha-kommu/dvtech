import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
import docx
import pdfplumber
import nltk

# Ensure required corpora are available
try:
    import textblob
    textblob.download_corpora()
except Exception:
    nltk.download('punkt')

# -------------------------------
# Function to extract text
# -------------------------------
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + " "

    elif uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    return text.strip()

# -------------------------------
# Streamlit App
# -------------------------------
st.title("📊 Document Visualization App")

uploaded_file = st.file_uploader("Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

if uploaded_file:
    text = extract_text_from_file(uploaded_file)

    if text:
        st.subheader("📄 Extracted Text Preview")
        st.write(text[:500] + "...")  # Show first 500 characters

        # -------------------------------
        # Word Frequency (Bar Chart)
        # -------------------------------
        words = text.lower().replace(".", "").replace(",", "").split()
        word_counts = Counter(words)
        common_words = word_counts.most_common(10)

        labels, values = zip(*common_words)
        fig, ax = plt.subplots()
        ax.bar(labels, values, color="orange")
        ax.set_title("Top 10 Word Frequencies")
        ax.set_xlabel("Words")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # -------------------------------
        # Sentiment Analysis (Pie Chart)
        # -------------------------------
        try:
            blob = TextBlob(text)
            sentences = blob.sentences

            pos, neg, neu = 0, 0, 0
            for s in sentences:
                polarity = s.sentiment.polarity
                if polarity > 0:
                    pos += 1
                elif polarity < 0:
                    neg += 1
                else:
                    neu += 1

            fig2, ax2 = plt.subplots()
            ax2.pie([pos, neg, neu],
                    labels=["Positive", "Negative", "Neutral"],
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["green", "red", "gray"])
            ax2.set_title("Sentiment Analysis")
            st.pyplot(fig2)

        except Exception as e:
            st.error("⚠️ Sentiment analysis failed. Please ensure required corpora are available.")
            st.text(str(e))
