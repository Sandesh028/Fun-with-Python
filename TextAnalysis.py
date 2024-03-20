import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import collections
import string
import nltk
import fitz  # PyMuPDF
from nltk.corpus import stopwords
import textstat
from transformers import pipeline

# Ensure required NLTK datasets are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

class TextAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Analysis Tool")
        self.configure(bg="#F5F5F5")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        self.style.map('Treeview', background=[('selected', '#F5F5F5')])
        
        self.init_ui()
        self.analysis_results = {}  # To store the latest analysis results

    def init_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=5, fill='x', expand=True)

        self.entry = ttk.Entry(self.frame)
        self.entry.pack(side=tk.LEFT, expand=True, fill='x')

        browse_btn = ttk.Button(self.frame, text="Browse", command=self.open_file)
        browse_btn.pack(side=tk.RIGHT, padx=(5,0))

        analyze_btn = ttk.Button(self, text="Analyze", command=self.analyze_and_display)
        analyze_btn.pack(pady=(5, 5))

        self.results_area = ttk.Treeview(self, columns=("Feature", "Value"), show="headings", height=15)
        self.results_area.heading("Feature", text="Feature")
        self.results_area.heading("Value", text="Value")
        self.results_area.column("Feature", anchor=tk.W, width=200)
        self.results_area.column("Value", anchor=tk.W, width=500)
        self.results_area.pack(fill=tk.BOTH, expand=True)

        save_btn = ttk.Button(self, text="Save Report", command=self.save_report)
        save_btn.pack(pady=(5, 10))

        detail_btn = ttk.Button(self, text="Show Detailed Frequencies", command=self.show_detailed_word_frequencies)
        detail_btn.pack(pady=(5, 0))

        for widget in self.winfo_children():
            widget.pack_configure(fill='both', expand=True)
            if hasattr(widget, "winfo_children"):
                for child in widget.winfo_children():
                    child.pack_configure(fill='both', expand=True)

        self.minsize(600, 400)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, filepath)

    def analyze_and_display(self):
        filepath = self.entry.get()
        if filepath and os.path.isfile(filepath):
            self.analysis_results = analyze_text(filepath)  # Store results
            for i in self.results_area.get_children():
                self.results_area.delete(i)
            for k, v in self.analysis_results.items():
                if k == "Top 10 Frequent Words (excluding common stopwords)":
                    self.results_area.insert("", tk.END, values=(k, "See 'Show Detailed Frequencies' button"))
                else:
                    self.results_area.insert("", tk.END, values=(k, v))
        else:
            messagebox.showerror("Error", "Please select a valid file.")

    def save_report(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as file:
                for child in self.results_area.get_children():
                    feature, value = self.results_area.item(child, 'values')
                    file.write(f"{feature}: {value}\n")
            messagebox.showinfo("Info", "Report saved successfully.")

    def show_detailed_word_frequencies(self):
        if "Top 10 Frequent Words (excluding common stopwords)" in self.analysis_results:
            top_words = self.analysis_results["Top 10 Frequent Words (excluding common stopwords)"]
            detailed_text =             "\n".join([f"{word}: {count}" for word, count in top_words])

            popup = tk.Toplevel(self)
            popup.title("Detailed Word Frequencies")
            text_widget = tk.Text(popup, wrap=tk.WORD, height=10, width=50)
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, detailed_text)
            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
            close_btn = ttk.Button(popup, text="Close", command=popup.destroy)
            close_btn.pack(pady=(0, 10))
        else:
            messagebox.showinfo("Information", "Please perform analysis to see detailed word frequencies.")

def analyze_text(filepath):
    text = ""
    try:
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding="iso-8859-1") as f:
                text = f.read()

        # Basic stats
        total_lines = text.count('\n')
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
        average_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0
        
        # Enhanced Sentiment Analysis
        sentiment_result = sentiment_pipeline(text[:512])  # Limiting to first 512 chars for performance reasons
        sentiment = sentiment_result[0]['label'] if sentiment_result else "Analysis Failed"
        
        # Compile results
        results = {
            "Total Lines": total_lines,
            "Total Characters (excluding spaces and new lines)": total_characters,
            "Total Words": total_words,
            "Unique Words": unique_words,
            "Special Characters Count": special_chars_count,
            "Top 10 Frequent Words (excluding common stopwords)": word_frequencies,
            "Reading Level (Flesch-Kincaid Grade)": flesch_kincaid_grade,
            "Average Sentence Length": average_sentence_length,
            "Sentiment": sentiment,
        }
        
        return results

    except IOError:
        print(f'"{filepath}" cannot be opened.')
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    app = TextAnalysisApp()
    app.mainloop()

