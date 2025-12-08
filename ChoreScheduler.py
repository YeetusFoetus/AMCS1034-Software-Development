import os.path as path
import json
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk


class ChoreScheduler:
    def __init__(self, root, back_callback):
        self.root = root
        self.chore_list = {}
        self.back_callback = back_callback ## function to call to go back to main menu 

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #ctk.CTkTabview(self.root).pack(fill="both", expand=True)

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
        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_archive = ttk.Treeview(table_frame, columns=("Chore", "Status"), show="headings", height=10)
        self.tree_archive.heading("Chore", text = "Chore")
        self.tree_archive.heading("Status", text = "Status")

        for item in self.tree_archive.get_children():
            self.tree_archive.delete(item)

        for index, chore in enumerate(self.chore_list.keys()):
            self.tree_archive.insert("", "end", iid=str(index), values=(chore, self.chore_list[chore]))
        
        self.tree_archive.pack()

        tk.Label(self.root, text = "Archive", font = ("Arial", 24, "bold")).pack(pady = 5)
        tk.Button(self.root, text = "Back", command = self.menu).pack(side = "bottom")
        tk.Button(self.root, text = "Delete Chore", command = self.delete_chore).pack(side="bottom")
        tk.Button(self.root, text = "Add Chore", command = self.add_chore_form).pack(side = "bottom")

    def save_chore(self):
        new_chore = self.entry.get().strip()
        if new_chore:
            self.chore_list[new_chore] = "Pending"
        self.archive()

    def delete_chore(self):
        selected = self.tree_archive.selection()
        if selected:
            for iid in selected:
                chore_name = self.tree_archive.item(iid)["values"][0]
                del self.chore_list[chore_name]
                self.tree_archive.delete(iid)

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