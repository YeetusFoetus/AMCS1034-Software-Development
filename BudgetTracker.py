import tkinter as tk
from tkinter import messagebox
import csv
import os
import datetime
import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter


class BudgetTracker:
    def __init__(self, window, back_callback):
        
        # --- Global Variables and Data File Setup ---
        self.window = window
        self.back_callback = back_callback
        self.budget_switch_btn = None
        self.DATA_FILE = "expenses.csv"
        self.CATEGORIES = ["Food", "Transport", "Housing", "Bills", "Entertainment", "Other"]
        self.current_category = ""
        self.category_buttons = {}
        self.listbox_expenses = None
        self.total_label = None
        self.entry_amount = None
        self.current_budget_view = None

    def menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        bg_image = Image.open("house_interior.png")
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(self.window, image=bg_photo, text="")
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()   # send it behind everything

        self.open_budget_page()     

    def open_budget_page(self):
        tk.Label(self.window, text="Welcome to Budget Tracker", font=("Microsoft HaYei",40,"bold")).pack(pady=10)
        self.budget_page = tk.Frame(self.window,width=700,height=900)
        self.budget_page.pack()
        self.budget_page.pack_propagate(False)

        # Budget page
        self.budget_switch_btn = ctk.CTkButton(self.budget_page, text="View Report", command=lambda: self.switch_budget_view("report"))
        #,bg='#ADD8E6', width=15
        self.budget_switch_btn.pack(pady=5)

        # --- 2. Input View Frame ---
        self.input_view = tk.Frame(self.budget_page, bg='red') 

        # Category Selection
        self.frame_category = tk.Frame(self.input_view, width=500, height=170, bg='orange')
        self.frame_category.pack(pady=10)
        self.frame_category.pack_propagate(False)

        tk.Label(self.frame_category, text="Select Category:").pack(side=tk.TOP, pady=(0, 5))

        self.frame_buttons = tk.Frame(self.frame_category, bg='yellow')
        self.frame_buttons.pack()
        #self.frame_buttons.pack_propagate(False)

        for i, cat in enumerate(self.CATEGORIES):
            btn = ctk.CTkButton(
                self.frame_buttons, text=cat, command=lambda c=cat: self.select_category(c), width=120, height=40
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.category_buttons[cat] = btn

        # Selected Category Indicator
        self.category_label_indicator = tk.Label(self.frame_category, text="Selected Category: None", fg='blue')
        self.category_label_indicator.pack(pady=5, side='bottom')

        # Transaction List and Total
        tk.Label(self.input_view, text="Transactions:").pack(pady=(50, 0))
        self.listbox_expenses = tk.Listbox(self.input_view, width=75, height=15, font=("Arial", 9)) 
        self.listbox_expenses.pack(pady=5)

        self.total_label = tk.Label(self.input_view, text="Total Expenses: RM 0.00", font=("Arial", 10, "bold")) 
        self.total_label.pack(pady=5)

        # Amount Input and Add/Clear Button Area
        self.frame_input = ctk.CTkFrame(self.input_view, width=350, height=100, fg_color='green')
        self.frame_input.pack(pady=(40, 10))
        self.frame_input.pack_propagate(False)

        amount_frame = tk.Frame(self.frame_input)
        amount_frame.pack(pady=(15, 0), side='top', anchor='center')
        amount_label = tk.Label(amount_frame, font=("Arial", 15), text="Amount:")
        amount_label.pack(side='left', padx=5, pady=5)
        amount_label.pack_propagate(False)
        self.entry_amount = tk.Entry(amount_frame, font=("Arial", 15)) # Assign to global variable
        self.entry_amount.pack(side='left', padx=5,pady=5)

        self.btn_add = tk.Button(self.frame_input, text="Add Expense", command=self.add_expense, bg='lightgreen')
        self.btn_add.pack(side='bottom', padx=5, pady=5)

        self.btn_clear = tk.Button(self.frame_input, text="Clear ALL", command=self.clear_expenses, bg='pink', fg='red')
        self.btn_clear.pack(side='bottom', padx=5, pady=5)

        # --- 3. Report View Frame ---
        self.report_view = tk.Frame(self.budget_page, bg='blue') 
        tk.Label(self.report_view, text="Spending Insights Report", font=("Arial", 14, "bold")).pack(pady=10)
        self.report_content = tk.Label(self.report_view, text="Click 'Go to Reports' to view data.", 
                                justify=tk.LEFT, font=("Courier", 10), 
                                anchor="nw", padx=10, bg="#F0F0F0")
        self.report_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self.budget_page, text="Back to Main Menu", command=self.back_callback).pack(side="bottom", pady=10)

        self.switch_budget_view("input")
        
        self.load_expenses() 
        self.switch_budget_view("input")   

    # --- Data Persistence Functions ---

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
        self.current_category = category
        for btn in self.category_buttons.values():
            '''if btn.cget("text") == category:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')'''
        
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
            if os.path.exists(self.DATA_FILE):
                os.remove(self.DATA_FILE)
                
            # 3. Reset the total count
            self.update_total()
            
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
        
        if self.current_budget_view is not None:
            self.current_budget_view.pack_forget()

        if view_name == "input":
            self.current_budget_view = self.input_view
            self.input_view.pack(fill=tk.BOTH, expand=True)
            self.load_expenses() 
            
            if self.budget_switch_btn:
                self.budget_switch_btn.configure(
                    text="View Report", 
                    command=lambda: self.switch_budget_view("report")
                )
            
        elif view_name == "report":
            self.current_budget_view = self.report_view
            self.report_view.pack(fill=tk.BOTH, expand=True)
            self.report_content.config(text=self.generate_report_text()) 
            
            if self.budget_switch_btn:
                self.budget_switch_btn.configure(
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
