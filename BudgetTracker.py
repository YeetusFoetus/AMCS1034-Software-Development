import tkinter as tk
from tkinter import messagebox
import csv
import os
import datetime

def open_grocery_page():
    grocery_page.pack()
    main_menu.pack_forget()

def open_chore_page():
    chore_page.pack()
    main_menu.pack_forget()

def open_budget_page():
    budget_page.pack()
    main_menu.pack_forget()
    load_expenses() 
    switch_budget_view("input")

def open_meal_page():
    meal_page.pack()
    main_menu.pack_forget()
    
def back_to_menu():
    grocery_page.pack_forget()
    chore_page.pack_forget()
    budget_page.pack_forget()
    meal_page.pack_forget()

    main_menu.pack()
    
window = tk.Tk()
window.title("Household Management Assistant App")
window.geometry("500x500")

main_menu = tk.Frame(window)
grocery_page = tk.Frame(window)
chore_page = tk.Frame(window)
budget_page = tk.Frame(window)
meal_page = tk.Frame(window)

# --- Main Menu UI ---
btn_grocery = tk.Button(main_menu, text="Grocery List Manager", font=("Helvetica", 8, "bold"), command=open_grocery_page,width=20, height=2, padx=10)
btn_grocery.pack(pady=(40,8))

btn_chore = tk.Button(main_menu, text="Chore Scheduler", font=("Helvetica", 8, "bold"), command=open_chore_page,width=20, height=2, padx=10)
btn_chore.pack(pady=8)

btn_budget = tk.Button(main_menu, text="Budget Tracker", font=("Helvetica", 8, "bold"), command=open_budget_page,width=20, height=2, padx=10)
btn_budget.pack(pady=8)

btn_meal = tk.Button(main_menu, text="Meal Planner", font=("Helvetica", 8, "bold"), command=open_meal_page,width=20, height=2, padx=10)
btn_meal.pack(pady=8)

main_menu.pack() # show main menu

# --- Global Variables and Data File Setup ---
DATA_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Housing", "Bills", "Entertainment", "Other"]
current_category = ""
category_buttons = {}
listbox_expenses = None
total_label = None
entry_amount = None
current_budget_view = None
budget_switch_btn = None

# --- Data Persistence Functions ---

def save_expense(category, amount, selected_date):
    """Saves a new expense record to the CSV file."""
    
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Category", "Amount", "Date"])
        writer.writerow([category, amount, selected_date ])

def load_expenses():
    """Loads expense data from CSV file and updates the Listbox."""
    if listbox_expenses is None: return

    if os.path.exists(DATA_FILE):
        listbox_expenses.delete(0, tk.END)

        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) < 3: continue
                category, amount_str, date = row
                
                try:
                    amount_float = float(amount_str)

                    listbox_expenses.insert(tk.END, f"{date} | {category}: RM {amount_float:.2f}")
                except ValueError:
                    pass

    update_total()

def update_total():
    """Calculates and updates the total spending currently displayed in the Listbox."""
    if total_label is None: return
    
    total = 0.0
    for i in range(listbox_expenses.size()):
        item = listbox_expenses.get(i)
        try:
            amount_str = item.split('RM')[1]
            total += float(amount_str)
        except (IndexError, ValueError):
            pass 
    
    total_label.config(text=f"Total Expenses: RM {total:.2f}")

def select_category(category):
    """Sets the current selected category and updates the indicator."""
    global current_category
    current_category = category
    for btn in category_buttons.values():
        if btn.cget("text") == category:
            btn.config(relief=tk.SUNKEN, bg='lightblue')
        else:
            btn.config(relief=tk.RAISED, bg='SystemButtonFace')
    
    category_label_indicator.config(text=f"Selected Category: {current_category}")

def add_expense():
    """Adds the expense to the list, saves it to the file, and updates total."""
    global current_category
    if entry_amount is None: return

    amount = entry_amount.get()

    if not current_category:
        tk.messagebox.showerror("Error", "Please select a category first.")
        return

    if amount:
        try:
            amount_float = float(amount)
            
            selected_date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            listbox_expenses.insert(tk.END, f"{selected_date} | {current_category}: RM {amount_float:.2f}")
            save_expense(current_category, amount_float, selected_date)
            
            # 3. Clear
            entry_amount.delete(0, tk.END)
            
            # 4. Update total
            update_total()
            
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number for amount")
    else:
        tk.messagebox.showerror("Error", "Please enter an amount.")      

def clear_expenses():
    """Clears all displayed expenses and deletes the data file."""
    if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear ALL expenses? This cannot be undone."):
        
        # 1. Clear the Listbox content
        listbox_expenses.delete(0, tk.END)
        
        # 2. Delete the data file
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            
        # 3. Reset the total count
        update_total()
        
        tk.messagebox.showinfo("Success", "All expenses have been cleared.")
        
def calculate_summary():
    """Calculates total spending and category summary using standard library."""
    spending_summary = {}
    grand_total = 0.0
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) < 3: continue 
                category, amount_str, date = row
                try:
                    amount = float(amount_str)
                    grand_total += amount
                    if category in spending_summary:
                        spending_summary[category] += amount
                    else:
                        spending_summary[category] = amount
                except ValueError:
                    continue 
    return spending_summary, grand_total

