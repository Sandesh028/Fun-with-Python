# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import collections
# import string
# import nltk
# import fitz  # PyMuPDF
# from nltk.corpus import stopwords
# import textstat
# from transformers import pipeline

# # Ensure required NLTK datasets are downloaded
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

# # Initialize sentiment analysis model with a specific model
# sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# def analyze_text(filepath):
#     text = ""
#     try:
#         if filepath.lower().endswith('.pdf'):
#             with fitz.open(filepath) as doc:
#                 text = " ".join(page.get_text() for page in doc)
#         else:  # Assuming a text file if not PDF
#             try:
#                 with open(filepath, 'r', encoding="utf-8") as f:
#                     text = f.read()
#             except UnicodeDecodeError:
#                 with open(filepath, 'r', encoding="iso-8859-1") as f:
#                     text = f.read()
        
#         # Analysis Logic
#         total_words = len(text.split())
#         unique_words = len(set(text.split()))
#         freq_dist = collections.Counter(text.split())
#         top_10_words = freq_dist.most_common(10)
        
#         # Example output dictionary
#         results = {
#             "Total Words": total_words,
#             "Unique Words": unique_words,
#             "Top 10 Words": top_10_words
#         }
#         return results
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to analyze the file: {e}")
#         return {}

# class TextAnalysisApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Text Analysis Tool")
#         self.init_ui()

#     def init_ui(self):
#         self.frame = ttk.Frame(self)
#         self.frame.pack(padx=10, pady=5, expand=True)

#         self.entry = ttk.Entry(self.frame)
#         self.entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

#         browse_btn = ttk.Button(self.frame, text="Browse", command=self.open_file)
#         browse_btn.pack(side=tk.RIGHT)

#         analyze_btn = ttk.Button(self, text="Analyze", command=self.analyze_and_display)
#         analyze_btn.pack(pady=5)

#         self.results_area = tk.Text(self, height=15)
#         self.results_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

#     def open_file(self):
#         filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Text Files", "*.txt")])
#         if filepath:
#             self.entry.delete(0, tk.END)
#             self.entry.insert(0, filepath)

#     def analyze_and_display(self):
#         filepath = self.entry.get().strip()
#         if filepath:
#             results = analyze_text(filepath)
#             self.display_results(results)
#         else:
#             messagebox.showwarning("Warning", "Please select a file first.")

#     def display_results(self, results):
#         self.results_area.delete('1.0', tk.END)
#         for key, value in results.items():
#             self.results_area.insert(tk.END, f"{key}: {value}\n")

# if __name__ == "__main__":
#     app = TextAnalysisApp()
#     app.mainloop()
