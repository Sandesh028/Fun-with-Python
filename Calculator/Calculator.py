import tkinter as tk
from tkinter import ttk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Calculator")
        self.root.geometry("320x500")  
        self.root.configure(background='#2C3E50')  

        # Configure styles
        style = ttk.Style()
        style.theme_use('default')

        # Entry style
        self.entry = tk.Entry(root, font=('Arial', 24), bg='#7F8C8D', fg='#ECF0F1', borderwidth=2, relief="flat")
        self.entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

        # Button style configuration
        self.configure_button_style()

        # Buttons configuration
        self.create_buttons()

        # History label and text widget for history
        self.create_history_widgets()
        self.setup_key_bindings()

        # Grid configuration for resizing
        self.configure_grid()

    def configure_button_style(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 18), borderwidth=1, foreground='#ECF0F1', background='#34495E', relief='flat')
        style.map('TButton',
                  foreground=[('active', '#ECF0F1')],
                  background=[('active', '#2980B9'), ('pressed', '#2980B9')])

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('0', 4, 1),
            ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3),
            ('C', 4, 0), ('=', 4, 2),
        ]
        for (text, row, col) in buttons:
            button = ttk.Button(self.root, text=text, command=lambda text=text: self.on_button_click(text), style='TButton')
            button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

    def create_history_widgets(self):
        self.history_label = ttk.Label(self.root, text="History ▼", font=('Arial', 12), background='#2C3E50', foreground='#ECF0F1', anchor='w')
        self.history_label.grid(row=5, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        self.history_label.bind("<Button-1>", self.toggle_history)

        self.history_text = tk.Text(self.root, height=4, bg="#34495E", fg="#ECF0F1", state='disabled', borderwidth=2, relief="flat")
        self.history_visible = False
        
    def setup_key_bindings(self):
        
        for key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            self.root.bind(key, self.handle_key_press)
        for key in ('+', '-', '*', '/'):
            self.root.bind(key, self.handle_key_press)
        self.root.bind('<Return>', self.handle_key_press)
        self.root.bind('<BackSpace>', self.handle_key_press)
        self.root.bind('C', self.handle_key_press)
        self.root.bind('c', self.handle_key_press)
        self.root.bind('=', self.handle_key_press)

    def handle_key_press(self, event):
        char = event.char 
        keysym = event.keysym  
        
        if keysym == 'Return':
            self.on_button_click('=')
        elif keysym == 'BackSpace':
            self.entry.delete(len(self.entry.get())-1)
        elif keysym in ('C', 'c'):
            self.on_button_click('C')
        else:
            
            if char in '0123456789+-*/':
                self.entry.insert(tk.END, char)
            
            elif keysym == 'equal':
                self.on_button_click('=')
                
    def toggle_history(self, event):
        if self.history_visible:
            self.history_text.grid_remove()
            self.history_label.config(text="History ▼")
        else:
            self.history_text.grid(row=6, column=0, columnspan=4, sticky='nsew', padx=10, pady=0)
            self.history_label.config(text="History ▲")
        self.history_visible = not self.history_visible

    def configure_grid(self):
        for i in range(6):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
    def on_button_click(self, char):
        if char == 'C':
            self.entry.delete(0, tk.END)
        elif char == '=':
            original_expression = self.entry.get()
            try:
                result = eval(original_expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.update_history(f"{original_expression} = {result}")
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        else:
            self.entry.insert(tk.END, char)

    def update_history(self, calculation):
        self.history_text.configure(state='normal')
        self.history_text.insert(tk.END, calculation + "\n")
        self.history_text.configure(state='disabled')

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
