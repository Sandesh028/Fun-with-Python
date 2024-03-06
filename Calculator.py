import tkinter as tk
from tkinter import ttk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Calculator")
        self.root.geometry("320x500")  # Window size
        self.root.configure(background='#2C3E50')  # Deep blue background for the app

        # Configure styles
        style = ttk.Style()
        style.theme_use('default')

        # Entry style (using standard tk.Entry for background color control)
        self.entry = tk.Entry(root, font=('Arial', 24), bg='#7F8C8D', fg='#ECF0F1', borderwidth=2, relief="flat")
        self.entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

        # Button style
        style.configure('TButton', font=('Arial', 18), borderwidth=1, foreground='#ECF0F1', background='#34495E', relief='flat')
        style.map('TButton',
                  foreground=[('active', '#ECF0F1')],
                  background=[('active', '#2980B9'), ('pressed', '#2980B9')])  # Dark blue/Persian blue for button background
        
        # Buttons configuration
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('0', 4, 1),
            ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3),
            ('C', 4, 0), ('=', 4, 2),
        ]

        # Create buttons using the configured style
        for (text, row, col) in buttons:
            button = ttk.Button(root, text=text, command=lambda text=text: self.on_button_click(text), style='TButton')
            button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        # Grid configuration for resizing
        for i in range(5):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)

        # History label
        self.history_label = ttk.Label(root, text="History", font=('Arial', 12), background='#2C3E50', foreground='#ECF0F1', anchor='w')
        self.history_label.grid(row=5, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

    def on_button_click(self, char):
        if char == 'C':
            self.entry.delete(0, tk.END)
        elif char == '=':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.update_history(f"{self.entry.get()} = {result}")
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        else:
            self.entry.insert(tk.END, char)

    def update_history(self, calculation):
        # This function will need implementation based on how you want to display history.
        pass

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
