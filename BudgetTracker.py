import tkinter as tk
from tkinter import messagebox
import csv
import os
import datetime

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

class BudgetTracker:
    def __init__(self, window, back_callback):
        self.window = window
        self.back_callback = back_callback

    def back_to_menu(self):
        self.budget_page.pack_forget()

    def open_budget_page(self):
        self.budget_page.pack()
        self.load_expenses() 
        self.switch_budget_view("input")

    ## change to .pack_forget()
    def menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.App()

    def App(self):
        self.budget_page = tk.Frame(self.window)

        # Budget page
        tk.Label(self.budget_page, text="Welcome to Budget Tracker").pack(pady=10)
        budget_switch_btn = tk.Button(self.budget_page, text="View Report", command=lambda: self.switch_budget_view("report"),bg='#ADD8E6', width=15)
        budget_switch_btn.pack(pady=5)

        # --- 2. Input View Frame ---
        self.input_view = tk.Frame(self.budget_page) 

        # Category Selection
        self.frame_category = tk.Frame(self.input_view)
        self.frame_category.pack(pady=5)

        tk.Label(self.frame_category, text="Select Category:").pack(side=tk.TOP, pady=(0, 5))

        self.frame_buttons = tk.Frame(self.frame_category)
        self.frame_buttons.pack()

        for i, cat in enumerate(CATEGORIES):
            btn = tk.Button(
                self.frame_buttons, text=cat, command=lambda c=cat: self.select_category(c), width=10, height=2, padx=10
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            category_buttons[cat] = btn

        # Selected Category Indicator
        self.category_label_indicator = tk.Label(self.input_view, text="Selected Category: None", fg='blue')
        self.category_label_indicator.pack(pady=5)

        # Amount Input and Add/Clear Button Area
        self.frame_input = tk.Frame(self.input_view)
        self.frame_input.pack(pady=10)

        tk.Label(self.frame_input, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount = tk.Entry(self.frame_input) # Assign to global variable
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        self.btn_add = tk.Button(self.frame_input, text="Add Expense", command=self.add_expense, bg='lightgreen')
        self.btn_add.grid(row=1, column=0, columnspan=2, pady=10)

        self.btn_clear = tk.Button(self.frame_input, text="Clear ALL", command=self.clear_expenses, bg='pink', fg='red')
        self.btn_clear.grid(row=2, column=0, columnspan=2, pady=5)

        # Transaction List and Total
        tk.Label(self.input_view, text="Transactions:").pack(pady=(10, 0))
        self.listbox_expenses = tk.Listbox(self.input_view, width=50, height=8) 
        self.listbox_expenses.pack(pady=5)

        self.total_label = tk.Label(self.input_view, text="Total Expenses: RM 0.00", font=("Arial", 10, "bold")) 
        self.total_label.pack(pady=5)


        # --- 3. Report View Frame ---
        self.report_view = tk.Frame(self.budget_page) 
        tk.Label(self.report_view, text="Spending Insights Report", font=("Arial", 14, "bold")).pack(pady=10)
        self.report_content = tk.Label(self.report_view, text="Click 'Go to Reports' to view data.", 
                                justify=tk.LEFT, font=("Courier", 10), 
                                anchor="nw", padx=10, bg="#F0F0F0")
        self.report_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self.budget_page, text="Back to Main Menu", command=self.back_to_menu).pack(side="bottom", pady=10)

        self.switch_budget_view("input")

    # --- Data Persistence Functions ---

    def save_expense(self, category, amount, selected_date):
        """Saves a new expense record to the CSV file."""
        
        file_exists = os.path.isfile(DATA_FILE)
        with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Category", "Amount", "Date"])
            writer.writerow([category, amount, selected_date ])

    def load_expenses(self):
        """Loads expense data from CSV file and updates the Listbox."""
        if self.listbox_expenses is None: return

        if os.path.exists(DATA_FILE):
            self.listbox_expenses.delete(0, tk.END)

            with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) < 3: continue
                    category, amount_str, date = row
                    
                    try:
                        amount_float = float(amount_str)

                        self.listbox_expenses.insert(tk.END, f"{date} | {category}: RM {amount_float:.2f}")
                    except ValueError:
                        pass

        self.update_total()

    def update_total(self):
        """Calculates and updates the total spending currently displayed in the Listbox."""
        if self.total_label is None: return
        
        total = 0.0
        for i in range(self.listbox_expenses.size()):
            item = self.listbox_expenses.get(i)
            try:
                amount_str = item.split('RM')[1]
                total += float(amount_str)
            except (IndexError, ValueError):
                pass 
        
        self.total_label.config(text=f"Total Expenses: RM {total:.2f}")

    def select_category(self, category):
        """Sets the current selected category and updates the indicator."""
        global current_category
        current_category = category
        for btn in category_buttons.values():
            if btn.cget("text") == category:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')
        
        self.self.category_label_indicator.config(text=f"Selected Category: {current_category}")

    def add_expense(self):
        """Adds the expense to the list, saves it to the file, and updates total."""
        global current_category
        if self.entry_amount is None: return

        amount = self.entry_amount.get()

        if not current_category:
            tk.messagebox.showerror("Error", "Please select a category first.")
            return

        if amount:
            try:
                amount_float = float(amount)
                
                selected_date = datetime.datetime.now().strftime('%Y-%m-%d')
                
                self.listbox_expenses.insert(tk.END, f"{selected_date} | {current_category}: RM {amount_float:.2f}")
                self.save_expense(current_category, amount_float, selected_date)
                
                # 3. Clear
                self.entry_amount.delete(0, tk.END)
                
                # 4. Update total
                self.update_total()
                
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid number for amount")
        else:
            tk.messagebox.showerror("Error", "Please enter an amount.")      

    def clear_expenses(self):
        """Clears all displayed expenses and deletes the data file."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear ALL expenses? This cannot be undone."):
            
            # 1. Clear the Listbox content
            self.listbox_expenses.delete(0, tk.END)
            
            # 2. Delete the data file
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                
            # 3. Reset the total count
            self.update_total()
            
            tk.messagebox.showinfo("Success", "All expenses have been cleared.")
            
    def calculate_summary(self):
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

    def generate_report_text(self):
        """Calculates summary and returns the formatted report string."""
        summary, grand_total = self.calculate_summary()
        
        if grand_total == 0:
            return "No expenses recorded yet."

        report_text = ["   --- SPENDING SUMMARY ---\n"]
        for category, total in summary.items():
            percentage = (total / grand_total) * 100
            report_text.append(f"{category:<12} : RM {total:6.2f} ({percentage:4.1f}%)")
        
        report_text.append("\n" + f"{'TOTAL':<12} : RM {grand_total:6.2f}")
        
        return "\n".join(report_text)

    def switch_budget_view(self, view_name):
        """Switches between the input view and the report view and updates the switch button."""
        global current_budget_view
        global budget_switch_btn
        
        if current_budget_view is not None:
            current_budget_view.pack_forget()

        if view_name == "input":
            current_budget_view = self.input_view
            self.input_view.pack(fill=tk.BOTH, expand=True)
            self.load_expenses() 
            
            if budget_switch_btn:
                budget_switch_btn.config(
                    text="View Report", 
                    command=lambda: self.switch_budget_view("report")
                )
            
        elif view_name == "report":
            current_budget_view = self.self.report_view
            self.self.report_view.pack(fill=tk.BOTH, expand=True)
            self.self.report_content.config(text=self.generate_report_text()) 
            
            if budget_switch_btn:
                budget_switch_btn.config(
                    text="Back to Input", 
                    command=lambda: self.switch_budget_view("input")
                )

    def display_spending_report(self):
        """Formats and displays the report."""
        global report_label
        if report_label is None: return
        
        summary, grand_total = self.calculate_summary()
        
        if grand_total == 0:
            report_label.config(text="No expenses recorded yet.")
            return

        report_text = ["--- SPENDING SUMMARY ---\n"]
        for category, total in summary.items():
            percentage = (total / grand_total) * 100
            report_text.append(f"{category:<12} : RM {total:6.2f} ({percentage:4.1f}%)")
        
        report_text.append("\n" + f"{'TOTAL':<12} : RM {grand_total:6.2f}")
        report_label.config(text="\n".join(report_text), justify=tk.LEFT, font=("Courier", 10))

        self.window.mainloop()