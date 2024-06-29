import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the categories
categories = ["Grocery Haul", "Fast Food/Restaurant", "Gas", "Rent", "Electricity Bill", "Water Bill", "Shopping", "Other"]

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
    
    # Check if there is already an entry for the same category and date
    if not df[(df['Date'] == date) & (df['Category'] == category)].empty:
        df.loc[(df['Date'] == date) & (df['Category'] == category), 'Amount'] += amount
    else:
        # Append the new data
        new_data = pd.DataFrame({"Date": [date], "Category": [category], "Amount": [amount]})
        df = pd.concat([df, new_data], ignore_index=True)
    
    # Write back to the Excel file
    df.to_excel(file_path, index=False)
    
    messagebox.showinfo("Success", "Expense added successfully!")
    amount_var.set("")
    update_pie_chart()

# Function to update the pie chart for the selected day
def update_pie_chart():
    selected_date = date_entry.get_date().strftime("%m-%d-%Y")
    df = pd.read_excel(file_path)
    df_day = df[df['Date'] == selected_date]
    if df_day.empty:
        messagebox.showinfo("No Data", "No expenses recorded for the selected date.")
        return
    
    df_grouped = df_day.groupby('Category')['Amount'].sum()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    df_grouped.plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title(f'Expenses for {selected_date}')
    ax.set_ylabel('')  # Hide y-label for pie chart
    
    # Clear the previous chart
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()
    
    # Add the new chart
    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to show weekly expenses
def show_weekly_expenses():
    selected_date = week_entry.get_date()
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    df = pd.read_excel(file_path)
    df_week = df[(pd.to_datetime(df['Date']) >= start_of_week) & (pd.to_datetime(df['Date']) <= end_of_week)]
    if df_week.empty:
        messagebox.showinfo("No Data", "No expenses recorded for the selected week.")
        return

    df_grouped = df_week.groupby('Category')['Amount'].sum()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    df_grouped.plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title(f'Weekly Expenses ({start_of_week.strftime("%m-%d-%Y")} to {end_of_week.strftime("%m-%d-%Y")})')
    ax.set_ylabel('')  # Hide y-label for pie chart
    
    # Clear the previous chart
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()
    
    # Add the new chart
    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to show monthly expenses
def show_monthly_expenses():
    selected_date = month_entry.get_date()
    selected_month = selected_date.strftime("%m-%Y")
    df = pd.read_excel(file_path)
    df['Month'] = pd.to_datetime(df['Date']).dt.strftime("%m-%Y")
    df_month = df[df['Month'] == selected_month]
    if df_month.empty:
        messagebox.showinfo("No Data", "No expenses recorded for the selected month.")
        return

    df_grouped = df_month.groupby('Category')['Amount'].sum()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    df_grouped.plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title(f'Monthly Expenses ({selected_month})')
    ax.set_ylabel('')  # Hide y-label for pie chart
    
    # Clear the previous chart
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()
    
    # Add the new chart
    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x600")
root.resizable(False, False)

# Create and set the variables
category_var = tk.StringVar(value=categories[0])
amount_var = tk.StringVar()

# Create and place the widgets with better formatting
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="Category:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
category_menu = ttk.Combobox(main_frame, textvariable=category_var, values=categories, font=("Helvetica", 12), width=25)
category_menu.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)

ttk.Label(main_frame, text="Amount:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
amount_entry = ttk.Entry(main_frame, textvariable=amount_var, font=("Helvetica", 12), width=25)
amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)

add_button = ttk.Button(main_frame, text="Add Expense", command=add_expense)
add_button.grid(row=2, columnspan=2, pady=10)

# Date picker and pie chart button
ttk.Label(main_frame, text="Select Date:", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
date_entry = DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Helvetica", 12))
date_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.EW)

pie_chart_button = ttk.Button(main_frame, text="Show Pie Chart", command=update_pie_chart)
pie_chart_button.grid(row=4, columnspan=2, pady=10)

# Weekly expenses button and date picker
ttk.Label(main_frame, text="Select Week:", font=("Helvetica", 12)).grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
week_entry = DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Helvetica", 12))
week_entry.grid(row=5, column=1, padx=10, pady=10, sticky=tk.EW)

weekly_expenses_button = ttk.Button(main_frame, text="Show Weekly Expenses", command=show_weekly_expenses)
weekly_expenses_button.grid(row=6, columnspan=2, pady=10)

# Monthly expenses button and date picker
ttk.Label(main_frame, text="Select Month:", font=("Helvetica", 12)).grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
month_entry = DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Helvetica", 12))
month_entry.grid(row=7, column=1, padx=10, pady=10, sticky=tk.EW)

monthly_expenses_button = ttk.Button(main_frame, text="Show Monthly Expenses", command=show_monthly_expenses)
monthly_expenses_button.grid(row=8, columnspan=2, pady=10)

# Pie chart frame
pie_chart_frame = ttk.Frame(root, padding="10")
pie_chart_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Set column configurations to make the layout responsive
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# Run the main event loop
root.mainloop()
