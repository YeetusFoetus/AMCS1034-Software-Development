import tkinter as tk
from tkinter import messagebox
import csv
import os
import datetime

# --- Global Variables and Data File Setup ---

class BudgetTracker:
    def __init__(self, window, back_callback):
        self.window = window
        self.back_callback = back_callback
        self.budget_switch_btn = None
        self.DATA_FILE = "expenses.csv"
        self.BUDGET_FILE = "budgets.csv" 
        
        self.CATEGORIES = ["Food", "Transport", "Housing", "Bills", "Entertainment", "Other"]
        self.current_category = ""
        self.category_buttons = {}
        self.budgets = {}
        self.listbox_expenses = None
        self.total_label = None
        self.entry_amount = None
        self.current_budget_view = None
        
        # UI Elements for switching views
        self.input_view = None
        self.report_view = None
        self.report_content = None
        self.net_balance_label = None

    def open_budget_page(self):
        tk.Label(self.window, text="Welcome to Budget Tracker").pack(pady=10)
        self.budget_page = tk.Frame(self.window)
        self.budget_page.pack()

        # Budget page
        self.budget_switch_btn = tk.Button(self.budget_page, text="View Report", command=lambda: self.switch_budget_view("report"),bg='#ADD8E6', width=15)
        self.budget_switch_btn.pack(pady=5)

        # --- 2. Input View Frame ---
        self.input_view = tk.Frame(self.budget_page) 

        # Category Selection and Expense Input (Kept at the top, spanning width)
        self.frame_category = tk.Frame(self.input_view)
        self.frame_category.pack(pady=5)

        tk.Label(self.frame_category, text="Select Category:").pack(side=tk.TOP, pady=(0, 5))

        self.frame_buttons = tk.Frame(self.frame_category)
        self.frame_buttons.pack()

        for i, cat in enumerate(self.CATEGORIES):
            btn = tk.Button(
                self.frame_buttons, text=cat, command=lambda c=cat: self.select_category(c), width=10, height=2, padx=10
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.category_buttons[cat] = btn

        # Selected Category Indicator
        self.category_label_indicator = tk.Label(self.input_view, text="Selected Category: None", fg='blue')
        self.category_label_indicator.pack(pady=5)

        # Amount Input and Add/Clear Button Area (EXPENSE)
        self.frame_input = tk.Frame(self.input_view)
        self.frame_input.pack(pady=10)

        tk.Label(self.frame_input, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount = tk.Entry(self.frame_input)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        self.btn_add = tk.Button(self.frame_input, text="Add Expense", command=self.add_expense, bg='lightgreen')
        self.btn_add.grid(row=1, column=0, columnspan=2, pady=10)

        self.btn_clear = tk.Button(self.frame_input, text="Clear ALL Expenses", command=self.clear_expenses, bg='pink', fg='red')
        self.btn_clear.grid(row=2, column=0, columnspan=2, pady=5)

        # --- NEW: Layout Frame for Side-by-Side Content (Budget Left, Transactions Right) ---
        self.frame_side_by_side = tk.Frame(self.input_view)
        self.frame_side_by_side.pack(pady=10, fill=tk.X, expand=True) 
        self.frame_side_by_side.grid_columnconfigure(0, weight=1)
        self.frame_side_by_side.grid_columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------
        # --- LEFT SIDE: Budget Setting Area (MONTHLY BUDGET) ---
        # -----------------------------------------------------------------------------------
        
        self.frame_budget_set = tk.Frame(self.frame_side_by_side, pady=10, padx=10, relief=tk.GROOVE, bd=1, bg="#FFFFFF")
        self.frame_budget_set.grid(row=0, column=0, padx=15, sticky='nsew')

        tk.Label(self.frame_budget_set, text="Set Monthly Budget Goal:", font=('Arial', 10, 'bold')).pack(pady=(0, 5))

        self.budget_entries = {}

        # Display Category and Entry for budget input
        for cat in self.CATEGORIES:
            frame_row = tk.Frame(self.frame_budget_set, bg="#FFFFFF")
            frame_row.pack(fill='x', padx=5, pady=2)

            tk.Label(frame_row, text=f"{cat}:", width=15, anchor='w').grid(row=0, column=0, sticky='w') 
            tk.Label(frame_row, text="RM").grid(row=0, column=1, sticky='w', padx=(0, 2))
            entry = tk.Entry(frame_row, width=8)
            entry.grid(row=0, column=2, padx=(0, 5))
            self.budget_entries[cat] = entry

        tk.Button(
            self.frame_budget_set, 
            text="Save Budgets", 
            command=self.set_budgets, 
            bg='#90EE90'
        ).pack(pady=10)
        
        # -----------------------------------------------------------------------------------
        # --- RIGHT SIDE: Transaction List and Total (TRANSACTIONS) ---
        # -----------------------------------------------------------------------------------
        
        self.frame_transactions = tk.Frame(self.frame_side_by_side, pady=10, padx=10, relief=tk.GROOVE, bd=1, bg="#FFFFFF")
        self.frame_transactions.grid(row=0, column=1, padx=15, sticky='nsew')
        self.frame_transactions.grid_rowconfigure(1, weight=1)
        self.frame_transactions.grid_columnconfigure(0, weight=1)
        
        tk.Label(self.frame_transactions, text="Transactions: (Expenses Only)").grid(row=0, column=0, pady=(0, 5))
        self.listbox_expenses = tk.Listbox(self.frame_transactions, width=35, height=14) 
        self.listbox_expenses.grid(row=1, column=0, pady=5, sticky='nsew')

        # MODIFIED: Use Net Balance Label
        self.net_balance_label = tk.Label(self.frame_transactions, 
                                          text="Net Balance: RM 0.00", 
                                          font=("Arial", 12, "bold"), 
                                          bg='#E0FFFF') 
        self.net_balance_label.grid(row=2, column=0, pady=10)

        # --- 3. Report View Frame ---
        self.report_view = tk.Frame(self.budget_page) 
        tk.Label(self.report_view, text="Spending Insights Report", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.report_content = tk.Label(self.report_view, text="Click 'View Report' to view data.", 
                                 justify=tk.LEFT, font=("Courier", 10), 
                                 anchor="nw", padx=10, bg="#F0F0F0")
        self.report_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self.budget_page, text="Back to Main Menu", command=self.back_callback).pack(side="bottom", pady=10)

        # --- Data Loading and Initialization (Moved to the end) ---
        self.load_budgets()
        
        for cat, amount in self.budgets.items():
            if cat in self.budget_entries:
                self.budget_entries[cat].delete(0, tk.END)
                self.budget_entries[cat].insert(0, str(amount))
                
        self.load_expenses() 
        self.update_net_balance_label() 
        self.switch_budget_view("input")
        
    def switch_budget_view(self, view_name):
        """Switches between the input and report views."""
        
        # Hide all view frames first
        self.input_view.pack_forget()
        self.report_view.pack_forget()
        
        if view_name == "input":
            self.input_view.pack(fill=tk.BOTH, expand=True)
            self.budget_switch_btn.config(text="View Report", command=lambda: self.switch_budget_view("report"))
            self.current_budget_view = self.input_view
        elif view_name == "report":
            self.report_view.pack(fill=tk.BOTH, expand=True)
            self.display_spending_report() 
            self.budget_switch_btn.config(text="Go Back", command=lambda: self.switch_budget_view("input"))
            self.current_budget_view = self.report_view
            
    def menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.open_budget_page()
        
    def set_budgets(self):
        """Reads all budget entries and saves them to the budget file."""
        valid_budgets = 0
        budgets_saved = False

        for category, entry in self.budget_entries.items():
            amount_str = entry.get().strip()
            
            if amount_str:
                try:
                    amount_float = float(amount_str)
                    if amount_float >= 0:
                        self.save_budget(category, amount_float)
                        valid_budgets += 1
                        budgets_saved = True
                    else:
                        tk.messagebox.showerror("Error", f"Budget for {category} must be non-negative.")
                        return
                except ValueError:
                    tk.messagebox.showerror("Error", f"Please enter a valid number for {category} budget.")
                    return
        
        if valid_budgets > 0:
            tk.messagebox.showinfo("Success", f"Successfully saved {valid_budgets} budget goals.")
        else:
            tk.messagebox.showinfo("Info", "No budget goals were set.")          
        if budgets_saved:
            self.update_net_balance_label() 
        if self.current_budget_view == self.report_view:
            self.switch_budget_view("report")
            
    def save_expense(self, category, amount, selected_date):
        """Saves a new expense record to the CSV file."""
        
        file_exists = os.path.isfile(self.DATA_FILE)
        with open(self.DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Category", "Amount", "Date"])
            writer.writerow([category, amount, selected_date ])
    
    def load_expenses(self):
        """Loads expense data from CSV file and updates the Listbox."""
        if self.listbox_expenses is None: return

        if os.path.exists(self.DATA_FILE):
            self.listbox_expenses.delete(0, tk.END)

            with open(self.DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
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

        self.update_net_balance_label()

    def load_budgets(self):
        """Loads budget goals from the budget CSV file."""
        self.budgets = {}
        if os.path.exists(self.BUDGET_FILE):
            with open(self.BUDGET_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) == 2:
                        category, amount_str = row
                        try:
                            self.budgets[category] = float(amount_str)
                        except ValueError:
                            continue 
    
    def save_budget(self, category, amount):
        """Saves a single budget goal to the budget CSV file."""
        
        self.budgets[category] = amount
        
        with open(self.BUDGET_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Budget"])
            for cat, amt in self.budgets.items():
                writer.writerow([cat, amt])
                
    def update_total(self):
        """Calculates and returns the total spending."""
        
        total = 0.0
        for i in range(self.listbox_expenses.size()):
            item = self.listbox_expenses.get(i)
            try:
                amount_str = item.split('RM ')[1] 
                total += float(amount_str)
            except (IndexError, ValueError):
                pass 
        
        return total

    def update_net_balance_label(self):
        """Updates the Net Balance label in the input view to display Total Monthly Budget, Total Expense and Balance."""
        if self.net_balance_label is None: return
        
        grand_total_expense = self.update_total() 
        total_monthly_budget = sum(self.budgets.values())
        new_budget_balance = total_monthly_budget - grand_total_expense
        
        color = 'green' if new_budget_balance >= 0 else 'red'
        
        text = (f"Total Monthly Budget: RM {total_monthly_budget:.2f}\n"
                f"Total Expense: RM {grand_total_expense:.2f}\n"
                f"Balance: RM {new_budget_balance:.2f}")
                
        self.net_balance_label.config(text=text, fg=color)

    def select_category(self, category):
        """Sets the current selected category and updates the indicator."""
        self.current_category = category
        for btn in self.category_buttons.values():
            if btn.cget("text") == category:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')
        
        self.category_label_indicator.config(text=f"Selected Category: {self.current_category}")

    def add_expense(self):
        """Adds the expense to the list, saves it to the file, and updates total."""
        if self.entry_amount is None: return

        amount = self.entry_amount.get()

        if not self.current_category:
            tk.messagebox.showerror("Error", "Please select a category first.")
            return

        if amount:
            try:
                amount_float = float(amount)
                
                selected_date = datetime.datetime.now().strftime('%Y-%m-%d')
                
                self.listbox_expenses.insert(tk.END, f"{selected_date} | {self.current_category}: RM {amount_float:.2f}")
                self.save_expense(self.current_category, amount_float, selected_date)
                
                self.entry_amount.delete(0, tk.END)
                
                self.update_net_balance_label()
                
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid number for amount")
        else:
            tk.messagebox.showerror("Error", "Please enter an amount.")

    def clear_expenses(self):
        """Clears all displayed expenses and deletes the data file."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear ALL expenses? This cannot be undone."):
            
            self.listbox_expenses.delete(0, tk.END)
            
            if os.path.exists(self.DATA_FILE):
                os.remove(self.DATA_FILE)
                
            self.update_net_balance_label()
            
            tk.messagebox.showinfo("Success", "All expenses have been cleared.")
            
    def calculate_summary(self):
        """Calculates total spending and category summary using standard library."""
        spending_summary = {}
        grand_total = 0.0
        
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
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
        """Calculates summary and returns the formatted report string, including budget."""
        summary, grand_total_expense = self.calculate_summary()
        self.load_budgets() 
        
        total_monthly_budget = sum(self.budgets.values())
        # Note: new_budget_balance is calculated but no longer displayed at the top of the report text
        new_budget_balance = total_monthly_budget - grand_total_expense
        
        report_text = [
            "  --- SPENDING SUMMARY & BUDGET ---",           
            f"{'Category':<12}\t{'Budget':>8}\t{'Spent':>8}\t{'Remain':>8}\t{'% of Total':>10}"
        ]
        
        all_categories = sorted(list(set(self.CATEGORIES))) 

        for category in all_categories:
            spent = summary.get(category, 0.0)
            budget = self.budgets.get(category, 0.0)
            remaining = budget - spent
            
            percentage = (spent / grand_total_expense) * 100 if grand_total_expense > 0 else 0.0
            
            budget_str = f"{budget:8.2f}"
            spent_str = f"{spent:8.2f}"
            
            if remaining < 0:
                remain_str = f"({abs(remaining):5.2f})" 
            else:
                remain_str = f"{remaining:8.2f}"
            
            report_text.append(
                f"{category:<12}\tRM {budget_str}\tRM {spent_str}\tRM {remain_str}\t({percentage:4.1f}%)"
            )
        
        return "\n".join(report_text)

    def display_spending_report(self):
        """Formats and displays the report."""
        if self.report_content is None: return
        
        report_text = self.generate_report_text()
        
        self.report_content.config(text=report_text, justify=tk.LEFT, font=("Courier", 10))


# --- Main Application Setup (for testing) ---
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("1000x650")
    
    def dummy_back_callback():
        print("Back to main menu logic executed.")
        root.destroy()
        
    app = BudgetTracker(root, dummy_back_callback)
    app.open_budget_page()
    
    root.mainloop()
