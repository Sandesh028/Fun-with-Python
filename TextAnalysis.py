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

from textgui import analyze_text

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
        self.style.map('Treeview', background=[('selected', '#E9E9E9')])
        
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
        self.results_area.column("Value", anchor=tk.W, width=500)  # Adjusted for better width management
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
        # Check if the analysis has been done and the results contain the top words information
        if "Top 10 Frequent Words (excluding common stopwords)" in self.analysis_results:
            top_words = self.analysis_results["Top 10 Frequent Words (excluding common stopwords)"]
            detailed_text = "\n".join([f"{word}: {count}" for word, count in top_words])

            # Create a pop-up window
            popup = tk.Toplevel(self)
            popup.title("Detailed Word Frequencies")

            # Create a read-only Text widget to display the top words
            text_widget = tk.Text(popup, wrap=tk.WORD, height=10, width=50)
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, detailed_text)
            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

            # Add a close button to the pop-up
            close_btn = ttk.Button(popup, text="Close", command=popup.destroy)
            close_btn.pack(pady=(0, 10))
        else:
            messagebox.showinfo("Information", "Please perform analysis to see detailed word frequencies.")
