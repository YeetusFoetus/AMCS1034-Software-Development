##hello
import tkinter as tk
from tkinter import messagebox

def open_grocery():
    print("Grocery List Manager clicked")

def open_chore():
    print("Chore Scheduler clicked")

def open_budget():
    print("Budget Tracker clicked")

def open_meal():
    print("Meal Planner clicked")

# main window
window = tk.Tk()
window.title("Household Management Assistant App")
window.geometry("400x300")  # width x height

# main menu
btn_grocery = tk.Button(window, text = "Grocery List Manager", width = 25, height = 2, command = open_grocery)
btn_grocery.pack(pady = 5)

btn_chore = tk.Button(window, text = "Chore Scheduler", width = 25, height = 2, command = open_chore)
btn_chore.pack(pady = 5)

btn_budget = tk.Button(window, text = "Budget Tracker", width = 25, height = 2, command = open_budget)
btn_budget.pack(pady = 5)

btn_meal = tk.Button(window, text = "Meal Planner", width = 25, height = 2, command = open_meal)
btn_meal.pack(pady = 5)

window.mainloop()   # start