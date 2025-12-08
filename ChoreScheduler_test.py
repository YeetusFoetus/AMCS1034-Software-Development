import os.path as path
import json
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk


class ChoreScheduler:
    def __init__(self, root, back_callback):
        self.root = root
        self.chore_list = []
        self.locations = []
        self.members = []
        self.back_callback = back_callback ## function to call to go back to main menu 

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()  

        #------------------------TABVIEW-----------------------------
        self.menu_tabview = ctk.CTkTabview(self.root,
                                      text_color="black",
                                      segmented_button_selected_color="#f7e7ce",
                                      segmented_button_selected_hover_color="white",
                                      fg_color="#c3b091")
        self.menu_tabview.pack(expand=True, fill="both")
        self.menu_tabview.add("Today's Tasks")
        self.menu_tabview.add("Locations")
        self.menu_tabview.add("Members")

        if len(self.chore_list) == 0:
            no_tasks = ctk.CTkLabel(self.menu_tabview.tab("Today's Tasks"), text = "No tasks yet")
            no_tasks.grid(row=0, column=5, padx=20, pady=20)
            add_task = ctk.CTkButton(self.menu_tabview.tab("Today's Tasks"), text = "Add task", command = self.add_chore_form)
            add_task.grid(row=1, column=5, padx=20, pady=20)
            back = ctk.CTkButton(self.menu_tabview.tab("Today's Tasks"), text = "Back", command = self.back_callback)
            back.grid(row=2, column=5, padx=20, pady=20)
        else:
            self.store_archive()

    def tasks_table(self):
        ttk.Treeview(self.frame)

    def store_archive(self):
        table_frame = ctk.CTkFrame(self.menu_tabview.tab("Today's Tasks"))
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_archive = ttk.Treeview(table_frame, 
                                         columns=("Chore", "Location", "Member", "Due By", "Repeat", "Status"), 
                                         show="headings", 
                                         height=10)
        
        self.tree_archive.heading("Chore", text = "Chore")
        self.tree_archive.heading("Location", text = "Location")
        self.tree_archive.heading("Member", text="Member")
        self.tree_archive.heading("Due By", text = "Due By")
        self.tree_archive.heading("Repeat", text="Repeat")
        self.tree_archive.heading("Status", text = "Status")

        for item in self.tree_archive.get_children():
            self.tree_archive.delete(item)

        for chore in self.chore_list:
            self.tree_archive.insert("", "end", values=chore)
        
        self.tree_archive.pack(fill="both", expand=True)

        button_frame = ctk.CTkFrame(self.menu_tabview.tab("Today's Tasks"), fg_color="#c3b091")
        button_frame.pack(fill="x", pady=5)

        ctk.CTkButton(button_frame, text = "Back", command = self.back_callback).pack(side = "bottom")
        ctk.CTkButton(button_frame, text = "Delete All Tasks", command = self.delete_chore).pack(side="bottom")
        ctk.CTkButton(button_frame, text = "Add Task", command = self.add_chore_form).pack(side = "bottom")
    
    def save_chore(self):
        new_chore = self.entry.get().strip()
        if new_chore:
            self.chore_list.append(new_chore)
        self.menu()

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

        tk.Label(self.root, text = "Enter new task: ").pack(pady = 10)
        
        self.entry = ttk.Entry(self.root, width=25)
        self.entry.pack(pady=5)

        tk.Button(self.root, text = "Save", command = self.save_chore).pack(pady=5)
        tk.Button(self.root, text = "Back", command = self.menu).pack(pady = 10)

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
            self.tree_archive.insert("", "end", values=(chore, ))


        tk.Button(self.root, text = "Add Chore", command = self.add_chore_form).pack(side = "left")
        tk.Button(self.root, text = "Back", command = self.menu).pack(side = "right")
        tk.Button(self.root, text = "Update Status").pack(pady = 20)
