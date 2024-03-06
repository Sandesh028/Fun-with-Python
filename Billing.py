import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os

class BillApp:
    current_bill_no = 1  # Class attribute for dynamic bill numbering

    def __init__(self, master):
        self.master = master
        self.master.title("Billing Software")
        self.master.geometry('1280x720')
        self.master.config(bg='lightblue')
        self.master.resizable(True, True)

        # Product List (Consider adding more products as per requirement)
        self.products = {'Milk': 3.5, 'Bread': 2.5, 'Eggs': 5.0, 'Cereal': 4.0, 'Apples': 3.0, 'Chicken': 9.0}
        self.selected_product = tk.StringVar()
        self.selected_quantity = tk.IntVar()

        # UI Setup
        self.setup_ui()

        # Initialize bill number with the current class attribute value
        self.update_bill_number()

    def setup_ui(self):
        # Title
        title = tk.Label(self.master, text="Billing Software", font=("Arial", 24, "bold"), bg="lightblue", fg="black")
        title.pack(side=tk.TOP, fill=tk.X)

        # Customer and Product Frame
        customer_product_frame = tk.Frame(self.master, bg='lightblue')
        customer_product_frame.pack(fill=tk.X, padx=20, pady=10)

        # Customer Details
        self.setup_customer_ui(customer_product_frame)
        
        # Product Selection
        self.setup_product_ui(customer_product_frame)

        # Bill Area
        self.setup_bill_area()

        # Button Frame
        self.setup_buttons()

    def setup_customer_ui(self, frame):
        customer_frame = tk.LabelFrame(frame, text="Customer Details", font=("Arial", 12, "bold"), bg='lightblue')
        customer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(customer_frame, text="Name", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(customer_frame, textvariable=self.selected_product, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(customer_frame, text="Phone No.", font=("Arial", 12, "bold"), bg='lightblue').grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(customer_frame, textvariable=self.selected_quantity, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=5)

    def setup_product_ui(self, frame):
        product_frame = tk.LabelFrame(frame, text="Products", font=("Arial", 12, "bold"), bg='lightblue')
        product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(product_frame, text="Select Product", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=0, padx=10, pady=5)
        product_menu = ttk.Combobox(product_frame, textvariable=self.selected_product, values=list(self.products.keys()), state="readonly", font=("Arial", 12), width=18)
        product_menu.grid(row=0, column=1, padx=10, pady=5)
        product_menu.bind('<<ComboboxSelected>>', self.add_product_to_bill)

        tk.Label(product_frame, text="Quantity", font=("Arial", 12, "bold"), bg='lightblue').grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(product_frame, textvariable=self.selected_quantity, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=5)

    def setup_bill_area(self):
        bill_area_frame = tk.Frame(self.master)
        bill_area_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.bill_text = scrolledtext.ScrolledText(bill_area_frame, font=("Arial", 12), width=100, height=20)
        self.bill_text.pack(fill=tk.BOTH, expand=True)

    def setup_buttons(self):
        button_frame = tk.Frame(self.master, bg='lightblue')
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(button_frame, text="Clear", command=self.clear_all, font=("Arial", 12, "bold"), width=10).pack(side=tk.RIGHT, padx=10)
        tk.Button(button_frame, text="Save Bill", command=self.save_bill, font=("Arial", 12, "bold"), width=10).pack(side=tk.RIGHT, padx=10)

    def add_product_to_bill(self, event=None):
        product = self.selected_product.get()
        quantity = self.selected_quantity.get()
        price = self.products.get(product, 0)
        total_price = quantity * price
        self.bill_text.insert(tk.END, f"{product:20} {quantity:5} {price:10.2f} {total_price:10.2f}\n")

    def clear_all(self):
        self.selected_product.set('')
        self.selected_quantity.set(0)
        self.bill_text.delete(1.0, tk.END)
        BillApp.current_bill_no += 1
        self.update_bill_number()

    def update_bill_number(self):
        self.bill_no = f"Bill{BillApp.current_bill_no}.txt"
        self.bill_text.insert(tk.END, f"Bill No: {self.bill_no}\n\n")

    def save_bill(self):
        bill_content = self.bill_text.get(1.0, tk.END)
        with open(self.bill_no, 'w') as file:
            file.write(bill_content)
        messagebox.showinfo("Saved", f"Bill {self.bill_no} has been saved.")
        self.clear_all()

if __name__ == "__main__":
    root = tk.Tk()
    app = BillApp(root)
    root.mainloop()
