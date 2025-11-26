import tkinter as tk
from tkinter import messagebox  ## popup windows
from tkinter import ttk         ## create table

class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management Assistant App")
        self.root.geometry("400x300")
        self.main_menu()   ## call to return to main menu

        self.chore_module = ChoreScheduler(self.root, back_callback = self.main_menu)

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
        self.chore_module.menu()

    def open_budget(self):
        print("Budget Tracker clicked")

    def open_meal(self):
        print("Meal Planner clicked")

class ChoreScheduler:
    def __init__(self, root, back_callback):
        self.root = root
        self.chore_list = {}
        self.back_callback = back_callback ## function to call to go back to main menu 
        self.tree_archive = ttk.Treeview(self.root, columns = "Chore", show = "headings")
        self.tree_archive.heading("Chore", text = "Chore")


    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text = "Archive", width = 25, height = 2, command = self.archive).pack(pady = 20)
        tk.Button(self.root, text = "Today's Chore List", width = 25, height = 2).pack(pady = 20)
        tk.Button(self.root, text = "Members", width = 25, height = 2).pack(pady = 20)
        tk.Button(self.root, text = "Back", command = self.back_callback).pack(pady = 20)

    ##----------------Chore Archive-------------------
    def archive(self):
        for widget in self.root.winfo_children():
            widget.destroy()  

        if len(self.chore_list) == 0:
            tk.Label(self.root, text = "No chores saved yet").pack(pady = 20)
            tk.Button(self.root, text = "Add Chore", command = self.add_chore_form).pack(pady = 20)
            tk.Button(self.root, text = "Back", command = self.menu).pack(pady = 20)
        else:
            self.store_archive()

    def store_archive(self):
        self.tree_archive.pack()

        for chore in self.chore_list:
            self.tree_archive.insert('', 'end', 'chore', values = chore)
        '''selected = self.tree_archive.selection()
        if selected:
            for id in selected:
                chore_data = self.tree_archive.item(id)'''

        tk.Label(self.root, text = "Archive", font = ("Arial", 24, "bold")).pack(pady = 5)
        tk.Button(self.root, text = "Back", command = self.menu).pack(side = "bottom")
        tk.Button(self.root, text = "Delete Chore", command = self.delete_chore).pack(side="bottom")
        tk.Button(self.root, text = "Add Chore", command = self.add_chore_form).pack(side = "bottom")

        for chore in self.chore_list:
            tk.Label(self.root, text = chore).pack()

    def save_chore(self):
        self.chore_list[self.entry.get()] = "Pending"
        self.archive()

    def delete_chore(self):
        for chore in self.chore_list:
            del self.chore_list[chore]

    def add_chore_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text = "Enter new chore: ").pack(pady = 10)
        
        self.entry = ttk.Entry(self.root, width=25)
        self.entry.pack(pady=5)

        tk.Button(self.root, text = "Save", command = self.save_chore).pack(pady=5)
        tk.Button(self.root, text = "Back", command = self.archive).pack(pady = 10)
    ## ------------------------------------------------

    ## ---------------Tdy List-----------------
    def chore_table(self):
        tk.Label(self.root, text = "Today's List of Chores")
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill = "both", expand = "True")

        columns = ("Chore", "Status")
        tree = ttk.Treeview(self.root, columns = columns, show = "headings")

        tree.heading("Chore", text = "Chore")
        tree.heading("Status", text = "Status")
        
        tree.pack(side = "top", fill = "both", expand = True)

        for chore in self.chore_list:
            tree.insert("", tk.END, values = (chore, "Pending"))

        tk.Button(self.root, text = "Add Chore", command = self.add_chore_form).pack(side = "left")
        tk.Button(self.root, text = "Back", command = self.menu).pack(side = "right")
        tk.Button(self.root, text = "Update Status").pack(pady = 20)
    ## ------------------------------------------
    ## ---------------Members---------------------
    ## ----------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()