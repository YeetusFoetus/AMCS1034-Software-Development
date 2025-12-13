import tkinter as tk
from tkinter import messagebox  ## popup windows
from tkinter import ttk         ## create table

class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management Assistant App")
        self.root.geometry("400x300")

        self.chore_list = []

        self.main_menu()

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
        print("Grocery List Manager clicked")

    def open_chore(self):
        self.chore_list = []

        for widget in self.root.winfo_children():
            widget.pack_forget()        

        def save_chore():
            add_chore = entry.get()
            if add_chore:                ## for empty input
                self.chore_list.append(add_chore)
                print("Enter chore:", add_chore)
                entry.delete(0, tk.END)

        def add_chore_form():
            global entry
            entry = ttk.Entry(self.root, width=25)
            entry.pack(pady=5)
            ttk.Button(self.root, text = "Save", command = save_chore).pack(pady=5)

        if len(self.chore_list) == 0:
            chore_empty = tk.Label(self.root, text = "No chores yet")
            chore_empty.pack(pady = 20)
            chore_add = tk.Button(self.root, text = "Add Chore", command = add_chore_form)
            chore_add.pack(pady = 20)
        else:
            columns = ("Chore", "Status")
            chore_list = ttk.Treeview(self.root, columns = columns, show = "headings")
            chore_list.pack(fill = "both", expand = True, padx = 20, pady = 20)

        btn_back = tk.Button(self.root, text = "Back", command = self.main_menu)
        btn_back.pack(pady = 20)

    def open_budget(self):
        print("Budget Tracker clicked")

    def open_meal(self):
        print("Meal Planner clicked")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()