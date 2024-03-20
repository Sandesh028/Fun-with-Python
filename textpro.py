# -*- coding: utf-8 -*-
import sys
import os
import collections
import string
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import textstat
from transformers import pipeline

# Ensure required NLTK datasets are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_text(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            text = f.read()
        
        # Basic stats
        total_lines = text.count(os.linesep)
        total_characters = len(text) - text.count(" ") - total_lines
        words = text.split()
        total_words = len(words)
        unique_words = len(set(words))
        special_chars_count = sum(v for k, v in collections.Counter(text).items() if k in string.punctuation)
        
        # Word frequency analysis (excluding stopwords)
        filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
        word_frequencies = collections.Counter(filtered_words).most_common(10)
        
        # Reading level assessment using textstat
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        
        # Sentence Analysis
        sentences = nltk.sent_tokenize(text)
        average_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
        
        # Enhanced Sentiment Analysis
        sentiment_result = sentiment_pipeline(text[:512])  # Limiting to first 512 chars for performance
        sentiment = sentiment_result[0]['label']
        
        # Compile results
        results = {
            "Total Lines": total_lines,
            "Total Characters": total_characters,
            "Total Words": total_words,
            "Unique Words": unique_words,
            "Special Characters": special_chars_count,
            "Top 10 Frequent Words": word_frequencies,
            "Reading Level (Flesch-Kincaid Grade)": flesch_kincaid_grade,
            "Average Sentence Length": average_sentence_length,
            "Sentiment": sentiment,
        }
        
        return results

    except IOError:
        print(f'"{filepath}" cannot be opened.')
        return None

def print_report(results, output_path=None):
    report = ""
    if results:
        for key, value in results.items():
            report += f"{key}: {value}\n"
        report += "\nAnalysis complete!"
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(report)
            print(f"Report saved to {output_path}")
        else:
            print(report)
    else:
        print("No data to display.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhanced_text_analyzer.py TEXTFILE [OUTPUTFILE]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    results = analyze_text(filepath)
    print_report(results, output_path)
