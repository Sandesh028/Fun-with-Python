import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import os

class BillApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Billing Software")
        self.master.geometry('1280x720')
        self.master.config(bg='lightblue')
        self.master.resizable(True, True)

        # Variables
        self.items = {'Milk': 3.5, 'Bread': 2.5, 'Eggs': 5.0, 'Cereal': 4.0, 'Apples': 3.0, 'Chicken': 9.0}
        self.payment_methods = ['Cash', 'Card', 'Apple Pay']
        self.item_vars = {item: tk.IntVar() for item in self.items}
        self.payment_method = tk.StringVar(value=self.payment_methods[0])
        self.total_price = tk.DoubleVar(value=0.0)
        self.total_tax = tk.DoubleVar(value=0.0)

        self.c_name = tk.StringVar()
        self.c_phone = tk.StringVar()
        self.bill_no = tk.StringVar(value=str(random.randint(1000, 9999)))

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = tk.Label(self.master, text="Billing Software", font=("Arial", 24, "bold"), bg="lightblue", fg="black")
        title.pack(side=tk.TOP, fill=tk.X)

        # Customer Frame
        customer_frame = tk.LabelFrame(self.master, text="Customer Details", font=("Arial", 12, "bold"), bg='lightblue')
        customer_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        tk.Label(customer_frame, text="Name", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(customer_frame, textvariable=self.c_name, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(customer_frame, text="Phone No.", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=2, padx=10, pady=5)
        tk.Entry(customer_frame, textvariable=self.c_phone, font=("Arial", 12), width=20).grid(row=0, column=3, padx=10, pady=5)

        tk.Label(customer_frame, text="Bill No.", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=4, padx=10, pady=5)
        bill_entry = tk.Entry(customer_frame, textvariable=self.bill_no, font=("Arial", 12), width=20)
        bill_entry.grid(row=0, column=5, padx=10, pady=5)
        bill_entry.config(state='readonly')

        # Product Frame
        product_frame = tk.LabelFrame(self.master, text="Products", font=("Arial", 12, "bold"), bg='lightblue')
        product_frame.pack(fill=tk.X, padx=20, pady=10)

        col = 0
        for item, var in self.item_vars.items():
            tk.Label(product_frame, text=item, font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=col, padx=10, pady=5)
            tk.Entry(product_frame, textvariable=var, font=("Arial", 12), width=10).grid(row=1, column=col, padx=10, pady=5)
            col += 1

        # Payment Method
        payment_frame = tk.LabelFrame(self.master, text="Payment Method", font=("Arial", 12, "bold"), bg='lightblue')
        payment_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(payment_frame, text="Payment Method:", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=0, padx=10, pady=5)
        payment_dropdown = ttk.Combobox(payment_frame, textvariable=self.payment_method, values=self.payment_methods, state="readonly", font=("Arial", 12), width=18)
        payment_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Button Frame
        button_frame = tk.Frame(self.master, bg='lightblue')
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(button_frame, text="Total", command=self.calculate_total, font=("Arial", 12, "bold"), width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Generate Bill", command=self.generate_bill, font=("Arial", 12, "bold"), width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_all, font=("Arial", 12, "bold"), width=10).pack(side=tk.LEFT, padx=10)

        # Bill Area
        bill_area_frame = tk.Frame(self.master)
        bill_area_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.bill_text = scrolledtext.ScrolledText(bill_area_frame, font=("Arial", 12), width=100, height=20)
        self.bill_text.pack(fill=tk.BOTH, expand=True)

    def calculate_total(self):
        total = sum(qty.get() * price for item, qty in self.item_vars.items() if (price := self.items[item]))
        tax = total * 0.07  # 7% Tax
        self.total_price.set(total)
        self.total_tax.set(tax)

    def generate_bill(self):
        if not self.c_name.get() or not self.c_phone.get():
            messagebox.showerror("Error", "Customer details are required!")
            return
        self.calculate_total()
        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(tk.END, f"Bill No.: {self.bill_no.get()}\n")
        self.bill_text.insert(tk.END, f"Customer Name: {self.c_name.get()}\n")
        self.bill_text.insert(tk.END, f"Phone No.: {self.c_phone.get()}\n")
        self.bill_text.insert(tk.END, "-"*40 + "\n")
        self.bill_text.insert(tk.END, f"{'Item':20}{'Qty':10}{'Price':10}\n")
        self.bill_text.insert(tk.END, "-"*40 + "\n")
        for item, var in self.item_vars.items():
            if var.get() > 0:
                self.bill_text.insert(tk.END, f"{item:20}{var.get():10}{self.items[item] * var.get():10.2f}\n")
        self.bill_text.insert(tk.END, "-"*40 + "\n")
        self.bill_text.insert(tk.END, f"{'Total Price:':30}{self.total_price.get():10.2f}\n")
        self.bill_text.insert(tk.END, f"{'Total Tax:':30}{self.total_tax.get():10.2f}\n")
        self.bill_text.insert(tk.END, f"{'Total Payable:':30}{self.total_price.get() + self.total_tax.get():10.2f}\n")
        self.bill_text.insert(tk.END, "-"*40 + "\n")
        self.bill_text.insert(tk.END, f"Payment Method: {self.payment_method.get()}\n")
        messagebox.showinfo("Bill Generated", "The bill has been generated successfully.")

    def clear_all(self):
        self.c_name.set('')
        self.c_phone.set('')
        for var in self.item_vars.values():
            var.set(0)
        self.payment_method.set(self.payment_methods[0])
        self.bill_no.set(str(random.randint(1000, 9999)))
        self.bill_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillApp(root)
    root.mainloop()
