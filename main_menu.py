import tkinter as tk
from tkinter import messagebox  ## popup windows
from tkinter import ttk         ## create table
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ChoreScheduler import ChoreScheduler
from GroceryListManager import groceryListManager
from BudgetTracker import BudgetTracker
from test import Test

class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management Assistant App")
        self.root.geometry("800x500")
        self.main_menu()   ## call to return to main menu

        self.chore_module = ChoreScheduler(self.root, back_callback = self.main_menu)
        self.grocery_module = groceryListManager(self.root, back_callback = self.main_menu)
        self.budget_module = BudgetTracker(self.root, back_callback = self.main_menu)
        self.notebook_module = Test(self.root, back_callback = self.main_menu)

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_main_menu = tb.Frame(self.root, bootstyle="warning")
        frame_main_menu.pack(fill="both", expand=True)

        btn_grocery = tb.Button(frame_main_menu, text = "Grocery List Manager", bootstyle="info", width = 20, command = self.open_grocery)
        btn_grocery.pack(pady = 5)

        btn_chore = tb.Button(frame_main_menu, text = "Chore Scheduler", bootstyle="info", width = 20, command = self.open_chore)
        btn_chore.pack(pady = 5)

        btn_budget = tb.Button(frame_main_menu, text = "Budget Tracker", bootstyle="info", width = 20, command = self.open_budget)
        btn_budget.pack(pady = 5)

        btn_meal = tb.Button(frame_main_menu, text = "Meal Planner", bootstyle="info", width = 20, command = self.open_meal)
        btn_meal.pack(pady = 5)

        btn_notebook = tb.Button(frame_main_menu, text = "Notebook", bootstyle="info", width = 20, command = self.open_notebook)
        btn_notebook.pack(pady = 5)

    def open_grocery(self):
        self.grocery_module.menu()

    def open_chore(self):
        self.chore_module.menu()

    def open_budget(self):
        self.budget_module.menu()

    def open_meal(self):
        print("Meal Planner clicked")

    def open_notebook(self):
        self.notebook_module.menu()



if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = App(root)
    root.mainloop()