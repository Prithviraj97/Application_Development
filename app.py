import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os

# Define the categories
categories = ["Grocery Haul", "Fast Food/Restaurant", "Gas", "Monthly Rent", "Electricity Bill", "Water Bill"]

# Define the file path for storing data
file_path = "expenses.xlsx"

# Create the Excel file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_excel(file_path, index=False)

# Function to add a new expense
def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    if not amount.replace('.', '', 1).isdigit():  # To allow for decimal amounts
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return
    amount = float(amount)
    date = datetime.now().strftime("%m-%d-%Y")
    
    # Read the existing data
    df = pd.read_excel(file_path)
    
    # Append the new data
    new_data = pd.DataFrame({"Date": [date], "Category": [category], "Amount": [amount]})
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Write back to the Excel file
    df.to_excel(file_path, index=False)
    
    messagebox.showinfo("Success", "Expense added successfully!")
    amount_var.set("")

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x250")
root.resizable(False, False) 

# Create and set the variables
category_var = tk.StringVar(value=categories[0])
amount_var = tk.StringVar()

# Create and place the widgets with better formatting
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="Category:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
category_menu = ttk.Combobox(main_frame, textvariable=category_var, values=categories, font=("Helvetica", 12))
category_menu.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)

ttk.Label(main_frame, text="Amount:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
amount_entry = ttk.Entry(main_frame, textvariable=amount_var, font=("Helvetica", 12))
amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)

add_button = ttk.Button(main_frame, text="Add Expense", command=add_expense)
add_button.grid(row=2, columnspan=2, pady=20)

# Set column configurations to make the layout responsive
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# Run the main event loop
root.mainloop()