def generate_report_text():
    """Calculates summary and returns the formatted report string."""
    summary, grand_total = calculate_summary()
    
    if grand_total == 0:
        return "No expenses recorded yet."

    report_text = ["   --- SPENDING SUMMARY ---\n"]
    for category, total in summary.items():
        percentage = (total / grand_total) * 100
        report_text.append(f"{category:<12} : RM {total:6.2f} ({percentage:4.1f}%)")
    
    report_text.append("\n" + f"{'TOTAL':<12} : RM {grand_total:6.2f}")
    
    return "\n".join(report_text)

def switch_budget_view(view_name):
    """Switches between the input view and the report view and updates the switch button."""
    global current_budget_view
    global budget_switch_btn
    
    if current_budget_view is not None:
        current_budget_view.pack_forget()

    if view_name == "input":
        current_budget_view = input_view
        input_view.pack(fill=tk.BOTH, expand=True)
        load_expenses() 
        
        if budget_switch_btn:
            budget_switch_btn.config(
                text="View Report", 
                command=lambda: switch_budget_view("report")
            )
        
    elif view_name == "report":
        current_budget_view = report_view
        report_view.pack(fill=tk.BOTH, expand=True)
        report_content.config(text=generate_report_text()) 
        
        if budget_switch_btn:
            budget_switch_btn.config(
                text="Back to Input", 
                command=lambda: switch_budget_view("input")
            )

def display_spending_report():
    """Formats and displays the report."""
    global report_label
    if report_label is None: return
    
    summary, grand_total = calculate_summary()
    
    if grand_total == 0:
        report_label.config(text="No expenses recorded yet.")
        return

    report_text = ["--- SPENDING SUMMARY ---\n"]
    for category, total in summary.items():
        percentage = (total / grand_total) * 100
        report_text.append(f"{category:<12} : RM {total:6.2f} ({percentage:4.1f}%)")
    
    report_text.append("\n" + f"{'TOTAL':<12} : RM {grand_total:6.2f}")
    report_label.config(text="\n".join(report_text), justify=tk.LEFT, font=("Courier", 10))

# Grocery Page
tk.Label(grocery_page, text="Welcome to Grocery Page!").pack(pady=20)
tk.Button(grocery_page, text="Back to Main Menu", command=back_to_menu).pack(side="bottom", pady=10)

# Chore Page
tk.Label(chore_page, text="Welcome to Chore Scheduler!").pack(pady=20)
tk.Button(chore_page, text="Back to Main Menu", command=back_to_menu).pack(side="bottom", pady=10)

# Budget page
tk.Label(budget_page, text="Welcome to Budget Tracker").pack(pady=10)
budget_switch_btn = tk.Button(budget_page, text="View Report", command=lambda: switch_budget_view("report"),bg='#ADD8E6', width=15)
budget_switch_btn.pack(pady=5)

# --- 2. Input View Frame ---
input_view = tk.Frame(budget_page) 

# Category Selection
frame_category = tk.Frame(input_view)
frame_category.pack(pady=5)

tk.Label(frame_category, text="Select Category:").pack(side=tk.TOP, pady=(0, 5))

frame_buttons = tk.Frame(frame_category)
frame_buttons.pack()

for i, cat in enumerate(CATEGORIES):
    btn = tk.Button(
        frame_buttons, text=cat, command=lambda c=cat: select_category(c), width=10, height=2, padx=10
    )
    btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
    category_buttons[cat] = btn

# Selected Category Indicator
category_label_indicator = tk.Label(input_view, text="Selected Category: None", fg='blue')
category_label_indicator.pack(pady=5)

# Amount Input and Add/Clear Button Area
frame_input = tk.Frame(input_view)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_input) # Assign to global variable
entry_amount.grid(row=0, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Add Expense", command=add_expense, bg='lightgreen')
btn_add.grid(row=1, column=0, columnspan=2, pady=10)

btn_clear = tk.Button(frame_input, text="Clear ALL", command=clear_expenses, bg='pink', fg='red')
btn_clear.grid(row=2, column=0, columnspan=2, pady=5)

# Transaction List and Total
tk.Label(input_view, text="Transactions:").pack(pady=(10, 0))
listbox_expenses = tk.Listbox(input_view, width=50, height=8) 
listbox_expenses.pack(pady=5)

total_label = tk.Label(input_view, text="Total Expenses: RM 0.00", font=("Arial", 10, "bold")) 
total_label.pack(pady=5)


# --- 3. Report View Frame ---
report_view = tk.Frame(budget_page) 
tk.Label(report_view, text="Spending Insights Report", font=("Arial", 14, "bold")).pack(pady=10)
report_content = tk.Label(report_view, text="Click 'Go to Reports' to view data.", 
                         justify=tk.LEFT, font=("Courier", 10), 
                         anchor="nw", padx=10, bg="#F0F0F0")
report_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Button(budget_page, text="Back to Main Menu", command=back_to_menu).pack(side="bottom", pady=10)

switch_budget_view("input")

# Meal Planner Page
tk.Label(meal_page, text="Welcome to Meal Planner!").pack(pady=20)
tk.Button(meal_page, text="Back to Main Menu", command=back_to_menu).pack(side="bottom", pady=10)

window.mainloop()