import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
import os
import collections
import string
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

def open_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def analyze_and_display():
    filepath = entry.get()
    if filepath and os.path.isfile(filepath):
        results = analyze_text(filepath)
        output_text = "\n".join(f"{k}: {v}" for k, v in results.items())
        output_area.config(state=tk.NORMAL)
        output_area.delete(1.0, tk.END)
        output_area.insert(tk.END, output_text)
        output_area.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Please select a valid file.")

def save_report():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
        return
    report_text = output_area.get("1.0", tk.END)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(report_text)
    messagebox.showinfo("Info", "Report saved successfully.")

app = tk.Tk()
app.title("Text Analysis Tool")

frame = ttk.Frame(app)
frame.pack(padx=10, pady=5, fill='x', expand=True)

entry = ttk.Entry(frame)
entry.pack(side=tk.LEFT, expand=True, fill='x')

browse_btn = ttk.Button(frame, text="Browse", command=open_file)
browse_btn.pack(side=tk.RIGHT, padx=(5,0))

analyze_btn = ttk.Button(app, text="Analyze", command=analyze_and_display)
analyze_btn.pack(pady=(5, 5))

output_area = scrolledtext.ScrolledText(app, state='disabled', height=15)
output_area.pack(fill=tk.BOTH, expand=True)

save_btn = ttk.Button(app, text="Save Report", command=save_report)
save_btn.pack(pady=(5, 10))

app.mainloop()
