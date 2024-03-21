import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import collections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import fitz  # PyMuPDF
import textstat
from transformers import pipeline

# Attempt to import ttkthemes for enhanced UI themes
try:
    from ttkthemes import ThemedTk
except ImportError:
    ThemedTk = None
    print("ttkthemes not installed. Run 'pip install ttkthemes' for better UI themes.")

# Ensure required NLTK datasets are downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Initialize sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_text(filepath):
    text = ""
    try:
        if filepath.lower().endswith('.pdf'):
            with fitz.open(filepath) as doc:
                text = " ".join(page.get_text() for page in doc)
        else:
            with open(filepath, 'r', encoding="utf-8") as f:
                text = f.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return {}

    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    
    total_lines = text.count('\n') + 1
    total_chars = sum(c.isalnum() for c in text)
    special_chars_count = sum(not c.isalnum() and not c.isspace() for c in text)
    reading_level = textstat.flesch_kincaid_grade(text)
    sentences = nltk.sent_tokenize(text)
    average_sentence_length = sum(len(word_tokenize(sentence)) for sentence in sentences) / len(sentences)
    sentiment = sentiment_pipeline(text)[0]
    freq_dist = collections.Counter(filtered_words)  # Convert list to Counter object
    top_10_words = freq_dist.most_common(10)  # Now you can use .most_common() method

    results = {
        "Total Lines": total_lines,
        "Total Characters (excluding spaces and new lines)": total_chars,
        "Total Words": len(words),
        "Unique Words": len(set(words)),
        "Special Characters Count": special_chars_count,
        "Top 10 Frequent Words (excluding common stopwords)": top_10_words,  # Use the correct variable here
        "Reading Level (Flesch-Kincaid Grade)": reading_level,
        "Average Sentence Length": average_sentence_length,
        "Sentiment": sentiment['label']
    }

    return results


class TextAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Analysis Tool")

        if ThemedTk:
            self.root.set_theme('equilux')  # Example theme

        self.init_ui()
        self.analysis_results = {}

    def init_ui(self):
        # Create a Style object
        style = ttk.Style(self.root)

        # Define a new style that specifies the button color
        # Note: Depending on the active theme, some properties might not apply as expected
        style.configure('Blue.TButton', foreground='aqua', background='blue', font=('Helvetica', 10))

        # Now specify this style for buttons when creating them
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.entry = ttk.Entry(frame)
        self.entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

        browse_btn = ttk.Button(frame, text="Browse", command=self.open_file, style='Blue.TButton')
        browse_btn.pack(side=tk.RIGHT)

        analyze_btn = ttk.Button(self.root, text="Analyze", command=self.analyze_and_display, style='Blue.TButton')
        analyze_btn.pack(pady=(5, 0))

        self.results_area = ttk.Treeview(self.root, columns=("Feature", "Value"), show="headings", height=15)
        self.results_area.heading("Feature", text="Feature")
        self.results_area.heading("Value", text="Value")
        self.results_area.column("Feature", anchor=tk.W, width=200)
        self.results_area.column("Value", anchor=tk.W, width=500)
        self.results_area.pack(padx=10, pady=(5, 0), fill='both', expand=True)

        save_btn = ttk.Button(self.root, text="Save Report", command=self.save_report, style='Blue.TButton')
        save_btn.pack(pady=(5, 0))

        detail_btn = ttk.Button(self.root, text="Show Detailed Frequencies", command=self.show_detailed_word_frequencies, style='Blue.TButton')
        detail_btn.pack(pady=(5, 10))

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, filepath)

    def analyze_and_display(self):
        filepath = self.entry.get()
        if filepath and os.path.isfile(filepath):
            self.analysis_results = analyze_text(filepath)
            self.display_analysis_results()
        else:
            messagebox.showerror("Error", "Please select a file first.")

    def save_report(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as file:
                for child in self.results_area.get_children():
                    feature, value = self.results_area.item(child, 'values')
                    file.write(f"{feature}: {value}\n")
            messagebox.showinfo("Info", "Report saved successfully.")

    def show_detailed_word_frequencies(self):
        if "Top 10 Frequent Words (excluding common stopwords)" in self.analysis_results:
            top_words = self.analysis_results["Top 10 Frequent Words (excluding common stopwords)"]
            detailed_text = "\n".join([f"{word}: {count}" for word, count in top_words])
            popup = tk.Toplevel(self.root)
            popup.title("Detailed Word Frequencies")
            text_widget = tk.Text(popup, wrap=tk.WORD, height=10, width=50)
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, detailed_text)
            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
            close_btn = ttk.Button(popup, text="Close", command=popup.destroy)
            close_btn.pack(pady=(0, 10))
        else:
            messagebox.showinfo("Information", "Please perform analysis to see detailed word frequencies.")

    def display_analysis_results(self):
        # Clear existing items in the Treeview
        for i in self.results_area.get_children():
            self.results_area.delete(i)
        # Insert new analysis results
        for k, v in self.analysis_results.items():
            if isinstance(v, list):  # For items like "Top 10 Frequent Words"
                v = ', '.join([f"{word}: {count}" for word, count in v])
            self.results_area.insert("", tk.END, values=(k, v))

if __name__ == "__main__":
    if ThemedTk:
        root = ThemedTk(theme="equilux")  # Use ThemedTk if available
    else:
        root = tk.Tk()  # Fallback to standard Tk window if ttkthemes is not installed
    app = TextAnalysisApp(root)  # Instantiate the app class with the root window
    root.mainloop()

