import tkinter as tk
from tkinter import messagebox  ## popup windows
from tkinter import ttk         ## create table
from test2 import ChoreScheduler
from test3 import groceryListManager

class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management Assistant App")
        self.root.geometry("400x300")
        self.main_menu()   ## call to return to main menu

        self.chore_module = ChoreScheduler(self.root, back_callback = self.main_menu)
        self.grocery_module = groceryListManager(self.root, back_callback = self.main_menu)

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        btn_grocery = tk.Button(self.root, text = "Grocery List Manager", width = 25, height = 2, command = self.open_grocery)
        btn_grocery.pack(pady = 5)

        btn_chore = tk.Button(self.root, text = "Chore Scheduler", width = 25, height = 2, command = self.open_chore)
        btn_chore.pack(pady = 5)

        btn_budget = tk.Button(self.root, text = "Budget Tracker", width = 25, height = 2, command = self.open_budget)
        btn_budget.pack(pady = 5)

        btn_meal = tk.Button(self.root, text = "Meal Planner", width = 25, height = 2, command = self.open_meal)
        btn_meal.pack(pady = 5)

    def open_grocery(self):
        self.grocery_module.menu()

    def open_chore(self):
        self.chore_module.menu()

    def open_budget(self):
        print("Budget Tracker clicked")

    def open_meal(self):
        print("Meal Planner clicked")



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()