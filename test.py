import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.root = root

        # Make Treeview an instance variable
        self.tree = ttk.Treeview(self.root, columns=("Name", "Age"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.pack()

        # Example: call another method to populate it
        self.populate_tree()

    def populate_tree(self):
        # Access self.tree here
        data = [("Alice", 25), ("Bob", 30), ("Charlie", 22)]
        for name, age in data:
            self.tree.insert("", "end", values=(name, age))

    def clear_tree(self):
        # You can also access self.tree to clear it
        for item in self.tree.get_children():
            self.tree.delete(item)

root = tk.Tk()
app = MyApp(root)
root.mainloop()
